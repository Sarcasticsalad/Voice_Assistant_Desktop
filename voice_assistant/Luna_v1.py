import pyttsx3
import speech_recognition as sr
import torch
import torchaudio
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
import io
import random
import datetime
import pyjokes
import os
import subprocess
from difflib import get_close_matches
import mapping_values as mv
import psutil
import pygetwindow as gw
import pyautogui
import time
import re
import webbrowser
from luna_ui import LunaUI
from threading import Thread
from yt_dlp import YoutubeDL
import threading
import requests
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
import screen_brightness_control as sbc
import smtplib
from email.message import EmailMessage
import soundfile as sf

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

# Initializing the model and processor
processor = Wav2Vec2Processor.from_pretrained(r"E:\CSIT\7thsem\FYP\models\sr_test_2")
model = Wav2Vec2ForCTC.from_pretrained(r"E:\CSIT\7thsem\FYP\models\sr_test_2")

# Global variable to track snooze activation
snooze_activated = False

# Text to Speech Function
def speak(audio):
    engine.say(audio) 
    print(audio)
    engine.runAndWait()

# # Input Pipeline Function
# def input_pipeline(audio_data):
#     # Load audio from bytes with torchaudio
#     waveform, sample_rate = torchaudio.load(io.BytesIO(audio_data), format="wav")

#     # Resampling as our devices take audio at 48khz
#     if sample_rate != 16000:
#         waveform = torchaudio.transforms.Resample(orig_freq=sample_rate, new_freq=16000)(waveform)

#     # Process and trasncribe with Wav2vec2
#     input_values = processor(waveform.squeeze(), sampling_rate=16000, return_tensors="pt").input_values
#     logits = model(input_values).logits
#     predicted_ids = torch.argmax(logits, dim=-1)
#     transcription = processor.decode(predicted_ids[0])

#     return transcription

# Input Pipeline Function
def input_pipeline(audio_data):
    # Load audio from BytesIO using soundfile
    audio_buffer = io.BytesIO(audio_data)
    waveform, sample_rate = sf.read(audio_buffer, dtype="float32")

    # Convert to PyTorch tensor
    waveform = torch.tensor(waveform).unsqueeze(0)  # Add batch dimension

    # Resample to 16kHz if needed
    if sample_rate != 16000:
        resampler = torchaudio.transforms.Resample(orig_freq=sample_rate, new_freq=16000)
        waveform = resampler(waveform)

    # Process and transcribe with Wav2Vec2
    input_values = processor(waveform.squeeze(), sampling_rate=16000, return_tensors="pt").input_values
    logits = model(input_values).logits
    predicted_ids = torch.argmax(logits, dim=-1)
    transcription = processor.decode(predicted_ids[0])

    return transcription

# Function that initializes the microphone and enables audio intake
def listen_audio(timeout, pharse_time_limit):
    try:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=1)
            print("Listening...")
            audio = r.listen(source, timeout=timeout, phrase_time_limit=pharse_time_limit)
            audio_data = audio.get_wav_data()
            transcription = input_pipeline(audio_data=audio_data).lower()
            return transcription
    
    except Exception as e:
        print(f"Error: {e}")
        return None        

# Function to detect wake word
def wake_word(wake_words):
    transcription = listen_audio(timeout=5, pharse_time_limit=10)
    if transcription:
        print(f"Wake word detected: {transcription}")
        norm_wake_word = normalize_wake_word(transcription)
        if any(wake_word in norm_wake_word for wake_word in wake_words):
            return True
    return False
          
# Function to Listen for commands
def listen_command():
    try:
        transcription = listen_audio(timeout=120, pharse_time_limit=60)
        print(f"Command received: {transcription}")
        return transcription
    
    except:
        speak("Could you repeat that, please?")
        return None
    
