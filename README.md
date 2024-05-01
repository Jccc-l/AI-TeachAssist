# AI-Assisted-Teaching-System

This is an artificial intelligence educational assistance system that supports gesture control and voice recognition.

## Fetures

## Dependencies

- python3.10
- python3-venv

## Installation and Running

```sh
# clone this repository and go into its directory
git clone https://github.com/Jccc-l/AI-Assisted-Teaching-System.git
cd AI-Assisted-Teaching-System

# create a virtual environment and activate it
python -m venv venv
source venv/bin/activate

# Follow the official PyTorch tutorial and install the corresponding version of torch.
pip3 install torch torchvision torchaudio

# Install the requirements.

pip install -r requirements.

# Download the model into the "Automatic_Speech_Recognition_Module" directory
git lfs install
git clone https://huggingface.co/Systran/faster-whisper-small\
./Automatic_Speech_Recognition_Module/small
```

The installation is finished, to start the system, run:
```sh
python ui.py
```
