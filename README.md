# Keyboard Piano Project
by Junhua (Michael) Ma


## Goals
- Design a piano with 7 octaves (84 notes) that can be played on keyboard.
- Should have optimal design so that the fingers represent normal typing position and is as comfortable as possible.
- Although it's fundamentally different playing experience than an actual piano, it should be fun and convenient to play anywhere on the computer and require a different type of mastery (like a rhythm game).
- Visual display of actual piano being played so that when pressing keys on the keyboard, the user can look where it corresponds to the actual piano
- Record function to record what is played at any time as Mp3 files at the press of a record button
- Stores chords/songs and provide practice mode to assist in mastery of a song similar to a rhythm game?


## Design
**How to fit piano keys onto typical small keyboard for laptops**
- I plan to use the number buttons 1-7 to correspond to the 7 octaves on a piano.
- I plan to break the keyboard into 2 parts similar to the standard speed typing partition so all fingers have easy reach and the usual typing motion can be incorporated into playing this piano.
- I plan to fix the left and right partition of the keyboard into respective octave range: the left hand side is for octaves 1 to 4, the right hand side is for octaves 4 to 7, to simulate the typical hand separation on piano.
  - This does limit the simulated piano playing to such that the left hand is always to the left of the right hand because the left hand, for example, can never play octaves above 4.
- Each left and right partition would have 12 active keys each corresponding to a segment of the piano. To increase the number of position, I plan to increased the inputs from the number buttons such that when two buttons are pressed at the same time, it correspond to a more detailed position (I assume that for most cases about 12 notes is a good enough window/stretching, but I have room for more keys if needed).
  - For example: number 1 and 2 pressed at the same time means to switch to octave "1.5", I can also implement a couple of special buttons for small adjustments left and right

**Design Clarification**
The goals of the design are listed below from highest to lowest priority:
- physically possible to play any arrangement playable on a real Piano
- comfortable, without causing any harm to hands / fingers
- sounds like a real piano


## Research and Development Log

### Date: 2/04/2022
**Piano Note Sound**
- The First library to test is mingus, http://bspaans.github.io/python-mingus/, which contains many music theory materials and utilizes a note player called FluidSynth, so I don't need to do the work of recreating a synthesizer. I would need to test if it can play all the scales and if I can set many different attributes to simulate an actual piano.
  - Issue: very complicated to install and use for my case
- I couldn't figure out how to work with mingus and FluidSynth, so I decided to test a simpler library called musicalbeeps, https://pypi.org/project/musicalbeeps/
  - Issue 1: has unpleasant sound at the termination of each note Sound
  - Issue 2: doesn't sound like a piano
- I decided to test synthesizer.
  - Issue: I can't pip install pyaudio, which is required by synthesizer.
- I couldn't find any existing synthesizer library that works for me, so I decided to program a simple piano synthesizer using the math provided here: https://dsp.stackexchange.com/questions/46598/mathematical-equation-for-the-sound-wave-that-a-piano-makes. Starting with a plain beep signal at a certain frequency as a sine wave, a series of operations are performed to make the resulting wave similar to a piano.
  - Issue 1: I use the basic sounddevice to play the wave. But the sound device can only play wave in form of numpy arrays, which means if multiple keys are pressed at the same time, I have to calculate the resulting waveform and store in array.
    - Solution: created function combine_wave to combine multiple waves into one wave. Can be modified and improved because the initial sound has unpleasant noise
    - Update (2/05/2022): I think I fixed the issue of unpleasant noise by accident with the insertion of this line of code at the very end of the get wave function: y = (y*1500).astype(np.int16). The value 1500 is obtained by trial and error, and it's similar to a filter value: if too high, then the original unpleasant noise would be included, lower it till the unpleasant noise disappears. It does make volume go down but that's actually more of a benefit since it was too loud previously.
    - Update (2/07/2022): the value 1500 is changed down to 1200 because of the noise detected when playing 4-5 notes at the same time.
  - Issue 2: I don't know how to make fast notes, like playing the note at k times speed.
    - Solution: by changing a constant in the amplitude calculation I accidentally sped up the sound and solved this problem. So I added a parameter to speed to the get_wave() function which would change the speed
    - Following Issue: how to change this actively when playing notes