# Normalize Command
def normalize_command(input_command):
    input_command = input_command.lower().strip()

    for command, details in mv.COMMAND_REGISTRY.items():
        # Check if the input matches any alias for the command
        for alias in details['aliases']:
            if re.fullmatch(alias, input_command):
                return command

        # get closest matches:
        closest_match = get_close_matches(input_command, details['aliases'], n=1, cutoff=0.6)
        if closest_match:
            return command

    return input_command
    
def normalize_wake_word(input_word):
    input_word = input_word.lower().strip()
    for word, aliases in mv.WAKE_WORD_ALIAS.items():
        if input_word in aliases:
            return word
    return input_word   

def normalize_exit_word(input_word):
    input_word = input_word.lower().strip()
    for word, aliases in mv.EXIT_WORD_ALIAS.items():
        if input_word in aliases:
            return word
    return input_word 


def Greet():
    hour = int(datetime.datetime.now().hour)

    if hour < 12:
       return "Good Morning"  

    elif hour >= 12 and hour<17:
        return "Good Afternoon"
    
    else:
        return "Good Evening"

def get_time():
    hour = datetime.datetime.now().hour
    minute = datetime.datetime.now().minute
    minute_str = str(minute).zfill(2)
    if hour >= 12 and hour != 24:
        if hour == 12:
            current_time = f"{hour}:{minute_str} PM"
        else:    
            hour_pm = hour - 12
            current_time = f"{hour_pm}:{minute_str} PM"
        
    else:
        if hour == 24:
            hour_am = hour - 12
            current_time = f"{hour_am}:{minute_str} AM"
        else:    
            current_time = f"{hour}:{minute_str} AM"
    
    return current_time 

def word_to_number(word):
    return mv.WORD_TO_NUMBER.get(word.lower(), None)

def find_program_dynamically(program_name):
    # Try to locate the program in the PATH using 'where
    try:
        result = subprocess.check_output(f"where {program_name}", shell=True, text=True)
        paths = result.strip().split('\n')
        if paths:
            # Return the first valid path
            return paths[0]
    except subprocess.CalledProcessError:
        pass    

    # Search in common installation directories
    common_dirs = [r"C:\Program Files", r"C:\Program Files (x86)", r"E:", r"F:", r"C:"]   
    for directory in common_dirs:
        for root, _, files in os.walk(directory):
            for file in files:
                if program_name.lower() in file.lower():
                    return os.path.join(root, file)

    # Search in user's home directory
    user_dir = os.path.expanduser("~")
    for root, _, files in os.walk(user_dir):
        for file in files:
            if program_name.lower() in file.lower():
                return os.path.join(root, file)

    # If the program isn't found return None
    return None        

def open_program_dynamically(program_name):
    path = find_program_dynamically(program_name)
    if path:
        try:
            os.startfile(path)
            speak(f"Opening {program_name}")
        except Exception as e:
            speak(f"Sorry, I couldn't open {program_name}. Error: {str(e)}")
    else:
        speak(f"Sorry, I couldn't find {program_name} on your system.")    

def get_uwp_apps():
    uwp_apps = {}
    try:
        # Run Powershell command to list all apps
        result = subprocess.run(
            ["powershell",
              "-Command",
                "Get-StartApps | ForEach-Object {$_.Name + ';' + $_.AppID}"],
            capture_output=True, text=True, check=True
        )

        # Parse output line by line
        for line in result.stdout.splitlines():
                parts = line.strip().split(";", maxsplit=1)
                if len(parts) == 2:
                    name, app_id = parts
                    uwp_apps[name.lower()] = app_id.strip()
    except Exception as e:
        print(f"Error fetching UWP apps: {str(e)}")

    return uwp_apps                    

def suggest_app(app_name, uwp_apps):
    suggestions = get_close_matches(app_name.lower(), uwp_apps.keys(), n=3, cutoff=0.6)
    if suggestions:
        return f"Did you mean: {', '.join(suggestions)}?"
    return "No similar apps found."    

