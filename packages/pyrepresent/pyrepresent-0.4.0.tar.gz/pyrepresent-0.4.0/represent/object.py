# object.py

import inspect
import builtins
import types
import six
import datetime as dt
from itertools import chain
from typing import (
    Any, Optional, Union, Iterable,
    Type, Dict, TypeVar
)

import pandas as pd
import numpy as np

from represent.indentation import indent
from represent.colors import colorize
from represent.structures import (
    structures, HiddenStructure, StringWrapper,
    CircularReferenceStructure, TypeStructure,
    FunctionStructure, hashable_structures
)

__all__ = [
    "Modifiers",
    "BaseModel",
    "unwrap",
    "represent",
    "to_string",
    "BASIC_TYPES"
]

MODIFIERS = "__modifiers__"

def is_bound_method(value: Any, /) -> bool:
    """
    Checks whether an object is a bound method or not.

    :param value: The object to check.

    :return: The boolean value.
    """

    try:
        return six.get_method_self(value) is not None

    except AttributeError:
        return False
    # end try
# end is_bound_method

class Modifiers(dict):
    """A class to represent the modifiers of structures."""

    __slots__ = (
        "assign", "protected", "force", "legalize", "defined",
        "color", "excluded", "hidden", "properties"
    )

    def __init__(
            self, *,
            assign: Optional[bool] = None,
            protected: Optional[bool] = None,
            force: Optional[bool] = None,
            legalize: Optional[bool] = None,
            defined: Optional[bool] = None,
            color: Optional[bool] = None,
            excluded: Optional[Iterable[Any]] = None,
            hidden: Optional[Iterable[Any]] = None,
            properties: Optional[Union[bool, Iterable[str]]] = None,
    ) -> None:
        """
        Defines the class attributes.

        :param assign: The value to assign a type name to each commands' structure.
        :param excluded: The valid_values to exclude from the commands structure.
        :param properties: The value to extract properties.
        :param protected: The value to extract protected attributes.
        :param legalize: The value to legalize the written valid_values to be strings.
        :param hidden: The valid_values of hidden keywords.
        :param color: The value to color the repr.
        :param force: The value to force the settings of the parsing.
        :param defined: The value to show only defined valid_values.
        """

        super().__init__()

        if assign is None:
            assign = True
        # end if

        if protected is None:
            protected = False
        # end if

        if legalize is None:
            legalize = False
        # end if

        if force is None:
            force = False
        # end if

        if defined is None:
            defined = True
        # end if

        if color is None:
            color = True
        # end if

        self.assign = assign
        self.protected = protected
        self.legalize = legalize
        self.force = force
        self.defined = defined
        self.color = color

        self.properties = properties or []
        self.excluded = list(excluded or [MODIFIERS])
        self.hidden = list(hidden or [])
    # end __init__

    def __setattr__(self, key: str, value: Any) -> None:
        """
        Sets the attribute.

        :param key: The key to the attribute.
        :param value: The value of the attribute.
        """

        self[key] = value

        object.__setattr__(self, key, value)
    # end __setattr__
# end Modifiers

class BaseModel:
    """A class to represent a base model."""

    modifiers = Modifiers()

    def __str__(self) -> str:
        """
        Returns a string to represent the model commands and structure.

        :return: The string representation of the model.
        """

        return to_string(self, modifiers=self.modifiers)
    # end __str__
# end BaseModel

def extract_attributes(data: Any, /) -> Dict[str, Any]:
    """
    Gets all attributes of an object.

    :param data: The object.

    :return: The attributes of the object.
    """

    return {
        **(data.__dict__ if hasattr(data, '__dict__') else {}),
        **(
            {
                key: getattr(data, key)
                for key in chain.from_iterable(
                    getattr(cls, '__slots__', [])
                    for cls in type(data).__mro__
                ) if hasattr(data, key)
            } if hasattr(data, '__slots__') else {}
        )
    }
# end extract_attributes

def extract_properties(
        data: Any, /, properties: Optional[Iterable[str]] = None
) -> Dict[str, Any]:
    """
    Gets all properties of an object.

    :param data: The object.
    :param properties: The properties to extract.

    :return: The properties of the object.
    """

    return {
        name: getattr(data, name) for (name, value) in
        inspect.getmembers(
            type(data), lambda attribute: isinstance(
                attribute, property
            )
        )
        if (properties is True) or (name in properties)
    }
# end extract_properties

def extract_data(
        data: Any, /, properties: Optional[Iterable[str]] = None
) -> Dict[str, Any]:
    """
    Gets all attributes and properties of an object.

    :param data: The object.
    :param properties: The properties to extract.

    :return: The properties of the object.
    """

    return {
        **extract_attributes(data),
        **(
            extract_properties(data, properties=properties)
            if properties else {}
        )
    }
# end extract_data

