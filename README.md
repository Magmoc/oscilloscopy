# oscilloscopy

`oscilloscopy` is a Python package to easily parse oscilloscope data. 

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install oscilloscopy.

```bash
pip install oscilloscopy
```

## Usage

```python
import oscilloscopy

# Returns the OscilloscopeData struct with all the data
data = oscilloscopy.from_csv("F0001CH1.CSV")

# Or

# The folder probably contains a bitmap, a set, and one or two channel data csvs.
data = oscilloscopy.from_folder("./OSCILLOSCOPE_FOLDER/")

# Get timestamp data
time = data.channel_1.time

# Get data points
values = data.channel_1.data

# Access the parameters
unit = data.channel_1.parameters.vertical_units

# Returns `None` or channel_2 data
data.channel_2

# Plot the data
plt.plot(time, values)
```

## Currently supported oscilloscopes

It can currently parse the data from the following oscilloscopes:

- (semi-untested) TDS2000C Digital Storage Oscilloscope

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.


## License

[MIT](https://choosealicense.com/licenses/mit/)

## Roadmap
- [ ] Verify working of library
- [ ] Math Functionality?
- [ ] Plotting Functionality?
- [ ] Live connection with the USB?
- [ ] Add more oscilloscopes

## Authors
Created for use in the labs for the Electrical Engineering Bachelor of TU Delft

- Erik van Weelderen, December 2024