def open_uwp_app_dynamically(app_name):
    uwp_apps = get_uwp_apps()
    print(uwp_apps)
    app_id = uwp_apps.get(app_name.lower())
    if app_id:
        try:
            # Print the full AppID
            print(f"Full AppID for {app_name}: {app_id}")
            command = f"powershell -Command \"Start-Process 'shell:AppsFolder\\{app_id}'\""
            print(f"Executing command: {command}")
            # Launch the app using its AppID
            subprocess.run(command, shell=True, check=True, text=True)   
            speak(f"Opening {app_name}")
        except Exception as e:
            speak(f"Sorry, I couldn't open {app_name}. Error: {str(e)}")
    else:
        suggestions = suggest_app(app_name, uwp_apps)
        speak(f"Sorry, I couldn't find the app {app_name}. {suggestions}")     

def normalize_program_name(input_name):
    input_name = input_name.lower().strip()
    for program, aliases in mv.PROGRAM_ALIAS.items():
        if input_name in aliases:
            return program

    return input_name        

def close_app(app_name):
    try:
        # Normalize the input name
        app_name = app_name.lower().strip()

        # First close application window
        closed_window = close_window(app_name)

        # Get all running process names
        running_processes = {process.info['name'].lower(): process.info['pid'] for process in psutil.process_iter(['name', 'pid'])}

        # Automatically find the closest match for the application name
        matching_processes = [
            (name, pid) for name, pid in running_processes.items() if app_name in name
        ]

        if matching_processes:
            print(f"Found {len(matching_processes)} processes for {app_name}")
            for name, pid in matching_processes:
                print(f"Attempting to close {name} (PID: {pid})")
                terminate_process(pid)
            # Terminate the process
            terminate_process(pid)

            print(f"{app_name} closed successfully.")

        elif not closed_window:
            print(f"No exact matches for {app_name}. Attempting taskkill fallback...")
            # Fallback to taskkill for unmatched processes
            result = subprocess.run(
                ["taskkill", "/F", "/IM", f"{app_name}.exe"], capture_output=True, text=True
            )
            if result.returncode == 0:
                print(f"{app_name} force-killed successfully using taskkill.")
            else:
                print(f"Failed to close {app_name} using taskkill. Error: {result.stderr}")         
        
        else:
            print(f"{app_name} windows closed but no processes matched.")

    except Exception as e:
        print(f"Failed to close {app_name}. Error: {e}")

def close_window(app_name):
    try:
        # Get all windows and match them by title
        windows = gw.getAllTitles()
        matching_windows = [title for title in windows if app_name in title.lower()]

        if matching_windows:
            for window in matching_windows:
                print(f"Closing window: {windows}")
                app_window = gw.getWindowsWithTitle(window)[0]
                app_window.close()
            return True
        else:
            print(f"No matching windows found for '{app_name}'.")    
            return False
    except Exception as e:
        print(f"Error while closing windows for '{app_name}': {e}")
        return False

# Recursively eliminate all processes
def terminate_process(pid):
    try:
        # Get the process object
        parent_process = psutil.Process(pid)

        # Get the children of the process
        children = parent_process.children(recursive=True)

        # Terminate child processes
        for child in children:
            print(f"Terminating child process {child.name()} (PID: {child.pid})")
            child.terminate()

        # Wait for all children processes to be terminated
        _, still_alive = psutil.wait_procs(children, timeout=5)

        # Force kill any remaining children processes if remaining
        for child in still_alive:
            print(f"Force-killing child process {child.name()} (PID: {child.pid})")
            child.kill()

        # Finally terminate the parent process
        print(f"Terminating parent process {parent_process.name()} (PID: {parent_process.pid})")     
        parent_process.terminate()

        # Wait for the parent process to terminate
        parent_process.wait(timeout=5)

    except psutil.NoSuchProcess:
        print(f"Process with PID {pid} already terminated.")

    except psutil.TimeoutExpired:    
        print(f"Timeout while waiting for process with PID {pid} to terminate. Force killing...")
        parent_process.kill()

    except Exception as e:
        print(f"Failed to terminate process with PID {pid}. Error: {e}")   

