//
// begin license header
//
// This file is part of Pixy CMUcam5 or "Pixy" for short
//
// All Pixy source code is provided under the terms of the
// GNU General Public License v2 (http://www.gnu.org/licenses/gpl-2.0.html).
// Those wishing to use Pixy source code, software and/or
// technologies under different licensing terms should contact us at
// cmucam@cs.cmu.edu. Such licensing terms are available for
// all portions of the Pixy codebase presented here.
//
// end license header
//
// This sketch is like hello_world but uses UART communications.  If you're
// not sure what UART is, run the hello_world sketch!
//
// Note, the default baudrate for Pixy's UART communications is 19200.  Given 
// the slow datarate and Arduino's shallow serial FIFO, this sletch sometimes
// gets checksum errors, when more than 1 block is present.  This is because
// printing more than 1 object block to the serial console (as this sketch does) 
// causes the Arduino's serial FIFO to overrun, which leads to communication 
// errors.  
//

#include "PixyUART.h"
#include "Pin Numbers.h"

PixyUART pixy;

void setup()
{
  Serial.begin(9600); // 9600 baud for the serial *console* (not for the UART connected to Pixy)
  Serial.print("Starting...\n");

  pinMode(BACK_MOTOR_PWM_PIN, OUTPUT); // sets the pin as output
  pinMode(LEFT_MOTOR_PWM_PIN, OUTPUT); // sets the pin as output
  pinMode(RIGHT_MOTOR_PWM_PIN, OUTPUT); // sets the pin as output
  pinMode(BACK_MOTOR_DIRECTION_PIN, OUTPUT); // sets the pin as output
  pinMode(LEFT_MOTOR_DIRECTION_PIN, OUTPUT); // sets the pin as output
  pinMode(RIGHT_MOTOR_DIRECTION_PIN, OUTPUT); // sets the pin as output
  delay(3000);
  
  pixy.init();
  digitalWrite(LEFT_MOTOR_DIRECTION_PIN, HIGH);
  digitalWrite(BACK_MOTOR_DIRECTION_PIN, HIGH);
  digitalWrite(RIGHT_MOTOR_DIRECTION_PIN, HIGH);
  analogWrite(LEFT_MOTOR_PWM_PIN, 55);
  analogWrite(BACK_MOTOR_PWM_PIN, 55);
  analogWrite(RIGHT_MOTOR_PWM_PIN, 55);
}

void loop()
{
  static int i = 0;
  int j;
  uint16_t blocks;
  char buf[32]; 
  
  blocks = pixy.getBlocks();
  
  if (blocks)
  {
    i++;
    
   // do this (print) every 5 frames because printing every
   // frame would bog down the Arduino
   if (i%5==0)
    {
      sprintf(buf, "Detected %d:\n", blocks);
      Serial.print(buf);
      for (j=0; j<blocks; j++)
      {
        sprintf(buf, "  block %d: ", j);
        Serial.print(buf); 
        pixy.blocks[j].print_and_do_something();
      }
    }
  }  
}
