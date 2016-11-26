String aStr = "";
boolean stringFlag = false;
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
  Serial.begin(9600);
}

bool isChar(char str){
  if(str >= (char)32 && str < (char)127){
    return true;
  }
  return false;
}

void serialEvent(){
  while(Serial.available()){
    char str = Serial.read();
    if(isChar(str)){
      stringFlag = true;
      aStr += str;
      int letter = (int) str;
    }
  }
}

void loop() {
  // put your main code here, to run repeatedly:
   if(stringFlag == true){
    Serial.println(aStr);
    aStr = "";
    stringFlag = false;
    testLights(); 
   }
   delay(500);
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
