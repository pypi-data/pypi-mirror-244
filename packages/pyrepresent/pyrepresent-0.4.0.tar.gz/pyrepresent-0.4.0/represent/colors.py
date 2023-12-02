# colors.py

import datetime as dt
from typing import Any, Optional

import numpy as np

from colorama import Fore, Style

__all__ = [
    "Colors",
    "colorize",
    "decolorize",
    "SIMPLE_TYPE_COLORS"
]

class Colors:
    """A class to represent colors."""

    RED = "$RED$"
    BLACK = "$BLACK$"
    GREEN = "$GREEN$"
    WHITE = "$WHITE$"
    BLUE = "$BLUE$"
    YELLOW = "$YELLOW$"
    MAGENTA = "$MAGENTA$"
    CYAN = "$CYAN$"
    END = "$END$"

    colors = {
        RED: Fore.RED,
        GREEN: Fore.GREEN,
        BLUE: Fore.BLUE,
        YELLOW: Fore.YELLOW,
        MAGENTA: Fore.MAGENTA,
        CYAN: Fore.CYAN,
        BLACK: Fore.BLACK,
        WHITE: Fore.WHITE,
        END: Style.RESET_ALL
    }

    @staticmethod
    def color_repr_address(content: str, color: Optional[bool] = True) -> str:
        """
        Colors the string of the object's repr.

        :param content: The string to color.
        :param color: The value to color the content.

        :return: The colored repr string
        """

        if not color:
            return content
        # end if

        return (
            content.
            replace("<", f"{Colors.RED}<{Colors.END}").
            replace(">", f"{Colors.RED}>{Colors.END}").
            replace("$END$$END$END$$", Colors.END)
        )
    # end color_repr_address

    @staticmethod
    def color_class(content: str, color: Optional[bool] = True) -> str:
        """
        Colors the string of the object's repr.

        :param content: The string to color.
        :param color: The value to color the content.

        :return: The colored repr string
        """

        if not color:
            return content
        # end if

        name = content

        return (
            name[:name.rfind(".") + 1] +
            Colors.CYAN +
            name[name.rfind(".") + 1:len(name) + name.find("(") + 1] +
            Colors.END +
            name[len(name) + name.find("(") + 1:]
        )
    # end color_repr_class

    @staticmethod
    def color_repr_class(content: str, color: Optional[bool] = True) -> str:
        """
        Colors the string of the object's repr.

        :param content: The string to color.
        :param color: The value to color the content.

        :return: The colored repr string
        """

        if not color:
            return content
        # end if

        name = content

        return (
            name[:name.rfind(".") + 1] +
            Colors.CYAN +
            name[name.rfind(".") + 1:name.find(" object at")] +
            Colors.END +
            name[name.find(" object at"):]
        )
    # end color_repr_class

    @staticmethod
    def color_repr(content: str, value: Any, color: Optional[bool] = True) -> str:
        """
        Colors the string of the object's repr.

        :param content: The string to color.
        :param value: The object.
        :param color: The value to color the content.

        :return: The colored repr string
        """

        if not color:
            return content
        # end if

        name = Colors.color_repr_address(content, color=color)

        address = f"0x00000{str(hex(id(value))).upper()[2:]}"

        name = (
            name[:name.find(f" {address}") + 1] +
            Colors.MAGENTA +
            name[
                name.find(f" {address}") + 1:
                name.find(f" {address}") + len(f" {address}")
            ] +
            Colors.END + name[name.find(f" {address}") + len(f" {address}"):]
        )

        name = Colors.color_repr_class(name, color=color)

        return name
    # end color_repr

    @staticmethod
    def color_hidden_value(content: str, color: Optional[bool] = True) -> str:
        """
        Colors the string of the object's repr.

        :param content: The string to color.
        :param color: The value to color the content.

        :return: The colored repr string
        """

        if not color:
            return content
        # end if

        return f"{Colors.RED}{content}{Colors.END}"
    # end color_hidden_value

    @staticmethod
    def color_builtin_value(content: str, value: Any, color: Optional[bool] = True) -> str:
        """
        Colors the string of the object's repr.

        :param content: The string to color.
        :param value: The object.
        :param color: The value to color the content.

        :return: The colored repr string
        """

        if not color:
            return content
        # end if

        try:
            color = SIMPLE_TYPE_COLORS[type(value)]

            if type(value) == str:
                chars = ["/", "\\", r"\t", r"\n"]
                content = "".join(
                    f"{color}{char}{Colors.END}"
                    if char not in chars
                    else char for char in content
                )
                content = content.replace(
                    ":\\", f"{Colors.MAGENTA}:\\{Colors.END}"
                )
                content = content.replace(
                    f"{color}:{Colors.END}\\",
                    f"{Colors.MAGENTA}:\\{Colors.END}"
                )

                for char in chars:
                    content = content.replace(
                        char, f"{Colors.MAGENTA}{char}{Colors.END}"
                    )
                # end for

                return content

            elif type(value) in (dt.datetime, dt.timedelta, dt.date, dt.time):
                content = "".join(
                    f"{color}{char}{Colors.END}"
                    if char != ":"
                    else char for char in content
                )
                content = content.replace(
                    ":", f"{Colors.RED}:{Colors.END}"
                )
                content = content.replace(
                    "-", f"{Colors.RED}-{Colors.END}"
                )

                return content

            else:
                return f"{color}{content}{Colors.END}"
            # end if

        except KeyError:
            return content
        # end try
    # end color_builtin_value

    @staticmethod
    def color_key_name(content: str, color: Optional[bool] = True) -> str:
        """
        Colors the string of the object's repr.

        :param content: The string to color.
        :param color: The value to color the content.

        :return: The colored repr string
        """

        if not color:
            return content
        # end if

        return Colors.color_builtin_value(
            content=content, color=color, value=""
        )
    # end color_key_name

    @staticmethod
    def color_attribute_name(content: str, color: Optional[bool] = True) -> str:
        """
        Colors the string of the object's repr.

        :param content: The string to color.
        :param color: The value to color the content.

        :return: The colored repr string
        """

        if not color:
            return content
        # end if

        return f"{Colors.WHITE}{content}{Colors.END}"
    # end color_attribute_name

    @staticmethod
    def color_pairing_operator(content: str, color: Optional[bool] = True) -> str:
        """
        Colors the string of the object's repr.

        :param content: The string to color.
        :param color: The value to color the content.

        :return: The colored repr string
        """

        if not color:
            return content
        # end if

        return f"{Colors.RED}{content}{Colors.END}"
    # end color_pairing_operator
