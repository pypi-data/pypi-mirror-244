# structures.py

import types
import subprocess
import os
from typing import Any, Callable
from functools import wraps

import pandas as pd
import numpy as np

from represent.colors import Colors

__all__ = [
    "DataStructure",
    "DataStructureMeta",
    "DictStructure",
    "HiddenStructure",
    "SetStructure",
    "StringWrapper",
    "ListStructure",
    "CircularReferenceStructure",
    "TupleStructure",
    "structures",
    "structure_types",
    "TypeStructure",
    "ObjectStructure",
    "FunctionStructure",
    "HashableDict",
    "HashableSet",
    "HashableList",
    "FrozenHashable",
    "hashable_structures"
]

def is_proxy_process() -> bool:
    """
    Returns True if the process is running from an IDE.

    :return: The boolean value.
    """

    shells = {
        "bash.exe", "cmd.exe", "powershell.exe",
        "WindowsTerminal.exe"
    }

    s = subprocess.check_output(
        [
            "tasklist", "/v", "/fo", "csv",
            "/nh", "/fi", f"PID eq {os.getppid()}"
        ]
    )

    entry = str(s).strip().strip('"').strip('b\'"').split('","')

    return not (entry and (entry[0] in shells))
# end is_proxy_process

def construct(constructor: Callable) -> Callable:
    """
    Wraps the constructor of the model class.

    :param constructor: The init method of the class.

    :return: The wrapped init method.
    """

    @wraps(constructor)
    def __str__(*args: Any, **kwargs: Any) -> str:
        """
        Defines the class attributes to wrap the init method.

        :param args: Any positional arguments.
        :param kwargs: Any keyword arguments

        :returns: The model object.
        """

        try:
            result: str = constructor(*args, **kwargs)
            result = (
                result.
                replace(")()", ")").
                replace("}()", "}").
                replace("]()", "]").
                replace("$END$$E$END$ND$", Colors.END).
                replace(Colors.END + Colors.END, Colors.END).
                replace(Colors.RED + Colors.RED, Colors.RED)
            )

            return result

        except RecursionError:
            return repr(CircularReferenceStructure(*args, **kwargs))
        # end try
    # end __str__

    return __str__
# end construct

class DataStructureMeta(type):
    """A class to create the data structure classes."""

    def __init__(cls, name, bases, attr_dict) -> None:
        """
        Defines the class attributes.

        :param name: The type _name.
        :param bases: The valid_bases of the type.
        :param attr_dict: The attributes of the type.
        """

        super().__init__(name, bases, attr_dict)

        cls.__str__ = construct(cls.__str__)
    # end __init__
# end DataStructureMeta

class DataStructure(metaclass=DataStructureMeta):
    """A class to represent a structure."""

    # noinspection PyBroadException
    try:
        _color = is_proxy_process()

    except Exception:
        _color = True
    # end try

    __type__ = None
    __value__ = None
    __base__ = False
    __color__ = _color

    def __repr__(self) -> str:
        """
        Returns a string to represent the object.

        :return: A string representation for the commands of the object.
        """

        return str(self)
    # end __repr__

    @property
    def _name(self) -> str:
        """
        Returns the _name of the object.

        :return: The _name string.
        """

        if self.__value__ is None:
            name = (
                str(self.__type__).
                replace("<class '", "").
                replace("'>", "")
            ) if not self.__base__ else self.__value__

            return Colors.color_class(name, color=self.__color__)

        else:
            name = repr(self.__value__)

            return Colors.color_repr(
                name, self.__value__, color=self.__color__
            )
        # end if
    # end _name
# end DataStructure

class TypeStructure(DataStructure):
    """A class to represent a structure."""

    def __init__(self, value: type) -> None:
        """
        Defines the class attributes.

        :param value: The value to hold.
        """

        self.value = value
    # end __init__

    def __str__(self) -> str:
        """
        Returns a string to represent the object.

        :return: A string representation for the commands of the object.
        """

        data = Colors.color_class(repr(self.value).replace("'", ''))
        data = data.replace('<class', f"<{Colors.CYAN}class{Colors.END}")
        data = Colors.color_repr_address(data)

        return data
    # end __str__
