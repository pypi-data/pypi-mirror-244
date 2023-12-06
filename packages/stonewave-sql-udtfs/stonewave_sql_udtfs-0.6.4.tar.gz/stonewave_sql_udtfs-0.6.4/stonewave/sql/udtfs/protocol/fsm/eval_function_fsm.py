from transitions import Machine
from stonewave.sql.udtfs.protocol import ipc
from stonewave.sql.udtfs.constants import PROCESS_ERROR_MSG_TEMPLATE
from stonewave.sql.udtfs.table_writer import TableWriter
from stonewave.sql.udtfs.logger import logger
from stonewave.sql.udtfs.protocol.fsm.base_function_fsm import BaseFunctionFsm


class EvalFunctionFsm(BaseFunctionFsm):
    states = ["start", "wait_for_next", "end"]

    def __init__(self, func, batch_sender, respond):
        BaseFunctionFsm.__init__(self, func, batch_sender, respond)
        self._row_writer = TableWriter()
        self._is_evaluated = False

        self.machine = Machine(model=self, states=EvalFunctionFsm.states, initial="start")

        self.machine.add_transition(
            trigger="eval",
            source="start",
            dest="wait_for_next",
            after="eval_params",
        )

        self.machine.add_transition(
            trigger="next",
            source="wait_for_next",
            dest="wait_for_next",
            after="send_next_batch",
        )

        self.machine.add_transition(trigger="end", source="*", dest="end", before="end_evaluation")

    def eval_params(self, params):
        self.send_next_batch(params)

    def send_next_batch(self, params):
        if not self._is_evaluated:
            self.func.initialize(self._row_writer)
            func_name = self.func.get_name()
            self._row_writer._before_process()
            try:
                self.func.process(params, self._row_writer, 0)
            except Exception as e:
                logger.error(
                    "failed to evaluate table function",
                    function=func_name,
                    params=str(params),
                    error=PROCESS_ERROR_MSG_TEMPLATE.format(func_name, str(e)),
                )
                raise Exception(PROCESS_ERROR_MSG_TEMPLATE.format(func_name, str(e)))
            finally:
                self._is_evaluated = True
                self._row_writer._after_process()

        batch = self._row_writer.flush(True)
        if batch is not None:
            result_batch = self._batch_sender.send(batch)
            self._respond(result_batch)
            return
        else:
            self.end(params)

    def end_evaluation(self, params, result=None):
        logger.debug("end func evaluation")
        self._respond(result or "finish", state="finish")
        self._clean_up()

    def _clean_up(self):
        self._row_writer = None
        self.machine = None
        BaseFunctionFsm._clean_up(self)
