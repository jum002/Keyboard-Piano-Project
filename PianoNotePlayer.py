from PianoNote import PianoNote
import numpy as np
import pygame
import time
#import matplotlib.pyplot as plt

"""
Play piano note or notes from input notes
"""
class PianoNotePlayer:
    __sample_rate = 44100 #Hz
    __notes_waves = []
    __PIANO_NOTES_TEMPLATE = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    __piano_notes_str = []  # store strings of notes
    __piano_notes = []   # stores all piano notes as PianoNote object
    __piano_notes_waves = []  # stores all piano note as waves(arrays) corresponding to each note
    __active_notes = []

    def __init__(self):
        # Initialize pygame.mixer for audio
        pygame.mixer.pre_init(self.__sample_rate, size=-16, channels=1)
        pygame.mixer.init()
        pygame.mixer.set_num_channels(50)
        # Initialize notes and waves
        for x in range(1, 8):
            self.__piano_notes_str.extend([s + str(x) for s in self.__PIANO_NOTES_TEMPLATE])

        self.__piano_notes = [PianoNote(s) for s in self.__piano_notes_str]
        self.__piano_notes_waves = [self.get_wave(s.get_freq()) for s in self.__piano_notes]


    def add_notes(self, notes):
        self.clear_list()
        for x in range(0, len(notes)):
            self.__active_notes.append(notes[x])


    def clear_list(self):
        self.__active_notes.clear()

    """
    Return an array that stores a transformed sine wave that simulates a piano
    note sound.
    """
    def get_wave(self, freq, duration=5, spd=0.0004):
        # Basic Wave
        t = np.linspace(0, duration, int(self.__sample_rate * duration))
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
        # Final modification?
        y *= 1 + 16 * t * np.exp(-6 * t)
        # scale to int16 for sound card
        y = (y*1200).astype(np.int16)
        return y

    """
    Get a basic unmodified sine wave of a certain frequency, can be played as a note
    """
    def get_test_wave(self, freq, amplitude=4096, duration=5):
        # Basic Wave
        t = np.linspace(0, duration, int(self.__sample_rate * duration))
        return amplitude * np.sin(2 * np.pi * freq * t)

    """
    Play wave (not note). To play note: play_wave(get_wave(note))
    """
    def play_wave(self, wave):
        wave = np.repeat(wave.reshape(len(wave), 1), 2, axis = 1)
        sound = pygame.sndarray.make_sound(wave)
        sound.play()


    """
    Main play function, combines and plays the combination of all notes in
    active_notes[] and removing them from the list
    """
    def play(self):
        if len(self.__active_notes) == 0:
            return

        pos = (self.__active_notes[0].get_octave()-1)*12+self.__active_notes[0].get_ind()
        wave = self.__piano_notes_waves[pos]
        for x in range(1, len(self.__active_notes)):
            pos = (self.__active_notes[x].get_octave()-1)*12+self.__active_notes[x].get_ind()
            wave = wave + self.__piano_notes_waves[pos]

        self.play_wave(wave)
        self.clear_list()

    """
    Plot wave for testing and designing purposes
    """
    """
    def plot_note(wave, duration=0.5):
        t = np.linspace(0, duration, int(self.__sample_rate * duration))
        plt.xlabel('time')
        plt.ylabel('amp')
        plt.title('Wave Plot')
        plt.plot(t, wave)
        plt.show()
    """
