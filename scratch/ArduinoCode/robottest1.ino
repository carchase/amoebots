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




void setup(){
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
  Serial.println("Hello World");
  
}

//command list:(command, speed)
//1 2 - move forward or backward
//3 4 - turn left or right
//5 - stop 6 -arm stop
//7 8 - move the arm
//11-16 function without time delay

void loop(){
  while(Serial.available() > 0){
    int f = Serial.parseInt();//1,2,3,4,5,6-forward backward left right
    int v = Serial.parseInt();//- stop standby, v range from 130-255
    //Serial.println(f);
    //Serial.println(v);
    //if (Serial.read()=='\n'){
      if (f == 1){
        Serial.println("Moving forward");
        fb(v,0);
      }
      else if (f==2){
        Serial.println("Moving backward");
        fb(v,1);
      }
      else if (f==3){
        Serial.println("Turning left");
        turn(v,0);
      }
      else if (f==4){
        Serial.println("Turning right");
        turn(v,1);
      }
      else if (f==5){
        Stop();
        Serial.println("Stopping");
      }
      else if (f==6){
        Serial.println("Stoppping arm");
        armstop();
      }
      else if (f==7){
        Serial.println("Moving the arm");
        arm(v,0);
      }
      else if (f==8){
        Serial.println("Moving the arm");
        arm(v,1);
      }
      else if (f==11){
        Serial.println("Moving forward");
        fb_nd(v,0);
      }
      else if (f==12){
        Serial.println("Moving backward");
        fb_nd(v,1);
      }
      else if (f==13){
        Serial.println("Turning left");
        turn_nd(v,0);
      }
      else if (f==14){
        Serial.println("Turning Right");
        turn_nd(v,1);
      }
      else if (f==15){
        Serial.println("Moving the arm");
        arm_nd(v,0);
      }
      else if (f==16){
        Serial.println("Moving the arm");
        arm_nd(v,1);
      }
    //}
  }
  
  


  
}



void move(int motor, int speed, int direction){
//Move specific motor at speed and direction
//motor: 0 for B 1 for A 2 for C 3 for D
//speed: 0 is off, and 255 is full speed
//direction: 0 clockwise, 1 counter-clockwise

  digitalWrite(STBY, HIGH); //disable standby

  boolean inPin1 = LOW;
  boolean inPin2 = HIGH;

  if(direction == 1){
    inPin1 = HIGH;
    inPin2 = LOW;}
  else{
    inPin1 = LOW;
    inPin2 = HIGH;
  }

  if(motor == 1){
    digitalWrite(AIN1, inPin1);
    //digitalWrite(AIN2, inPin2);
    analogWrite(PWMA, speed);
  }else if(motor ==0){
    digitalWrite(BIN1, inPin1);
    //digitalWrite(BIN2, inPin2);
    analogWrite(PWMB, speed);
  }else if(motor ==2){
    digitalWrite(CIN1, inPin1);
    //digitalWrite(BIN2, inPin2);
    analogWrite(PWMC, speed);
  }else if(motor ==3){
    digitalWrite(DIN1, inPin1);
    //digitalWrite(BIN2, inPin2);
    analogWrite(PWMD, speed);
  }
}

void fb(int v, int forback){
 //forback: 0 forward, 1 backward 
 //v: PWM from 0 -255
  Serial.println("function fb activiated");
  if(forback == 0){
    move(1,v,0);
    move(0,v,1);}
  else{
    move(1,v,1);
    move(0,v,0);
  }
  delay(2000);
  Stop();
  Serial.println("Stopped");
  
}

void fb_nd(int v, int forback){
//fb function without delay
 //forback: 0 forward, 1 backward 
 //v: PWM from 0 -255
  //Serial.println("function fb activiated");
  if(forback == 0){
    move(1,v,0);
    move(0,v,1);}
  else{
    move(1,v,1);
    move(0,v,0);
  }
  
}

void turn(int vt, int lr){
//vt: from 130-255
//lr: 0 left, 1 right
  Serial.println("function turn activiated");
  if(lr == 0){
    move(1,vt,1);
    move(0,vt,1);}
  else{
    move(1,vt,0);
    move(0,vt,0);
  }
  delay(1000);
  Stop();

}

void turn_nd(int vt, int lr){
//turn function without delay
//vt: from 130-255
//lr: 0 left, 1 right
  //Serial.println("function turn activiated");
  if(lr == 0){
    move(1,vt,1);
    move(0,vt,1);}
  else{
    move(1,vt,0);
    move(0,vt,0);
  }
}


void arm(int vp, int dir){
//function to drive the arm
//vt - speed from 130-255
//dir - 0 or 1
  Serial.println("function ARM activiated");
  if(dir ==0){
    move(2,vp,1);
    move(3,vp,1);}
  else{
    move(2,vp,0);
    move(3,vp,0);
  }
  delay(500);
  armstop();
}

void arm_nd(int vp, int dir){
//function to drive the arm without delay
//vt - speed from 130-255
//dir - 0 or 1
  //Serial.println("function ARM activiated");
  if(dir ==0){
    move(2,vp,1);
    move(3,vp,1);}
  else{
    move(2,vp,0);
    move(3,vp,0);
  }
}


void Stop()
{
  
//This stops the motor by setting both IN pins to LOW
  //Serial.println("function stop activiated");
  digitalWrite(AIN1, LOW);
  digitalWrite(BIN1, LOW);
  analogWrite(PWMA, 0);
  analogWrite(PWMB, 0);
}

void armstop(){
  //Serial.println("function armstop activiated");
  digitalWrite(CIN1, LOW);
  digitalWrite(DIN1, LOW);
  analogWrite(PWMC, 0);
  analogWrite(PWMD, 0);
  //Serial.println("Stopped");
}




void standby(){
//enable standby
  Serial.println("function standby activiated");  
  digitalWrite(STBY, LOW); 
}
