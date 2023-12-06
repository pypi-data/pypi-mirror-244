from transitions import Machine
from stonewave.sql.udtfs.protocol import ipc
from stonewave.sql.udtfs.protocol.fsm.shared_record_batch_reader import (
    read_record_batch,
)
from stonewave.sql.udtfs.table_writer import TableWriter
from stonewave.sql.udtfs.constants import PROCESS_ERROR_MSG_TEMPLATE
from stonewave.sql.udtfs.protocol.fsm.base_function_fsm import BaseFunctionFsm
from stonewave.sql.udtfs.logger import logger


class EvalFunctionWithTableParamFsm(BaseFunctionFsm):
    states = ["start", "wait_for_next_table_batch", "wait_for_next", "end"]

    def __init__(self, func, batch_sender, respond):
        BaseFunctionFsm.__init__(self, func, batch_sender, respond)
        self.machine = Machine(model=self, states=EvalFunctionWithTableParamFsm.states, initial="start")

        self.machine.add_transition(
            trigger="eval_with_table_param",
            source="start",
            dest="wait_for_next_table_batch",
            after="eval_params",
        )

        self.machine.add_transition(
            trigger="eval_with_table_param",
            source="wait_for_next_table_batch",
            dest="wait_for_next_table_batch",
            after="eval_params",
        )

        self.machine.add_transition(
            trigger="end_table_param",
            source="wait_for_next_table_batch",
            dest="wait_for_next",
            after="send_next_batch",
        )

        self.machine.add_transition(
            trigger="next",
            source="wait_for_next",
            dest="wait_for_next",
            after="send_next_batch",
        )

        self.machine.add_transition(trigger="end", source="wait_for_next", dest="end", before="end_evaluation")

        self.machine.add_transition(trigger="*", source="end", dest="end", before="end_evaluation")
        self._row_writer = TableWriter()
        self.func.initialize(self._row_writer)
        self._batches = []
        self._batch_idx = 0
        self._read_record_batch_func = read_record_batch

    @property
    def read_record_batch_func(self):
        return self._read_record_batch_func

    # a method used for injecting a different function for unit testing purpose
    @read_record_batch_func.setter
    def read_record_batch_func(self, value):
        self._read_record_batch_func = value

    def eval_params(self, params):
        batch = self._read_record_batch_func(params[0])
        params[0] = batch
        try:
            func_name = self.func.get_name()
            if batch is not None:
                self.func.process(params, self._row_writer, 0)
                next_batch = self._row_writer.flush(forced=False)
                if next_batch:
                    self._batches.append(next_batch)
                self._respond("next_table_batch")
            else:
                self.func.process(params, self._row_writer, 0)
                self.end_table_param(params)
        except Exception as e:
            raise Exception(PROCESS_ERROR_MSG_TEMPLATE.format(func_name, str(e)))

    def send_next_batch(self, params):
        if self._batch_idx < len(self._batches):
            batch = self._batches[self._batch_idx]
            self._batch_idx += 1
            result_batch = self._batch_sender.send(batch)
            self._respond(result_batch)
            return
        batch = self._row_writer.flush()
        if batch is not None:
            result_batch = self._batch_sender.send(batch)
            self._respond(result_batch)
            return
        batch = self._row_writer.flush(forced=True)
        if batch is not None:
            result_batch = self._batch_sender.send(batch)
            self._respond(result_batch)
            return
        self.end(params)

    def end_evaluation(self, params, result=None):
        logger.debug("end func evaluation with table params")
        self._respond(result or "finish", state="finish")
        self._clean_up()

    def _clean_up(self):
        self._row_writer = None
        self._batches = None
        self.machine = None
        self._read_record_batch_func = None
        self.read_record_batch_func = None
        BaseFunctionFsm._clean_up(self)
