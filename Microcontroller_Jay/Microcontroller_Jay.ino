/*

University of California, Berkeley
CE 186 Design of Cyber-Physical Systems (Fall Term 2018)
Hanging Gardens: Microcontroller.ino
Group 6

DESCRIPTION

*/

#include <Servo.h>
/////////////// tags
int LightLeft_tag = -1;      // int in lux
int LightRight_tag = -2;     // int in lux
int LightCenter_tag = -3;    // int in lux
int WaterLevelLw_tag = -4;   // int in mm
int WaterLevelUp_tag = -5;   // int in mm
int Temperature_tag = -6;    // data float

/////////////// Jay's parameters
/////////////// pin IDs
int LED = 2;
int PP = 3;
int Vlwr   = 4 ; // valve on lower rack
int Vupr   = 5 ; // valve on upper rack
int Srvlwr1 = 6 ; // lower servo motor
int Srvlwr2 = 7;
int Srvupr1 = 8; // upper servo motor
int Srvupr2 = 9;

Servo SMlwr1; // instantiate lower servo motor
Servo SMlwr2;
Servo SMupr1; // instantiate upper servo motor
Servo SMupr2;
int pos = 0; // servo position

/////////////// Distance meter
int trigLw = 12;    // trigger lower
int echoLw = 13;    // echo lower
int trigUp = 10;    // trigger upper
int echoUp = 11;    // trigger lower
long duration, cm;
///////////////

/////////////// actuator tags

int Roof_tag = -1;
int flush_tag = -2;
int LED_tag = -3;
int RoofLeft = 1;
int RoofRight = 2;
int RoofCenter = 3;
int flushOn = 1;
int flushOff = 0;
int LEDon = 1;
int LEDoff = 0;
///////////////

