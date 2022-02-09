"""
This is a testing file with no connection to the program.
"""

import numpy as np
import pygame
import time
from PianoNote import PianoNote
from PianoNotePlayer import PianoNotePlayer

sample_rate = 44100
PIANO_NOTES_TEMPLATE = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
piano_notes_str = []  # store strings of notes
piano_notes = []   # stores all piano notes as PianoNote object
piano_notes_waves = []  # stores all piano note as waves(arrays) corresponding to each note

def get_wave(freq, duration=0.5, spd=0.0004):
    # Basic Wave
    t = np.linspace(0, duration, int(sample_rate * duration))
    amplitude = np.exp(-spd * 2 * np.pi * freq * t)  # change 0.0004 to change speed
    y = amplitude * np.sin(2 * np.pi * freq * t)
    # Adding Overtones
    y += amplitude / 2 * np.sin(4 * np.pi * freq * t)
    y += amplitude / 4 * np.sin(6 * np.pi * freq * t)
    y += amplitude / 8 * np.sin(8 * np.pi * freq * t)
    y += amplitude / 16 * np.sin(10 * np.pi * freq * t)
    y += amplitude / 32* np.sin(12 * np.pi * freq * t)
    # Make sound more saturated
    y += y * y * y
    # Final modification
    y *= 1 + 16 * t * np.exp(-6 * t)
    # scale to int16 for sound card
    y = (y*1500).astype(np.int16)
    return y

def get_test_wave(self, freq, amplitude=4096, duration=5):
    # Basic Wave
    t = np.linspace(0, duration, int(sample_rate * duration))
    return amplitude * np.sin(2 * np.pi * freq * t)


note1 = PianoNote('C3')
note2 = PianoNote('C#3')

pp = PianoNotePlayer()
wave = get_wave(note1.get_freq, 5)

wave = np.repeat(wave.reshape(len(wave), 1), 2, axis = 1)
sound = pygame.sndarray.make_sound(wave)

"""
prev_time = 0

while True:
    if time.time() - prev_time >= 0.1:
        prev_time = time.time()
        pp.add_notes([PianoNote('C4')])
        pp.play()
    #time.sleep(1)
"""
"""
import os

def resource_path(relative_path):
    # Get absolute path to resource, works for dev and for PyInstaller
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

Logo = resource_path("piano_keys.jpg")
print(Logo)
"""
"""
# create a sound from NumPy array of file
snd = pygame.mixer.Sound(my_sound_source)

# open new wave file
sfile = wave.open('pure_tone.wav', 'w')

# set the parameters
sfile.setframerate(SAMPLINGFREQ)
sfile.setnchannels(NCHANNELS)
sfile.setsampwidth(2)

# write raw PyGame sound buffer to wave file
sfile.writeframesraw(snd.get_buffer().raw)

# close file
sfile.close()
"""
