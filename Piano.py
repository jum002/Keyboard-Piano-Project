from PianoNotePlayer import PianoNotePlayer
from PianoKeyboard import PianoKeyboard
from PianoNote import PianoNote
import pygame
import time
import os

scale_refresh_rate = 0.1
prev_time = 0
octave_spacing = round(11.3*7)

# Initialize the pygame library
pygame.init()

# Initialize class objects
pkb = PianoKeyboard()
pp = PianoNotePlayer()

# Set up the drawing window
screen = pygame.display.set_mode([610, 250])
pygame.display.set_caption('Piano')

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Images
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

img_path = resource_path("piano_keys.jpg")
piano_image = pygame.image.load(str(img_path))

# Positional variables
first_pos_w = (41, 160)
first_pos_b = (47, 142)
ws = pkb.get_window_size()-12

def calculate_position_x(note):
    if note.get_sharp() == False:
        diff = int(note.get_octave()-1)*7 + note.get_ind_w()
        return round(41 + 11.3 * diff)

    else:
        note_str = note.to_str()
        note_str = note_str[0]+note_str[2]
        ns_note = PianoNote(note_str)
        diff = int(ns_note.get_octave()-1)*7 + note.get_ind_w()
        return round(41 + 11.3 * diff)+6

# Run until the user asks to quit
running = True
h_list = []
while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if time.time() - prev_time >= scale_refresh_rate:
        prev_time = time.time()
        pkb.update_scales()
        pkb.update_scale_input()
        pkb.update_note_inputL()
        pkb.update_note_inputR()
        pp.add_notes(pkb.get_active_list())
        pp.play()

    h_list = pkb.get_hold_list()
    screen.blit(piano_image, (0, 0))

    # Draw Note Indicators
    for x in range(0, len(h_list)):
        if h_list[x].get_sharp() == False:
            pygame.draw.circle(screen, RED, (calculate_position_x(h_list[x]), 160), 5)
        else:
            pygame.draw.circle(screen, RED, (calculate_position_x(h_list[x]), 142), 5)

    # Draw Window Indicators
    w_list = pkb.get_current_scale()
    if pkb.in_connect_mode() == False:
        pygame.draw.rect(screen, BLUE, (37+w_list[0]//12*octave_spacing+(w_list[0]%12)*6.6,110,octave_spacing+ws*6.6,10))
        pygame.draw.rect(screen, GREEN, (37+w_list[1]//12*octave_spacing+(w_list[1]%12)*6.6,110,octave_spacing+ws*6.6,10))
    else:
        pygame.draw.rect(screen, YELLOW, (37+w_list[0]//12*octave_spacing+(w_list[0]%12)*6.6,110,octave_spacing+ws*6.6,10))
        pygame.draw.rect(screen, YELLOW, (37+w_list[1]//12*octave_spacing+(w_list[1]%12)*6.6,110,octave_spacing+ws*6.6,10))

    # Flip the display
    pygame.display.flip()

    h_list.clear()


pygame.quit()
