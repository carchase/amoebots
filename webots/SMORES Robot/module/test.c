/*
 * File:         void.c
 * Description:  This is an empty robot controller, the robot does nothing. 
 * Author:       www.cyberbotics.com
 * Note:         !!! PLEASE DO NOT MODIFY THIS SOURCE FILE !!!
 *               This is a system file that Webots needs to work correctly.
 */

#include <webots/robot.h>
#include <webots/motor.h>

int main() {
  wb_robot_init();
  int time_step = wb_robot_get_basic_time_step();
  if (time_step == 0)
    time_step = 1;
  for (;;) wb_robot_step(time_step);
  return 0;
  
  // initialize motors
  WbDeviceTag wheels[4];
  char wheels_names[4][8] = {
    "wheel1", "wheel2", "wheel3", "wheel4"
  };
  for (i=0; i<4 ; i++)
    wheels[i] = wb_robot_get_device(wheels_names[i]);
    
  double speed = -1.5; // [rad/s]
  wb_motor_set_position(wheels[0], INFINITY);
  wb_motor_set_velocity(wheels[0], speed);
}

