# AmbientAgenda

## Description
AmbientAgenda is an innovative device which uses Sony projection technology to harmoniously integrate a shared calendar into any home environment. Using cutting-edge machine learning technologies to maximise useability and lower the skill floor,  AmbientAgenda aims to bring all members of the family together, regardless of their technical dexterity - if they can write, they can use AmbientAgenda. What sets AmbientAgenda apart from conventional shared calendars is its ambient nature. Through novel use of sight and sound, our system projects upcoming events for all family members onto a household surface, all while preserving the ambiance of the family's living space. 

## Operation
Upon setup of a Raspberry Pi with the listed devices, the program can be run via the terminal. Begin by running the main file `observer.py` using `python3`. Once running observer should automatically launch `displayer.py`, This will bring up the display which should be shown through a projector. Once set-up, users can write on top of the projection and use the connected buttons, configured to the coded pin values, to take pictures which will automatically be run through the recognition file `recog.py`, with the text then automatically sent to the cloud. This upload is then pull by all other devices connected to this 'family' network. The device will also play relevant chimes on startup/un-dim, and if there is an event in the coming hour. The display will ambiently switch off when the room gets dark when correctly connected to the Light sensor. The displayed calendar is also automatically updated if a users' family member pushes an event or if they enter an event into their conneted google calendar. 

## Installation Instructions
### To install this project you will require these hardware devices
- Raspberry Pi running 64 bit
- USB Webcam
- USB Speaker
- Breadoboard with two buttons
- Light sensor

### Then run the following on the Raspberry Pi
Clone the repository using:
```bash
git clone https://github.com/rkoll55/Byte-Me
```

And then perform
```bash
pip install -r requirements.txt
```
This build also requires ESRGAN2 for machine learning follow [these](https://huggingface.co/ai-forever/Real-ESRGAN/resolve/0a00b8e4dc6dd1e1fe0ebb453d4ffeb3f52f89a4/README.md) installation instructions to complete.


Once all steps above have been complete run
```bash
./observer.py
```
to launch the application.
If any dependencies have been missed in the initial installation, run the extras as required by the `observer.py` file.

## Website
We have an associated website that allows users to login and register their Pis. The code repository for the website can be found [here](https://github.com/rkoll55/Ambiance)

## Dependencies
Please refer to requirements.txt for a list of all the software dependencies we used for this project

## Software We Reused
For the associated website we reused code used from an INFS3202 project. Link to the repository has been provided above.

## Sounds
Sourced from ZapSplat [here](https://www.zapsplat.com/basic-member-home/).

### The DECO3801 project by  
-*Rohan Kollambalath*  
-*Aiden Richards*   
-*Gil Wise*   
-*Matilda Damman*  
-*Jess Froio*  
-*Toby Turner*
