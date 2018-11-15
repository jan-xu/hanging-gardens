#include <Servo.h>

int Srvlft_tag = -1000;
int Srvrgt_tag = -2000;
int Srvctr_tag = -1500;
int Srvlwr = 9;
int Srvupr = 10;
Servo SMlwr;
Servo SMupr;
int pos = 0;
int Srv_tag = 6;

void setup() {
  Serial.begin(9600);
  SMlwr.attach(Srvlwr);
  SMupr.attach(Srvupr);
}

void roofactuators() { // manipulate servo motors and LED
  if (Serial.available() > 0) {
    if (Serial.read() == Srv_tag) {
      
      if (Serial.read() == Srvlft_tag) { // rotate roof to left
        if (pos == 180) {
          // already on left position, do nothing
        }
        else if (pos == -180) {
          // rotate from right to left
          for (pos = -180; pos <= 180; pos += 1) {
            SMlwr.write(pos);
            SMupr.write(pos);
            delay(15);
          }
        }
        else if (pos == 0) {
          // rotate from center to left
          for (pos = 0; pos <= 180; pos += 1) {
            SMlwr.write(pos);
            SMupr.write(pos);
            delay(15);
          }
        }
        
      } else if (Serial.read() == Srvrgt_tag) { // rotate roof to right
        if (pos == -180) {
          // already on right position, do nothing
        }
        else if (pos == 180) {
          // rotate from left to right
          for (pos = 180; pos >= -180; pos -= 1) {
            SMlwr.write(pos);
            SMupr.write(pos);
            delay(15);
          }
        }
        else if (pos == 0) {
          // rotate from center to right
          for (pos = 0; pos >= -180; pos -= 1) {
            SMlwr.write(pos);
            SMupr.write(pos);
            delay(15);
          }
        }
        
      } else if (Serial.read() == Srvctr_tag) { // rotate roof to center
        if (pos == 0) {
          // alreadt at center, do nothing
        }
        if (pos == 180) {
          // rotate from left to center
          for (pos = 180; pos >= 0; pos -= 1) {
            SMlwr.write(pos);
            SMupr.write(pos);
            delay(15);
          } 
        }
        else if (pos == -180) {
          // rotate from right to center
          for (pos = -180; pos <= 0; pos += 1) {
            SMlwr.write(pos);
            SMupr.write(pos);
            delay(15);
          }
        }
      }
    }

//    if (Serial.read() == LED_tag) {
//      LED_set = Serial.read();
//      if (LED_set == 1) {
//        digitalWrite(LED, LOW); // LOW to turn on LED on relay module
//      } 
//      else if (LED_set == 0) {
//        digitalWrite(LED, HIGH); // HIGH to turn off LED on relay module
//      }
//    }
  }
}

void loop () {
  roofactuators();
}

