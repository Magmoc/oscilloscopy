class OscilloscoPyError(Exception):
    pass


class NoChannelDataPresentError(OscilloscoPyError):
    pass


class CustomFolderStructureError(OscilloscoPyError):
    pass


class EmptyFolderError(OscilloscoPyError):
    pass


class InvalidParameterError(OscilloscoPyError):
    pass


class MissingParameterError(OscilloscoPyError):
    pass
