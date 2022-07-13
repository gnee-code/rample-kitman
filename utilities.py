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
import pydub as pd

# Define a kit class to store the data
class kit:

    layout = [[],[],[],[]]

    def __init__(self, letter, number):
        self.letter = letter.upper()
        self.number = number
        self.name = letter + str(number)


    def AddMonoSample(self, sample, slot):
        self.layout[slot].append(sample)

    def AddStereoSample(self, sample, slot):
        sample_left = sample[0]
        sample_right = sample[1]
        self.layout[slot].append(sample_left)
        self.layout[slot+1].append(sample_right)

    def RemoveSample(self, slot, index):
        self.layout[slot].pop(index)

    
     
