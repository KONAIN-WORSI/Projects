import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os
import requests
import json
import subprocess
import sys

class VoiceAgent:
    def __init__(self):
        # Initialize speech recognition
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Initialize text-to-speech
        self.tts_engine = pyttsx3.init()
        self.setup_tts()
        
        # Adjust for ambient noise
        print("Adjusting for ambient noise... Please wait.")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
        print("Ready to listen!")
        
    def setup_tts(self):
        """Configure text-to-speech settings"""
        voices = self.tts_engine.getProperty('voices')
        if voices:
            # Use female voice if available, otherwise use default
            for voice in voices:
                if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                    self.tts_engine.setProperty('voice', voice.id)
                    break
        
        # Set speech rate and volume
        self.tts_engine.setProperty('rate', 150)
        self.tts_engine.setProperty('volume', 0.9)
    
    def speak(self, text):
        """Convert text to speech"""
        print(f"JARVIS: {text}")
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()
    
    def listen(self):
        """Listen for voice input and convert to text"""
        try:
            with self.microphone as source:
                print("Listening...")
                # Listen for audio with timeout
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
            
            print("Processing speech...")
            # Use Google's speech recognition
            command = self.recognizer.recognize_google(audio).lower()
            print(f"You said: {command}")
            return command
            
        except sr.WaitTimeoutError:
            return None
        except sr.UnknownValueError:
            self.speak("Sorry, I couldn't understand that. Could you repeat?")
            return None
        except sr.RequestError:
            self.speak("Sorry, there was an error with the speech recognition service.")
            return None
    
    def get_current_time(self):
        """Get current time"""
        now = datetime.datetime.now()
        time_str = now.strftime("%I:%M %p")
        return f"The current time is {time_str}"
    
    def get_current_date(self):
        """Get current date"""
        now = datetime.datetime.now()
        date_str = now.strftime("%A, %B %d, %Y")
        return f"Today is {date_str}"
    
    def search_web(self, query):
        """Open web browser with search query"""
        search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        webbrowser.open(search_url)
        return f"Searching for {query} on Google"
    
    def open_application(self, app_name):
        """Open applications"""
        apps = {
            'notepad': 'notepad.exe',
            'calculator': 'calc.exe',
            'paint': 'mspaint.exe',
            'chrome': 'chrome.exe',
            'firefox': 'firefox.exe',
            'word': 'winword.exe',
            'excel': 'excel.exe',
            'brave' : 'brave.exe'
        }
        
        app_name = app_name.lower()
        if app_name in apps:
            try:
                subprocess.Popen(apps[app_name])
                return f"Opening {app_name}"
            except FileNotFoundError:
                return f"Sorry, {app_name} is not installed or not found"
        else:
            return f"Sorry, I don't know how to open {app_name}"
    
    def get_weather(self, city="your location"):
        """Get weather information (requires API key)"""
        # Note: You'll need to get a free API key from OpenWeatherMap
        # and replace 'YOUR_API_KEY' with your actual key
        api_key = "2fc62f4b0ec74ddc369d89d577e5f212"
        
        if api_key == "YOUR_API_KEY":
            return "Weather service is not configured. Please add your OpenWeatherMap API key."
        
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
            response = requests.get(url)
            data = response.json()
            
            if response.status_code == 200:
                temp = data['main']['temp']
                description = data['weather'][0]['description']
                return f"The weather in {city} is {description} with a temperature of {temp}°C"
            else:
                return "Sorry, I couldn't get the weather information"
        except:
            return "Sorry, there was an error getting the weather"
    
    def process_command(self, command):
        """Process voice commands and execute appropriate actions"""
        if not command:
            return
        
        # Time-related commands
        if any(word in command for word in ['time', 'clock']):
            response = self.get_current_time()
            
        # Date-related commands
        elif any(word in command for word in ['date', 'today', 'day']):
            response = self.get_current_date()
            
        # Search commands
        elif 'search' in command or 'google' in command:
            query = command.replace('search', '').replace('google', '').replace('for', '').strip()
            if query:
                response = self.search_web(query)
            else:
                response = "What would you like me to search for?"
                
        # Open application commands
        elif 'open' in command:
            app_name = command.replace('open', '').strip()
            response = self.open_application(app_name)
            
        # Weather commands
        elif 'weather' in command:
            response = self.get_weather()
            
        # Exit commands
        elif any(word in command for word in ['exit', 'quit', 'goodbye', 'bye']):
            response = "Goodbye! Have a great day!"
            self.speak(response)
            return False
            
        # Help commands
        elif 'help' in command or 'what can you do' in command:
            response = """I can help you with:
            - Telling time and date
            - Searching the web
            - Opening applications like notepad, calculator, or paint
            - Getting weather information
            - Just say 'exit' or 'goodbye' to quit"""
            
        # Default response for unrecognized commands
        else:
            response = "Sorry, I didn't understand that command. Say 'help' to see what I can do."
        
        self.speak(response)
        return True
    
    def run(self):
        """Main loop to run the voice agent"""
        self.speak("Hello! I'm your voice assistant. How can I help you today?")
        
        while True:
            command = self.listen()
            if not self.process_command(command):
                break

def main():
    print("Voice Command AI Agent")
    print("======================")
    print("\nRequired libraries:")
    print("pip install speechrecognition pyttsx3 pyaudio requests")
    print("\nNote: On Windows, you might need to install PyAudio using:")
    print("pip install pipwin && pipwin install pyaudio")
    print("\n" + "="*50)
    
    try:
        agent = VoiceAgent()
        agent.run()
    except KeyboardInterrupt:
        print("\nProgram interrupted by user")
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Make sure all required libraries are installed")

if __name__ == "__main__":
    main()