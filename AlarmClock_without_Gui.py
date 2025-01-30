import datetime
import time
from playsound import playsound
import os

# Formats of the time
TIME_FORMAT = "%I:%M:%S %p"

# Directory containing sound files
ALARM_SOUNDS_DIR = "AlarmSounds"

# Get the alarm time from the user
def get_alarm():
    while True:
        alarm_time = input("Enter the time HH:MM:SS AM/PM (two-digit format): ")
        try:
            alarm_time_obj = datetime.datetime.strptime(alarm_time, TIME_FORMAT).time()
            return alarm_time_obj
        except ValueError:
            print("Invalid time format! Please enter time in HH:MM:SS AM/PM format")

# Get the custom message from the user
def get_custom_message():
   while True:
       message=input("Enter the message you want to display: ")
       if message:
           return message
       print("Invalid message format! Please enter the message you want to display")
  
    
# Get the sound files from the directory
def get_sound_paths():
    return [os.path.join(ALARM_SOUNDS_DIR, sound) for sound in os.listdir(ALARM_SOUNDS_DIR) if sound.endswith('.mp3')]

# Play the sound file
def play_sound(sound_file):
    try:
        playsound(sound_file)
    except Exception as e:
        print(f"Error playing sound: {e}")


# Alarm clock function
def alarm_clock(alarm_time, sound_file,message, repeat_interval: int = 5):
    now = datetime.datetime.now()
    alarm_datetime = datetime.datetime.combine(now.date(), alarm_time)
    
    if alarm_datetime < now:
        alarm_datetime += datetime.timedelta(days=1)  # Set for the next day
    
    print(f"Alarm is set for: {alarm_datetime.strftime(f'{TIME_FORMAT} %Y-%m-%d')}\nWaiting...")
    try:
        while True:
            current_time = datetime.datetime.now()
            print(f"Current time is: {current_time.strftime(f'{TIME_FORMAT}')}", end="\r")
            if current_time >= alarm_datetime:
                print(f"\nMessage: {message}")
                play_sound(sound_file)
                print("\nTo stop alarm press Ctrl+C")

                for _ in range(repeat_interval - 1):
                    time.sleep(2)
                    play_sound(sound_file)
                break
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nAlarm stopped.")

# Display the available sounds
def display_sounds(sounds):
    print("Available Alarm Sounds:")
    for i, sound in enumerate(sounds, start=1):
        print(f"{i}. {os.path.basename(sound)}")
        
# Select the sound file      
def select_sound(sounds):
    
    while True:
        
        display_sounds(sounds)  # Display available sounds
        try:
            choice = int(input("Choose a sound by entering the corresponding number: "))
            if 1 <= choice <= len(sounds):
                return sounds[choice - 1]
            print(f"Invalid choice. Please select a number between 1 and {len(sounds)}.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

# Main function
def main():
    sounds = get_sound_paths()
    print("Welcome to Alarm Clock")
    alarm_time = get_alarm()
    selected_sound = select_sound(sounds)
    repeat_interval = int(input("Enter the repeat interval (default is 5): ") or 5)
    custom_message=get_custom_message()
    alarm_clock(alarm_time=alarm_time, sound_file=selected_sound,message=custom_message, repeat_interval=repeat_interval)

# Run the main function
if __name__ == "__main__":
    main()
