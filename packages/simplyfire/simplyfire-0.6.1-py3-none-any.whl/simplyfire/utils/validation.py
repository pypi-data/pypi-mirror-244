"""
Validation used in tkinter Entry widgets.

SimplyFire - Customizable analysis of electrophysiology data
Copyright (C) 2022 Megumi Mori
This program comes with ABSOLUTELY NO WARRANTY

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
from matplotlib import colors
import os
from simplyfire.setting import config
from simplyfire.utils import formatting

valid_types = [
    "float",
    "int",
    "positive_zero_int",
    "positive_nonzero_int",
    "auto",
    "dir",
    "None",
    "indices",
    "color"
]


def validate(validate_type, value):
    if validate_type is None:
        return True
    if len(validate_type) == 0:
        return True
    types = validate_type.split('/')
    for type in types:
        if type == 'float':
            if is_float(value):
                return True
        elif type == 'int':
            if is_int(value):
                return True
        elif type == 'positive_int':
            if is_int(value):
                if int(value) > 0:
                    return True
        elif type == 'zero':
            if is_int(value):
                if int(value) == 0:
                    return True
        elif type == 'color':
            if colors.is_color_like(value):
                return True
        # elif type == 'auto':
        #     if (value.casefold()).__eq__("auto".casefold()):
        #         return True
        elif type == "string":
            return True
        elif type == "dir":
            if os.path.isdir(value):
                return True
        elif type == "indices":
            if formatting.is_indices(value):
                return True
        elif type == "None":
            if is_na(value):
                return True
        elif type[0] == '[' and type[-1] == ']': #probably can do this better with regex?
            try:
                if (value.casefold()).__eq__(type[1:-1].casefold()):
                    return True
            except (AttributeError):
                pass

        else:
            pass
    return False

def convert(validate_type, value):
    if validate_type is None:
        return value
    if len(validate_type) == 0:
        return value
    types = validate_type.split('/')
    for type in types:
        if type == 'string':
            return value
        elif type == 'None':
            if is_na(value):
                return None
        else:
            try:
                if type == 'float':
                    return float(value)
                elif type == 'int':
                    return int(value)
            except:
                pass
    return value




# def is_auto(s):
#     return (s.casefold()).__eq__("auto".casefold())
#
#
# def is_color(s):
#     return colors.is_color_like(s)


def is_int(s):
    try:
        return s.isnumeric()
    except:
        return False


def is_float(s):
    try:
        float(s)
        return True
    except:
        return False

def is_na(s):
    if s is None:
        return True
    if s == "":
        return True
    for word in config.validation_na:
        if (s.casefold()).__eq__(word.casefold()):
            return True
    return False

def is_auto(s):
    return (s.casefild()).__eq__('auto'.casefold())