def is_protected(
        key: Any,
        assignment: Optional[Any] = None,
        protected: Optional[bool] = None
) -> bool:
    """
    Checks if a key should be allowed.

    :param key: The key to validate.
    :param assignment: The value for the key.
    :param protected: The protected values.

    :return: The validation value.
    """

    return not (
        (
            isinstance(key, str) and
            (
                (not key.startswith("_")) or
                (assignment is None) or
                protected
            )
        ) or (not isinstance(key, str))
    )
# end is_protected

def is_excluded(
        key: Any,
        value: Any,
        excluded: Optional[Iterable[Any]] = None,
        defined: Optional[bool] = None
) -> bool:
    """
    Checks if a key should be allowed.

    :param key: The key to validate.
    :param value: The value for the key.
    :param excluded: The excluded values.
    :param defined: The value to show only defined valid_values.

    :return: The validation value.
    """

    try:
        if value == 0:
            bool_value = True

        else:
            bool_value = bool(value)
        # end try

    except ValueError:
        bool_value = True
        # end try

    return (
        (
            (excluded is not None) and
            ((key in excluded) or (type(value) in excluded))
        ) or
        (
            defined and
            (not (isinstance(value, bool) or bool_value))
        )
    )
# end is_excluded

def is_hidden(
        key: Any,
        assignment: Optional[Any] = None,
        hidden: Optional[Iterable[Any]] = None
) -> bool:
    """
    Checks if the value of the key should be hidden.

    :param key: The key object.
    :param assignment: The assignment value of the object.
    :param hidden: The hidden values.

    :return: The boolean flag.
    """

    return (
        (hidden is not None) and
        (key in hidden) and
        (assignment is not None)
    )
# end is_hidden

def early_cache(
        data: Any, /, *, ids: Dict[int, Any], legalize: Optional[bool] = False
) -> None:
    """
    Caches the object data early in the ids.

    :param data: The object.
    :param ids: The ids cache dictionary.
    :param legalize: The value to legalize the output.
    """
    data_id = id(data)

    if isinstance(data, types.FunctionType):
        ids[data_id] = repr(data) if legalize else FunctionStructure(data)

        return ids[data_id]
        # end if

    if (
        (type(data).__name__ in dir(builtins) + dir(dt)) or
        (data is None)
    ):
        ids[data_id] = data

    elif repr(data) != repr(HiddenStructure()):
        ids[data_id] = (
            repr(CircularReferenceStructure(data))
            if legalize else
            StringWrapper(repr(CircularReferenceStructure(data)))
        )

    else:
        ids[data_id] = (data if legalize else StringWrapper(repr(data)))
    # end if
# end early_cache

def wrap_object(
        data: Any, /, *,
        assignment: Optional[Any] = None,
        assign: Optional[bool] = None,
        legalize: Optional[bool] = None,
        color: Optional[bool] = None
) -> Any:
    """
    Wraps the object with the wrapper class.

    :param data: The data of the object.
    :param assignment: The assignment value.
    :param assign: The value to assign values to classes and attributes.
    :param legalize: The value to legalize the output repr.
    :param color: The value to color the repr.

    :return: The wrapped object.
    """

    if assign and (data is not None):
        if type(data) in hashable_structures:
            data = hashable_structures[type(data)](data)

        else:
            data = structures[type(data)](data)
        # end if

        if assignment is not None:
            data.__type__ = assignment

            if not legalize:
                data.__value__ = assignment
            # end if
        # end if

        data.__color__ = color
    # end if

    return data
# end wrap_object

def has_modifiers(data: Any, /) -> bool:
    """
    Checks if the object has modifiers.

    :param data: The object to check.

    :return: The boolean flag.
    """

    return (
        (
            (
                hasattr(data, MODIFIERS) and
                isinstance(data.__modifiers__, Modifiers)
            ) or
            (
                hasattr(type(data), MODIFIERS) and
                isinstance(type(data).__modifiers__, Modifiers)
            )
        )
    )
# end has_modifiers

BASIC_TYPES = [
    bool, int, float, str, bytes, bytearray, dt.time,
    dt.timedelta, dt.datetime, dt.timezone, dt.date,
    np.float64, np.int64, np.float32, np.int32,
    np.float16, np.int16
]

def is_basic(data: Any, /) -> bool:
    """
    Checks if the object is a basic object.

    :param data: The object to check.

    :return: The boolean flag.
    """

    return type(data) in BASIC_TYPES
# end is_basic

def has_data(data: Any, /) -> bool:
    """
    Checks if the object has data.

    :param data: The object. to check.

    :return: The boolean flag.
    """

    return hasattr(data, '__dict__') or hasattr(data, "__slots__")
# end has_data

