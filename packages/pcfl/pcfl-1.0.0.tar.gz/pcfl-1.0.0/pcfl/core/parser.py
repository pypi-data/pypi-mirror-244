import mido

from pcfl.core.exceptions import MidiParseFailedException


def parse_midi(file_root: str) -> mido.MidiFile:
    try:
        midi = mido.MidiFile(file_root)
    except FileNotFoundError as e:
        raise e
    except (EOFError, OSError):
        raise MidiParseFailedException("Midi pasing Failed.")
    except Exception as e:
        raise RuntimeError(f"Other Errors: {str(e)}")
    else:
        return midi