The decision at this point is to stick with my custom piano synthesizer, and maybe wrap it up with OOP later.

**Piano Note Frequencies**
- I found the formula to calculate all frequencies from the fundamental frequency A4 = 440Hz: https://pages.mtu.edu/~suits/NoteFreqCalcs.html
- Solution: create a function to calculate frequency for all notes, thus I don't need CSV files to map note name to frequencies


### Date: 2/05/2022
**Python Getting Keyboard Input**
- Detecting input from keyboard is very easy with python: https://stackoverflow.com/questions/24072790/how-to-detect-key-presses
- In the while loop, the boolean is_pressed() function is constantly updating. So if the fingers remains pressing the button, the function returns true until the button is released.
- Implemented my change scale design with basic conditionals. Have to use time() and a fixed refresh interval to detect input because it's very difficult to press or stop pressing 2 buttons simultaneously.
  - Update (2/06/2022): this refresh_rate design forms the foundation of all operations in the main loop like the PianoNotePlayer, not just for keyboard

**Object Oriented Programming**  
My program has now reached the complexity that would greatly benefit from OOP. My design is as follows:
- PianoNote class: create a basic note with attributes name, sharp (boolean), octave, and methods like get_frequency(), to_str(). There are 2 constructors such that a Note can be constructed the normal way of passing 3 variables to initialize each of the 3 attributes or initialize by passing a formatted string.
- PianoNotePlayer class: wraps around note and sounddevice* to make it simple to generate waves and play notes, and especially multiple notes at once or notes at different speeds
  - Added function: initialize and stores all the waves for all the piano notes at the beginning of program so that no more wave generation is needed for individual notes during program.
    - Follow up issue: all waves are initialized ay fixed default speeds, so I can no longer think of any way to change speed of each note with this approach, so if it's really important to change speed of notes, I would have to make changes to this approach
  - Update (2/06/2022)*: souddevice is changed to pygame.mixer
- WavePlotter Class: does all the plotting of the notes, useful for testing and designing
  - I Decided to add plot function directly in NotePlayer instead, so this class is removed for now
- PianoKeyboard class: contains all logic, mappings, and design of computer keyboard to piano keys
After all this, in piano.py as the main function, only need to declare objects and have them work/work together in a main loop: PianoKeyboard sends a list of notes currently played (detected by keyboard input) to PianoNotePlayer, which addes the notes by superposition and play the final note.
  - Issue: when a button is pressed and is not released, it would keep sending data as pressed. So it can't be directly added to the list to be played because it would be repeatedly played throughout the duration of the press.
    - Solution: I used a list that keeps track of which notes are currently pressed. So the list of notes sent to the player only contains a note once each time it's pressed, and no more duplicate is sent to the player for the remaining duration of the press

**Update to playing sounds**  
I have been using sounddevice up to this point to easily play any wave encoded as a numpy array. However, the way to play sounds with sounddevice require the use of sleep function, and in the case of my program that requires adding waves when multiple notes are played while keeping track of individual notes, this becomes very complicated to do.
- Potential solution: I'm looking for something in python (or if I need to program it myself) that can connect with the audio output port throughout the duration of the program, so a variable t (time) is constantly updating - like a live plot. During this "live plot", when a note is played, it's wave is added to whatever the existing wave is - like a input to the live plot by the principle of superposition.
  - I decide to test pygame's capability to play sounds as an alternative to soundevice
  - I was able to play a sound with this guide: https://stackoverflow.com/questions/64950167/trying-to-play-a-sound-wave-on-python-using-pygame
  - unlike sounddevice, pygame has the following benefits that's great for this project:
    - even with sleep, the audio isn't shut down abruptly but it connected with the previous playing notes, so even in a while loop with sleep(), the notes played won't be cut after each iteration, so it's exactly what I'm looking for.
    - in fact, I can completely leave out sleep function and the previously separated notes would just play simultaneously, this is not possible with sounddevice and is great for the project