def unwrap(
        data: Any, /, *,
        assign: Optional[bool] = None,
        protected: Optional[bool] = None,
        legalize: Optional[bool] = None,
        force: Optional[bool] = None,
        defined: Optional[bool] = None,
        color: Optional[bool] = None,
        hidden: Optional[Iterable[Any]] = None,
        properties: Optional[Union[bool, Iterable[str]]] = None,
        excluded: Optional[Iterable[Union[str, Type]]] = None,
        ids: Optional[Dict[int, Any]] = None
) -> Any:
    """
    Unwraps the models to get the valid_values as dictionaries.

    :param assign: The value to assign a type name to each commands' structure.
    :param data: The commands to process.
    :param ids: The ids of the collected objects.
    :param excluded: The keys to exclude from the commands structure.
    :param properties: The value to extract properties.
    :param protected: The value to extract hidden attributes.
    :param color: The valur to color the object.
    :param legalize: The value to legalize the written valid_values to be strings.
    :param hidden: The valid_values of hidden keywords.
    :param force: The value to force the settings of the parsing.
    :param defined: The value to show only defined valid_values.

    :return: The dictionary of unwrapped objects.
    """

    if inspect.isclass(data):
        return TypeStructure(data)
    # end if

    if is_basic(data):
        return data
    # end if

    if has_modifiers(data) and ids and (not force):
        modifiers = data.__modifiers__

    else:
        modifiers = Modifiers(
            assign=assign, protected=protected, legalize=legalize,
            force=force, defined=defined, color=color, hidden=hidden,
            properties=properties, excluded=excluded
        )
    # end if

    assign = modifiers.assign
    excluded = modifiers.excluded
    properties = modifiers.properties
    protected = modifiers.protected
    hidden = modifiers.hidden
    legalize = modifiers.legalize
    defined = modifiers.defined
    color = modifiers.color

    if (
        inspect.isfunction(data) or
        inspect.ismethod(data)
    ):
        if is_bound_method(data) and legalize:
            return repr(data)
        # end if

        return FunctionStructure(data)
    # end if

    if isinstance(data, (pd.DataFrame, np.ndarray)):
        return wrap_object(
            data, assignment=data, assign=assign,
            legalize=legalize, color=color
        )
    # end if

    if isinstance(data, (HiddenStructure, StringWrapper)):
        return repr(data) if legalize else StringWrapper(repr(data))
    # end if

    ids = ids or {}

    if (data_id := id(data)) in ids:
        return ids[data_id]

    else:
        early_cache(data, ids=ids, legalize=legalize)
    # end if

    assignment = None

    if has_data(data):
        assignment = data

        data = extract_data(data, properties=properties)
    # end if

    results = None

    if isinstance(data, dict):
        results = {}

        for key, value in data.items():
            if (
                is_protected(key=key, protected=protected, assignment=assignment) or
                is_excluded(key=key, value=value, excluded=excluded, defined=defined)
            ):
                continue
            # end if

            if is_hidden(key=key, assignment=assignment, hidden=hidden):
                value = HiddenStructure()
            # end if

            key = unwrap(
                key, assign=assign, ids=ids, excluded=excluded,
                properties=properties, protected=protected,
                hidden=hidden, legalize=legalize, force=force,
                defined=defined, color=color
            )
            # end if

            results[key] = unwrap(
                value, assign=assign, ids=ids, excluded=excluded,
                properties=properties, protected=protected,
                hidden=hidden, legalize=legalize, force=force,
                defined=defined, color=color
            )
        # end for

    elif isinstance(data, (tuple, list, set)):
        results = []

        for value in data:
            results.append(
                unwrap(
                    value, assign=assign, ids=ids, excluded=excluded,
                    properties=properties, protected=protected,
                    hidden=hidden, legalize=legalize, force=force,
                    defined=defined, color=color
                )
            )
        # end for

        results = type(data)(results)
    # end if

    results = wrap_object(
        results, assignment=assignment, assign=assign,
        legalize=legalize, color=color
    )

    ids[data_id] = results

    return results
# end unwrap

def to_string(data: Any, /, modifiers: Optional[Modifiers] = None) -> str:
    """
    Returns a string to represent the model commands and structure.

    :param data: The object to represent.
    :param modifiers: The modifiers for the process.

    :return: The string representation of the model.
    """

    if modifiers is None:
        if has_modifiers(data):
            modifiers = data.__modifiers__

        else:
            modifiers = Modifiers()
        # end if
    # end if

    result = indent(str(unwrap(data, **modifiers)))

    if modifiers.assign and modifiers.color:
        result = colorize(result)
    # end if

    return result
# end to_string

_C = TypeVar("_C")

def __str__(self) -> str:
    """
    Returns a string to represent the model commands and structure.

    :return: The string representation of the model.
    """

    return to_string(self)
# end __str__

def represent(base: _C, /) -> _C:
    """
    Adds the string method and modifiers to represent the model.

    :param base: The base class.

    :return: The modified base class.
    """

    base.__str__ = __str__

    if not has_modifiers(base):
        base.__modifiers__ = Modifiers()
    # end if

    return base
# end represent