def switch_tab():
    try:

        # Using Alt+Tab to switch between windows
        pyautogui.hotkey('alt', 'tab')
        time.sleep(0.5)  # Optional delay to ensure the window has switched

        print("Switched to the next window.")

    except Exception as e:
        print(f"An error occurred while switching to the next tab. Error: {str(e)}")

def get_joke():
    return pyjokes.get_joke()

# Function to open windows clock
def open_windows_clock():
    try:
        command = "powershell -Command \"Start-Process 'shell:AppsFolder\\Microsoft.WindowsAlarms_8wekyb3d8bbwe!App'\""
        subprocess.run(command, shell=True, check=True, text=True)
        time.sleep(3)
        speak("Opening Clock")
    except Exception as e:
        speak(f"Sorry, I couldn't open the Alarms and Clock application. Error: {str(e)}")    

def parse_alarm_time(command):
    # Normalize the command to lowercase and remove "set an alarm for" or "set an alarm at"
    command = command.lower()
    command = re.sub(r'\b(set an alarm (for|at))\b', '', command).strip()  

    # Check for AM/PM
    if "am" in command or "pm" in command:
        meridian = "AM" if "am" in command else "PM"
        command = command.replace("am", "").replace("pm", "").strip()  

        # Parse time part (like "three thirty" or "nine")
        time_parts = re.findall(r'\b(\d+|\w+)\b', command)

        hour_part = time_parts[0] if len(time_parts) > 0 else ''
        minute_part = time_parts[1] if len(time_parts) > 1 else '00'

        # If hour is a word, convert it to a number
        if hour_part.isalpha():
            hour_part = mv.WORD_TO_NUMBER.get(hour_part, None)
            if hour_part is None:
                print("Could not understand the hour part.")
                return None
        hour_part = int(hour_part)

        # If minute part is also a word, convert it to a number
        if minute_part.isalpha():
            minute_part = mv.WORD_TO_NUMBER.get(minute_part, '00')

        # Ensure minute part is two digits
        minute_part = str(minute_part).zfill(2)

        # Construct time in HH:MM AM/PM format
        time_string = f"{hour_part}:{minute_part} {meridian}"
        return time_string
    else:
        print("Could not understand the time. Please try again.")
        return None
    
# Function to set an alarm using pyautogui
def automate_alarm_setting(alarm_time):
    try:
        time.sleep(0.1)

        # Press 'Tab' to navigate to Add Alarm
        pyautogui.press("tab", presses=6, interval=0.5)
        pyautogui.press("enter")
        time.sleep(0.5)

        # Split the alarm time into components
        hour, rest = alarm_time.split(":")
        minute, am_pm = rest.split(" ")

        # Navigate to Hours and enter value
        pyautogui.write(hour)

        # Navigate to Minutes and enter the minute
        pyautogui.press("tab")
        pyautogui.write(minute)

        # Navigate to AM/PM toggle
        pyautogui.press("tab")
        if am_pm.lower() == "am":
            pyautogui.press("up")  # Set AM
        else:
            pyautogui.press("down")  # Set PM

         # Navigate to Save button and press Enter
        pyautogui.press("tab", presses=6, interval=0.5)
        pyautogui.press("enter")


    except Exception as e:
        print(f"Error automating alarm setting: {e}")    

def set_alarm(command):
    alarm_time = parse_alarm_time(command)
    if alarm_time:
        print(f"Setting an alarm for {alarm_time}")
        open_windows_clock()  
        automate_alarm_setting(alarm_time)  
    else:
        print("Could not understand the time. Please try again.")

# def normalize_url(command):
#     command = command.lower().strip()

#     # Replace mispronunciations
#     for wrong, correct in mv.URL_MISPRONUNCIATIONS.items():
#         command = command.replace(wrong, correct)

#      # Replace 'dot' with '.' for general cases
#     command = command.replace(" dot ", ".")

#     return command

# def get_url(command):
#     for url, keywords in mv.URL.items():
#         if any(keyword in command for keyword in keywords):
#             return url
#     return None 

