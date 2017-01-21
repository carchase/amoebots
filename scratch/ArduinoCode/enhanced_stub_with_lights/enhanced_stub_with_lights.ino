//Modular robot project @IPFW
//Carter Chase, CS

//Connections:
//Pin 3 -> Light 1
//Pin 3 -> Light 2
//Pin 3 -> Light 3
//Pin 3 -> Light 4

//Pin configure

void setup(){
  // put your setup code here, to run once:
  pinMode(3,OUTPUT);
  pinMode(4,OUTPUT);
  pinMode(5,OUTPUT);
  pinMode(6,OUTPUT);
  pinMode(7,OUTPUT);
  Serial.begin(115200);
  Serial.println("Robot is Online");
}

void loop(){
  while(Serial.available() > 0){
    int f = Serial.parseInt();//1,2,3,4,5,6-forward backward left right
    int v = Serial.parseInt();//- stop standby, v range from 130-255
    int d = Serial.parseInt();//the amount of delay prior to stoping the motors
                              //may be used for encoder position in the future
    Serial.println(action(f, v, d));
  }
}

/*
 * act signifies which action the robot will take
 * speed indicates how fast the motor will move
 * del indicates the delay prior to the command being terminated
 * which may be used to indicate encoder position in the future
 */
String action(int act, int speed, int del){
  String message = "";
  int whichStop = 0;

  switch(act){
    case 1:
      move(1,speed,1);
      move(0,speed,0);
      message += "Moving Forward for " + String(del);
      break;
    case 2:
      move(1,speed,0);
      move(0,speed,1);
      message += "Moving Backward for " + String(del); 
      break;
    case 3:
      move(1,speed,0);
      move(0,speed,0);
      message += "Turning Left for " + String(del);
      break;
    case 4:
      move(1,speed,1);
      move(0,speed,1);
      message += "Turning Right for " + String(del);
      break;
    case 5:
      move(2,speed,1);
      move(3,speed,1);
      message += "Moving the arm in direction 1 for " + String(del);
      whichStop = 1;
      break;
    case 6:
      move(2,speed,0);
      move(3,speed,0);
      message += "Moving the arm in direction 2 for " + String(del);
      whichStop = 1;
      break;
    case 7:
      message += "Move key out";
      whichStop = 2;
      break;
    case 8:
      message += "Move key in";
      whichStop = 2;
      break;
    case 99:
      message += "Robot is Online";
      break;
  }

  //delay is used to allow the motor to move for a predetermined
  //amount of time before it's turned off
  delay(del);

  //indicates which stop function is called
  Stop(whichStop);

  return message;
}

void Stop(int which){
//This stops the motor by setting both IN pins to LOW
  if (which == 0){
    //stops the robot movement
    digitalWrite(3,LOW);
    digitalWrite(4,LOW);
  } else if (which == 1){
    //stops the arm
    digitalWrite(5,LOW);
    digitalWrite(6,LOW);
  } else {
    //stops the key
  }
}

void standby(){
//enable standby
  Serial.println("function standby activiated");
}

void move(int motor, int speed, int direction){
//Move specific motor at speed and direction
//motor: 0 for B 1 for A 2 for C 3 for D
//speed: 0 is off, and 255 is full speed
//direction: 0 clockwise, 1 counter-clockwise

  boolean inPin1 = LOW;
  boolean inPin2 = HIGH;

  if(direction == 1){
    inPin1 = HIGH;
    inPin2 = LOW;
  }
  
  digitalWrite(motor + 3,inPin1);
}