# end TypeStructure

class ObjectStructure(DataStructure):
    """A class to represent a structure."""

    def __init__(self, value: object) -> None:
        """
        Defines the class attributes.

        :param value: The value to hold.
        """

        self.__value__ = value
        self.__type__ = type(value)
    # end __init__

    def __str__(self) -> str:
        """
        Returns a string to represent the object.

        :return: A string representation for the commands of the object.
        """

        string = (
            f"<{type(self.__value__).__module__}."
            f"{type(self.__value__).__name__} "
            f"object at 0x00000{str(hex(id(self.__value__))).upper()[2:]}>"
        )

        data = Colors.color_class(string, color=self.__color__)
        data = Colors.color_repr_address(data, color=self.__color__)
        data = Colors.color_repr(data, self.__value__, color=self.__color__)

        return f"{data}()"
    # end __str__
# end ObjectStructure

class SetStructure(DataStructure, set):
    """A class to represent a structure."""

    def __str__(self) -> str:
        """
        Returns a string to represent the object.

        :return: A string representation for the commands of the object.
        """

        content = ', '.join(
            [
                Colors.color_builtin_value(
                    str(value) if (type(value) != str) else repr(value),
                    value, color=self.__color__
                )
                for value in self
            ]
        )

        if self.__type__ is None:
            return "{" + content + "}"
        # end if

        return f"{self._name}({content})"
    # end __str__
# end SetStructure

class DictStructure(DataStructure, dict):
    """A class to represent a structure."""

    _hash = None

    def __str__(self) -> str:
        """
        Returns a string to represent the object.

        :return: A string representation for the commands of the object.
        """

        if self.__type__ is None:
            separator = ": "
            wrapper = "'"

        else:
            separator = "="
            wrapper = ""
        # end if

        separator = Colors.color_pairing_operator(
            separator, color=self.__color__
        )

        addresses = []
        pairs = []

        for key, value in self.items():
            if type(key) in hashable_structures:
                if key.__value__ in addresses:
                    continue
                # end if

                addresses.append(key.__value__)
            # end if

            pairs.append(
                (
                    str(key) if (type(key) != str)
                    else (
                        Colors.color_key_name(
                            f"{wrapper}{key}{wrapper}", color=self.__color__
                        )
                        if wrapper == "'" else
                        Colors.color_attribute_name(
                            f"{wrapper}{key}{wrapper}", color=self.__color__
                        )
                    )
                ) + separator +
                Colors.color_builtin_value(
                    str(value) if (type(value) != str) else repr(value),
                    value, color=self.__color__
                )
            )
        # end for

        content = ', '.join(pairs)

        if self.__type__ is None:
            return "{" + content + "}"
        # end if

        return f"{self._name}({content})"
    # end __str__
# end DictStructure

class ListStructure(DataStructure, list):
    """A class to represent a structure."""

    def __str__(self) -> str:
        """
        Returns a string to represent the object.

        :return: A string representation for the commands of the object.
        """

        content = ', '.join(
            [
                Colors.color_builtin_value(
                    str(value) if (type(value) != str) else repr(value),
                    value, color=self.__color__
                )
                for value in self
            ]
        )

        if self.__type__ is None:
            return "[" + content + "]"
        # end if

        return f"{self._name}({content})"
    # end __str__
# end ListStructure

class TupleStructure(DataStructure, tuple):
    """A class to represent a structure."""

    def __str__(self) -> str:
        """
        Returns a string to represent the object.

        :return: A string representation for the commands of the object.
        """

        content = ', '.join(
            [
                Colors.color_builtin_value(
                    str(value) if (type(value) != str) else repr(value),
                    value, color=self.__color__
                )
                for value in self
            ]
        )

        if self.__type__ is None:
            return "(" + content + ")"
        # end if

        return f"{self._name}({content})"
    # end __str__
