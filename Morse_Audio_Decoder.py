# Morse decoder from .wav file
# The best match will be with 1000Hz Audio Frequency and Morse Code Speed (words / minute): 5-7
# Please use this site to check this program
# http://www.meridianoutpost.com/resources/etools/calculators/calculator-morse-code.php?


import matplotlib.pyplot as plt
import numpy as np
import wave
import math
from scipy.io import wavfile
from tkinter import *
import os

window = Tk()
window.title("Morse decoder")
window.geometry('500x110+400+150') # Aplication window size

lable_place_of_application = Label(window, text="Enter the .wav file path")
lable_place_of_application.pack(fill=BOTH)

user_path = Entry(window, bd = 5)
user_path.pack(fill=BOTH, padx=8)

label_info = Label(window, text="", fg="black")


def demorse():
    global dot_or_dash
    dot_or_dash = []

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
                    waveform = np.array([])

                    while signal is None or signal.size > 0:
                        signal = np.frombuffer(wav_file.readframes(process_chunk_size), dtype='int16')

                        # Take mean of absolute values per 0.001 seconds
                        sub_waveform = np.nanmean(
                            np.pad(np.absolute(signal), (0, ((downsample - (signal.size % downsample)) % downsample)), mode='constant', constant_values=np.NaN).reshape(-1, downsample),
                            axis=1
                        )

                        waveform = np.concatenate((waveform, sub_waveform))
                        
                    #----------------------------------------------- Main decoding part
                    encoded_list = []
                    for i in waveform:  # Use wave form to find the peaks of code
                        if i <= 15000:
                            dot_or_dash.append("Yes")
                        else:
                            if 2 < len(dot_or_dash) <= 10:
                                encoded_list.append("*")
                            elif len(dot_or_dash) > 10:
                                encoded_list.append("-")
                            else:
                                pass
                            dot_or_dash = []
                    encoded_word = ''.join(encoded_list)
                    #print(encoded_word)
                    label_info.configure(text=encoded_word, fg="green")
                    #-----------------------------------------------
                    #Plot
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

window.mainloop()

