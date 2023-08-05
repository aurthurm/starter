import logging
from datetime import datetime

import pytz
from sqlalchemy import inspect
from sqlalchemy.ext.hybrid import hybrid_method, hybrid_property
from sqlalchemy.orm import (DeclarativeBase, Mapped, MappedAsDataclass,
                            RelationshipProperty, mapped_column)

from core.uid_gen import get_flake_uid
from core.utils import classproperty

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DBModel(MappedAsDataclass, DeclarativeBase):
    __name__: str
    __abstract__ = True
    __repr_attrs__ = []
    __repr_max_length__ = 15
    __mapper_args__ = {"eager_defaults": True}

    @classproperty
    def columns(cls):
        return inspect(cls).columns.keys()

    @classproperty
    def primary_keys_full(cls):
        """Get primary key properties for a SQLAlchemy cls.
        Taken from marshmallow_sqlalchemy
        """
        mapper = cls.__mapper__
        return [mapper.get_property_by_column(column) for column in mapper.primary_key]

    @classproperty
    def primary_keys(cls):
        return [pk.key for pk in cls.primary_keys_full]

    @classproperty
    def relations(cls):
        """Return a `list` of relationship names or the given model"""
        return [
            c.key
            for c in cls.__mapper__.iterate_properties
            if isinstance(c, RelationshipProperty)
        ]

    @classproperty
    def settable_relations(cls):
        """Return a `list` of relationship names or the given model"""
        return [r for r in cls.relations if getattr(cls, r).property.viewonly is False]

    @classproperty
    def hybrid_properties(cls):
        items = inspect(cls).all_orm_descriptors
        return [item.__name__ for item in items if isinstance(item, hybrid_property)]

    @classproperty
    def hybrid_methods_full(cls):
        items = inspect(cls).all_orm_descriptors
        return {
            item.func.__name__: item for item in items if type(item) == hybrid_method
        }

    @classproperty
    def hybrid_methods(cls):
        return list(cls.hybrid_methods_full.keys())

    @classproperty
    def settable_attributes(cls):
        return cls.columns + cls.hybrid_properties + cls.settable_relations

    @property
    def _id_str(self):
        ids = inspect(self).identity
        if ids:
            return "-".join([str(x) for x in ids]) if len(ids) > 1 else str(ids[0])
        else:
            return "None"

    @property
    def _repr_attrs_str(self):
        max_length = self.__repr_max_length__

        values = []
        single = len(self.__repr_attrs__) == 1
        for key in self.__repr_attrs__:
            if not hasattr(self, key):
                raise KeyError(
                    "{} has incorrect attribute '{}' in "
                    "__repr__attrs__".format(self.__class__, key)
                )
            value = getattr(self, key)
            wrap_in_quote = isinstance(value, string_types)

            value = str(value)
            if len(value) > max_length:
                value = value[:max_length] + "..."

            if wrap_in_quote:
                value = "'{}'".format(value)
            values.append(value if single else "{}:{}".format(key, value))

        return " ".join(values)

    def __repr__(self):
        # get id like '#123'
        id_str = ("#" + self._id_str) if self._id_str else ""
        # join class name, id and repr_attrs
        return "<{} {}{}>".format(
            self.__class__.__name__,
            id_str,
            " " + self._repr_attrs_str if self._repr_attrs_str else "",
        )

    def fill(self, **kwargs):
        for name in kwargs.keys():
            if name in self.settable_attributes:
                setattr(self, name, kwargs[name])
            else:
                raise KeyError("Attribute '{}' doesn't exist".format(name))

        return self

    uid: Mapped[str] = mapped_column(
        init=False, default_factory=get_flake_uid, primary_key=True
    )

    created_at: Mapped[datetime] = mapped_column(
        # insert_default=func.now(),
        insert_default=lambda: datetime.now(pytz.utc),
        default=None,
        init=False,
        index=True,
    )

    def to_dict(self, nested=False, hybrid_attributes=False, exclude=None):
        """Return dict object with model's data.

        :param nested: flag to return nested relationships' data if true
        :type: bool
        :param hybrid_attributes: flag to include hybrid attributes if true
        :type: bool
        :return: dict
        """
        result = dict()

        if exclude is None:
            view_cols = self.columns
        else:
            view_cols = filter(lambda e: e not in exclude, self.columns)

        for key in view_cols:
            result[key] = getattr(self, key)

        if hybrid_attributes:
            for key in self.hybrid_properties:
                result[key] = getattr(self, key)

        if nested:
            for key in self.relations:
                obj = getattr(self, key)

                if isinstance(obj, SerializeMixin):
                    result[key] = obj.to_dict(hybrid_attributes=hybrid_attributes)
                elif isinstance(obj, Iterable):
                    result[key] = [
                        o.to_dict(hybrid_attributes=hybrid_attributes)
                        for o in obj
                        if isinstance(o, SerializeMixin)
                    ]

        return result

    def marshal_simple(self, exclude=None) -> dict:
        """convert instance to dict
        leverages instance.__dict__
        """
        if exclude is None:
            exclude = []
        exclude.append("_sa_instance_state")

        data = self.__dict__
        return_data = {}

        for field in data:
            if field not in exclude:
                return_data[field] = data[field]

        return return_data

    def marshal_nested(self, obj=None):
        if obj is None:
            obj = self

        if isinstance(obj, dict):
            return {k: self.marshal_nested(v) for k, v in obj.items()}
        elif hasattr(obj, "_ast"):
            return self.marshal_nested(obj._ast())
        elif not isinstance(obj, str) and hasattr(obj, "__iter__"):
            return [self.marshal_nested(v) for v in obj]
        elif hasattr(obj, "__dict__"):
            return {
                k: self.marshal_nested(v)
                for k, v in obj.__dict__.items()
                if not callable(v) and not k.startswith("_")
            }
        else:
            return obj
