class Node:
    pass


class DataField(Node):
    def __init__(self, name, field_name, field_type, setter=None, getter=None):
        self.name = name
        self.field_name = field_name
        self.field_type = field_type
        self.setter = setter
        self.getter = getter


def extra_data_node(root, data: dict):
    """
    root and data should be same level of deep
    Meta attribute should be:
        class Meta:
            # strict, default False if not set
            # fields, list of fields, str or DataField: name - attribute name,
            ##field_name: corresponding key in data node,
            # setter: setter for the attribute, should return value will be set to attr
            # getter: attribute's getter
            strict = False
            fields = [
                "attribute_name",
                DataField(name="attr_2", field_name="field_name", setter=setter, getter=getter)
            ]
    :param root: root object cls
    :param data: the corresponding data node
    :return:
    """
    meta_node = getattr(root, "Meta", None)
    # for serialization should support a non-params constructor
    instance = meta_node.get_instance() if meta_node else root()
    fields = getattr(meta_node, "fields", tuple())
    strict = getattr(meta_node, "strict", False)
    for key, value in data.items():
        for field in fields:
            if isinstance(field, str):
                if strict and key != field:
                    continue
                setattr(instance, field, value)
            elif isinstance(field, DataField) and key == field.field_name:
                setter = field.setter
                _instance = setter(value)
                setattr(instance, field.name, _instance)
    return instance
