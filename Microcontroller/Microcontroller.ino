/*

University of California, Berkeley
CE 186 Design of Cyber-Physical Systems (Fall Term 2018)
Hanging Gardens: Microcontroller.ino
Group 6

DESCRIPTION

*/

#include <Servo.h>
#include <Wire.h>
#include "TSL2561.h"
TSL2561 tsl(TSL2561_ADDR_FLOAT); 

/////////////// tags
int LightLeft_tag    = -1; // int in mV
int LightRight_tag   = -2; // int in mV
int LightCenter_tag  = -3; // int in lux
int WaterLevelLw_tag = -4; // int in mm
int WaterLevelUp_tag = -5; // int in mm
int Temperature_tag  = -6; // data float

/////////////// Jay's parameters
/////////////// pin IDs
// analog
int Temp       = 0; // temperature sensor --> Analog Pin A0
int LightLeft  = 1; // right photocell    --> Analog Pin A1
int LightRight = 2; // left photocell     --> Analog Pin A2

// digital
int LED     = 2; // LED on both racks   --> Digital Pin 2
int PP      = 3; // water pump          --> Digital Pin 3
int Vlwr    = 4; // valve on lower rack --> Digital Pin 4
int Vupr    = 5; // valve on upper rack --> Digital Pin 5
int Srvlwr1 = 6; // lower servo motor 1 --> Digital Pin 6
int Srvlwr2 = 7; // lower servo motor 2 --> Digital Pin 7
int Srvupr1 = 8; // upper servo motor 1 --> Digital Pin 8
int Srvupr2 = 9; // upper servo motor 2 --> Digital Pin 9

Servo SMlwr1; // instantiate lower servo motor 1
Servo SMlwr2; // instantiate lower servo motor 2
Servo SMupr1; // instantiate upper servo motor 1
Servo SMupr2; // instantiate upper servo motor 2
int pos = 90; // servo position

/////////////// Distance meter
int trigLw = 12; // lower trigger
int echoLw = 13; // lower echo
int trigUp = 10; // upper trigger
int echoUp = 11; // upper echo
long duration, mm;
float tempC;
///////////////

/////////////// Actuator tags
int tag = 0;
char act_tag   = '0';
char Roof_tag  = 'a';
char flush_tag = 'b';
char LED_tag   = 'c';
int RoofLeft   = 1;
int RoofRight  = 2;
int RoofCenter = 3;
int flushOn    = 1;
int flushOff   = 0;
int LEDon      = 1;
int LEDoff     = 0;
///////////////

/////////////// Valves and pump tags
int Vlwr_tag = -101;
int Vupr_tag = -102;
int PP_tag   = -103;
///////////////

/////////////// Actuator settings
int Roof_pos = 3;
int flushMode = 0;
int LED_set = 0;

void setup() {
  // Initialize serial communication at 9600 bps
  Serial.begin(9600);

  tsl.setGain(TSL2561_GAIN_0X); // set no gain for light sensor in center
  
  // Initalize actuators as outputs
  pinMode(LED, OUTPUT); // LED on both racks
  pinMode(PP , OUTPUT); // water pump in tank

  // Initialize servos
  SMlwr1.attach(Srvlwr1); // lower servo --> Pin 6
  SMlwr2.attach(Srvlwr2); // lower servo --> Pin 7
  SMupr1.attach(Srvupr1); // upper servo --> Pin 8
  SMupr2.attach(Srvupr2); // upper servo --> Pin 9

  //////////////// Distance meter
  pinMode(trigLw, OUTPUT); // lower trigger --> Pin 12
  pinMode(echoLw, INPUT);  // lower echo    --> Pin 13
  pinMode(trigUp, OUTPUT); // upper trigger --> Pin 10
  pinMode(echoUp, INPUT);  // upper echo    --> Pin 11

  //////////////// Flushing
  pinMode(Vlwr, OUTPUT); // valve on lower rack
  pinMode(Vupr, OUTPUT); // valve on upper rack

  // Initialize all actuators
  initiator();
}

// photocell on left roof
int photocellLeft() {
  int Vout = map(analogRead(LightLeft), 0, 1023, 0, 5000);
  return Vout;
}

// photocell on right roof
int photocellRight() {
  int Vout = map(analogRead(LightRight), 0, 1023, 0, 5000);
  return Vout;
}

// light sensor in center
uint16_t light_sensor() {
  uint32_t lum = tsl.getFullLuminosity();
  uint16_t ir, full;
  ir = lum >> 16;
  full = lum & 0xFFFF;
  uint16_t lux = tsl.calculateLux(full, ir);
  return lux;
}


// lower water level
int waterLevelLw() {
  digitalWrite(trigLw, LOW);
  delayMicroseconds(5);
  digitalWrite(trigLw, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigLw, LOW);
  duration = pulseIn(echoLw, HIGH);
  mm = (duration/2) / 2.91; // Divide by 2.91 or multiply by 0.343
  return mm;
}

// upper water level
int waterLevelUp() {
  digitalWrite(trigUp, LOW);
  delayMicroseconds(5);
  digitalWrite(trigUp, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigUp, LOW);
  duration = pulseIn(echoUp, HIGH);
  mm = (duration/2) / 29.1; // Divide by 2.91 or multiply by 0.343
  return mm;
}

// temperature
float temperature() {
  int reading = analogRead(Temp);
  float voltage = reading * 5.0;
  voltage /= 1024.0;
  float temperatureC = (voltage - 0.5) * 100;
  return temperatureC;
}

