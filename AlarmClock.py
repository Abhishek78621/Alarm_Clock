import datetime
import time
from playsound import playsound
import Alarm_sounds
import os

# Formats of the time
TIME_FORMAT = "%I:%M:%S %p"

# Directory containing sound files
ALARM_SOUNDS_DIR = "AlarmSounds"


# Function to get alarm time from user
def get_alarm():

    while True:
        alarm_time = input(
            "Enter the time HH:MM:SS AM/PM (two digit format): ")

        try:
            datetime.datetime.strptime(alarm_time, TIME_FORMAT)

            return alarm_time
        except ValueError:
            print("Invalid time format! Please enter time in HH:MM:SS AM/PM format")


# Function to get full paths for sound files
def get_sound_paths():
    return [
        os.path.join(ALARM_SOUNDS_DIR, sound) for sound in Alarm_sounds.sound_files
    ]


# function to play alarm tone
def play_sound(sound_file):
    try:
        # play the sound
        playsound(sound_file)
    except Exception as e:
        print(f"Error playing sound:{e}")


def alarm_clock(alarm_time, sound_file, repeat_interval: int = 5):

    date = datetime.datetime.now()
    date = date.strftime("%Y-%m-%d")

    print(f"Alarm is set for: {alarm_time} at date {date}.\nWaiting...")
    try:
        while True:
            current_time = datetime.datetime.now().strftime("%I:%M:%S %p")
            print(f"Current time is: {current_time}", end="\r")
            if current_time.casefold() == alarm_time.casefold():
                print("\n\nIt's time to wake up!")
                play_sound(sound_file)
                print("\nTo stop alarm press ctrl+c")

                # Repeat the alarm at regular intervals
                for _ in range(repeat_interval-1):
                    time.sleep(2)  # wait for 2 seconds
                    play_sound(sound_file)
                break

            time.sleep(1)
    except KeyboardInterrupt:
        print("\nAlarm stopped.")


# Function to dipalay the sound list and get user choice
def display_sounds(sounds):

    print("Available Alarm Sounds:")
    for i, sound in enumerate(sounds, start=1):
        print(f"{i}. {os.path.basename(sound)}")
    while True:
        choice = int(
            input("Choose a sound by entering the corresponding number: "))
        if 1 <= choice <= len(sounds):
            return sounds[choice - 1]
        print(f"Invalid choice. Please select a number between 1 and { len(sounds)}.")

# Main function
def main():
    sounds = get_sound_paths()
    print("Welcome to Alarm Clock")
    alarm_time = get_alarm()
    selected_sound = display_sounds(sounds)
    repeat_interval = int(
        input("Enter the repeat interval (default is 5): ") or 5)
    alarm_clock(alarm_time, selected_sound, repeat_interval)
    
    
if __name__ == "__main__":
    main()


