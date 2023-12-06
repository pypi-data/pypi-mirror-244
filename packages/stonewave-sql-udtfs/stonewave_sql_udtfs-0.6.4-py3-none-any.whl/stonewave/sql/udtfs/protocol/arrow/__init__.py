def rename_duplicated_field(schema, field):
    name = field.name
    field_id = 0
    while schema.get_field_index(name) != -1:
        field_id += 1
        name = "{}${}".format(field.name, field_id)
    return field if name == field.name else field.with_name(name)
