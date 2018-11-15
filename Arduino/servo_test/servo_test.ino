/* Sweep
 by BARRAGAN <http://barraganstudio.com>
 This example code is in the public domain.

 modified 8 Nov 2013
 by Scott Fitzgerald
 http://www.arduino.cc/en/Tutorial/Sweep
*/

#include <Servo.h>

Servo myservo1;  // create servo object to control a servo
Servo myservo2;
// twelve servo objects can be created on most boards

int pos = 0;    // variable to store the servo position

void setup() {
  Serial.begin(9600);
  myservo1.attach(9);  // attaches the servo on pin 9 to the servo object
  myservo2.attach(10);
}


void loop() {
  for (pos = 0; pos <= 180; pos += 1) { // goes from 0 degrees to 180 degrees
    Serial.println("inside for1 loop");
    Serial.println(pos);
    // in steps of 1 degree
    myservo1.write(pos);              // tell servo to go to position in variable 'pos'
    myservo2.write(180-pos);
    delay(15);                       // waits 15ms for the servo to reach the position
  }
  
  for (pos = 180; pos >= 0; pos -= 1) { // goes from 180 degrees to 0 degrees
    Serial.println("inside for2 loop");
    Serial.println(pos);
    myservo1.write(pos);              // tell servo to go to position in variable 'pos'
    myservo2.write(180-pos);
    delay(15);                       // waits 15ms for the servo to reach the position
  }
}

