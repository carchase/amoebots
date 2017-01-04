#include "PixyUART.h"

void setup() {
  Serial.begin(9600);
  Serial.println("Starting...");
  pinMode(LEFT_SENSOR_ECHO_PIN, INPUT);
  pinMode(LEFT_SENSOR_TRIG_PIN, OUTPUT);
  pinMode(RIGHT_SENSOR_ECHO_PIN, INPUT);
  pinMode(RIGHT_SENSOR_TRIG_PIN, OUTPUT);
}

void loop() {
  long duration_left, distance_left;
  long duration_right, distance_right;

      delayMicroseconds(2); // Added this line
  digitalWrite(LEFT_SENSOR_TRIG_PIN, HIGH);
  delayMicroseconds(10); // Added this line
  digitalWrite(LEFT_SENSOR_TRIG_PIN, LOW);
  
  duration_left = pulseIn(LEFT_SENSOR_ECHO_PIN, HIGH);
  distance_left = (duration_left/2) / 29.1;
  
  delayMicroseconds(2); // Added this line
  digitalWrite(RIGHT_SENSOR_TRIG_PIN, HIGH);
  delayMicroseconds(10); // Added this line
  digitalWrite(RIGHT_SENSOR_TRIG_PIN, LOW);
  
  duration_right = pulseIn(RIGHT_SENSOR_ECHO_PIN, HIGH);
  distance_right = (duration_right/2) / 29.1;

  if (distance_left >= 200 || distance_left <= 0){
    Serial.println("Left out of range");
  }
  else {
    Serial.print(distance_left);
    Serial.println(" cm");
  }
  if (distance_right >= 200 || distance_right <= 0){
    Serial.println("Right out of range");
  }
  else {
    Serial.print(distance_right);
    Serial.println(" cm");
  }
    }
  delay(1000);
}
