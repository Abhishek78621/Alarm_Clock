import datetime
import time
import os
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox
from threading import Thread
import pygame

TIME_FORMAT = "%I:%M:%S %p"
ALARM_SOUNDS_DIR = "AlarmSounds"
DEFAULT_SOUND = "loudest_alarm.mp3"  # Default sound file

# Global variable to stop the alarm
stop_alarm_flag = False

# Initialize pygame mixer
pygame.mixer.init()

def get_sound_paths():
    if not os.path.exists(ALARM_SOUNDS_DIR):
        os.makedirs(ALARM_SOUNDS_DIR)
    return [os.path.join(ALARM_SOUNDS_DIR, sound) for sound in os.listdir(ALARM_SOUNDS_DIR) if sound.endswith('.mp3')]

def play_sound(sound_file):
    # Play the sound file.
    try:
        pygame.mixer.music.load(sound_file)
        pygame.mixer.music.play(-1)  # Loop the sound indefinitely
    except FileNotFoundError:
        print(f"Sound file {sound_file} not found.")
    except Exception as e:
        print(f"Error playing sound: {e}")

def stop_sound():
    pygame.mixer.music.stop()

def alarm_clock(alarm_time, sound_file, message, repeat_interval):
    global stop_alarm_flag
    stop_alarm_flag = False
    try:
        while True:
            current_time = datetime.datetime.now()
            if current_time >= alarm_time:
                if stop_alarm_flag:
                    break
                if message:
                    alarm_message_label.config(text=f"Message: {message}", fg="#008000")
                    alarm_message_label.update()

                if sound_file:
                    for _ in range(repeat_interval):
                        if stop_alarm_flag:  # Stop immediately if flag is set
                            break
                        # Play sound for 1 minute (60 seconds)
                        play_sound(sound_file)
                        time.sleep(60)  # Alarm plays for 1 minute
                        stop_sound()  # Stop the sound after 1 minute
                        if stop_alarm_flag:  # Stop the alarm if flag is set after each repeat
                            break
                        # Repeat after the specified interval
                        time.sleep(repeat_interval * 60)
                break
            if stop_alarm_flag:
                break
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nAlarm stopped.")
    finally:
        stop_alarm_flag = False  # Reset the flag when alarm stops

def validate_time_format(time_str):
    try:
        datetime.datetime.strptime(time_str, TIME_FORMAT)
        return True
    except ValueError:
        return False

def parse_alarm_time(alarm_time_str):
    current_time = datetime.datetime.now()
    try:
        alarm_time = datetime.datetime.strptime(alarm_time_str, TIME_FORMAT)
        alarm_time = current_time.replace(
            hour=alarm_time.hour, minute=alarm_time.minute, second=alarm_time.second, microsecond=0
        )
        if alarm_time < current_time:
            alarm_time += datetime.timedelta(days=1)
        return alarm_time
    except ValueError:
        messagebox.showerror("Error", "Invalid alarm time.")
        return None

def set_alarm():
    global stop_alarm_flag
    stop_alarm_flag = False  # Reset stop flag
    alarm_time_str = time_entry.get()

    if not validate_time_format(alarm_time_str):
        messagebox.showerror("Invalid Time Format", "Please enter a valid time format (HH:MM:SS AM/PM).")
        return

    alarm_time = parse_alarm_time(alarm_time_str)
    if alarm_time is None:
        return

    custom_message = message_entry.get()
    
    # Get the sound file: if the user hasn't chosen one, use the default
    sound_choice = sound_combo.get() or DEFAULT_SOUND
    sound_path = os.path.join(ALARM_SOUNDS_DIR, sound_choice)
    
    # Get the repeat interval: if the user hasn't entered one, use the default (5)
    repeat_interval = int(repeat_entry.get() or 5)

    alarm_message_label.config(
        text=f"Alarm set for {alarm_time.strftime('%I:%M:%S %p on %Y-%m-%d')}.\n\nMessage: {custom_message or 'No message'}",
        fg="#fc0404",
        bg="white",
    )

    # Run the alarm clock in a separate thread to keep GUI responsive
    Thread(target=alarm_clock, args=(alarm_time, sound_path, custom_message, repeat_interval), daemon=True).start()

