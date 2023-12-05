"""
This module contains 'Config' dataclass having different data fields.
'Config' class has the ability to load the default values by passing
the DEFAULT_CONFIG_PATH to the 'Config' object.
Also, 'Config' class can update the existing value of data field or
add new values by calling 'update' function.
"""

import yaml

from dataclasses import dataclass, field, fields
from mergedeep import merge


@dataclass
class Config:
    DEFAULT_CONFIG_PATH: str = field(default_factory=lambda: None)
    DEPLOYMENT: dict = field(default_factory=dict)
    ENV_DATA: dict = field(default_factory=dict)
    REPORTING: dict = field(default_factory=dict)
    RUN: dict = field(default_factory=dict)
    UPGRADE: dict = field(default_factory=dict)

    def __post_init__(self):
        if self.DEFAULT_CONFIG_PATH:
            self.update(self.get_defaults())

    def get_defaults(self):
        """
        Return a fresh copy of the default configuration
        """
        with open(self.DEFAULT_CONFIG_PATH) as file_stream:
            return {
                k: (v if v is not None else {})
                for (k, v) in yaml.safe_load(file_stream).items()
            }

    def update(self, user_dict: dict):
        """
        Override configuration items with items in user_dict, without wiping
        out non-overridden items
        """
        if user_dict is None:
            return
        field_names = [f.name for f in fields(self)]
        for k, v in user_dict.items():
            if k not in field_names:
                raise ValueError(
                    f"{k} is not a valid config section. "
                    f"Valid sections: {field_names}"
                )
            if v is None:
                continue
            section = getattr(self, k)
            merge(section, v)
