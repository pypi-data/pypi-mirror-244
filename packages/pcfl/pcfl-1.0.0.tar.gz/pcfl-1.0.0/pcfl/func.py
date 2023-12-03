import mido

from pcfl.core import core_pcfl
from pcfl.core.output import save_output
from pcfl.core.parser import parse_midi
from pcfl.validator import Validator


def pcfl(midi: mido.MidiFile) -> None:
    core_pcfl(midi)


def pcfl_by_file(file: str, output: str) -> str:
    """
    PCFL By File Function

    :param file: input filepath
    :param output: result root
    :return: result filepath
    """
    Validator(file=file, output=output).validate()
    midi = parse_midi(file)
    pcfl(midi)
    save_output(midi, output)
    return output
