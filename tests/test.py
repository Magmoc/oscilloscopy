import unittest
from pathlib import Path

from classes import Channel, OscilloscoPyHeader, Unit
from errors import (
    CustomFolderStructureError,
    EmptyFolderError,
    InvalidParameterError,
    MissingParameterError,
    NoChannelDataPresentError,
)
from oscilloscopy import OscilloscopeData

TEST_FOLDER_1 = "./tests/files/test1"

TEST_FOLDER_MISSING_DATA = "./tests/files/missing_channel_data"

TEST_FILE_CH_1 = "./tests/files/test1/F0001CH1.CSV"

TEST_FOLDER_EMPTY = "./tests/files/empty_folder"
TEST_CUSTOM_FOLDER_STRUCTURE = "./tests/files/folder_3_csv"


class TestOscilloscopy(unittest.TestCase):
    def setUp(self) -> None:
        self.testfolder = Path(TEST_FOLDER_1).resolve()
        self.testfolder_missing_data = Path(TEST_FOLDER_MISSING_DATA).resolve()
        self.testfile_ch1 = Path(TEST_FILE_CH_1).resolve()
        return super().setUp()

    def test_sanity(self) -> None:
        self.assertTrue(True)

    def test_header_from_dict(self) -> None:
        data = {
            "Record Length": 2.500000e03,
            "Sample Interval": 2.000000e-10,
            "Trigger Point": 1.250000000000e03,
            "Source": "CH1",
            "Vertical Units": "V",
            "Vertical Scale": 1.000000e00,
            "Vertical Offset": -2.400000e00,
            "Horizontal Units": "s",
            "Horizontal Scale": 5.000000e-08,
            "Pt Fmt": "Y",
            "Yzero": 0.000000e00,
            "Probe Atten": 1.000000e00,
            "Model Number": "TDS2022C",
            "Serial Number": "C050447",
            "Firmware Version": "FV:v24.26",
        }

        test = OscilloscoPyHeader.from_dict(data)

        expected = OscilloscoPyHeader(
            record_length=2.5e3,
            sample_interval=2.0e-10,
            trigger_point=1.25e3,
            source=Channel.channel_1,
            vertical_units=Unit.volt,
            vertical_scale=1,
            vertical_offset=-2.4,
            horizontal_units=Unit.second,
            horizontal_scale=5e-8,
            y_zero=0,
            probe_attenuation=1,
            model_number="TDS2022C",
            serial_number="C050447",
            firmware_version="FV:v24.26",
        )

        self.assertEqual(test, expected)

    def test_wrong_header_from_dict(self) -> None:
        weird_entry = "Weird entry"
        weird_value = 3.4e3

        data = {
            weird_entry: weird_value,
            "Record Length": 2.500000e03,
            "Sample Interval": 2.000000e-10,
            "Trigger Point": 1.250000000000e03,
            "Source": "CH1",
            "Vertical Units": "V",
            "Vertical Scale": 1.000000e00,
            "Vertical Offset": -2.400000e00,
            "Horizontal Units": "s",
            "Horizontal Scale": 5.000000e-08,
            "Pt Fmt": "Y",
            "Yzero": 0.000000e00,
            "Probe Atten": 1.000000e00,
            "Model Number": "TDS2022C",
            "Serial Number": "C050447",
            "Firmware Version": "FV:v24.26",
        }

        with self.assertRaises(InvalidParameterError) as e:
            OscilloscoPyHeader.from_dict(data)

        self.assertIn(weird_entry, str(e.exception))

    def test_missing_data_header_from_dict(self) -> None:
        data = {
            # "Record Length": 2.500000e03,
            "Sample Interval": 2.000000e-10,
            "Trigger Point": 1.250000000000e03,
            "Source": "CH1",
            "Vertical Units": "V",
            "Vertical Scale": 1.000000e00,
            "Vertical Offset": -2.400000e00,
            "Horizontal Units": "s",
            "Horizontal Scale": 5.000000e-08,
            "Pt Fmt": "Y",
            "Yzero": 0.000000e00,
            "Probe Atten": 1.000000e00,
            "Model Number": "TDS2022C",
            "Serial Number": "C050447",
            "Firmware Version": "FV:v24.26",
        }

        with self.assertRaises(MissingParameterError) as _:
            OscilloscoPyHeader.from_dict(data)

    def test_header(self) -> None:
        data = {
            "Record Length": 2.500000e03,
            "Sample Interval": 2.000000e-10,
            "Trigger Point": 1.250000000000e03,
            "Source": "CH1",
            "Vertical Units": "V",
            "Vertical Scale": 1.000000e00,
            "Vertical Offset": -2.400000e00,
            "Horizontal Units": "s",
            "Horizontal Scale": 5.000000e-08,
            "Pt Fmt": "Y",
            "Yzero": 0.000000e00,
            "Probe Atten": 1.000000e00,
            "Model Number": "TDS2022C",
            "Serial Number": "C050447",
            "Firmware Version": "FV:v24.26",
        }

        expected = OscilloscoPyHeader.from_dict(data)

        result = OscilloscopeData._parse_header(self.testfile_ch1)

        self.assertEqual(expected, result)

    def test_array_length(self) -> None:
        """
        Assume that all testing data will be fine if all data is imported,
        since there are no transformations on the data in the code itself.
        """
        result = OscilloscopeData.from_csv(self.testfile_ch1)

        assert result.channel_1

        length = len(result.channel_1.data)

        # according to the user manual, there must always be 2500 data points
        # TODO: maybe this should also be tested in actual creation of the oscilloscopy file.
        expected_length = 2500

        self.assertEqual(length, expected_length)

    def test_parse_from_folder(self) -> None:
        result = OscilloscopeData.from_folder(self.testfolder)
        self.assertIsNotNone(result.channel_1)
        self.assertIsNotNone(result.channel_2)

    def test_parse_from_csv(self) -> None:
        result = OscilloscopeData.from_csv(self.testfile_ch1)

        self.assertIsNotNone(result.channel_1)
        self.assertIsNone(result.channel_2)

    def test_no_channel_data_present_error(self) -> None:
        with self.assertRaises(NoChannelDataPresentError) as _:
            OscilloscopeData(None, None, None)

    def test_incomplete_data(self) -> None:
        with self.assertRaises(MissingParameterError) as _:
            OscilloscopeData.from_folder(TEST_FOLDER_MISSING_DATA)

    def test_custom_folder_structure_error(self) -> None:
        with self.assertRaises(CustomFolderStructureError) as _:
            OscilloscopeData.from_folder(TEST_CUSTOM_FOLDER_STRUCTURE)

    def test_empty_folder_error(self) -> None:
        with self.assertRaises(EmptyFolderError) as _:
            OscilloscopeData.from_folder(TEST_FOLDER_EMPTY)
