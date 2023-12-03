from enum import Enum
from dataclasses import dataclass
import os

from pcfl.core.exceptions import NotAMidiFile, IsLinkFile


class IntervalRange(Enum):
    MIN = 0.01
    MAX = 0.5

@dataclass
class Validator:
    file: str
    output: str

    def _validate_file(self):
        if not os.path.isfile(self.file):
            raise FileNotFoundError(f"{self.file} is not exists.")
        if os.path.isdir(self.file):
            raise IsADirectoryError(f"{self.file} is directory.")
        _, ext = os.path.splitext(self.file)

        if not ext.lower() in {".mid", ".midi"}:
            raise NotAMidiFile(file=self.file)
        if os.path.islink(self.file):
            raise IsLinkFile(file=self.file)

    def _validate_output(self):
        if os.path.isfile(self.output):
            raise FileExistsError(f"{self.output} is already exist.")
        if os.path.isdir(self.output):
            raise IsADirectoryError(f"{self.output} is already exists as directory")

    def validate(self):
        self._validate_file()
        self._validate_output()
