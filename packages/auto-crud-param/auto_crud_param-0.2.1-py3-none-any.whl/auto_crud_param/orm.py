import param as pm
from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    Float,
    Integer,
    PickleType,
    Sequence,
    String,
)


def param_to_sqlalchemy_type(param_type):
    if isinstance(param_type, pm.String):
        return String
    elif isinstance(param_type, pm.Number):
        return Float
    elif isinstance(param_type, pm.Integer):
        return Integer
    elif isinstance(param_type, pm.Boolean):
        return Boolean
    elif isinstance(param_type, pm.Date):
        return Date
    elif isinstance(param_type, pm.DateTime):
        return DateTime
    elif isinstance(param_type, (pm.List, pm.Dict, pm.Tuple)):
        return PickleType
    elif isinstance(param_type, pm.Selector):
        # Assuming string type for simplicity; adjust based on actual use case
        return String
    else:
        raise TypeError(f'Unsupported param type: {type(param_type)}')


def parameterized_to_model(cls, Base):
    # Define a primary key column
    attrs = {'id': Column(Integer, primary_key=True)}
    # Add other columns based on param attributes
    attrs.update(
        {
            name: Column(param_to_sqlalchemy_type(param))
            for name, param in cls.param.objects().items()
            if isinstance(param, pm.Parameter)
        }
    )
    attrs['__tablename__'] = cls.__name__.lower()
    return type(cls.__name__ + 'Model', (Base,), attrs)