# def open_website(command, browser=None):
#     norm_command = normalize_url(command)
#     print(norm_command)
#     url = get_url(norm_command)
#     if url:
#         # Determine which browser to use
#         browser_id = mv.BROWSERS.get(browser, mv.BROWSERS["default"])
#         if browser_id:
#             subprocess.run(["powershell", "Start-Process", browser_id, url], shell=True)
#         else:
#             webbrowser.open(url)    
#     else:
#         speak("I couldn't understand the website. Could you try again?")            

def google_search(query, browser="default"):

    # Format for the google search url
    search_url = f"https://www.google.com/search?q={query}"
    if browser and browser in mv.BROWSERS:
        browser_command = mv.BROWSERS[browser]
        try:
            # Use PowerShell to open the specified browser
            subprocess.run([
                "powershell", "-Command",
                f"Start-Process '{browser_command}' '{search_url}'"
            ])
        except Exception as e:
            print(f"Failed to open browser {browser}: {e}")
    else:
        # Open in default browser
        webbrowser.open(search_url)

def play_youtube_video_in_browser(video_title):
    try:

        ydl_opts = {
            "format": "best",
            # Suppress console output
            "quiet": True,  
            # Ensure only a single video is processed
            "noplaylist": True,  
        }

        # Use yt-dlp to fetch the video URL
        with YoutubeDL(ydl_opts) as ydl:
            # Search for the video on YouTube
            results = ydl.extract_info(f"ytsearch:{video_title}", download=False)
            if "entries" in results and len(results["entries"]) > 0:
                video_url = results["entries"][0]["webpage_url"]
            else:
                raise Exception("No results found for the video.")
        
        # Open the video in the default web browser
        webbrowser.open(video_url)
    
    except Exception as e:
        print(f"Error opening video: {e}")
        speak("Sorry, I couldn't open the video. Please try again.")

def get_current_location():
    try:
        # Use the provided access token
        token = "31a16b3a85014a"
        response = requests.get("https://ipinfo.io", params={"token": token})
        
        # Print response for debugging
        print("IPInfo response:", response.json())
        
        if response.status_code == 200:
            data = response.json()
            # Extract city from the response
            city = data.get("city", "Unknown")
            return city
        else:
            print(f"Error fetching location: {response.status_code}")
            return "Unknown"
    except Exception as e:
        print(f"Exception in get_current_location: {str(e)}")
        return "Unknown"

def get_weather(city=None):
    api_key = "c887d64f464629e8f6d340f0b2c8a6eb"
    if not city:
        # Gets current location
        city = get_current_location()  

    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(base_url)
        if response.status_code == 200:
            data = response.json()
            weather_description = data['weather'][0]['description']
            temperature = data['main']['temp']
            feels_like = data['main']['feels_like']
            city_name = data['name']
            country = data['sys']['country']
            return f"The weather in {city_name}, {country} is {weather_description} with a temperature of {temperature}°C (feels like {feels_like}°C)."
        else:
            return "I'm unable to fetch the weather data. Please try again later."
    except Exception as e:
        return f"An error occurred while fetching the weather: {str(e)}"

def create_new_document_in_application():
    try:
        pyautogui.hotkey('ctrl', 'n')  
        speak("A new document has been created.")
        time.sleep(0.5)
    except Exception as e:
        print(f"Error creating a new document: {e}")
        speak("Failed to create a new document.")
 
def write_in_application(content):
    try:
        time.sleep(0.5)  
        pyautogui.write(content, interval=0.05) 
        speak("The content has been written.")
    except Exception as e:
        print(f"Error writing content: {e}")
        speak("Failed to write the content.") 

def save_content():
    try:
        pyautogui.hotkey('ctrl', 's')
        speak("The content has been saved.")
    except Exception as e:
        print(f"Error saving content: {e}")
        speak("Failed to save the content.")

