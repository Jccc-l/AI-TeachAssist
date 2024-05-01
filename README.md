# AI-Assisted-Teaching-System

## Dependencies

- Python3.10

## Installation

```sh
# clone this repository and go into its directory
git clone https://github.com/Jccc-l/AI-Assisted-Teaching-System.git
cd AI-Assisted-Teaching-System

# create a virtual environment and activate it
python -m venv venv
source venv/bin/activate

# Install the requirements.

pip install -r requirements.

# Download the model
git lfs install
git clone https://huggingface.co/Systran/faster-whisper-small\
./Automatic_Speech_Recognition_Module/small
```

The installation is finished, to start the system, run:
```sh
python ui.py
```