After the implementation of OOP and pygame, all works well besides some minor problems. The sound sounds very good.
- Issue: when I play repeatedly very fast such that lots of sounds stack on each other, the input at some point would no longer play any sound until a while later when some previous sounds go alway
  - Solution: I found out that the reason why pygame.mixer works so well is because it uses multiple channels (default of 8 channels). So when in a loop and play() is repeatedly called, the first sound would go to channel 1 and if the second sound is played before the duration of the first sound, the second sound would go to channel 2, and other subsequent sound follows the same idea to occupy all the channels. So the solution can be approached by either decrease the duration of each note or increase the number of channels such that more than duration * sample_rate of sound can be played simultaneously. So I increased my number of channels from default 8 to 50 (5*0.1)

A trick that really helped me up to this point is the use of a testing file called test.py, which is separated from the main file but can use all the classes. I used this to figure out how pygame.mixer, my own classes, and many other unfamiliar libraries work.


### Date: 2/06/2022
**Adding and Improving Scale Changing**  
Updated Design for changing scales:
- Since there are only 7 octaves but there are 10 number buttons from 1 to 0, I decide to give up the exact correspondence between the number of the button for the convenience of playing and switching scales. So I plan to use the 10 number buttons in the following way:
  - Button 1-2: switch left scale left or right by 1 note
  - Buttons 3-9: change octave for fixed position starting at C
    - Pressing 34, 45 at the same time correspond to 1.5-2.5 and 2.5-3.5
    - Pressing 56, 67, 78, 89 at the same time correspond to 4.5-5.5, 5.5-6.5, 6.5-7.5
  - Buttons 0 and -: switch right scale left or right by 1 note

During development of this feature, it becomes increasingly clear to me that I'm adding many duplicate codes because the left scale and the right scale function very similarly. So later on I can try to reduce the redundancy and make it more compact.

