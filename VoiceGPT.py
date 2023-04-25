import json
import openai
import speech_recognition as sr
import pyttsx3
import tkinter as tk
from tkinter import ttk, simpledialog, PhotoImage
from tkinter.font import Font
import os
import simpleaudio as sa
import sys

class ChatGPTApp:
    def __init__(self):
        self.init_tts_engine()
        self.config = self.load_config()
        openai.api_key = self.config["openai_key"]
        self.init_speech_recognition()
        self.load_conversation_history()
        self.create_gui()

    def load_config(self):
        default_config = {
            "openai_key": "",
            "engine": "text-davinci-003",
            "tokens": 500,
            "Max_Tokens": 4096,
            "temperature": 0.3
        }
        
        if not os.path.exists("config.json"):
            self.config = default_config
            self.save_config()
        else:
            with open("config.json", "r") as f:
                self.config = json.load(f)
        
        if self.config["openai_key"] == "":
            self.speak_text("Welcome to VoiceGPT, Please enter your OpenAI key")
            key = simpledialog.askstring("OpenAI API Key", "Please enter your OpenAI API key:")
            if key:
                if self.test_api_key(key, self.config["engine"]):
                    self.speak_text("OpenAI said your key is valid, thank you")
                    self.config["openai_key"] = key
                    self.save_config()
                else:
                    self.speak_text("OpenAI said your key is invalid, please try again")
                    sys.exit()
            else:
                self.speak_text("Terminating VoiceGPT")
                sys.exit()
        
        return self.config

    def save_config(self):
        with open("config.json", "w") as f:
            json.dump(self.config, f)

    def init_tts_engine(self):
        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty("voice", "female")

    def init_speech_recognition(self):
        self.speech_recognizer = sr.Recognizer()

    def create_gui(self):
        self.speak_text("Starting VoiceGPT")
        self.window = tk.Tk()
        self.window.title("VoiceGPT")
        
        # Variables
        self.api_key = tk.StringVar()
        self.selected_engine = tk.StringVar()
        self.max_tokens = tk.IntVar()
        self.temperature = tk.DoubleVar()
        self.temperature_value = tk.StringVar()
        
        # Logo
        logo_path = os.path.join(sys._MEIPASS, "logo.png") if getattr(sys, 'frozen', False) else "logo.png"
        self.logo = PhotoImage(file=logo_path)
        logo_label = tk.Label(self.window, image=self.logo)
        logo_label.grid(row=0, column=0, columnspan=8, pady=50)
        
        # API Key Input
        api_key_label = tk.Label(self.window, text="OpenAI API Key:")
        api_key_label.grid(row=1, column=0, pady=5, sticky=tk.E)
        api_key_entry = ttk.Entry(self.window, textvariable=self.api_key, width=100)
        api_key_entry.grid(row=1, column=1, pady=5,columnspan=8,sticky=tk.W)

        # Engine Selection
        engines = self.get_available_engines()
        engine_label = tk.Label(self.window, text="Engine:")
        engine_label.grid(row=2, column=0, pady=5, sticky=tk.E)
        engine_dropdown = ttk.Combobox(self.window, textvariable=self.selected_engine, values=engines)
        engine_dropdown.current(0)
        engine_dropdown.grid(row=2, column=1, pady=5, sticky=tk.W)

        # Max Tokens
        max_tokens_label = tk.Label(self.window, text="Max Tokens:")
        max_tokens_label.grid(row=2, column=2, pady=5, sticky=tk.E)
        max_tokens_entry = ttk.Entry(self.window, textvariable=self.max_tokens)
        max_tokens_entry.grid(row=2, column=3, pady=5, sticky=tk.W)
        
        # Temperature
        temperature_label = tk.Label(self.window, text="Temperature:")
        temperature_label.grid(row=2, column=4, pady=5, sticky=tk.E)
        temperature_scale = ttk.Scale(self.window, variable=self.temperature, from_=0.0, to=1.0, orient=tk.HORIZONTAL,command=self.update_temperature_label)
        temperature_scale.grid(row=2, column=5, pady=5, sticky=tk.E)
        
        # Temperature value display
        temperature_value_label = tk.Label(self.window, textvariable=self.temperature_value)
        temperature_value_label.grid(row=2, column=6, pady=5, sticky=tk.W)

        # Create a custom font for buttons
        button_font = Font(family="Helvetica", size=14, weight="bold")

        # Buttons
        listen_button = tk.Button(self.window, text="Listen", command=self.on_listen_button_click, width=10, font=button_font)
        listen_button.grid(row=5, column=7, pady=0, sticky=tk.E)
        save_button = tk.Button(self.window, text="Save Config", command=self.on_save_button_click)
        save_button.grid(row=3, column=1, pady=0, sticky=tk.W)
        reset_button = tk.Button(self.window, text="Reset", command=self.on_reset_button_click)
        reset_button.grid(row=5, column=1, pady=0, sticky=tk.SW)

        # Conversation History
        conversation_history_label = tk.Label(self.window, text="Conversation History:")
        conversation_history_label.grid(row=5, column=0, pady=5, sticky=tk.SW)
        conversation_history_frame = tk.Frame(self.window)
        conversation_history_frame.grid(row=6, column=0, columnspan=15, padx=10, pady=5)  # Update the columnspan value
        self.conversation_history_scrollbar = tk.Scrollbar(conversation_history_frame)
        self.conversation_history_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.conversation_history_text = tk.Text(conversation_history_frame, height=10, width=100, yscrollcommand=self.conversation_history_scrollbar.set)  # Update the width value
        self.conversation_history_text.pack(side=tk.LEFT, fill=tk.BOTH)
        self.conversation_history_scrollbar.config(command=self.conversation_history_text.yview)
        
        # Set Variables
        self.api_key.set(self.config["openai_key"])
        self.selected_engine.set(self.config["engine"])
        self.max_tokens.set(self.config["tokens"])
        self.temperature.set(self.config["temperature"])
        self.temperature_value.set(self.config["temperature"])        
        self.conversation_history_text.insert(tk.END, '\n'.join([f"User: {msg[0]}\nAI: {msg[1]}\n" for msg in self.conversation_history]))
        self.conversation_history_text.see(tk.END)

        self.window.mainloop()
        
    def update_temperature_label(self, value):
        self.temperature_value.set("{:.2f}".format(float(value)))

    def on_listen_button_click(self):
        user_input = self.listen_to_audio()
        self.conversation_history_text.insert(tk.END, f"User: {user_input}\n")
        self.window.update()
        self.conversation_history_text.see(tk.END)
        self.window.update()

        response_text = self.send_text_to_gpt(user_input)
        self.conversation_history_text.insert(tk.END, f"AI: {response_text}\n\n")
        self.window.update()
        self.conversation_history_text.see(tk.END)
        self.window.update()
        
        self.conversation_history.append((user_input, response_text))
        self.save_conversation_history()
        
        self.speak_text(response_text)

        
    def on_save_button_click(self):
        self.speak_text("Saving configuration")
        self.config["openai_key"] = self.api_key.get()
        self.config["engine"] = self.selected_engine.get()
        self.config["tokens"] = self.max_tokens.get()
        self.config["temperature"] = "{:.2f}".format(self.temperature.get())
        self.save_config()

    def on_reset_button_click(self):
        self.speak_text("Clearing conversation history")
        self.conversation_history = []
        self.conversation_history_text.delete(1.0, tk.END)
        self.save_conversation_history()
        
    def test_api_key(self, key, model):
        openai.api_key = key
        try:
            response = openai.Completion.create(
                engine=model,
                prompt="Hello World!",
                max_tokens=1
            )
            return True
        except openai.error.AuthenticationError as e:
            return False
        except openai.error.InvalidRequestError as e:
            return False        
        
    def get_available_engines(self):
        try:
            response = openai.Model.list()
            engines = [model.id for model in response['data']]
        except openai.error.AuthenticationError as e:
            return "Authentication Error: Please check your OpenAI API key."
        except openai.error.InvalidRequestError as e:
            return "InvalidRequest Error: " + str(e)
        return engines
    
    def send_text_to_gpt(self, text):
        # If the total tokens exceed 4097, remove messages from the beginning of the conversation history
        while self.calculate_tokens(text) > self.config["Max_Tokens"]:
            removed_message = self.conversation_history.pop(0)
            conversation_history_tokens -= (len(removed_message[0]) + len(removed_message[1])) // 4

        # Update the text variable with the new conversation history
        conversation_history = "\n".join([f"{msg[0]}\n{msg[1]}" for msg in self.conversation_history])
        text = f"{conversation_history}\n{text}"
    
        try:
            response = openai.Completion.create(
                engine=self.selected_engine.get(),
                prompt=text,
                max_tokens=self.max_tokens.get(),
                temperature=self.temperature.get(),
                n=1,
                stop=None,
                echo=False
            )
            return response.choices[0].text.strip()
        except openai.error.AuthenticationError as e:
            return "Authentication Error: Please check your OpenAI API key."
        except openai.error.InvalidRequestError as e:
            return "InvalidRequest Error: " + str(e)
            

    
    def listen_to_audio(self):
        with sr.Microphone() as source:
            self.play_beep()
            audio = self.speech_recognizer.listen(source,timeout=10, phrase_time_limit=10)
        try:
            text = self.speech_recognizer.recognize_google(audio)
            return text
        except Exception as e:
            return ""

    def speak_text(self, text):
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()
        
    def play_beep(self):
        wave_obj = sa.WaveObject.from_wave_file("beep.wav")
        play_obj = wave_obj.play()
        play_obj.wait_done()
        
    def load_conversation_history(self):
        if not os.path.exists("conversation_history.json"):
            self.conversation_history = []
            return

        with open("conversation_history.json", "r") as f:
            self.conversation_history = json.load(f)

    def save_conversation_history(self):
        with open("conversation_history.json", "w") as f:
            json.dump(self.conversation_history, f)
    
    def calculate_tokens(self, request):
        # MAX TOKES IS 4097
        history_characters = sum(len(msg[0]) + len(msg[1]) for msg in self.conversation_history)
        request_characters = len(request)
        total_characters = history_characters + request_characters + self.config["tokens"]
        return total_characters / 4
    
if __name__ == "__main__":
    app = ChatGPTApp()
