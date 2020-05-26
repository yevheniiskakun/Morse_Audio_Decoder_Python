# Morse decoder from .wav file
# The best match will be with 1000Hz Audio Frequency and Morse Code Speed (words / minute): 5-7
# Please use this site to check this program
# http://www.meridianoutpost.com/resources/etools/calculators/calculator-morse-code.php?

# WORKS ONLY WITH ENGLISH WORDS

# Morse translator taken from
# https://www.geeksforgeeks.org/morse-code-translator-python/

import matplotlib.pyplot as plt
import numpy as np
import wave
import math
from scipy.io import wavfile
from tkinter import *
import os

morse_code = ["*-", "-***", "-*-*", "-**", "*", "**-*", "--*", "****", "**", "*---", "-*-", "*-**", "--", "-*", "---", "*--*", "--*-", "*-*", "***", "-", "**-", "***-", "*--", "-**-", "-*--", "--**", "*----", "**---", "***--", "****-", "*****", "-****", "--***", "---**", "----*", "-----", "|"]
alphabetEN = ['a',    'b',    'c',   'd',  'e',   'f',   'g',    'h',   'i',   'j',   'k',    'l',   'm',  'n',  'o',    'p',    'q',   'r',   's',  't',  'u',   'v',    'w',    'x',    'y',    'z',    '1',     '2',     '3',     '4',      '5',     '6',     '7',    '8',     '9',     '0',   ' ']
alphabetEN_length = len(alphabetEN) - 1

window = Tk()
window.title("Morse decoder")
window.geometry('500x115+400+150') # Aplication window size

lable_place_of_application = Label(window, text="Enter the .wav file path")
lable_place_of_application.pack(fill=BOTH)

user_path = Entry(window, bd = 5)
user_path.pack(fill=BOTH, padx=8)

label_info = Label(window, text="", fg="black")
label_word = Label(window, text="", fg="black")


def demorse():
    global dot_or_dash
    dot_or_dash = []
    global spaces
    spaces = []
    global spaces_length
    spaces_length = []
    global letter_spacing

    waveform = np.array([])

    file = user_path.get()

    if file != "":

            try:
                with wave.open(file,'r') as wav_file:

                    num_channels = wav_file.getnchannels()
                    frame_rate = wav_file.getframerate()
                    downsample = math.ceil(frame_rate * num_channels / 1000) # Get 1000 samples per second!

                    process_chunk_size = 600000 - (600000 % frame_rate)
                    #
                    signal = None


                    while signal is None or signal.size > 0:
                        signal = np.frombuffer(wav_file.readframes(process_chunk_size), dtype='int16')

                        # Take mean of absolute values per 0.001 seconds
                        sub_waveform = np.nanmean(
                            np.pad(np.absolute(signal), (0, ((downsample - (signal.size % downsample)) % downsample)), mode='constant', constant_values=np.NaN).reshape(-1, downsample),
                            axis=1
                        )

                        waveform = np.concatenate((waveform, sub_waveform))
                    #===========================
                    #
                    for i in waveform:  # Use wave form to find the spacing between letters
                        if i <= 15000:
                            spaces_length.append(len(spaces))
                            spaces = []
                        else:
                            spaces.append("No")

                    #letter_spacing = max(spaces_length)
                    letter_spacing = int((max(spaces_length) + sum(spaces_length)/len(spaces_length))/3) # handmade expression to detect the spaces between letters
                    #print(letter_spacing)
                    #=========================================
                    # Firstly, we find the spacing interval and the we will add spaces to decoded word
                    #----------------------------------------------- Main decoding part
                    encoded_list = []
                    for i in waveform:  # Use wave form to find the peaks of code
                        if i <= 15000:
                            dot_or_dash.append("Yes")
                            if len(spaces) >= letter_spacing:
                                encoded_list.append("|")
                            else:
                                pass
                            spaces = []
                        else:
                            spaces.append("No")
                            if 2 < len(dot_or_dash) <= 10:
                                encoded_list.append("*")
                            elif len(dot_or_dash) > 10:
                                encoded_list.append("-")
                            else:
                                pass
                            dot_or_dash = []

                    encoded_list.append("|")            # add | for symmetry
                    encoded_word = ''.join(encoded_list)

                    #print(encoded_word)
                    label_info.configure(text=encoded_word, fg="green")
                    #-----------------------------------------------

                    #~~~~~~~~~~~~~~~~~~~~~~~ Decoding
                    encrypted = []
                    encoded_list = encoded_word.split("|")
                    #print(encoded_list)
                    encoded_list_length = len(encoded_list)
                    ''' Here we have SOS priority'''
                    if (encoded_word == "***---***"):
                        print("sos")
                    else:
                        for j in range(encoded_list_length):
                           if encoded_list[j] in morse_code:
                               try:
                                  ''' Checking every letter in our word and changing it with normal letters '''
                                  encrypted.append(alphabetEN[morse_code.index(encoded_list[j])])
                               except:
                                   pass
                           else:
                               pass
                        ''' Joining the letters of English alphabet into word or sentence '''
                        encrypted = ''.join(encrypted)

                        label_word.configure(text=encrypted, fg="green")
                    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~

                    #Plot
                    plt.cla()
                    plt.figure(1)
                    plt.title('Waveform')
                    plt.plot(waveform)
                    plt.show()


            except:
                label_info.configure(text="Please check path name", fg="red")
    else:
        label_info.configure(text="Path name can not be empty", fg="red")


# declare Button and initialize the lable
button_demorse = Button(window, text="Start", command=demorse)
button_demorse.pack()

# Lable for dispalying the info about errors and result
label_info.pack(fill=BOTH)
# Lable for displaying decoded word
label_word.pack(fill=BOTH)

window.mainloop()