The main challenge during this development is figuring out left and right shift. Previously, each number points to a window that always start at C, and this would not be the case when the user can freely slide the window left and right.
- The letters like "C" or "C#" are easy to switch due to python's great list slicing abilities.
- The main difficulty likes in keeping track of the octaves in a window, which is previously all the same number, and is now partitioned into 2 numbers based on the position of the window.
  - I decided to use a simple brute force approach to this problem thanks to the fact that there are only about 80 keys in the piano. I initializes a 1D-array that stores all the octaves for each note of the piano as a list (i.e. it would be 12 1's followed by 12 2's followed by 12 3's...). With this approach, all I need to keep track of are two pointers pointing at two distinct position of this array to represent a window's position, and I can then quickly obtain the correct octave numbers in the window. This approach does require me to change some other methods in the class as well, but it works for all of the previous methods as well as new ones.

**Piano Virtual Display**  
It's easy to develop a basic display with pygame, which is already imported and used to play sounds. The code of pygame is directly added to Piano.py, the main file of the project.
- I decided to use the image of all the piano keys as the main display instead of drawing over 80 rectangles.
  - As a result, instead of having each key light up when pressed or in window, I only need to draw some indicator rectangles at the position of the key on the image, and have a window indicator which is a big half transparent rectangle covering the window on the image.
- I used trial and error to determine the position and size of the components, including 2 window indicators as rectangle bars and various number of note indicators as small circles based on the number of notes pressed.
  - OOP is very beneficial in this case because I can simply connect my PianoKeyboard class with pygame main loop to provide values for window positions and list of notes that are pressed, which pygame can then draw to the window.


### Date: 2/07/2022
**Attempt to Create the first exe file**  
At this point, the result looks good for the version 1 to packaged into an executable file to be run at any time as a simple application.
- I used pyinstaller to make the executable file
  - The first executable crashed out at the beginning, so I decided to remove matplotlib and the plotting function for now to simplify the program.
  - I also think an issue is with the image I used, so I looked up the solution here: https://stackoverflow.com/questions/31836104/pyinstaller-and-onefile-how-to-include-an-image-in-the-exe-file
  - Have no success so far, the exe immediately crashes so I can't read the error message either, maybe will look more into this at a later time.


### Date: 2/08/2022
**Add window connection mode**  
After playing around with my piano, I realized a problem: there's a frequent situation when playing the piano, which is that both hands may switch to a higher or lower position at the same time and covering a continuous large chunk of notes. This is hard to execute with the current design because the left and right is separated, and the only way to shift the left scale to a left position is by moving the window one note at a time, which is too slow and tedious. I plan to design it such that:
- when the user press the space bar, window connection mode turned on, press the space bar again would turn this mode off
- visual display of the 2 windows being connected as a new color to help user distinguish.
- As of now, I would do: when user exit this mode, it always resets the two windows at initial center position.
- The number buttons work for the entire connected window, with left scale buttons set the left edge and right scale buttons set the right edge.
  - For the 4 buttons used for shifting the left scale and right scale, I plan to make them into two sets of shifts of 1 note at a time and 3 notes at a time (because 5 notes should be mostly covered by pressing two buttons at once feature)

Implementation of this feature is very quick and easy because I can reuse my previous functions in my PianoKeyboard class. Because a combined back-to-back window is really just a special case of the previously established left window and right window for which right window remains exactly 12 notes after the left window. So I just needed to add a new boolean attribute to keep track of connect mode in the PianoKeyboard class, modify update_scale_input() function to run the previous logic or my newly implemented combined window logic based on the boolean attribute. the shifting function is used in combined windows mode is the exact same since both windows are always shifted by the exact same amount. I can also reuse my code that draws the windows, all I needed to do is to change the color of both windows to yellow to signify connect mode is on.
- Issue: after some debugging, the only issue that remains is the +3 and -3 shifting feature. Due to the design of the shifting function in PianoKeyboard right now, it only supports shifting by 1.
  - Potential solution: to also support adding more notes to the window later, I plan to use a similar approach that I used for the octave on the note names, which is to compute all the note names in one big array at the beginning so I can easily slide windows across the array to acquire values without performing countless individual array modifications.


### Date: 2/09/2022
**Add more notes to the window**   
After playing around with my piano, I realize that I should try to add as many notes as possible beyond just 12 notes on each scale because it turns out that it's rather common. Based on the number of keys I have on my keyboard, I should be about to at least add 3 notes to each scale for now. In the connected window mode, this would add 6 keys which is half an octave, making connected windows mode have a reach from 2 octaves to 2.5 octaves. These added notes, in combination of all the switch features I added, should allow even more complex piano playing.

Design:
- top row: q-t, y-p  5 notes each (same as before)
- middle row: a-g, h-; 5 notes each (same as before)
- bottom row: z-b, n-/  5 notes each (added 3 notes each)

Changes to PianoKeyboard class:  
As mentioned before, I decided to use a long array to store all the note names so I can apply the sliding window design to easily find the scale at any window position. I have previously used this method to store the octave of notes in the scale, and I'm now extending the same approach to store the name of the notes too.
- Shifting now becomes very simple as the only thing I need to do is to change the window position and obtain the resulting scale names by slicing the corresponding section of the big array.
  - Since the big array is computed initially, I don't need to perform any individual slicing or array operations when shifting. So I could also easily add the function to shift more than one note at a time. I added the ability to shift 3 notes at a time in connected mode, but this really sets up so that I can move as many notes as I want at any time.
- This also sets the state for adding new notes. The previous design relies on the fact that the window size is exactly one octave. With this new design, I can change to any window size since I just need to obtain the corresponding chunk from the big array through slicing.

After the changes to the PianoKeyboard class, I just need to add to the previous keyboard conditional logic to include more keys.


### Date: 2/09/2022
**Add single window mode**  
I decide to also provide a single window mode, which is one single large window covering about 50% of the entire piano keyboard, using as many keys on the keyboard as possible to construct a large window. I got this idea from this virtual piano web app https://www.onlinepianist.com/virtual-piano. The issues with the design of this web app, however, is that:
- it cannot shift the window left or right in any way, so some lowest and highest octaves simply have no keyboard mappings
- it uses shift+key to indicate black notes. This is very limiting because most piano play in keys other than the key of C, which requires a frequent combination of black and white keys in chords and scales.

My window will inherit all the attributes of previous windows, besides it's the largest window possible. In addition, my design provides:
- left and right shifting with a default of 6 keys (half an octave) at a time
- 2 fixed positions: in the center or split on left and right side 


### Date: 2/10/2022
**Add record as mp3 feature**


- slightly increase sample rate?
- more accurate piano sound (low and high scales)?
- add store song and practice mode?
