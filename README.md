# AmbientAgenda

## Description
AmbientAgenda is an innovative device which uses Sony projection technology to harmoniously integrate a shared calendar into any home environment. Using cutting-edge machine learning technologies to maximise useability and lower the skill floor,  AmbientAgenda aims to bring all members of the family together, regardless of their technical dexterity - if they can write, they can use AmbientAgenda. What sets AmbientAgenda apart from conventional shared calendars is its ambient nature. Through novel use of sight and sound, our system projects upcoming events for all family members onto a household surface, all while preserving the ambiance of the family's living space. 

## Operation
The programme is run through the main file `observer.py`. Once running observer should automatically launch `displayer.py`, This will bring up the display which should be shown through a projector. Once set users can write on top of the projection and use the asoociated buttons on their raspberry pis to take pictures and automatically send to the cloud which in turn sends it to all of the pis on their family network. The device will also play relevant chimes if there is an event in the coming hour and should ambiently switch off when the room gets dark. The displayed calendar is also automatically updated if a users' family member pushes an event or if they enter an event into their conneted google calendar. 

## Installation Instructions
To install this project you will require these hardware devices
- Raspberry Pi running 64 bit
- USB Webcam
- USB Speaker
- Breadoboard with two buttons
- LIDAR sensor

After this clone the repository
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

## Website
We had an associated website that allows users to login and register their Pis. The code for the website can be found [here](https://github.com/rkoll55/Ambiance)

## Dependencies
Please refer to requirements.txt for a list of all the software dependencies we used for this project

## Software We Reused
For the associated website we reused code used from an INFS3202 project. Link to the repository has been provided above.

## Sounds
Sourced from [here](https://www.zapsplat.com/basic-member-home/).

### The DECO3801 project by  
-*Rohan Kollambalath*  
-*Aiden Richards*   
-*Gil Wise*   
-*Matilda Damman*  
-*Jess Froio*  
-*Toby Turner*