def stop_alarm():
    global stop_alarm_flag
    stop_alarm_flag = True
    stop_sound()  # Stop the sound immediately
    alarm_message_label.config(text="Alarm stopped.", fg="red")

def configure_grid(frame):
    for i in range(2):
        frame.grid_columnconfigure(i, weight=1)
    frame.grid_rowconfigure(7, weight=1)

# GUI setup
root = tk.Tk()
root.title("Alarm Clock")
root.geometry("700x500")
root.iconbitmap("alarm_clock_icon.ico")
root.minsize(700, 400)
root.maxsize(700, 400)

BACKGROUND_COLOR = "#91ad61"
root.configure(background=BACKGROUND_COLOR)

# Main Frame
main_frame = tk.Frame(root, bg=BACKGROUND_COLOR)
main_frame.place(relwidth=1, relheight=1)

# Left side: Image
image_frame = tk.Frame(main_frame, bg=BACKGROUND_COLOR)
image_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

try:
    clock_img = PhotoImage(file="alarm_clock_image.png").subsample(2, 2)
    img_label = tk.Label(image_frame, image=clock_img, bg=BACKGROUND_COLOR)
    img_label.pack(expand=True)
except Exception:
    img_label = tk.Label(image_frame, text="Image not found", font=("Arial", 14), bg=BACKGROUND_COLOR)
    img_label.pack(expand=True)

# Right side: Input Fields
input_frame = tk.Frame(main_frame, bg=BACKGROUND_COLOR)
input_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

# Alarm Time Entry
time_label = tk.Label(input_frame, text="Enter Alarm Time (HH:MM:SS AM/PM)", font=("Arial", 12), bg=BACKGROUND_COLOR)
time_label.grid(row=0, column=0, sticky="w", pady=5)
time_entry = tk.Entry(input_frame, font=("Arial", 15), width=15, bd=1, relief="solid")
time_entry.grid(row=0, column=1, pady=10,padx=10, sticky="ew")

# Custom Message Entry
message_label = tk.Label(input_frame, text="Enter Custom Message:",  font=("Arial", 12), bg=BACKGROUND_COLOR)
message_label.grid(row=1, column=0, sticky="w", pady=5)
message_entry = tk.Entry(input_frame, font=("Arial", 15), width=15, bd=1, relief="solid")
message_entry.grid(row=1, column=1, pady=10,padx=10, sticky="ew")

# Sound Selection Combobox
sounds = [os.path.basename(path) for path in get_sound_paths()]
sound_label = tk.Label(input_frame, text="Select Alarm Sound:", font=("Arial", 12), bg=BACKGROUND_COLOR)
sound_label.grid(row=2, column=0, sticky="w", pady=5)
sound_combo = Combobox(input_frame, values=sounds, font=("Arial", 13), state="readonly", width=15)
sound_combo.grid(row=2, column=1, pady=10, padx=12, sticky="ew")

# Repeat Interval Entry
repeat_label = tk.Label(input_frame, text="Enter Repeat Interval time (default 5):", font=("Arial", 12), bg=BACKGROUND_COLOR)
repeat_label.grid(row=3, column=0, sticky="w", pady=5)
repeat_entry = tk.Entry(input_frame, font=("Arial", 15), width=15, bd=1, relief="solid")
repeat_entry.grid(row=3, column=1, pady=10,padx=10, sticky="ew")

# Set Alarm Button
set_alarm_button = tk.Button(input_frame, text="Set Alarm", command=set_alarm, bg="orange", font=("Arial", 12))
set_alarm_button.grid(row=4, column=0, pady=30,padx=50,sticky="ew")

# Stop Alarm Button
stop_alarm_button = tk.Button(input_frame, text="Stop Alarm", command=stop_alarm, bg="red", font=("Arial", 12))
stop_alarm_button.grid(row=4, column=1, pady=30,padx=10, sticky="ew")

# Alarm message label
alarm_message_label = tk.Label(input_frame, text="", font=("Arial", 16), bg=BACKGROUND_COLOR, fg="red")
alarm_message_label.grid(row=5, column=0, columnspan=2, pady=5, sticky="ew")

# Configure grid for input_frame
configure_grid(input_frame)

# Start the GUI loop
root.mainloop()
