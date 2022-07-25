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
import os

st.set_page_config(page_icon="📥",page_title="rample-kitman")

def main():
    st.title("rample-kitman")
    st.markdown("A web app designed to generate 'kits' for the Squarp Rample Eurorack module.")

    # root = tk.Tk()
    # root.withdraw()
    # root.wm_attributes('-topmost', 1)
    st.write('Please select the location of your Squarp Rample-formatted SD card:')
    dirname = st.text_input('SD card location:')
    if os.path.exists(dirname):
        dir_exists = True
    else:
        dir_exists = False
        st.info('Please select a valid directory')

    if dir_exists:
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

        # Create a kit object with these created values
        kit = Kit(letter_bank,number_bank)
        st.markdown ("Upload to Kit {}...".format(kit.name))

        with st.form("Kit details", clear_on_submit=True):


            # Slot 1 file upload
            f1 = st.file_uploader("Slot 1:",type=VALID_FORMATS,accept_multiple_files=True)
            if f1 is not None:
                kit.AddSample(1,[Sample(f,type="BytesIO") for f in f1])
                st.success("Files loaded in Slot 1: {}".format(" ".join(kit.slots[0].names)))

            # Slot 2 file upload
            f2 = st.file_uploader("Slot 2:",type=VALID_FORMATS,accept_multiple_files=True)
            if f2 is not None:
                kit.AddSample(2,[Sample(f,type="BytesIO") for f in f2])
                st.success("Files loaded in Slot 2: {}".format(" ".join(kit.slots[1].names)))

            # Slot 3 file upload
            f3 = st.file_uploader("Slot 3:",type=VALID_FORMATS,accept_multiple_files=True)
            if f3 is not None:
                kit.AddSample(3,[Sample(f,type="BytesIO") for f in f3])
                st.success("Files loaded in Slot 3: {}".format(" ".join(kit.slots[2].names)))

            # Slot 4 file upload
            f4 = st.file_uploader("Slot 4:",type=VALID_FORMATS,accept_multiple_files=True)
            if f4 is not None:
                kit.AddSample(4,[Sample(f,type="BytesIO") for f in f4])
                st.success("Files loaded in Slot 4: {}".format(" ".join(kit.slots[3].names)))

            # # Save the kit
            # st.markdown ("Save Kit {}...".format(kit.name))
            # if st.button("Save Kit"):
            #     SaveKit(kit,dirname)
            #     st.success("Kit saved")

            # Save and clear the kit and reset the app
            st.markdown ("Save Kit and Reset {}...".format(kit.name))
            clear = st.form_submit_button("Finish Kit")
            if clear:
                SaveKit(kit,dirname)
                kit.ClearKit()
                st.success("Kit Finished.")
    st.markdown("Copyright (C) 2022 George N")



main()

