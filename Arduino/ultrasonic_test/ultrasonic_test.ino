/*
 * created by Rui Santos, https://randomnerdtutorials.com
 * 
 * Complete Guide for Ultrasonic Sensor HC-SR04
 *
    Ultrasonic sensor Pins:
        VCC: +5VDC
        Trig : Trigger (INPUT) - Pin11
        Echo: Echo (OUTPUT) - Pin 12
        GND: GND
 */
 
int trigLw = 12;    // Trigger
int echoLw = 13;    // Echo
int trigUp = 10;
int echoUp = 11;
long duration, cm;
 
void setup() {
  //Serial Port begin
  Serial.begin (9600);
  //Define inputs and outputs
  pinMode(trigLw, OUTPUT);
  pinMode(echoLw, INPUT);
  pinMode(trigUp, OUTPUT);
  pinMode(echoUp, INPUT);
}

int waterLevelLw() {
  digitalWrite(trigLw, LOW);
  delayMicroseconds(5);
  digitalWrite(trigLw, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigLw, LOW);
  pinMode(echoLw, INPUT);
  duration = pulseIn(echoLw, HIGH);
  cm = (duration/2) / 29.1;     // Divide by 29.1 or multiply by 0.0343
  return cm;
}

int waterLevelUp() {
  digitalWrite(trigUp, LOW);
  delayMicroseconds(5);
  digitalWrite(trigUp, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigUp, LOW);
  pinMode(echoUp, INPUT);
  duration = pulseIn(echoUp, HIGH);
  cm = (duration/2) / 29.1;     // Divide by 29.1 or multiply by 0.0343
  return cm;
}
 
void loop() {

  cm = waterLevelLw();
  Serial.println("lower");
  Serial.println(cm);  // for lower rack in cm

  cm = waterLevelUp();
  Serial.println("upper");
  Serial.println(cm);  // for upper rack in cm

  //delay(1000);
}
