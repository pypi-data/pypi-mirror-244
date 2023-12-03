class FileException(Exception):
    file: str
    str_format: str

    def __init__(self, file):
        self.file = file

    def __str__(self):
        return self.str_format.format(file=self.file)

class NotAMidiFile(FileException):
    str_format = "{file} is not a midi-file"

class IsLinkFile(FileException):
    str_format = "{file} is not link-file. pcfl cannot use this."

class MidiParseFailedException(Exception): ...
