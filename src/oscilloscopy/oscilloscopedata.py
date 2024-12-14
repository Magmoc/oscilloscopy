from pathlib import Path
from typing import Optional, Self

import pandas as pd

from oscilloscopy.classes import Channel, ChannelData, Parameters
from oscilloscopy.errors import CustomFolderStructureError, EmptyFolderError, NoChannelDataPresentError

OSCILLOSCOPE_FILE_EXTENSIONS = [
    ".csv",
]

# Allow both .CSV (native from the oscilloscope)
# and .csv (probably user changed) extension
OSCILLOSCOPE_FILE_EXTENSIONS.extend([ext.upper() for ext in OSCILLOSCOPE_FILE_EXTENSIONS])


TIME = "Time"
VALUE = "Value"
PARAMETER = "Parameter"


class OscilloscopeData:
    # TODO Add docstring for everything

    input_path: Path | None
    channel_1: ChannelData | None
    channel_2: ChannelData | None

    def __init__(
        self,
        channel_1: ChannelData | None = None,
        channel_2: ChannelData | None = None,
        input_path: Optional[Path] = None,
    ) -> None:
        if not (channel_1 or channel_2):
            raise NoChannelDataPresentError("Channel 1 or Channel 2 must have a value.")

        self.channel_1 = channel_1
        self.channel_2 = channel_2
        self.input_path = input_path

    def __str__(self) -> str:
        return str(vars(self))

    @staticmethod
    def _parse_header(input: Path) -> Parameters:
        df = pd.read_csv(
            input,
            usecols=[0, 1],
            nrows=18,
            names=[PARAMETER, VALUE],
            header=None,
        )

        df = df.dropna()

        entries = {x.get(PARAMETER): x.get(VALUE) for x in df.to_dict("records")}

        # TODO should raise error here
        return Parameters.from_dict(entries)

    @staticmethod
    def _parse_channel(input_file: Path) -> ChannelData:
        df = pd.read_csv(
            input_file,
            usecols=[3, 4],
            names=[TIME, VALUE],
            header=None,
        )

        df = df.dropna()

        time_arr = df[TIME].to_numpy()
        data_arr = df[VALUE].to_numpy()

        parameters = OscilloscopeData._parse_header(input_file)

        return ChannelData(parameters=parameters, time=time_arr, data=data_arr)

    @classmethod
    def from_csv(cls, input_file: Path | str) -> Self:
        input_path = Path(input_file).resolve()

        channel_1 = OscilloscopeData._parse_channel(input_path)
        channel_2 = None

        return cls(channel_1, channel_2, input_path)

    @classmethod
    def from_folder(cls, input_folder: Path | str) -> Self:
        input_path = Path(input_folder).resolve()

        files: list[Path] = []
        for extension in OSCILLOSCOPE_FILE_EXTENSIONS:
            files.extend(input_path.glob(f"**/*{extension}"))

        if not len(files):
            raise EmptyFolderError("Empty folder!")

        if len(files) > 2:
            # TODO: Better error
            raise CustomFolderStructureError(
                "This is not a folder from the Oscilloscope. It does not work with changed folders... yet..."
            )

        datalist: list[ChannelData] = list()
        for file in files:
            datalist.append(cls._parse_channel(file))

        channel_1 = None
        channel_2 = None

        for data in datalist:
            match data.parameters.source:
                case Channel.channel_1:
                    channel_1 = data
                case Channel.channel_2:
                    channel_2 = data

        return cls(channel_1, channel_2, input_path)
