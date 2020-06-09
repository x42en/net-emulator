# Net-Emulator

---
- Created at: 09/06/2020
- Updated at: 06/06/2020
- Author: Ben Mz (bmz)
- Maintainer: Ben Mz (bmz)
- Client: ProHacktive (https://prohacktive.io)

A very basic project to generate results from scan over emulated networks.  
First aim is to validate data format from AI

## Install
Setup using [poetry](https://python-poetry.org/)

```bash
git clone https://github.com/x42en/net-emulator.git
cd net-emulator
poetry install
poetry shell
```

## Usage
The project contains server **AND** client. Just use them as is in order to test
```bash
# launch server in one terminal
./main.py
```

```bash
# launch client in another terminal
./client.py
```

Note: client support command auto-completion for ease of use only

## TODO
- Setup unit-tests
- Add docs
