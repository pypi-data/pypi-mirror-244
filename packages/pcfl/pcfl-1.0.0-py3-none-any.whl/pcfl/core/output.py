import mido


def save_output(midi: mido.MidiFile, new_file_root: str) -> str:
    midi.save(new_file_root)
    return new_file_root
