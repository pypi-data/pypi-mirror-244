import multiprocessing as mp
from threading import Lock
from stonewave.sql.udtfs.logger import logger
from stonewave.sql.udtfs.singleton import singleton
import os

DEFAULT_POOL_SIZE = int(os.getenv("STONEWAVE_PY_TABLE_FUNC_POOL_SIZE", int(mp.cpu_count() / 2)))


def _limit_pool_size(new_pool_size):
    # TODO change max_limit to a configuarable constant
    min_limit = 4
    max_limit = 32
    pool_size = max(min(max_limit, new_pool_size), min_limit)
    return pool_size


@singleton
class TaskManager(object):
    # ideally the pool_size can be controlled by a config variable
    def __init__(self, pool_size=DEFAULT_POOL_SIZE):
        self._reset(pool_size=pool_size)

    ## add a reset function used in unit test for this singleton object, mock reinitilization of TaskManager
    def _reset(self, pool_size=mp.cpu_count()):
        if hasattr(self, "_pool"):
            self._pool.close()
            self._pool.terminate()
        logger.info("init worker pool", pool_size=pool_size)
        pool_size = _limit_pool_size(pool_size)
        self.max_pool_size = pool_size

        self._pool = mp.Pool(processes=pool_size)
        # ensures the semaphore is not replaced while used
        self.workers_mutex = Lock()
        self._current_execution_id = 0
        # this is a mapping from execution_id ==> communication channels of a worker thread (queues)
        self.queues_map = {}
        self.manager = mp.Manager()
        return True

    def get_pool(self):
        return self._pool

    def change_pool_size(self, new_size):
        """Set the Pool to a new size."""
        logger.info("change task manager pool size", new_size=new_size)
        with self.workers_mutex:
            if self.queues_map:
                logger.error(
                    "there are still ongoing tasks, cannot change pool size",
                    ongoing_tasks=len(self.queues_map),
                )
                return False
            self._reset(pool_size=new_size)
            return True

    def new_task(self, task, func_name):
        """Start a new task."""
        with self.workers_mutex:
            exec_id, send_queue, recv_queue = self._assign_queues()
            args = (
                func_name,
                send_queue,
                recv_queue,
            )
            result = self._pool.apply_async(task, args=args, callback=self.task_done)
            return (exec_id, send_queue, recv_queue), result

    def _assign_queues(self):
        send_queue = self.manager.Queue()
        recv_queue = self.manager.Queue()
        self._current_execution_id += 1
        self.queues_map[self._current_execution_id] = (send_queue, recv_queue)
        return self._current_execution_id, send_queue, recv_queue

    def get_queues(self, exec_id):
        exec_id = int(exec_id)
        with self.workers_mutex:
            queues = self.queues_map.get(exec_id, (None, None))
            return queues

    def release_queues(self, exec_id):
        exec_id = int(exec_id)
        with self.workers_mutex:
            queues = self.queues_map.pop(exec_id, None)
            ongoing_tasks_size = len(self.queues_map)
            if not queues:
                logger.warn("queues already released", execution_id=exec_id)
            else:
                logger.debug(
                    "queue released",
                    execution_id=exec_id,
                    ongoing_tasks_size=ongoing_tasks_size,
                )
            return ongoing_tasks_size

    def task_done(self, *args, **kwargs):
        """Called once task is done."""
        with self.workers_mutex:
            logger.debug("function execution task submitted")
