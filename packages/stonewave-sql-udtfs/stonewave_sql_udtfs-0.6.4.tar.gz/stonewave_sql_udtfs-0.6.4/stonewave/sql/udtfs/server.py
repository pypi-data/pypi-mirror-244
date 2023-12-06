from fastapi import FastAPI, HTTPException
import multiprocessing as mp
from pydantic import BaseModel, Json
from typing import Optional
from stonewave.sql.udtfs.task_manager import TaskManager
import uvicorn
import stonewave.sql.udtfs.function_executor as function_executor
from stonewave.sql.udtfs.logger import logger, get_logger_config
import json, os
from stonewave.sql.udtfs.main import list_udtfs, register_udtf, remove_udtf
import sys

app = FastAPI()
timeout = 60


class RequestObj(BaseModel):
    func_name: Optional[str] = None
    method: str
    params: Json
    execution_id: Optional[int] = None

    class Config:
        schema_extra = {"example": {"func_name": "faker", "method": "eval", "params": {}}}


class RegisterArgs(BaseModel):
    function_name: str
    function_path: str
    update: Optional[bool] = False

    class Config:
        schema_extra = {
            "example": {
                "function_name": "add_two",
                "function_path": os.path.join(
                    os.path.dirname(os.path.abspath(__file__)),
                    "example_function",
                    "add_two_table_func_2022021711.tar.gz",
                ),
                "update": False,
            }
        }


@app.post("/table-functions/execs")
def create(req: RequestObj):
    try:
        logger.info("start create function request in worker", func_name=req.func_name, param=json.dumps(req.params))
        func_name = req.func_name
        # acquire resources from task manager
        task_manager = TaskManager()
        (execution_id, send_queue, recv_queue), result = task_manager.new_task(
            function_executor.execute_worker, func_name
        )
        logger.debug("new task succeed")
        # transmit request to child process
        try:
            send_queue.put(req)
            send_queue.join()
        except Exception as e:
            remaining_tasks = len(task_manager.queues_map)
            logger.error("full request queue", error=str(e), remaining_tasks=remaining_tasks)
            raise HTTPException(500, detail="full request queue {}, remaining_tasks {}".format(str(e), remaining_tasks))

        try:
            response = recv_queue.get(timeout=timeout)
            recv_queue.task_done()
        except Exception as e:
            # wait for finish and clean up
            response = recv_queue.get()
            recv_queue.task_done()
            task_manager.release_queues(execution_id)
            logger.error("process timeout", error=str(e), response=response)
            raise e

        logger.debug("receive response")
        res_json = json.loads(response)
        res_json["execution_id"] = str(execution_id)
        if res_json.get("state") == "finish":
            task_manager.release_queues(execution_id)
            logger.info("finish execution in create", execution_id=execution_id, req=str(req))
            return res_json
        logger.info("start execution", execution_id=execution_id, req=str(req))
        return res_json
    except HTTPException as e:
        logger.error("http exception occurred", exception=e.detail)
        raise e
    except Exception as e:
        logger.error("http exception occurred", exception=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/table-functions/execs/{execution_id}")
def receive_req(req: RequestObj, execution_id: str):
    try:
        # acquire send queue and recv queue resource by execution_id
        task_manager = TaskManager()
        logger.info("start execution", execution_id=execution_id, req=req)

        if execution_id is None:
            raise HTTPException(status_code=400, detail="no execution_id provided")

        (send_queue, recv_queue) = task_manager.get_queues(execution_id)
        if send_queue is None or recv_queue is None:
            if req.method == "finish":
                return {"result": "finish", "error": None, "state": "finish"}
            raise HTTPException(status_code=500, detail="queue map execution_id not valid")

        # transmit request to worker process
        try:
            send_queue.put(req)
            send_queue.join()
        except Exception as e:
            remaining_tasks = len(task_manager.queues_map)
            logger.error("full request queue", error=str(e), remaining_tasks=remaining_tasks)
            raise HTTPException(500, detail="full request queue {}, remaining_tasks {}".format(str(e), remaining_tasks))
        logger.debug("send data")

        try:
            response = recv_queue.get(timeout=timeout)
            recv_queue.task_done()
        except Exception as e:
            # wait for finish and clean up
            response = recv_queue.get()
            recv_queue.task_done()
            task_manager.release_queues(execution_id)
            logger.error("process timeout", error=str(e), response=response)
            raise e

        res_json = json.loads(response)
        res_json["execution_id"] = str(execution_id)
        if res_json["state"] == "finish":
            ongoing_tasks_size = task_manager.release_queues(execution_id)
            logger.info(
                "finish execution",
                ongoing_tasks_size=ongoing_tasks_size,
                execution_id=execution_id,
                req=str(req),
            )
        return res_json
    except HTTPException as e:
        logger.error("http exception occurred", e.detail)
        raise e
    except Exception as e:
        logger.error("http exception occurred", exception=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/table-functions/")
def get_list(path: str = None):

    udtfs_list = list_udtfs()
    if path:
        with open(path, "w") as f:
            f.write(json.dumps(udtfs_list, indent=4))
    else:
        return udtfs_list


@app.put("/table-functions")
def register(register_args: RegisterArgs):
    try:
        register_udtf(
            register_args.function_name,
            register_args.function_path,
            register_args.update,
        )

        return "success"
    except HTTPException as e:
        logger.error("register error", exception=e.detail)
        raise e
    except Exception as e:
        logger.error("register error", exception=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/table-functions/{function_name}")
def remove(function_name):
    try:
        remove_udtf(function_name)
    except Exception as e:
        logger.error("remove function error", function_name=function_name, exception=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/workers/pool-size")
def repopulate(num_procs: int):
    pool_instance = TaskManager()
    if pool_instance.change_pool_size(num_procs):
        return "succeed"
    else:
        raise HTTPException(status_code=500, detail="repopulate internal error")


@app.get("/status")
def heartbeat():
    return "success"


if __name__ == "__main__":
    DEFAULT_PORT = int(os.getenv("STONEWAVE_PY_TABLE_FUNC_PORT", 9720))
    mp.set_start_method("spawn")
    try:
        if len(sys.argv) > 1:
            timeout = int(sys.argv[1])
        task_manager = TaskManager()
    except Exception as e:
        logger.error("error when init task manager", exception=str(e))
    logger.info("starting python table function server", port=DEFAULT_PORT, timeout=timeout, sys_arg=str(sys.argv))
    uvicorn.run(app, host="127.0.0.1", port=DEFAULT_PORT, log_config=get_logger_config())
