from stonewave.sql.udtfs.record_batch_builder import RecordBatchBuilder


class ApplyLeftTableBuilder(RecordBatchBuilder):
    def __init__(self, left_table):
        super().__init__()
        self.left_table = left_table
        self.left_table_field_names = left_table.schema.names
        for name, type in zip(self.left_table_field_names, left_table.schema.types):
            self.add_column(name, type)
        self.total_repeats = 0

    def repeat(self, row_idx, repeats):
        # repeat left_table[row_idx] multiple times, determined by `repeats` in the batch builder
        if repeats > 0:
            self.total_repeats += repeats
            for fi in range(0, len(self.left_table_field_names)):
                cell_value = self.left_table.column(fi)[row_idx].as_py()
                for i in range(repeats):
                    self.append(self.left_table_field_names[fi], cell_value)

    def get_total_repeats(self):
        return self.total_repeats
