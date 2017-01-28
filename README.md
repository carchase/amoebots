# AmoeBots
Senior Capstone Project August 2016 to May 2017

## Team
Mastermind:        Carter Chase

Augmentor:         Ben Smith

Better Augmentor:  Jeff Ross

Roboteer:          Trevor Seitz 

Bossman:           Dr. John Licato

## Background
A senior project group in Electrical + Computer Engineering (ECE) has been creating a robot array consisting 
of several modular units that can reconfigure themselves into a wide variety of possible arrangements.  
Ideally, the robots would be able to form (for example): a bridge, stairs, a wall, etc.  Additionally, the 
engineers have produced a robotic arm capable of lifting and moving the robots.  All robots will communicate 
with each other using a well-known protocol such as WIFI or Bluetooth.

The artificial intelligence still needs to be programmed.  Choosing a possible shape to transform into is 
relatively easy, but actually designing a step-by-step plan so that the robot modules can move into place 
without any human assistance, is a more difficult AI problem.  Every robot will communicate with a central 
server that handles the transformation algorithms.  This server will receive all sensor data, compute 
actions, and send instructions to the modular bots.  The team will be responsible for creating both the high 
level algorithms and the API for robot-server communication.

Unfortunately, the CS senior design team will not have access to the final robots until midway through the 
project.  To aid in development in the meantime, they will have access to the Webots 3D simulator.  The 
team will first develop transformations for the simulation platform and then, once the robots are complete, 
they will implement the algorithms on the actual modular bots.  The team will need to design the central 
server’s API to be versatile enough to communicate with both the virtual robots and the real robots.

In addition to working with Dr. Licato, the CS senior design team will work with the ECE senior design 
groups in a first-ever collaboration between departments here at IPFW.  Progress made in this project will 
be used as a launching point for at least one external funding proposal to be written by Dr. Licato, in 
collaboration with other ETCS Faculty (Drs. PomalzaARaez (ECE), Liu (ECE), and Bi (ME)).  The robotics 
projects and code completed by the CS and ECE senior project teams will be used in future robotics courses 
here at IPFW.

## Installation
1. Download and install [python 3](https://www.python.org/downloads/). You can verify it is installed by running the following command:
 
 >$ py --version // Should be 3.6.0 or greater
2. Install pyserial in order to communicate with the robots:
 
 >$ py -m pip install pyserial
3. Clone the project repository to your local drive by running the following command:

 >$ git clone https://github.com/car-chase/amoebots.git
4. Start the AI by running the following command from the project root:

 >$ py ./source/ai_controller/main.py