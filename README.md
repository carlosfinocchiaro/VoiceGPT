# VoiceGPT

VoiceGPT is a voice-based interface for interacting with OpenAI's GPT model. It allows users to have a conversation with the GPT model using voice input and output. The program is built using Python and leverages the tkinter library for its graphical user interface (GUI).

## Features

- Voice input using speech recognition
- Text-to-speech for AI responses
- Customizable GPT model settings (API Key, Engine, Max Tokens, and Temperature)
- GUI for easy interaction
- Save and load conversation history

## Dependencies

- openai
- speech_recognition
- pyttsx3
- tkinter
- simpleaudio
- json
- sys

You can install these dependencies using pip:

```bash
pip install openai speechrecognition pyttsx3 tkinter simpleaudio
```

## Usage

1. Clone the repository:

```bash
git clone https://github.com/your-username/VoiceGPT.git
```

2. Navigate to the project directory:

```bash
cd VoiceGPT
```

3. Run the `VoiceGPT.py` script:

```bash
python VoiceGPT.py
```

4. Enter your OpenAI API key when prompted.

5. The GUI will open, and you can interact with the GPT model using the "Listen" button.

6. To save your configuration, click the "Save Config" button.

7. To reset the conversation history, click the "Reset" button.

## Building an Executable

A `build.bat` script is provided to build an executable version of the VoiceGPT program. To use the script, follow these steps:

1. Make sure you have [PyInstaller](https://www.pyinstaller.org/) installed. If not, install it using:

```bash
pip install pyinstaller
```

2. Run the `build.bat` script by double-clicking it or executing it from the command prompt:

```bash
build.bat
```

The script will create a single executable file called `VoiceGPT.exe` in a `dist` folder and compress it into a `VoiceGPT.zip` file.

## Contributing

Feel free to fork the repository and submit pull requests for any improvements or bug fixes. If you have any questions or suggestions, feel free to open an issue.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.