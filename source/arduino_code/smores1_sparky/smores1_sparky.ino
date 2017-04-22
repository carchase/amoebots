//Modular robot project @IPFW
//Zhitian Zhang, ECE
//motor A connected between A01 and A02
//motor B connected between B01 and B02
//motor C connected between C01 and C02
//motor D connected between D01 and D02

//Connections:
//Pin 2 -> PWMA
//Pin 3 -> AIN2
//Pin 4 -> AIN1
//Pin 5 -> STBY1,STBY2
//Pin 6 -> BIN2
//Pin 7 -> BIN1
//Pin 8 -> PWMB


//Pin configure

int STBY = 12; //standby

//Motor A Left motor
int PWMA = 3; //Speed control
//int AIN2 = 3; //Direction
int AIN1 = 2; //Direction

//Motor B right motor
int PWMB = 5; //Speed control
int BIN1 = 4; //Direction
//int BIN2 = 6; //Direction

//Motor C left arm
int CIN1 = 6;
int PWMC = 7;

//Motor D right arm
int DIN1 = 8;
int PWMD = 9;

//Magnitude constants
int speed = 75;
int cmPerSecond = 1;
int degPerSecond = 1;
int topDegPerSecond = 1;
int topSpinDegPerSecond = 1;


void setup() {
  pinMode(STBY, OUTPUT);

  pinMode(PWMA, OUTPUT);
  pinMode(AIN1, OUTPUT);
  //pinMode(AIN2, OUTPUT);

  pinMode(PWMB, OUTPUT);
  pinMode(BIN1, OUTPUT);
  //pinMode(BIN2, OUTPUT);

  pinMode(PWMC, OUTPUT);
  pinMode(CIN1, OUTPUT);

  pinMode(PWMD, OUTPUT);
  pinMode(DIN1, OUTPUT);

  Serial.begin(115200);
  Serial.println("Robot is Online");
}

//command list:(command, speed)
//1 2 - move forward or backward
//3 4 - turn left or right
//5 6 - move arm up or down
//7 8 - spin the arm cw or ccw
//9 10 - move key in or out
//99 - get robot type

void loop() {
  while (Serial.available() > 0) {
    int f = Serial.parseInt();//1,2,3,4,5,6-forward backward left right
    int m = Serial.parseInt();//- stop standby, v range from 130-255
    // int d = Serial.parseInt();//the amount of delay prior to stoping the motors
    //may be used for encoder position in the future
    Serial.println(action(f, m));
  }
}

/*
   act signifies which action the robot will take
   speed indicates how fast the motor will move
   del indicates the delay prior to the command being terminated
   which may be used to indicate encoder position in the future
*/
String action(int act, int magnitude) {
  String message = "";
  int whichStop = 0;

  switch (act) {
    case 1:
      move(1, speed, 1);
      move(0, speed, 0);
      message = jsonResponse("move-result", "{\"success\":true,\"message\":\"Moving forward " + String(magnitude) + " cm\"}");
      break;
    case 2:
      move(1, speed, 0);
      move(0, speed, 1);
      message += jsonResponse("move-result", "{\"success\":true,\"message\":\"Moving backward " + String(magnitude) + " cm\"}");
      break;
    case 3:
      move(1, speed, 0);
      move(0, speed, 0);
      message += jsonResponse("move-result", "{\"success\":true,\"message\":\"Turning left " + String(magnitude) + " degrees\"}");
      break;
    case 4:
      move(1, speed, 1);
      move(0, speed, 1);
      message += jsonResponse("move-result", "{\"success\":true,\"message\":\"Turning right " + String(magnitude) + " degrees\"}");
      break;
    case 5:
      move(2, speed, 1);
      move(3, speed, 0);
      message += jsonResponse("move-result", "{\"success\":true,\"message\":\"Moving the arm down " + String(magnitude) + " degrees\"}");
      whichStop = 1;
      break;
    case 6:
      move(2, speed, 0);
      move(3, speed, 1);
      message += jsonResponse("move-result", "{\"success\":true,\"message\":\"Moving the arm up " + String(magnitude) + " degrees\"}");
      whichStop = 1;
      break;
    case 7:
      move(2, speed, 1);
      move(3, speed, 1);
      message += jsonResponse("move-result", "{\"success\":true,\"message\":\"Spin the arm clockwise " + String(magnitude) + " degrees\"}");
      whichStop = 1;
      break;
    case 8:
      move(2, speed, 0);
      move(3, speed, 0);
      message += jsonResponse("move-result", "{\"success\":true,\"message\":\"Spin the arm in counterclockwise " + String(magnitude) + " degrees\"}");
      whichStop = 1;
      break;
    case 9:
      message += jsonResponse("move-result", "{\"success\":true,\"message\":\"Move key out\"}");
      whichStop = 2;
      break;
    case 10:
      message += jsonResponse("move-result", "{\"success\":true,\"message\":\"Move key in\"}");
      whichStop = 2;
      break;
    case 90:
      message += jsonResponse("robot-info", "{\"type\":\"smores\"}");
      break;
    case 99:
      message += jsonResponse("ping", "{}");
      break;
    default:
      message += jsonResponse("unsupported", "\"command not supported\"");
  }

  //delay is used to allow the motor to move for a predetermined
  //amount of time before it's turned off
  delay(getDelay(act, magnitude));

  //indicates which stop function is called
  Stop(whichStop);

  return message;
}

