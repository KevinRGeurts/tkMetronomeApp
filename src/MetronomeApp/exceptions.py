
class MetronomeError(Exception):
    """
    Base exception class for all custom exceptions specific to MetronomeApp project.
    """
    pass


class InvalidRhythmSpecificationError(MetronomeError):
    """
    Custom exception to be raised when the user provides a value for rhythm member that does not validate as valid.
    Arguments expected in **kwargs:
        error_msg: A string describing why the rhythm specification is invalid, string
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.error_msg = kwargs.get('error_msg')