def write_via_voice(ui):
    try:
        ui.update_status("Listening for content to write...")
        speak("What would you like to write?")
        content = listen_command()

        if content:
            print(f"Writing: {content}")
            write_in_application(content)
        else:
            speak("I didn't catch that. Please try again.")
    except Exception as e:
        print(f"Error during voice-based writing: {e}")
        speak("Failed to process your request for writing.")    

def send_whatsapp_message(contact, message):
    try:
        open_uwp_app_dynamically("whatsapp")
        time.sleep(1)

        # Search for the contact
        pyautogui.hotkey('ctrl', 'f')
        time.sleep(1)
        pyautogui.write(contact)
        time.sleep(1)
        pyautogui.press("enter")
        time.sleep(1)

        if message:
            pyautogui.press('down')
            pyautogui.press('enter')
            pyautogui.write(message)
            pyautogui.press('enter')
            speak(f"Message sent to {contact}")

        else:
            speak("I couldn't hear the message. Please try again.")

    except Exception as e:
        print(f"Failed to send message: {e}")
        speak("Something went wrong. Please try again.")           

def adjust_volume(command):
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = interface.QueryInterface(IAudioEndpointVolume)

        # Get current volume level (scalar value between 0.0 and 1.0)
        current_volume = volume.GetMasterVolumeLevelScalar()
        print(f"Current volume level: {current_volume * 100:.1f}%")

        # Split command into words and look for a number word
        words = command.split()
        percentage = None
        for word in words:
            percentage = word_to_number(word)
            if percentage is not None:
                break

        if percentage is None:
            speak("By how much should I adjust the volume?")
            response = listen_audio(timeout=5, pharse_time_limit=3)  # Listen for the percentage
            print(f"Received follow-up command: {response}")
            words = response.split()
            for word in words:
                percentage = word_to_number(word)
                if percentage is not None:
                    break

        if percentage is not None:
            # Convert to scalar (0.0 to 1.0)
            scalar_change = percentage / 100.0

            if "increase" in command:
                new_volume = min(current_volume + scalar_change, 1.0)
            elif "decrease" in command:
                new_volume = max(current_volume - scalar_change, 0.0)

            volume.SetMasterVolumeLevelScalar(new_volume, None)
            print(f"New volume level: {new_volume * 100:.1f}%")
            speak(f"Volume {'increased' if 'increase' in command else 'decreased'} by {percentage} percent.")
        else:
            speak("I couldn't understand the percentage. Please try again.")

    except Exception as e:
        print(f"Failed to adjust volume: {e}")
        speak("Something went wrong while adjusting the volume.")


def adjust_brightness(command):
    try:
        # Get the current brightness level (returns a list, take the first value)
        current_brightness = sbc.get_brightness()[0]
        print(f"Current brightness level: {current_brightness}%")

        # Split command into words and look for a number word
        words = command.split()
        percentage = None
        for word in words:
            percentage = word_to_number(word)
            if percentage is not None:
                break

        if percentage is None:
            speak("By how much should I adjust the brightness?")
            response = listen_audio(timeout=5, pharse_time_limit=3)
            print(f"Received follow-up command: {response}")
            words = response.split()
            for word in words:
                percentage = word_to_number(word)
                if percentage is not None:
                    break

        if percentage is not None:
            if "increase" in command:
                new_brightness = min(current_brightness + percentage, 100)
            elif "decrease" in command:
                new_brightness = max(current_brightness - percentage, 0)

            sbc.set_brightness(new_brightness)
            print(f"New brightness level: {new_brightness}%")
            speak(f"Brightness {'increased' if 'increase' in command else 'decreased'} by {percentage} percent.")
        else:
            speak("I couldn't understand the percentage. Please try again.")

    except Exception as e:
        print(f"Failed to adjust brightness: {e}")
        speak("Something went wrong while adjusting the brightness.")

