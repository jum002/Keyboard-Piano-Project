import keyboard
from PianoNote import PianoNote

class PianoKeyboard:
    __currentScaleL = 24 # 1-3
    __currentScaleR = 36 # 4-7
    __scale_buttonsL = [False, False, False]
    __scale_buttonsR = [False, False, False, False]
    __scale_refresh_rate = 0.1 #sec
    __scale_prev_time = 0
    __PIANO_NOTES_TEMPLATE = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    __PIANO_NOTES_TEMPLATE_H = ['F#', 'G', 'G#', 'A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F']
    __SST = [1]*12
    __left_scale = __PIANO_NOTES_TEMPLATE[:]
    __right_scale = __PIANO_NOTES_TEMPLATE[:]
    __active_list = []
    __hold_list = []
    __hold_listR = []
    __left_shift = 0
    __right_shift = 0
    __connect_w = False


    def __init__(self):
        for x in range(2,8):
            self.__SST.extend([x]*12)


    def update_scales(self):
        # Change Scales
        self.__scale_buttonsL = [keyboard.is_pressed('3'), keyboard.is_pressed('4'),
                                 keyboard.is_pressed('5')]
        self.__scale_buttonsR = [keyboard.is_pressed('6'), keyboard.is_pressed('7'),
                                 keyboard.is_pressed('8'), keyboard.is_pressed('9')]

    def update_scale_input_NC(self):
        if self.__scale_buttonsL[0] == True and self.__scale_buttonsL[1] == True:
            self.__currentScaleL = 6
            self.__left_scale = self.__PIANO_NOTES_TEMPLATE_H[:]
        elif self.__scale_buttonsL[1] == True and self.__scale_buttonsL[2] == True:
            self.__currentScaleL = 18
            self.__left_scale = self.__PIANO_NOTES_TEMPLATE_H[:]
        elif self.__scale_buttonsL[0] == True:
            self.__currentScaleL = 0
            self.__left_scale = self.__PIANO_NOTES_TEMPLATE[:]
        elif self.__scale_buttonsL[1] == True:
            self.__currentScaleL = 12
            self.__left_scale = self.__PIANO_NOTES_TEMPLATE[:]
        elif self.__scale_buttonsL[2] == True:
            self.__currentScaleL = 24
            self.__left_scale = self.__PIANO_NOTES_TEMPLATE[:]

        if self.__scale_buttonsR[0] == True and self.__scale_buttonsR[1] == True:
            self.__currentScaleR = 42
            self.__right_scale = self.__PIANO_NOTES_TEMPLATE_H[:]
        elif self.__scale_buttonsR[1] == True and self.__scale_buttonsR[2] == True:
            self.__currentScaleR = 54
            self.__right_scale = self.__PIANO_NOTES_TEMPLATE_H[:]
        elif self.__scale_buttonsR[2] == True and self.__scale_buttonsR[3] == True:
            self.__currentScaleR = 66
            self.__right_scale = self.__PIANO_NOTES_TEMPLATE_H[:]
        elif self.__scale_buttonsR[0] == True:
            self.__currentScaleR = 36
            self.__right_scale = self.__PIANO_NOTES_TEMPLATE[:]
        elif self.__scale_buttonsR[1] == True:
            self.__currentScaleR = 48
            self.__right_scale = self.__PIANO_NOTES_TEMPLATE[:]
        elif self.__scale_buttonsR[2] == True:
            self.__currentScaleR = 60
            self.__right_scale = self.__PIANO_NOTES_TEMPLATE[:]
        elif self.__scale_buttonsR[3] == True:
            self.__currentScaleR = 72
            self.__right_scale = self.__PIANO_NOTES_TEMPLATE[:]

        # Detect Left-Right input (at the end to be prioritized over the above)
        scale_changeL = False
        scale_changeR = False
        if keyboard.is_pressed('1') and self.__left_shift == 0:
            self.__left_shift = -1
            scale_changeL = True
        elif keyboard.is_pressed('2') and self.__left_shift == 0:
            self.__left_shift = 1
            scale_changeL = True
        elif keyboard.is_pressed('1') == False and keyboard.is_pressed('2') == False:
            self.__left_shift = 0

        if keyboard.is_pressed('0') and self.__right_shift == 0:
            self.__right_shift = -1
            scale_changeR = True
        elif keyboard.is_pressed('-') and self.__right_shift == 0:
            self.__right_shift = 1
            scale_changeR = True
        elif keyboard.is_pressed('0') == False and keyboard.is_pressed('-') == False:
            self.__right_shift = 0


        if scale_changeL == True or scale_changeR == True:
            self.update_LR_scale()


    def update_LR_scale(self):
        if self.__left_shift != 0:
            self.__currentScaleL += self.__left_shift
            if self.__left_shift < 0:
                temp_list = self.__left_scale[0:11]
                temp_list.insert(0, self.__left_scale[11])
                self.__left_scale = temp_list[:]

            else:
                temp_list = self.__left_scale[1:]
                temp_list.append(self.__left_scale[0])
                self.__left_scale = temp_list[:]

        if self.__right_shift != 0:
            self.__currentScaleR += self.__right_shift
            if self.__right_shift < 0:
                temp_list = self.__right_scale[0:11]
                temp_list.insert(0, self.__right_scale[11])
                self.__right_scale = temp_list[:]

            else:
                temp_list = self.__right_scale[1:]
                temp_list.append(self.__right_scale[0])
                self.__right_scale = temp_list[:]


    def update_scale_input_C(self):
        self.__currentScaleR = self.__currentScaleL + 12
        if keyboard.is_pressed('3'):
            self.__currentScaleL = 0
            self.__currentScaleR = self.__currentScaleL + 12
            self.__left_scale = self.__PIANO_NOTES_TEMPLATE[:]
            self.__right_scale = self.__PIANO_NOTES_TEMPLATE[:]
        elif keyboard.is_pressed('4'):
            self.__currentScaleL = 12
            self.__currentScaleR = self.__currentScaleL + 12
            self.__left_scale = self.__PIANO_NOTES_TEMPLATE[:]
            self.__right_scale = self.__PIANO_NOTES_TEMPLATE[:]
        elif keyboard.is_pressed('5'):
            self.__currentScaleL = 24
            self.__currentScaleR = self.__currentScaleL + 12
            self.__left_scale = self.__PIANO_NOTES_TEMPLATE[:]
            self.__right_scale = self.__PIANO_NOTES_TEMPLATE[:]
        elif keyboard.is_pressed('6'):
            self.__currentScaleL = 36
            self.__currentScaleR = self.__currentScaleL + 12
            self.__left_scale = self.__PIANO_NOTES_TEMPLATE[:]
            self.__right_scale = self.__PIANO_NOTES_TEMPLATE[:]
        elif keyboard.is_pressed('7'):
            self.__currentScaleL = 48
            self.__currentScaleR = self.__currentScaleL + 12
            self.__left_scale = self.__PIANO_NOTES_TEMPLATE[:]
            self.__right_scale = self.__PIANO_NOTES_TEMPLATE[:]
        elif keyboard.is_pressed('8'):
            self.__currentScaleL = 60
            self.__currentScaleR = self.__currentScaleL + 12
            self.__left_scale = self.__PIANO_NOTES_TEMPLATE[:]
            self.__right_scale = self.__PIANO_NOTES_TEMPLATE[:]
        elif keyboard.is_pressed('1') and self.__left_shift == 0:
            self.__left_shift = -1
            self.__right_shift = -1
        elif keyboard.is_pressed('2') and self.__left_shift == 0:
            self.__left_shift = 1
            self.__right_shift = 1
        else:
            self.__left_shift = 0
            self.__right_shift = 0

        self.update_LR_scale()

        """ Temperarily removed
        elif keyboard.is_pressed('9') and self.__left_shift == 0:
            self.__left_shift = -3
            self.__right_shift = -3
        elif keyboard.is_pressed('0') and self.__left_shift == 0:
            self.__left_shift = 3
            self.__right_shift = 3
        """


    def update_scale_input(self):
        if keyboard.is_pressed(' '):
            self.__connect_w = not (self.__connect_w)

        if self.__connect_w == False:
            self.update_scale_input_NC()
        else:
            self.update_scale_input_C()


    def get_current_scale(self):
        return [self.__currentScaleL, self.__currentScaleR]

    def update_note_inputL(self):
        self.__active_list.clear()
        active_list = []
        if keyboard.is_pressed('q'):
            active_list.append(0)
        if keyboard.is_pressed('w'):
            active_list.append(1)
        if keyboard.is_pressed('e'):
            active_list.append(2)
        if keyboard.is_pressed('r'):
            active_list.append(3)
        if keyboard.is_pressed('t'):
            active_list.append(4)
        if keyboard.is_pressed('a'):
            active_list.append(5)
        if keyboard.is_pressed('s'):
            active_list.append(6)
        if keyboard.is_pressed('d'):
            active_list.append(7)
        if keyboard.is_pressed('f'):
            active_list.append(8)
        if keyboard.is_pressed('g'):
            active_list.append(9)
        if keyboard.is_pressed('z'):
            active_list.append(10)
        if keyboard.is_pressed('x'):
            active_list.append(11)

        # delete notes from holding
        strS = ''
        remove_list = []
        for h in range(0, len(self.__hold_list)):
            dele = True
            for x in range(0, len(active_list)):
                strS = self.__left_scale[active_list[x]]+str(self.__SST[self.__currentScaleL+active_list[x]])
                if strS == self.__hold_list[h].to_str():
                    dele = False
                    break

            if dele == True:
                 remove_list.append(self.__hold_list[h])

        for x in range(0, len(remove_list)):
            self.__hold_list.remove(remove_list[x])

        # add new notes to active list and ignore old notes
        add_list = []
        for x in range(0, len(active_list)):
            strS = self.__left_scale[active_list[x]]+str(self.__SST[self.__currentScaleL+active_list[x]])
            add = True
            for h in range(0, len(self.__hold_list)):
                if self.__hold_list[h].to_str() == strS:
                    add = False
                    break

            if add == True:
                add_list.append(x)

        for x in range(0, len(add_list)):
            self.__active_list.append(PianoNote(str(self.__left_scale[active_list[x]]+str(self.__SST[self.__currentScaleL+active_list[x]]))))
            self.__hold_list.append(PianoNote(str(self.__left_scale[active_list[x]]+str(self.__SST[self.__currentScaleL+active_list[x]]))))


    def update_note_inputR(self):
        active_list = []
        if keyboard.is_pressed('y'):
            active_list.append(0)
        if keyboard.is_pressed('u'):
            active_list.append(1)
        if keyboard.is_pressed('i'):
            active_list.append(2)
        if keyboard.is_pressed('o'):
            active_list.append(3)
        if keyboard.is_pressed('p'):
            active_list.append(4)
        if keyboard.is_pressed('h'):
            active_list.append(5)
        if keyboard.is_pressed('j'):
            active_list.append(6)
        if keyboard.is_pressed('k'):
            active_list.append(7)
        if keyboard.is_pressed('l'):
            active_list.append(8)
        if keyboard.is_pressed(';'):
            active_list.append(9)
        if keyboard.is_pressed('b'):
            active_list.append(10)
        if keyboard.is_pressed('n'):
            active_list.append(11)

        # delete notes from holding
        strS = ''
        remove_list = []
        for h in range(0, len(self.__hold_listR)):
            dele = True
            for x in range(0, len(active_list)):
                strS = self.__right_scale[active_list[x]]+str(self.__SST[self.__currentScaleR+active_list[x]])
                if strS == self.__hold_listR[h].to_str():
                    dele = False
                    break

            if dele == True:
                 remove_list.append(self.__hold_listR[h])

        for x in range(0, len(remove_list)):
            self.__hold_listR.remove(remove_list[x])

        # add new notes to active list and ignore old notes
        add_list = []
        for x in range(0, len(active_list)):
            strS = self.__right_scale[active_list[x]]+str(self.__SST[self.__currentScaleR+active_list[x]])
            add = True
            for h in range(0, len(self.__hold_listR)):
                if self.__hold_listR[h].to_str() == strS:
                    add = False
                    break

            if add == True:
                add_list.append(x)

        for x in range(0, len(add_list)):
            self.__active_list.append(PianoNote(str(self.__right_scale[active_list[x]]+str(self.__SST[self.__currentScaleR+active_list[x]]))))
            self.__hold_listR.append(PianoNote(str(self.__right_scale[active_list[x]]+str(self.__SST[self.__currentScaleR+active_list[x]]))))


    def get_active_list(self):
        return self.__active_list

    def in_connect_mode(self):
        return self.__connect_w

    def get_hold_list(self):
        list = self.__hold_list[:]
        list.extend(self.__hold_listR[:])
        return list

    def print_active_list(self):
        ans = ''
        for x in range(0, len(self.__active_list)):
            ans = ans + self.__active_list[x].to_str() + " "

        print(ans)