void sensorsNormalOperation() {
  // Print tags followed by data reading of all sensors

  // Left light sensor on upper roof
  int Vout = photocellLeft();
  Serial.println(LightLeft_tag);
  Serial.println(Vout);

  // Right light sensor on upper roof
  Vout = photocellRight();
  Serial.println(LightRight_tag);
  Serial.println(Vout);

  // Center light sensor on upper roof
  uint16_t lux = light_sensor();
  Serial.println(LightCenter_tag);
  Serial.println(lux);

  // Water level (ultrasonic) meter on lower rack
  int mm = waterLevelLw();
  Serial.println(WaterLevelLw_tag);
  Serial.println(mm); // for lower rack in mm

  // Water level (ultrasonic) meter on upper rack
  mm = waterLevelUp();
  Serial.println(WaterLevelUp_tag);
  Serial.println(mm); // for upper rack in cm
  
  // Temperature meter on upper rack
  float tempC = temperature();
  Serial.println(Temperature_tag);
  Serial.println(tempC);

}

// LED
void LED_setting(int LED_set) {
  if (LED_set == 1) {
    digitalWrite(LED, LOW);
  } else {
    digitalWrite(LED, HIGH);
  }
}

// roof done
void roofactuators(int Roof_pos) { // manipulate servo motors and LED 
  if (Roof_pos == RoofLeft) { // rotate roof to left
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
    
  } else if (Roof_pos == RoofRight) { // rotate roof to right
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
    
  } else if (Roof_pos == RoofCenter) { // rotate roof to center
    if (pos == 90) {                        // to 90 degrees
      // already at center, do nothing
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

//flushing
void flushing(int flushMode) { // determine whether to flush or not

  if (flushMode == flushOff) { // if flushing is not ordered
    digitalWrite(Vlwr, HIGH);  // make sure valves and pump
    digitalWrite(Vupr, HIGH);  // are closed and not running
    digitalWrite(PP, HIGH);
  }
  
  if (flushMode == flushOn) {             // if flushing is ordered
    Serial.println(Vlwr_tag); // send tag of lower valve
    Serial.println(1);        // send tag that lower valve is open
    do {
      digitalWrite(Vlwr, LOW);  // open lower valve
    } while (waterLevelLw() < 60); // keep lower valve open until lower water level is lower than 60mm
    
    Serial.println(Vupr_tag); // send tag of upper valve
    Serial.println(1);        // send tag that upper valve is open
    do {
      digitalWrite(Vupr, LOW);  // open upper valve
    } while (waterLevelUp() < 60); // keep upper valve open until upper water level is lower than 60mm
    
    // we are done with emptying racks
    // let the pump rinse the racks for 10 sec
    Serial.println(PP_tag); // send tag of pump
    Serial.println(1);      // send tag that pump is on
    for (int ppRinse = 0; ppRinse < 10; ppRinse += 1) {
      digitalWrite(PP, LOW); // run pump for 15 sec
      delay(1000);
    }
    
    // now we need to fill up the racks with water
    // pump is still running
    // close lower valve first
    Serial.println(Vlwr_tag); // send tag of lower valve
    Serial.println(0);        // send tag that lower valve is closed
    do {
      digitalWrite(Vlwr, HIGH); // close lower valve
    } while (waterLevelLw() > 20); // wait until lower water level is higher than 20mm

    Serial.println(Vupr_tag); // send tag of upper valve
    Serial.println(0);        // send tag that upper valve is closed
    do {
      digitalWrite(Vupr, HIGH);  // close upper valve
    } while (waterLevelUp() > 20); // wait until upper rack is filled with water

    Serial.println(PP_tag); // send tag of pump
    Serial.println(0);      // send tag that pump is off
    digitalWrite(PP, HIGH); // turn off pump assuming both racks are filled with water
  }
}

void initiator() { // run only once when start
/////////////////////////// roof ready
  //SMlwr1.write(pos);
  //SMlwr2.write(pos);
  //SMupr1.write(pos);
  //SMupr2.write(pos);

/////////////////////////// LED ready
  digitalWrite(LED, HIGH);

/////////////////////////// valves ready
  digitalWrite(Vlwr, HIGH);
  digitalWrite(Vupr, HIGH);

/////////////////////////// pump ready
  digitalWrite(PP, HIGH);

/////////////////////////// water ready
  digitalWrite(Vupr, LOW); // open upper valve
  do {
    digitalWrite(PP, LOW); // turn on pump
  } while (waterLevelLw() > 20); // wait until lower rack is filled with water
  digitalWrite(Vupr, HIGH); // close upper valve to fill in upper rack with water
  do {
    digitalWrite(PP, LOW);
  } while (waterLevelUp() > 20); // wait until upper rack is filled
  // assuming both racks are filled up with water
  // stop pump
  digitalWrite(PP, HIGH); 
}

void loop() {

  sensorsNormalOperation(); // read all sensors every 15 mins
  delay(10000); // allow time for data processing

  while (!Serial.available()) {}
  
  // Wait for actuator settings from Python (might have to copy and paste this three times instead)
  while (Serial.available() > 0) {
    act_tag = Serial.read();
    Serial.println(act_tag);
    delay(1000);
    if (act_tag == Roof_tag) {
      Roof_pos = int(Serial.read()) - 48; // subtract 48 to convert '0' (ASCII 48) to 0 and '1' (ASCII 49) to 1
      Serial.println(Roof_pos);
    } else if (act_tag == flush_tag) {
      flushMode = int(Serial.read()) - 48;
      Serial.println(flushMode);
    } else if (act_tag == LED_tag) {
      LED_set = int(Serial.read()) - 48;
      Serial.println(LED_set);
    }
    delay(3000);
  }

  // Send actuator signals  
  //roofactuators(Roof_pos);
  LED_setting(LED_set);
  //flushing(flushMode);

  delay(3000);
}