# end Colors

def colorize(content: str, /) -> str:
    """
    Colors the string with the pre-written color codes.

    :param content: The string to color.

    :return: The colored string.
    """

    for key, value in Colors.colors.items():
        content = content.replace(key, value)
    # end for

    return content
# end colorize

def decolorize(content: str, /) -> str:
    """
    Colors the string with the pre-written color codes.

    :param content: The string to color.

    :return: The colored string.
    """

    for key, value in Colors.colors.items():
        content = content.replace(key, "")
        content = content.replace(value, "")
    # end for

    return content
# end uncolor

SIMPLE_TYPE_COLORS = {
    str: Colors.YELLOW,
    bytes: Colors.CYAN,
    int: Colors.MAGENTA,
    float: Colors.MAGENTA,
    np.float64: Colors.MAGENTA,
    np.int64: Colors.MAGENTA,
    np.float32: Colors.MAGENTA,
    np.int32: Colors.MAGENTA,
    np.float16: Colors.MAGENTA,
    np.int16: Colors.MAGENTA,
    dt.timedelta: Colors.MAGENTA,
    dt.time: Colors.MAGENTA,
    dt.datetime: Colors.MAGENTA,
    dt.date: Colors.MAGENTA,
    bool: Colors.CYAN,
    type(None): Colors.CYAN
}