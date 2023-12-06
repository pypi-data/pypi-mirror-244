import sys
import os
import json
from stonewave.sql.udtfs.load_function import function_loader
from stonewave.sql.udtfs.logger import logger
from stonewave.sql.udtfs.constants import USER_DEFINED_TABLE_FUNCTIONS_PATH
from stonewave.sql.udtfs.protocol.fsm.apply_function_fsm import ApplyFunctionFsm
from stonewave.sql.udtfs.protocol.fsm.eval_function_fsm import EvalFunctionFsm
from stonewave.sql.udtfs.protocol.fsm.eval_function_with_table_param_fsm import (
    EvalFunctionWithTableParamFsm,
)
from stonewave.sql.udtfs.protocol.fsm.result_batch_sender import (
    SharedMemoryRecordBatchSender,
)
import threading


class UdtfLoader:
    def __init__(self, func_name):
        self.func_name = func_name
        self.func_sys_path = None
        self.func = None

    def __enter__(self):
        if not USER_DEFINED_TABLE_FUNCTIONS_PATH in sys.path:
            sys.path.append(USER_DEFINED_TABLE_FUNCTIONS_PATH)
        self.func_sys_path = os.path.join(USER_DEFINED_TABLE_FUNCTIONS_PATH, self.func_name)
        if not self.func_sys_path in sys.path:
            sys.path.append(self.func_sys_path)

        loader = function_loader()
        self.func = loader.load_function_by_name(self.func_name)
        return self.func

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.func_sys_path in sys.path:
            sys.path.remove(self.func_sys_path)
        if USER_DEFINED_TABLE_FUNCTIONS_PATH in sys.path:
            sys.path.remove(USER_DEFINED_TABLE_FUNCTIONS_PATH)
        return False


def _create_fsm_for_command(method, func, batch_sender, respond):
    if method == "apply":
        fsm = ApplyFunctionFsm(func, batch_sender, respond)
    elif method == "eval":
        fsm = EvalFunctionFsm(func, batch_sender, respond)
    elif method == "eval_with_table_param":
        fsm = EvalFunctionWithTableParamFsm(func, batch_sender, respond)
    else:
        raise Exception("invalid_method={}".format(method))
    return fsm


def _run_fsm_loop(input, func_name, func, batch_sender, respond):
    fsm = None
    while True:
        logger.debug("waiting for request", function=func_name)
        command = input()
        logger.debug("receive request", function=func_name, request=command)

        if fsm is None:
            fsm = _create_fsm_for_command(command.method, func, batch_sender, respond)
        fsm_trigger = getattr(fsm, command.method, None)
        try:
            fsm_trigger(command.params)
        except Exception as e:
            logger.error("error occurred during function execution", error=str(e))
            command = None
            fsm_trigger = None
            fsm._clean_up()
            respond(result="finish", error=e.args[0], state="finish")
            break
        logger.debug("finish executing request", function=func_name, state=fsm.state)
        if fsm.is_end():
            logger.debug("finish function execution", function=func_name)
            break


def execute_func(func_name, input, output):
    # input: a function to return command
    # output: a function to send response
    def respond(result, error=None, state=None):
        res = json.dumps({"result": result, "error": error, "state": state})
        logger.debug("send response", function=func_name, response=res)
        output(res)

    try:
        with UdtfLoader(func_name) as function:
            if function is None:
                command = input()
                respond(
                    result="finish",
                    error="function not found, name={} command={}".format(func_name, command),
                    state="finish",
                )
                return

            func = function()
            batch_sender = SharedMemoryRecordBatchSender()
            _run_fsm_loop(input, func_name, func, batch_sender, respond)
    except Exception as e:
        logger.error("error occured", error=str(e))
        respond("finish", error=str(e), state="finish")
    finally:
        batch_sender = None
        function = None


def execute_worker(func_name, recv_queue, send_queue):
    def input():
        command = recv_queue.get()
        recv_queue.task_done()
        return command

    def output(res):
        send_queue.put(res)
        send_queue.join()

    thread = threading.Thread(target=execute_func, args=(func_name, input, output))
    thread.start()
    logger.info(
        "start executing function",
        function=func_name,
        thread_id=thread.ident,
        thread_native_id=thread.native_id,
    )
