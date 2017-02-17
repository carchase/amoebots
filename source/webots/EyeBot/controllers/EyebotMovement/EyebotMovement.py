# File:          EyebotMovement.py
# Date:          12/17/2016
# Description:   
# Author:        Jeffery Ross
# Modifications: 

from controller import Robot
import time
import math

left_motor = None
right_motor = None
back_motor = None
front_conn = None
back_conn = None
left_conn = None
right_conn = None
left_sonar = None
right_sonar = None
front_cam = None
gps = None
compass = None

class EyebotMovement (Robot):

  def run(self):
    global left_motor
    global right_motor
    global back_motor
    global front_conn
    global left_conn
    global right_conn
    global back_conn
    global left_sonar
    global right_sonar
    global front_cam
    global gps
    global compass

    left_motor = self.getMotor("left wheel motor")
    right_motor = self.getMotor("right wheel motor")
    back_motor = self.getMotor("back wheel motor")

    front_conn = self.getConnector("front connector")
    front_conn.enablePresence(64)
    left_conn = self.getConnector("left connector")
    left_conn.enablePresence(64)
    right_conn = self.getConnector("right connector")
    right_conn.enablePresence(64)
    back_conn = self.getConnector("back connector")
    back_conn.enablePresence(64)

    left_sonar = self.getDistanceSensor("left distance sensor")
    left_sonar.enable(64)
    right_sonar = self.getDistanceSensor("right distance sensor")
    right_sonar.enable(64)

    front_cam = self.getCamera("camera")
    front_cam.enable(64)

    gps = self.getGPS("gps")
    gps.enable(64)
    compass = self.getCompass("compass")
    compass.enable(64)

    while True:
      if self.step(64) == -1:
        break

      cmd = 1
      vel = 1
      delay = 1000

      print action(self, cmd, vel, delay)
      print action(self, 97, vel, delay)
      print action(self, 98, vel, delay)

def action(self, cmd, vel, delay):
  global left_motor
  global right_motor
  global back_motor
  global front_conn
  global left_conn
  global right_conn
  global back_conn
  global left_sonar
  global right_sonar
  global front_cam
  global gps
  global compass

  whichStop = 0

  if cmd == 1:
    move(self, left_motor, vel, 1)
    move(self, right_motor, vel, 1)
    message = jsonResponse('text', 'Moving forward for ' + str(delay))
  elif cmd == 2:
    move(self, left_motor, vel, -1)
    move(self, right_motor, vel, -1)
    message = jsonResponse('text', 'Moving backward for ' + str(delay))
  elif cmd == 3:
    move(self, back_motor, vel, 1)
    message = jsonResponse('text', 'Turning left for ' + str(delay))
  elif cmd == 4:
    move(self, back_motor, vel, -1)
    message = jsonResponse('text', 'Turning right for ' + str(delay))
  elif cmd == 97:
    message = jsonResponse('text', 'Robot position: ' + str(getPosition(gps)))
  elif cmd == 98:
    message = jsonResponse('text', 'Robot orientation: ' + str(getBearing(compass)))
  elif cmd == 99:
    message = jsonResponse('json', '{\"type\":\"smore\"}')

  # delay is used to allow the motor to move for a predetermined
  # amount of time before it's turned off
  self.step(delay)

  # indicates which stop function is called
  if whichStop == 0:
    right_motor.setVelocity(0)
    left_motor.setVelocity(0)
  elif whichStop == 1:
    top_motor.setVelocity(0)

  return message

def move(self, motor, speed, direction):
  # move motor specific speed and direction
  # speed: 0 is off, 255 is full speed
  # direction: 1 clockwise, -1 counter-clockwise
  motor.setPosition(float('inf'))
  motor.setVelocity(direction * speed)

# returns the position of the given gps in a 3d vector <x, y, z>
def getPosition(gps):
  return gps.getValues()

# returns the bearing of the given compass in degrees
def getBearing(compass):
  north = compass.getValues()
  rad = math.atan2(north[0], north[1])
  bearing = (rad - 1.5708) / math.pi * 180.0
  if bearing < 0.0:
    bearing += 360.0
  return bearing

def jsonResponse(content, data):
  message = "{\"content\":\"" + content + "\",\"data\":\"" + data + "\"}"
  return message

# The main program starts from here

controller = EyebotMovement()
controller.run()