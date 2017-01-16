boolean dataFlag = false;
boolean* light = new boolean[5];
int fastPause = 100;
int slowPause = 2000;

void setup() {
  // put your setup code here, to run once:
  pinMode(3,OUTPUT);
  pinMode(4,OUTPUT);
  pinMode(5,OUTPUT);
  pinMode(6,OUTPUT);
  pinMode(7,OUTPUT);
  for(int i = 0; i < 5; i++){
    light[i] = false;
  }
  testLights();
  Serial.begin(115200);
  Serial.println("Robot is Online");
}

void loop() {
  // put your main code here, to run repeatedly:
  while(Serial.available() > 0){
    int cmd = Serial.parseInt();//1,2,3,4,5,6-forward backward left right
    int vel = Serial.parseInt();//- stop standby, v range from 130-255
    handleInput(cmd);
  }
}

void handleInput(int cmd){
  switch(cmd){
    case 1:
      Serial.println("Moving forward");
      stopWheels();
      lights(0);
      lights(1);
      delay(2000);
      stopWheels();
      Serial.println("Stopped");
      break;
    case 2:
      Serial.println("Moving backward");
      stopWheels();
      lights(0);
      lights(1);
      delay(2000);
      stopWheels();
      Serial.println("Stopped");
      break;
    case 3:
      Serial.println("Turning left");
      stopWheels();
      lights(1);
      delay(1000);
      stopWheels();
      break;
    case 4:
      Serial.println("Turning right");
      stopWheels();
      lights(0);
      delay(1000);
      stopWheels();
      break;
    case 5:
      stopWheels();
      Serial.println("Stopping");
      break;
    case 6:
      stopArm();
      Serial.println("Stoppping arm");
      break;
    case 7:
      Serial.println("Moving the arm");
      stopArm();
      lights(2);
      lights(3);
      delay(500);
      stopArm();
      break;
    case 8:
      Serial.println("Moving the arm");
      stopArm();
      lights(2);
      lights(3);
      delay(500);
      stopArm();
      break;
    case 11:
      Serial.println("Moving forward");
      stopWheels();
      lights(0);
      lights(1);
      break;
    case 12:
      Serial.println("Moving backward");
      stopWheels();
      lights(0);
      lights(1);
      break;
    case 13:
      Serial.println("Turning left");
      stopWheels();
      lights(1);
      break;
    case 14:
      Serial.println("Turning Right");
      stopWheels();
      lights(0);
      break;
    case 15:
      Serial.println("Moving the arm");
      stopArm();
      lights(2);
      lights(3);
      break;
    case 16:
      Serial.println("Moving the arm");
      stopArm();
      lights(2);
      lights(3);
      break;
    default:
      Serial.println("Unsupported command: " + String(cmd));
  }
}

// Stops the wheels
void stopWheels(){
  if(light[0] == true){
    lights(0);
  }
  if(light[1] == true){
    lights(1);
  }
}

// Stops the arm
void stopArm(){
  if(light[2] == true){
    lights(2);
  }
  if(light[3] == true){
    lights(3);
  }
}

void lights(int num){
  if(light[num] == false){
    digitalWrite(num + 3,HIGH);
    light[num] = true;
  }else{
    digitalWrite(num + 3,LOW);
    light[num] = false;
  }
}

void testLights(){
  for(int i = 0; i < 5; i++){
    lights(i);
    delay(slowPause / 32);
    lights(i);
    delay(fastPause / 40);
  }
}

void turnLightsOff(){
  for (int i = 0; i < 5; i++){
    if(light[i] == true){
      lights(i);
    }
  }
}