def mute_audio(command):
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = interface.QueryInterface(IAudioEndpointVolume)

        # Get current mute state (True if muted, False if unmuted)
        is_muted = volume.GetMute()

        if "mute" in command and not is_muted:
            # Mute the audio if it's not already muted
            volume.SetMute(True, None)
            speak("Audio is now muted.")
        elif "unmute" in command and is_muted:
            # Unmute the audio if it's currently muted
            volume.SetMute(False, None)
            speak("Audio is now unmuted.")
        else:
            # If the command is not clear or volume is already in desired state
            speak("The audio is already in the desired state.")

    except Exception as e:
        print(f"Failed to mute/unmute audio: {e}")
        speak("Something went wrong while muting or unmuting the audio.")    


def send_email():
    try:
        # Ask for recipient name
        speak("Who do you want to send the email to?")
        recipient_name = listen_audio(timeout=30, phrase_time_limit=10).lower().strip()

        # Check if the name exists in the email contacts
        if recipient_name in mv.EMAIL_CONTACTS:
            recipient_email = mv.EMAIL_CONTACTS[recipient_name]
        else:
            speak(f"I don't have an email for {recipient_name}. Please try again.")
            return

        # Ask for the subject
        speak("What is the subject of the email?")
        subject = listen_audio(timeout=30, phrase_time_limit=10)
        if not subject:
            speak("I didn't catch the subject. Please try again.")
            return

        # Ask for the body of the email
        speak("What would you like to say in the email?")
        body = listen_audio(timeout=60, phrase_time_limit=20)
        if not body:
            speak("I didn't catch the message. Please try again.")
            return

        # Compose the email
        email = EmailMessage()
        email['From'] = 'your_email@example.com'  # Replace with your email
        email['To'] = recipient_email
        email['Subject'] = subject
        email.set_content(body)

        # Send the email using SMTP
        with smtplib.SMTP_SSL('smtp.your_email_provider.com', 465) as server:
            server.login('your_email@example.com', 'your_password')  # Replace with your credentials
            server.send_message(email)
        
        speak(f"Email sent to {recipient_name}.")
    
    except Exception as e:
        print(f"Failed to send email: {e}")
        speak("Something went wrong while sending the email. Please try again.")




