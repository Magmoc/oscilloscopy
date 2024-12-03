from pathlib import Path
from typing import Optional, Self

import pandas as pd

from classes import Channel, ChannelData, OscilloscoPyHeader

OSCILLOSCOPE_FILE_EXTENSIONS = [
    ".csv",
]

TIME = "Time"
VALUE = "Value"
PARAMETER = "Parameter"


class OscilloscopeData:
    # TODO Add docstring for everything

    parameters: OscilloscoPyHeader
    channel_1: ChannelData
    channel_2: ChannelData | None

    def __init__(self, input: Optional[str] = None) -> None:
        if not input:
            return

        self.input_path = Path(input).resolve()

        if self.input_path.is_dir():
            self.output = self.parse_from_folder(self.input_path)
        elif self.input_path.suffix.lower() in OSCILLOSCOPE_FILE_EXTENSIONS:
            self.output = self.parse_from_csv(self.input_path)
        else:
            # TODO: fix error type
            raise NameError

    def _parse_header(self, input: Path) -> OscilloscoPyHeader:
        df = pd.read_csv(
            input,
            usecols=[0, 1],
            nrows=18,
            names=[PARAMETER, VALUE],
            header=None,
        )

        df = df.dropna()

        entries = {x.get(PARAMETER): x.get(VALUE) for x in df.to_dict("records")}

        return OscilloscoPyHeader.from_dict(entries)

    def _parse_data(self, input_file: Path) -> ChannelData:
        df = pd.read_csv(
            input_file,
            usecols=[3, 4],
            names=[TIME, VALUE],
            header=None,
        )

        df = df.dropna()

        time_arr = df[TIME].to_numpy()
        data_arr = df[VALUE].to_numpy()

        return ChannelData(time=time_arr, data=data_arr)

    @classmethod
    def parse_from_csv(cls, input_file: Path) -> Self:
        instance = cls()

        instance.parameters = instance._parse_header(input_file)

        instance.channel_1 = instance._parse_data(input_file)
        instance.channel_2 = None

        return instance

    @classmethod
    def parse_from_folder(cls, input_folder: Path) -> Self:
        instance = cls()

        files: list[Path] = []
        for extension in OSCILLOSCOPE_FILE_EXTENSIONS:
            files.extend(input_folder.glob(f"**/*{extension}"))

        if len(files) > 2:
            # TODO: Better error
            raise KeyError(
                "This is not a folder from the Oscilloscope. It does not work with changed folders... yet..."
            )

        for file in files:
            if Channel.channel_1.value in file.name:
                instance.channel_1 = instance._parse_data(file)
            if Channel.channel_2.value in file.name:
                instance.channel_2 = instance._parse_data(file)

        return instance


if __name__ == "__main__":
    a = OscilloscopeData("./tests/files/test1")
