from datetime import datetime
from urllib.parse import urlparse, urljoin
from flask import request
import re


"""
Container for all the default values throughout the App.
"""


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class InputType(object):
    def __init__(self, name, label, data_type):
        self.name = name
        self.label = label
        self.data_type = data_type


def dynamic(value):
    return value


def email(value):
    if re.match(r'^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$', value):
        return value
    raise ValueError(f"{value}: invalid email address.")


def boolean(value):
    if value.lower() in ("true", "1", "t"):
        return True
    if value.lower() in ("false", "0", "f"):
        return False
    raise ValueError(f"'{value}' is an invalid value for this parameter. "
                     f"You can only use (true, t or 1) for True values, and (false, f or 0) for False ones.")


def mash(form, parser):

    for field in form.fields:
        args = {"type": PY_DTYPES[field.data_type],
                "required": field.required,
                "choices": field.choices,
                "location": "json",
                "help": field.help_text}
        valid_args = {key: val for key, val in args.items() if val is not None}
        parser.add_argument(field.name, **valid_args)

    return parser


def is_safe_url(target):
    refer_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ("http", "https") and refer_url.netloc == test_url.netloc


INPUT_TYPES = ["Short answer",
               "Paragraph",
               ##################
               "Multiple choice",
               "Checkbox",
               "Dropdown",
               ##################
               "File upload",
               ##################
               "Linear scale",
               "Multiple choice grid",
               "Checkbox grid",
               ##################
               "Date",
               "Time"]

PY_DTYPES = {"bool": bool,
             "datetime": datetime,
             "dict": dict,
             "dynamic": dynamic,
             "email": email,
             "float": float,
             "int": int,
             "list": list,
             "str": str}

