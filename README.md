# AI Teaching Assistance System

This is an artificial intelligence educational assistance system that supports gesture control and voice recognition.
<!--<img src="https://raw.githubusercontent.com/Jccc-l/AI-TeachAssist/main/UI.png?token=GHSAT0AAAAAACRXB5RMXYU656CQ4JNBL6E6ZRSPEMA" width="40%">
<img src="https://raw.githubusercontent.com/Jccc-l/AI-TeachAssist/main/Subtitles.png?token=GHSAT0AAAAAACRXB5RNDBXQSMROCJPS32C4ZRSPDKA" width="50%">-->
<img src="https://raw.githubusercontent.com/Jccc-l/AI-TeachAssist/main/Screenshot.png?token=GHSAT0AAAAAACRXB5RMLYPACTHGXLXWQ24SZRSPDZQ" width="100%">

## Fetures

- Gesture Control for Software Operation——[MediaPipe](https://github.com/google/mediapipe) and [PyAUtoGUI](https://github.com/asweigart/pyautogui):
    - Utilizes MediaPipe Library: MediaPipe is employed for real-time hand gesture detection, leveraging its robust framework for building multimodal applied ML pipelines.
    - PyAutoGUI for Action Execution: PyAutoGUI is used to execute actions corresponding to detected gestures, providing cross-platform support for controlling mouse and keyboard.
    - Supported Gestures: Various gestures such as click, drag, swipe, and more are supported, enhancing user interaction with software applications.
- Voice Recognition——[Whisper](https://github.com/openai/whisper) and [FasterWhisper](https://github.com/SYSTRAN/faster-whisper):
    - Powered by FasterWhisper and Whisper Libraries: The system utilizes FasterWhisper, built on top of Whisper, for efficient voice recognition. These libraries leverage deep learning models for speech-to-text conversion.
    - Integration with [CTranslate2](https://github.com/OpenNMT/CTranslate2/): FasterWhisper utilizes CTranslate2 engine's powerful inference capabilities, improving speed and reducing memory consumption for speech transcription.
    - Voice Command Support: Users can interact with the system through a range of voice commands, enabling control of the educational assistance system and execution of various tasks.
- Multi-Modal Interaction:
    - Gesture and Voice Integration: Combining gesture control and voice recognition provides a more intuitive and efficient user experience.
    - Seamless Switching: Users can seamlessly switch between gestures and voice commands based on their preference and the task at hand.
    - Adaptive Interface: The system provides a versatile and adaptive interface, enhancing user interaction with the educational assistance system.
- Educational Assistance Functions:
    - Tailored Educational Features: The system includes features specifically designed for educational purposes, such as note-taking, task management, and resource searching.
    - Integration with Educational Platforms: Integration with educational platforms and tools allows seamless access to educational resources and content, enhancing the learning experience.

## Dependencies

- python3.10

## Usage

### Installation

Clone this repository and go into its directory

```ps1
git clone https://github.com/Jccc-l/AI-TeachAssist.git
cd AI-TeachAssist
```

Create a virtual environment and activate it

```ps1
python -m venv venv
source venv/bin/activate
```

Follow the official [PyTorch](https://pytorch.org) tutorial and install the corresponding version of torch.

```ps1
pip3 install torch torchvision torchaudio
```

Install the requirements.

```ps1
pip install -r requirements
```

Download the model with git-lfs

```ps1
git lfs install
git clone https://huggingface.co/Systran/faster-whisper-small
```

The installation is finished, to start the system, run:

```ps1
python ui.py
```

### Operating Introduction

#### Gesture Control

| Gestures                                 | Actions         |
|------------------------------------------|-----------------|
| Index and middle fingers raised          | Cursor movement |
| Index and middle fingers together        | Left-Click      |
| Index finger upright, middle finger bent | Right-Click     |
| Fist clenched                            | Drag            |
| Thumb extended, others bent              | Up arrow key    |
| Thumb bent, others vertical              | Down arrow key  |

## FAQ

### Receive the following error when using Voice Recognition!

> OMP: Error #15: Initializing libiomp5md.dll, but found libiomp5md.dll already initialized.
OMP: Hint This means that multiple copies of the OpenMP runtime have been linked into the program. That is dangerous, since it can degrade performance or cause incorrect results. The best thing to do is to ensure that only a single OpenMP runtime is linked into the process, e.g. by avoiding static linking of the OpenMP runtime in any library. As an unsafe, unsupported, undocumented workaround you can set the environment variable KMP_DUPLICATE_LIB_OK=TRUE to allow the program to continue to execute, but that may cause crashes or silently produce incorrect results. For more information, please see http://www.intel.com/software/products/support/.

Remove the file `venv/Library/bin/libiomp5md.dll` in the virtual environment.