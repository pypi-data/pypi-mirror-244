if __name__ == "__main__":
    import schema

    builder = schema.Builder()
    schemaobject = {
        "$schema": "http://json-schema.org/schema#",
        "type": "object",
        "properties": {"hi": {"type": ["integer", "string"]}},
    }
    schema_node = schema.SchemaNode(**schemaobject)
    print(schema_node)
