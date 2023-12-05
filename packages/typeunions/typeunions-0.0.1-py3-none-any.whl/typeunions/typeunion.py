from dataclasses import make_dataclass

def process_type(name: str, t):
    match t:
        case type():
            return (name, t)
        case _:
            raise TypeError(f"{t} should be a type")

def to_dataclass_attributes(values):
    match values:
        case type():
            return [('_0', values)]
        case tuple():
            return [process_type(f"_{i}", t) for i, t in enumerate(values)]
        case dict():
            return [process_type(f, t) for f, t in values.items()]
        case _:
            return None

def typeunion(cls):
    annotation = cls.__dict__.get('__annotations__', {})
    for name, value in list(annotation.items()):

        attributes = to_dataclass_attributes(value)
        if attributes is None:
            continue

        member_cls = make_dataclass(name, attributes, bases=(cls,))
        if not attributes:
            member_cls = member_cls()
        setattr(cls, name, member_cls)
        del cls.__dict__['__annotations__'][name]

    return cls
