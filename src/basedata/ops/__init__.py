"""
This submodule contains the BaseDataOps class, which aggregates basedata.ops
mixin classes and BaseDataClass functionality.
"""
from .base import BaseDataClass
# from .cols import ColumnConversionsMixin
from .ids import DedupeMixin, ValidIDsMixin


Mixins = [
    #     ColumnConversionsMixin,
    DedupeMixin,
    ValidIDsMixin,
]


class BaseDataOps(*Mixins, BaseDataClass):
    """
    The BaseDataOps class inherits core class functionality from the
    BaseDataClass parent class and acts as the core data operations class in
    which the methods of the many specialized mixin classes is combined.
    """
    pass