void setup() {
  // Initialize serial communication at 9600 bps
  Serial.begin(9600);



  // Initalize actuators as outputs
  pinMode(LED , OUTPUT); // LED on both racks
  pinMode(PP  , OUTPUT); // water pump in tank

  // Initialize servos
  SMlwr1.attach(Srvlwr1); // lower servo --> Pin 9
  SMlwr2.attach(Srvlwr2);
  // SMlwr.writeMicroseconds(Srvctr); // set lower servo to center position
  SMupr1.attach(Srvupr1); // upper servo --> Pin 10
  SMupr2.attach(Srvupr2);
  // SMupr.writeMicroseconds(Srvctr); // set upper servos to center position

  //////////////// Jay's setup
  //////////////// distance meter
  pinMode(trigLw, OUTPUT);
  pinMode(echoLw, INPUT);
  pinMode(trigUp, OUTPUT);
  pinMode(echoUp, INPUT);

  //////////////// flushing
  pinMode(Vlwr, OUTPUT); // valve on lower rack
  pinMode(Vupr, OUTPUT); // valve on upper rack
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

void sensorsNormalOperation() {
  // Print tags followed by data reading of all sensors

  // Left light sensor on upper roof
  Serial.println(LightLeft_tag);
  Serial.println(50000);

  // Right light sensor on upper roof
  Serial.println(LightRight_tag);
  Serial.println(40000);

  // Center light sensor on upper roof
  Serial.println(LightCenter_tag);
  Serial.println(10000);

  // Water level (ultrasonic) meter on lower rack         updated 11/14
  cm = waterLevelLw();
  Serial.println(WaterLevelLw_tag);
  //Serial.println(cm);  // for lower rack in cm
  Serial.println(4);

  // Water level (ultrasonic) meter on upper rack         updated 11/14
  cm = waterLevelUp();
  Serial.println(WaterLevelUp_tag);
  //Serial.println(cm);  // for upper rack in cm
  Serial.println(10);

  // Temperature meter on upper rack
  Serial.println(Temperature_tag);
  Serial.println(30.4);

}

void roofactuators() { // manipulate servo motors and LED
  if (Serial.available() > 0) {
    if (Serial.read() == Roof_tag) {
      
      if (Serial.read() == RoofLeft) { // rotate roof to left
        if (pos == 180) {               // to 180
          // already on left position, do nothing
        }
        else if (pos == 0) {
          // rotate from right to left
          for (pos = 0; pos <= 180; pos += 1) {
            SMlwr1.write(pos);
            SMlwr2.write(pos);
            SMupr1.write(pos);
            SMupr2.write(pos);
            delay(50);
          }
        }
        else if (pos == 90) {
          // rotate from center to left
          for (pos = 90; pos <= 180; pos += 1) {
            SMlwr1.write(pos);
            SMlwr2.write(pos);
            SMupr1.write(pos);
            SMupr2.write(pos);
            delay(50);
          }
        }
        
      } else if (Serial.read() == RoofRight) { // rotate roof to right
        if (pos == 0) {                      // to 0 degrees angle
          // already on right position, do nothing
        }
        else if (pos == 180) {
          // rotate from left to right
          for (pos = 180; pos >= 0; pos -= 1) {
            SMlwr1.write(pos);
            SMlwr2.write(pos);
            SMupr1.write(pos);
            SMupr2.write(pos);
            delay(50);
          }
        }
        else if (pos == 90) {
          // rotate from center to right
          for (pos = 90; pos >= 0; pos -= 1) {
            SMlwr1.write(pos);
            SMlwr2.write(pos);
            SMupr1.write(pos);
            SMupr2.write(pos);
            delay(50);
          }
        }
        
      } else if (Serial.read() == RoofCenter) { // rotate roof to center
        if (pos == 90) {                        // to 90 degrees
          // alreadt at center, do nothing
        }
        if (pos == 180) {
          // rotate from left to center
          for (pos = 180; pos >= 90; pos -= 1) {
            SMlwr1.write(pos);
            SMlwr2.write(pos);
            SMupr1.write(pos);
            SMupr2.write(pos);
            delay(50);
          } 
        }
        else if (pos == 0) {
          // rotate from right to center
          for (pos = 0; pos <= 90; pos += 1) {
            SMlwr1.write(pos);
            SMlwr2.write(pos);
            SMupr1.write(pos);
            SMupr2.write(pos);
            delay(50);
          }
        }
      }
    }
  }
}

//void initiator() { // run only once when start
//                    // need to figure out when to run this func
///////////////////////////// roof ready
//SMlwr1.write(90);
//SMlwr2.write(90);
//SMupr1.write(90);
//SMupr2.write(90);
//
///////////////////////////// water ready
//  digitalWrite(Vupr, LOW); // open upper valve
//  do {
//    digitalWrite(PP, LOW); // turn on pump
//  } while (WaterLevelLw > 3); // wait until lower rack is filled with water
//  digitalWrite(Vupr, HIGH); // close upper valve to fill in upper rack with water
//  do {
//    digitalWrite(PP, LOW);
//  } while ((WaterlLevelLw < 3) && (WaterLevelUp > 3)); // wait until upper rack is filled
//  // assuming both racks are filled up with water
//  // stop pump
//  digitalWrite(PP, HIGH); 
//}
//
//void flushing() {                           // determine whether to flush or not
//  if (Serial.available() > 0) {
//    if (Serial.read() == flushMode_tag) {   // identify flushing order
//////////////////////////////////////////////////////////////
//      if (Serial.read() == 0) {           // if flushing is not ordered
//        digitalWrite(Vlwr, HIGH);         // make sure valves and pump
//        digitalWrite(Vupr, HIGH);         // are closed and not running
//        digitalWrite(PP, HIGH);
//      }
//////////////////////////////////////////////////////////////  
//      if (Serial.read() == 1) {             // if flushing is ordered
//        do {
//          digitalWrite(Vlwr, LOW);          // open lower valve
//        } while (WaterLevelLw < 10);        // keep lower valve open until lower water level is lower than 2cm
//        if (WaterLevelLw > 10) {             // if lower water level is lower than 3cm
//          do {
//            digitalWrite(Vupr, LOW);        // open upper valve
//                                  // keep upper valve open until upper water level is lower than 2cm
//                                  // while lower water level is lower than 2cm
//          } while ((WaterLevelUp < 10) && (WaterLevelLw > 10)); 
//        }
//        // we are done with emptying racks
//        // let the pump rinse the racks for 15 sec
//        if ((WaterLevelLw > 10) && (WaterLevelUp > 10)) {
//          // pumping is faster than flushing. maybe less than 15 sec
//          for (int ppRinse = 0; ppRinse < 16; ppRinse += 1) {
//            digitalWrite(PP, LOW); // run pump for 15 sec
//            delay(1000);
//          }
//        }
//        // now we need to fill up the racks with water
//        // pump is still running
//        // close lower valve first
//        do {
//          digitalWrite(Vlwr, HIGH);     // close lower valve
//        } while (WaterLevelLw > 3);     // wait until lower water level is higher than 10cm
//        do {
//          digitalWrite(Vupr, HIGH);     // close upper valve
//        } while ((WaterLevelLw < 3) && (WaterLevelUp > 3))  // wait until upper rack is filled with water
//        digitalWrite(PP, HIGH); // turn off pump assuming both racks are filled with water
//      }
//    }
//  }
//}

void loop() {
  // set all actuators initially to be closed (LOW)
  
  sensorsNormalOperation(); // read all sensors every 15 mins
  delay(5000); // allow time for data processing
//
//  roofactuators();
//
//  while (Serial.available() > 0) {
//    roofactuators();
//    delay(1000); // allow time for data to be sent to Serial monitor
//    
//    if (Serial.read() == flushMode_tag) {
//      flushing();
//    }
//  }
  
}
