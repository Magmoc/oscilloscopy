import unittest
from pathlib import Path

from classes import Channel, OscilloscoPyHeader, Unit
from oscilloscopy import OscilloscopeData

TEST_FOLDER_1 = "./tests/files/test1"
TEST_FILE_1 = "./tests/files/test1/F0001CH1.CSV"


class TestOscilloscopy(unittest.TestCase):
    def setUp(self) -> None:
        self.testfolder = Path(TEST_FOLDER_1).resolve()
        self.testfile = Path(TEST_FILE_1).resolve()
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

        result = OscilloscopeData._parse_header(self.testfile)

        self.assertEqual(expected, result)

    def test_array_length(self) -> None:
        """
        Assume that all testing data will be fine if all data is imported,
        since there are no transformations on the data in the code itself.
        """
        result = OscilloscopeData.from_csv(self.testfile)

        assert result.channel_1

        length = len(result.channel_1.data)

        # according to the user manual, there must always be 2500 data points
        expected_length = 2500

        self.assertEqual(length, expected_length)
