from dataclasses import dataclass
from enum import Enum
from typing import Any, Self

import numpy as np
import numpy.typing as npt
from pydantic import BaseModel


class Channel(Enum):
    channel_1 = "CH1"
    channel_2 = "CH2"


@dataclass
class ChannelData:
    time: npt.NDArray[np.float64]
    data: npt.NDArray[np.float64]


class Unit(Enum):
    # TODO add more units
    voltage = "V"
    current = "A"
    seconds = "s"


class Parameters(Enum):
    record_length = "Record Length"
    sample_interval = "Sample Interval"
    trigger_point = "Trigger Point"
    source = "Source"
    vertical_units = "Vertical Units"
    vertical_scale = "Vertical Scale"
    vertical_offset = "Vertical Offset"
    horizontal_units = "Horizontal Units"
    horizontal_scale = "Horizontal Scale"
    point_format = "Pt Fmt"
    y_zero = "Yzero"
    probe_attenuation = "Probe Atten"
    model_number = "Model Number"
    serial_number = "Serial Number"
    firmware_version = "Firmware Version"


class OscilloscoPyHeader(BaseModel):
    record_length: float
    sample_interval: float
    trigger_point: float
    source: Channel

    vertical_units: Unit
    vertical_scale: float
    vertical_offset: float

    horizontal_units: Unit
    horizontal_scale: float

    # What is this??
    # point_format: "y"

    y_zero: float
    probe_attenuation: int
    model_number: str
    serial_number: str
    firmware_version: str

    @classmethod
    def filter_keys(cls, input: dict) -> dict[str, Any]:
        field_names = {field for field in cls.model_fields}
        filtered_dict = {key: value for key, value in input.items() if key in field_names}
        return filtered_dict

    @classmethod
    def from_dict(cls, entry_dict: dict) -> Self:
        parsed_dict = dict()

        for key, val in entry_dict.items():
            try:
                parsed_key = Parameters(key)
                parsed_val = val

                if parsed_key in [Parameters.source]:
                    parsed_val = Channel(val)

                if parsed_key in [
                    Parameters.vertical_units,
                    Parameters.horizontal_units,
                ]:
                    parsed_val = Unit(val)

                if parsed_key in [Parameters.probe_attenuation]:
                    parsed_val = int(float(val))

                parsed_dict[parsed_key.name] = parsed_val

            # TODO: Use appropriate error
            except KeyError:
                raise KeyError("Something went wrong with parsing...")

        filtered_dict = OscilloscoPyHeader.filter_keys(parsed_dict)

        return cls(**filtered_dict)
