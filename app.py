################################################################
#                                                              
# RAMPLE-KITMAN: A web app designed to generate 'kits' for the 
#                Squarp Rample Eurorack module.                
#
# app.py: Contains code for the interactive app 
#        
#
# Copyright (C) 2022 George N
################################################################

# Build an app using StreamLit to load sound files into a kit
# The kit is user-defined from drop-down menus for 'Letter' and 'Number'
# The app shows four `slots' which the user can then add sound files to
# The user can then select a file location to save the kit to.

# Import packages
from utilities import *
import streamlit as st
import tkinter as tk
from tkinter import filedialog


st.set_page_config(page_icon="📥",page_title="rample-kitman")

def main():
    st.title("rample-kitman")
    st.markdown("A web app designed to generate 'kits' for the Squarp Rample Eurorack module.")
    st.markdown("Copyright (C) 2022 George N")
    
    lcol,ncol = st.columns(2)
    with lcol:
        letter_bank = st.selectbox(
            "Select Letter Bank",
            ("A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z")
        )
    with ncol:
        number_bank = st.number_input(
            "Select Number",
            min_value=0, max_value=99, value=0, step=1, format="%i"
        )
    # Create a kit
    kit = Kit(letter_bank,number_bank)

    st.markdown ("Upload to Kit {}...".format(kit.name))


    f1 = st.file_uploader("Slot 1:",type=VALID_FORMATS,accept_multiple_files=True)
    if f1 is not None:
        kit.AddSample(1,f1)
        st.success("Files loaded in Slot 1: {}".format(" ".join(kit.slot[0].samples)))
    # else:
    #     st.error("No sample loaded")

    f2 = st.file_uploader("Slot 2:",type=VALID_FORMATS,accept_multiple_files=True)
    if f2 is not None:
        kit.AddSample(2,f2)
        st.success("Files loaded in Slot 2: {}".format(" ".join(kit.slot[1].samples)))
    # else:
    #     st.error("No sample loaded")

    f3 = st.file_uploader("Slot 3:",type=VALID_FORMATS,accept_multiple_files=True)
    if f3 is not None:
        kit.AddSample(3,f3)
        st.success("Files loaded in Slot 3: {}".format(" ".join(kit.slot[2].samples)))
    # else:
    #     st.error("No sample loaded")

    f4 = st.file_uploader("Slot 4:",type=VALID_FORMATS,accept_multiple_files=True)
    if f4 is not None:
        kit.AddSample(4,f4)
        st.success("Files loaded in Slot 4: {}".format(" ".join(kit.slot[3].samples)))
    # else:
    #     st.error("No sample loaded")


    root = tk.Tk()
    root.withdraw()

    # # Make folder picker dialog appear on top of other windows
    root.wm_attributes('-topmost', 1)
    st.write('Please select the location of your Squarp Rample-formatted SD card:')
    clicked = st.button('Select SD card location')
    if clicked:
        dirname = st.text_input('Selected folder:', filedialog.askdirectory(master=root))

    # Save the kit
    st.markdown ("Save Kit {}...".format(kit.name))
    savekit = st.button("Save Kit")
    if savekit is not None:
        SaveKit(kit,dirname)
        st.success("Kit saved")
    elif dirname is None:
        st.error("No location specified")
    
    # Clear the kit
    st.markdown ("Clear Kit {}...".format(kit.name))
    if st.button("Clear Kit"):
        kit.ClearKit()
        st.success("Kit cleared")




main()

