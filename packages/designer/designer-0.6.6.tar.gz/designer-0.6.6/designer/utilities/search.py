from designer.objects.designer_object import DesignerObject


def _detect_objects_recursively(data):
    """ Recursively detects any references to DesignerObjects,
     and returns them as a flattened set. """
    if isinstance(data, (list, set, tuple, frozenset)):
        result = set()
        for item in data:
            result.update(_detect_objects_recursively(item))
        return result
    elif isinstance(data, dict):
        result = set()
        for key, value in data.items():
            result.update(_detect_objects_recursively(key))
            result.update(_detect_objects_recursively(value))
        return result
    elif isinstance(data, DesignerObject):
        return {data}
    else:
        result = set()
        try:
            for key, value in vars(data).items():
                result.update(_detect_objects_recursively(value))
        except TypeError:
            try:
                for key in data.__slots__:
                    result.update(_detect_objects_recursively(getattr(data, key)))
            except AttributeError:
                pass
        return result
