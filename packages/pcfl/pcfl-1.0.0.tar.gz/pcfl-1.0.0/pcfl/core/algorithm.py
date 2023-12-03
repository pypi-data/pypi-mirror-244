import mido

from pcfl.core.output import save_output
from pcfl.core.parser import parse_midi


def is_cc64(m: mido.Message, is_end: bool = False) -> bool:
    """
    해당 메세지가 cc64인지 확인

    :param m: 확인 대상 미디 메세지
    :param is_end: cc64의 끝인지 확인
    :return: 해당 메세지가 CC64의 끝인 경우 True, 아니면 False
    """
    mdict = m.__dict__
    mtype: str | None = mdict.get("type", None)
    control: int = mdict.get("control", -1)
    value: int = mdict.get("value", -1)

    return all([
        mtype == "control_change",
        control == 64,
        value == 0 if is_end else value > 0
    ])

def process_in_track(track: mido.MidiTrack):
    """
    메인 알고리즘

    :param track: 단일 트랙
    :return:
    """
    for i, m in enumerate(track):
        if not isinstance(m, mido.Message):
            continue
        if all((
            i > 2,
            is_cc64(track[i], is_end=False),
            is_cc64(track[i-1], is_end=True),
        )):
            # 미디 순서: 음표 또는 쉼표(i-2) -> cc64_off(i-1) -> cc64_on(i)
            # 바뀌어야 할 미디 순서: cc64_off(i-1) -> 음표 또는 쉼표(i-2) -> cc64_on(i)
            sum_t = track[i-2].time - track[i-1].time
            message_t = 3
            cc64_t = sum_t - message_t
            message_t = sum_t - cc64_t
            track[i-1].time = cc64_t
            track[i-2].time = message_t
            track[i-1], track[i-2] = track[i-2], track[i-1]

def core_pcfl(midi: mido.MidiFile) -> None:
    for track in midi.tracks:
        process_in_track(track)
