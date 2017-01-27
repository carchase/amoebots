#define ControlPin1 6
#define ControlPin2 7
#define ControlPin3 8
#define PWMpin1 9
#define PWMpin2 10
#define PWMpin3 11

void setup() {
  // put your setup code here, to run once:
  pinMode(PWMpin1, OUTPUT); // sets the pin as output
  pinMode(PWMpin2, OUTPUT); // sets the pin as output
  pinMode(PWMpin3, OUTPUT); // sets the pin as output
  pinMode(ControlPin1, OUTPUT); // sets the pin as output
  pinMode(ControlPin2, OUTPUT); // sets the pin as output
  pinMode(ControlPin3, OUTPUT); // sets the pin as output
  delay(5000);
}

void loop() {
  // put your main code here, to run repeatedly:
  analogWrite(PWMpin1, 150);
  analogWrite(PWMpin2, 150);
  analogWrite(PWMpin3, 150);
  digitalWrite(ControlPin1, LOW);
  digitalWrite(ControlPin2, LOW);
  digitalWrite(ControlPin3, LOW);
  delay(1000);
  digitalWrite(ControlPin1, HIGH);
  digitalWrite(ControlPin2, HIGH);
  digitalWrite(ControlPin3, HIGH);
  delay(1000);
}