void Stop(int which) {
  //This stops the motor by setting both IN pins to LOW
  if (which == 0) {
    //stops the robot movement
    digitalWrite(AIN1, LOW);
    digitalWrite(BIN1, LOW);
    analogWrite(PWMA, 0);
    analogWrite(PWMB, 0);
  } else if (which == 1) {
    //stops the arm
    digitalWrite(CIN1, LOW);
    digitalWrite(DIN1, LOW);
    analogWrite(PWMC, 0);
    analogWrite(PWMD, 0);
  } else {
    //stops the key

  }
}

void standby() {
  //enable standby
  Serial.println("function standby activiated");
  digitalWrite(STBY, LOW);
}

void move(int motor, int speed, int direction) {
  //Move specific motor at speed and direction
  //motor: 0 for B 1 for A 2 for C 3 for D
  //speed: 0 is off, and 255 is full speed
  //direction: 0 clockwise, 1 counter-clockwise

  digitalWrite(STBY, HIGH); //disable standby

  boolean inPin1 = LOW;
  boolean inPin2 = HIGH;

  if (direction == 1) {
    inPin1 = HIGH;
    inPin2 = LOW;
  }

  switch (motor) {
    case 0:
      digitalWrite(BIN1, inPin1);
      analogWrite(PWMB, speed);
      break;
    case 1:
      digitalWrite(AIN1, inPin1);
      analogWrite(PWMA, speed);
      break;
    case 2:
      digitalWrite(CIN1, inPin1);
      analogWrite(PWMC, speed);
      break;
    case 3:
      digitalWrite(DIN1, inPin1);
      analogWrite(PWMD, speed);
      break;
  }
}

double getDelay(int cmd, int magnitude) {
  //Calculates the duration of the action based on what the command is
  //Different wheels move at different speeds
  if (cmd == 1 || cmd == 2) {
    return ((1.0 * magnitude) / cmPerSecond) * 1000;
  } else if (cmd == 3 || cmd == 4) {
    return ((1.0 * magnitude) / degPerSecond) * 1000;
  } else if (cmd == 5 || cmd == 6) {
    return ((1.0 * magnitude) / topDegPerSecond) * 1000;
  } else if (cmd == 7 || cmd == 8) {
    return ((1.0 * magnitude) / topSpinDegPerSecond) * 1000;
  }
  // return 1 second as a default
  return 1000;
}

String jsonResponse(String content, String data) {
  String message = "";
  if (!content.equals("text")) {
    message = "{\"content\":\"" + content + "\",\"data\":" + data + "}";
  }
  else {
    message = "{\"content\":\"" + content + "\",\"data\":\"" + data + "\"}";
  }
  return message;
}
