################################################################
#                                                              
# RAMPLE-KITMAN: A web app designed to generate 'kits' for the 
#                Squarp Rample Eurorack module.                
#
# utilities.py: Contains functions for saving and loading
#               sample files.
#
# Copyright (C) 2022 George N
################################################################

# Imports
import os
import numpy as np
import librosa
# import pydub as pd
import soundfile

# Define valid soundfile formats
VALID_FORMATS = ["wav","aiff","flac","ogg","mp3"]

# Define sample rate for Squarp Rample
SAMPLE_RATE = 44100


# Define a sample class to store music data
# Class should be initialised by taking a filename of music data
# with any format supported by librosa.load.
# Constructor should convert the file to mono and resample to
# a sample rate of 44100 Hz and a bit depth of 16 bits.
class Sample:
    def __init__(self,filename):

        # Store the filename
        self.filename = filename

        # Load the file to self.data using librosa.load
        self.data, self.sr = librosa.load(filename, mono=True, sr=SAMPLE_RATE)

        # Convert to 16-bit
        self.data = self.data.astype(np.int16)
        # Store the bit depth
        self.bit_depth = 16
        # Store the length of the sample
        self.length = self.data.shape[0]



# Define a slot class to store the information for a single slot
# A slot is a list containing Sample objects or "None" if the slot
# is empty. The slot is initialised with a number indicating its place
# in the Kit, and should be able to store a Sample object and securely
# maintain the index of the Sample in the Slot.
class Slot:

    def __init__(self,number):
        self.number = number
        self.samples = []
        self.index = None

    def AddSample(self,filename):
        self.samples.append(Sample(filename))

    def RemoveSample(self,index):
        self.samples.pop(index)


# Define a Kit class consisting of 4 Slots
# The Kit class should be initialised with a name, consisting of a
# single upper-case letter A-Z, and a number from 0-99.
# The Kit class should be able to add samples to a specified slot,
# and remove the slots based on what is specified.
class Kit:

    def __init__(self,letter,number):
        self.letter = letter.upper()
        self.number = number
        self.name = letter + str(number)
        self.slots = [Slot(1),Slot(2),Slot(3),Slot(4)]

    def AddSample(self,slot,filename):
        self.slots[slot-1].AddSample(filename)

    def RemoveSample(self,slot,index):
        self.slots[slot-1].RemoveSample(index)

    def ClearKit(self):
        for slot in self.slots:
            slot.samples = []
            slot.index = None





# Define a function to save the kit to a given location
# Function takes the drive location and the specified kit
# as arguments, and creates a folder with the kit name,
# saving the kit layout with the naming convention:
# <slot number>_<original file name>.wav
# The file format must be .wav with a sample rate of 44100,
# and a bit depth of 16 bits.
def SaveKit(kit,location):
    # Create the folder
    try:
        os.mkdir(location + kit.name)
    except FileExistsError:
        print("Kit already exists")
        return False

    # Loop through the layout and save the samples using soundfile.write
    for slot in kit.slots:
        if slot.samples != []:
            for sample in slot.samples:
                soundfile.write(location + kit.name + "/" + str(slot.number) + "_" + str(slot.samples.index(sample)+1) + "_" + sample.filename.split("/")[-1], sample.data, sample.sample_rate, subtype="PCM_16")

    return True


# Define a function to print a kit's layout to console
# Function takes the kit as an argument, and prints the
# layout of the kit to the console.
def PrintKit(kit):
    print("Kit: " + kit.name)
    for slot in kit.slots:
        if slot.samples != []:
            for sample in slot.samples:
                print("Slot " + str(slot.number) + ": " + sample.filename)
        else:
            print("Slot " + str(slot.number) + ": Empty")
    print("")
    return True

# Function to check whether file can be loaded
def CheckSampleType(filename):
    if filename.split(".")[-1] in VALID_FORMATS:
        return True
    else:
        return False