# end TupleStructure

class HiddenStructure(DataStructure):
    """A class to represent a structure."""

    __type__ = str

    def __str__(self) -> str:
        """
        Returns a string to represent the object.

        :return: A string representation for the commands of the object.
        """

        return "..."
    # end __str__
# end HiddenStructure

class StringWrapper(DataStructure):
    """A class to represent a structure."""

    __type__ = str

    def __init__(self, value: str) -> None:
        """
        Defines the class attributes.

        :param value: The value to hold.
        """

        self.value = value
    # end __init__

    def __str__(self) -> str:
        """
        Returns a string to represent the object.

        :return: A string representation for the commands of the object.
        """

        return self.value
    # end __str__
# end StringWrapper

class FunctionStructure(DataStructure):
    """A class to represent a structure."""

    def __init__(self, value: Any) -> None:
        """
        Defines the class attributes.

        :param value: The value to hold.
        """

        self.__value__ = value

        self.__type__ = type(self.__value__)
    # end __init__

    def __str__(self) -> str:
        """
        Returns a string to represent the object.

        :return: A string representation for the commands of the object.
        """

        return Colors.color_repr_address(
            (
                f"<{Colors.CYAN}function{Colors.END}" +
                self._name[
                    self._name.find(' '):
                    self._name.find(self.__value__.__name__)
                ] +
                f"{Colors.GREEN}{self.__value__.__name__}{Colors.END}" +
                self._name[self._name.find(" at "):]
            ),
            color=self.__color__
        )
    # end __str__
# end FunctionStructure

class CircularReferenceStructure(DataStructure):
    """A class to represent a structure."""

    def __init__(self, value: Any) -> None:
        """
        Defines the class attributes.

        :param value: The value to hold.
        """

        self.__value__ = value

        self.__type__ = type(self.__value__)
    # end __init__

    def __str__(self) -> str:
        """
        Returns a string to represent the object.

        :return: A string representation for the commands of the object.
        """

        return Colors.color_repr_address(
            f"<circular referenced object: {self._name}>",
            color=self.__color__
        )
    # end __str__
# end CircularReferenceStructure

class FrozenHashable:
    """A hashable dict structure."""

    def __hash__(self) -> int:
        """
        Returns the hash of the signature for hashing the object.

        :return: The hash of the object.
        """

        return id(self)
    # end __hash__

    def _immutable(self, *args: Any, **kwargs: Any) -> None:
        """
        Collects any arguments and raises an error.

        :param args: Any positional arguments.
        :param kwargs: Any keyword arguments.
        """

        raise TypeError(f"{self} is an immutable object if type {type(self)}.")
    # end __immutable

    __setitem__ = _immutable
    __delitem__ = _immutable
    clear = _immutable
    update = _immutable
    setdefault = _immutable
    pop = _immutable
    popitem = _immutable
# end HashableDict

class HashableDict(FrozenHashable, DictStructure, dict):
    """A hashable dict structure."""
# end HashableDict

class HashableList(FrozenHashable, ListStructure, list):
    """A hashable list structure."""
# end HashableDict

class HashableSet(FrozenHashable, SetStructure, set):
    """A hashable list structure."""
# end HashableDict

hashable_structures = {
    dict: HashableDict,
    list: HashableList,
    set: HashableSet
}

structures = {
    set: SetStructure, list: ListStructure,
    tuple: TupleStructure, dict: DictStructure,
    type: TypeStructure, types.FunctionType: FunctionStructure,
    pd.DataFrame: ObjectStructure, np.ndarray: ObjectStructure
}

structure_types = (
    SetStructure, DictStructure, ListStructure,
    TupleStructure, FunctionStructure
)