def process_commands(ui):
     while True:
                command = listen_command()
                if command:
                    ui.update_status(f"Processing: {command}")
                    norm_command = normalize_command(command)
                    print(f"Command: {norm_command}")

                    if any(exit_word in normalize_exit_word(command) for exit_word in mv.exit_words):
                        exit_message = random.choice(["goodbye", "see you later", "bye"])
                        ui.update_response(exit_message)
                        speak(exit_message)
                        break

                    elif "how are you" in command:
                        response = "I'm just a program, but I'm functioning well! How about you ?"
                        ui.update_response(response)
                        speak(response) 

                    elif "what can you do" in command:
                        tasks = ', '.join(mv.TASKS.get("tasks", []))
                        response = f"I can help you with different desktop functionalities. The commands you can use are: {tasks}"
                        ui.update_response(response) 
                        speak(response)

                    elif "are you still there" in command or "are you still here" in command:
                        response = random.choice(["Yes, how may I assist you", "Yes I'm here. How can I help you ?"])
                        ui.update_response(response)
                        speak(response)

                    # elif "what's the time" in command or "what time is it" in command or "can you tell me the time" in command:
                    #     response = f"It's {get_time()}"
                    #     ui.update_response(response)
                    #     speak(response)

                    elif norm_command == "what's the time":
                        response = f"It's {get_time()}"
                        ui.update_response(response)
                        speak(response)

                    elif norm_command == "tell me a joke":
                        response = get_joke()
                        ui.update_response(response)
                        speak(response)

                    elif "open" in norm_command:
                        program_name = command.replace("open", "").strip()
                        if program_name:
                            # Normalizing the program name using aliases
                            normalized_name = normalize_program_name(program_name)
                            # First, try to open UMP apps dynamically
                            uwp_apps = get_uwp_apps()
                            if normalized_name.lower() in uwp_apps:
                                open_uwp_app_dynamically(normalized_name)
                            else:
                                open_program_dynamically(normalized_name)

                            ui.update_response(f"Opening {normalized_name}")    

                    elif "close" in norm_command:
                        program_name = command.replace("close", "").strip()
                        if program_name:
                            # Normalizing the program name using aliases
                            program_name = normalize_program_name(program_name)
                            close_app(program_name)
                            ui.update_response(f"Closing {program_name}")  
                            speak(f"Closing {program_name}")  

                    elif norm_command == "switch to the next tab":
                        switch_tab()

                    elif "set an alarm for" in command or "set an alarm at" in command:
                        set_alarm(command)

                    # elif "go to" in command:
                    #     browser = None 
                    #     for browser_name in mv.BROWSERS.keys():
                    #         if browser_name in command:
                    #             browser = browser_name
                    #             break 

                    #     # Remove browser name from the command to avoid interference
                    #     if browser:
                    #         command = command.replace(browser, "").strip()
                    #     open_website(command, browser)

                    elif "google" in command:
                        query = command.replace("google", "").strip()
                        browser = None

                        if "in chrome" in query:
                            browser = mv.BROWSERS["chrome"]
                            query = query.replace("in chrome", "").strip()
                        elif "in edge" in query:
                            browser = mv.BROWSERS["edge"]
                            query = query.replace("in edge", "").strip()
                        elif "in arc" in query:
                            browser = mv.BROWSERS["arc"]
                            query = query.replace("in arc", "").strip()

                        google_search(query, browser)
                        ui.update_response(f"{query}")

                    elif "play" in norm_command and "on youtube" in norm_command:
                        # Extract the video title from the command
                        video_title = command.replace("play", "").replace("on youtube", "").strip()
                        if video_title:
                            ui.update_status(f"Playing {video_title} on YouTube")
                            response = f"Playing {video_title} on YouTube."
                            ui.update_response(response)
                            speak(response)
                            
                            # Play the video in the browser in a separate thread
                            threading.Thread(target=play_youtube_video_in_browser, args=(video_title,), daemon=True).start()
                        else:
                            speak("Please specify what you want to play on YouTube.")    

                    elif "what's the weather today" in command or "what is the weather today" in command or "how's the weather today" in command:
                        # Check if the user specified a city
                        if "in" in command:
                            city = command.split("in")[-1].strip()
                        else:
                            city = None

                        weather_info = get_weather(city)
                        ui.update_response(weather_info)
                        speak(weather_info)   

                    elif norm_command == "write":
                        # Function to write
                        write_via_voice(ui)

                    elif norm_command == "create a new":
                        create_new_document_in_application()

                    elif norm_command == "save":
                        save_content()        

                    elif "send a message on whatsapp" in norm_command:
                        speak("Who do you want to message?")
                        contact = listen_audio(timeout=60, pharse_time_limit=10)

                        if contact:
                            speak("What would you like to say?")
                            message = listen_audio(timeout=60, pharse_time_limit=60)

                            if message:
                                send_whatsapp_message(contact, message)

                            else:
                                speak("I couldn't hear the message. Please try again.")    

                        else:
                            speak("I couldn't get the contact name. Please try again")     

                    elif "mute audio" in norm_command:
                        mute_audio(norm_command)

                    elif "unmute audio" in norm_command:
                        mute_audio(norm_command)

                    elif "increase the volume" in norm_command or "decrease the volume" in norm_command:
                        adjust_volume(norm_command)    

                    elif "increase brightness" in norm_command or "decrease brightness" in norm_command:
                        adjust_brightness(norm_command)
             

                else:
                    speak("let's try again")

def workflow(ui):

    while True:
    
       ui.update_status("Listening for a command....")

       if wake_word(mv.wake_words):
            wish = Greet()
            response = random.choice([f"{wish}! I am Luna, your virtual assistant. How can I help you?"])
            ui.update_response(response)
            speak(response)

            process_commands(ui)  

if __name__ == "__main__":
    # Initialize the UI
    ui = LunaUI()

    # Start the background assistant logic in a separate thread
    thread = Thread(target=workflow, args=(ui,))
    thread.daemon = True
    thread.start()

    ui.run()
    
    
           
                
                       

    


