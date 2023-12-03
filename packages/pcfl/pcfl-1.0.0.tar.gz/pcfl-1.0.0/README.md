# pcfl

![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/skywinz/pcfl/test-ubuntu.yml?label=test-ubuntu)
![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/skywinz/pcfl/test-windows.yml?label=test-windows)
[![CI](https://github.com/skywinz/pcfl/actions/workflows/ci.yml/badge.svg)](https://github.com/skywinz/pcfl/actions/workflows/ci.yml)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pcfl?logo=python&logoColor=white)
![PyPI - Version](https://img.shields.io/pypi/v/pcfl)
![GitHub](https://img.shields.io/github/license/skywinz/pcfl)





* MuseScore4에서 FL Studio에 피아노 페달(CC64)이 포함된 미디파일을 임포트할 때, 페달 사이의 간격을 벌려 정상적으로 임포트를 하게 하는
전처리 라이브러리 및 프로그램 입니다.
* 페달이 연속으로 붙어있는 미디파일을 FL Studio에 임포트 하면 그 두 개의 페달이 하나로 합쳐저 불협화음을 발생시킵니다.
* PCFL는 이를 막기 위해 두 페달 사이의 간격을 3 ticks 정도 벌립니다.
* [이전 구현체](https://github.com/skywinz/pcfl-legacy)에서는 Musescore3까지만 대응할 수 있고 Musescore4 부터 대응이 불가능 하여 새 구현체를 구현하게 되었습니다.


## Installation (As User)
```shell
$ pip install pcfl
```

## Installation (As Dev)
```shell
$ git clone https://github.com/skywinz/pcfl.git
$ poetry install
```

## Usage
### As CLI
```shell
$ python -m pcfl -f input.mid -o output.mid
```

### As Library
```python
import mido
from pcfl import pcfl, pcfl_by_file

# 파일을 사용할 경우
output_filepath = pcfl_by_file("input.mid", "output.mid")

# mido.MidiFile을 사용할 경우
midi = mido.MidiFile("input.mid")
pcfl(midi)
```

### ThirdParty
* [mido](https://github.com/mido/mido)
  * 이전 legacy 버전에서 사용했던 [music21](https://github.com/cuthbertLab/music21)대신 mido를 사용했습니다.
  * 기본 midi R/W 말고도 많은 분석 툴까지 포함되어 상당히 무거운 music21과는 달리 mido는 단순히 midi 데이터를 R/W하는 데만 집중되어 있어 훨씬 가볍습니다.