/*

University of California, Berkeley
CE 186 Design of Cyber-Physical Systems (Fall Term 2018)
Hanging Gardens: Microcontroller.ino
Group 6

DESCRIPTION

*/

#include <Servo.h>

// Declare Pin ID's for all sensors
int Llft = 0; // left light sensor on upper roof
int Lrgt = 1; // right light sensor on upper roof
int Lctr = 2; // center light sensor on upper rack
int Wlwr = 3; // water level (ultrasonic) meter on lower rack
int Wupr = 4; // water level (ultrasonic) meter on upper rack
int Tupr = 5; // temperature meter on upper rack

// Declare Pin ID's for all actuators and initialize servos
int LED    = 2 ; // LED on both racks
int PP     = 4 ; // water pump in tank
int Vlwr   = 7 ; // valve on lower rack
int Vupr   = 8 ; // valve on upper rack
int Srvlwr = 9 ; // lower servo motor
int Srvupr = 10; // upper servo motor
Servo SMlwr; // instantiate lower servo motor
Servo SMupr; // instantiate upper servo motor
int pos = 0; // servo position

// Declare sensor tags
int Llft_tag = -1; // left light sensor on upper roof
int Lrgt_tag = -2; // right light sensor on upper roof
int Lctr_tag = -3; // center light sensor on upper rack
int Wlwr_tag = -4; // water level (ultrasonic) meter on lower rack
int Wupr_tag = -5; // water level (ultrasonic) meter on upper rack
int Tupr_tag = -6; // temperature meter on upper rack

// Declare actuator tags
int LED_tag = 2;
int PP_tag = 3;
int Vlwr_tag = 4;
int Vupr_tag = 5;
int Srv_tag = 6;

// Initialize actuator settings;
int LED_set  = 0; // LED on both racks off
int PP_set   = 0; // water pump in tank off
int Vlwr_set = 0; // valve on lower rack closed
int Vupr_set = 0; // valve on upper rack closed

// Declare some useful parameters
// int Srvlft = 1000; // servo fully anti-clockwise (left position)
// int Srvrgt = 2000; // servo fully clockwise (right position)
// int Srvctr = 1500; // servo midpoint (center position)
// int Srvlft_tag = -1000; // tag for servo fully anti-clockwise (left position)
// int Srvrgt_tag = -2000; // tag for servo fully clockwise (right position)
// int Srvctr_tag = -1500; // tag for servo midpoint (center position)
// int flushMode = 0; // indicator of flushing mode (0: off, 1: on)
int flushMode_tag = 9; // tag that toggles flushing mode
double timeIntervalNormal = 900000; // [ms] -- 15 mins interval between each reading (normal operation)
int timeIntervalFlush = 1000; // [ms] -- 1 sec interval between each reading (for flushing)
int waterLvlmax = 20; // [mm] -- 20 mm distance between ultrasonic meter and water level required to stop pumping
int waterLvlmin = 50; // [mm] -- 50 mm distance between ultrasonic meter and water level required to initiate flushing
int waterLvlempty = 120; // [mm] -- 120 mm distance between ultrasonic meter and water level of an empty tube
int flush_max_its = 300; // 300 seconds maximum of flushing







void setup() {
  // Initialize serial communication at 9600 bps
  Serial.begin(9600);

  // Initialize sensors as inputs
  pinMode(Llft, INPUT); // left light sensor on upper roof
  pinMode(Lrgt, INPUT); // right light sensor on upper roof
  pinMode(Lctr, INPUT); // center light sensor on upper rack
  pinMode(Wlwr, INPUT); // water level (ultrasonic) meter on lower rack
  pinMode(Wupr, INPUT); // water level (ultrasonic) meter on upper rack
  pinMode(Tupr, INPUT); // temperature meter on upper rack

  // Initalize actuators as outputs
  pinMode(LED , OUTPUT); // LED on both racks
  pinMode(PP  , OUTPUT); // water pump in tank
  pinMode(Vlwr, OUTPUT); // valve on lower rack
  pinMode(Vupr, OUTPUT); // valve on upper rack

  // Initialize servos
  SMlwr.attach(Srvlwr); // lower servo --> Pin 9
  // SMlwr.writeMicroseconds(Srvctr); // set lower servo to center position
  SMupr.attach(Srvupr); // upper servo --> Pin 10
  // SMupr.writeMicroseconds(Srvctr); // set upper servos to center position
}

void sensorsNormalOperation() {
  // Print tags followed by data reading of all sensors

  // Left light sensor on upper roof
  Serial.println(Llft_tag);
  Serial.println(analogRead(Llft));

  // Right light sensor on upper roof
  Serial.println(Lrgt_tag);
  Serial.println(analogRead(Lrgt));

  // Center light sensor on upper roof
  Serial.println(Lctr_tag);
  Serial.println(analogRead(Lctr));

  // Water level (ultrasonic) meter on lower rack
  Serial.println(Wlwr_tag);
  Serial.println(analogRead(Wlwr));

  // Water level (ultrasonic) meter on upper rack
  Serial.println(Wupr_tag);
  Serial.println(analogRead(Wupr));

  // Temperature meter on upper rack
  Serial.println(Tupr_tag);
  Serial.println(analogRead(Tupr));

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

    if (Serial.read() == LED_tag) {
      LED_set = Serial.read();
      if (LED_set == 1) {
        digitalWrite(LED, LOW); // LOW to turn on LED on relay module
      } 
      else if (LED_set == 0) {
        digitalWrite(LED, HIGH); // HIGH to turn off LED on relay module
      }
    }
  }
}



void flushactuators() {
  if (Serial.available() > 0) {
    if (Serial.read() == PP_tag) {
      if (Serial.read() == 1) {
        digitalWrite(PP, HIGH);
      } else if (Serial.read() == 0) {
        PP_set = LOW;
      }
    }

    if (Serial.read() == Vlwr_tag) {
      if (Serial.read() == 1) {
        Vlwr_set = HIGH;
      } else if (Serial.read() == 0) {
        Vlwr_set = LOW;
      }
    }

    if (Serial.read() == Vupr_tag) {
      if (Serial.read() == 1) {
        Vupr_set = HIGH;
      } else if (Serial.read() == 0) {
        Vupr_set = LOW;
      }
    }
  }
}

void flushing() {
  int i = 0;
  digitalWrite(Vlwr, HIGH);
  int waterLvllwr = analogRead(Wlwr); // add mapping if required
  while (waterLvllwr < waterLvlempty) {
    ++i; // increment i by 1
    delay(timeIntervalFlush);
    waterLvllwr = analogRead(Wlwr); // add mapping if required
    if (i >= flush_max_its) {
      break;
    }
  }

  i = 0;
  digitalWrite(Vupr, HIGH);
  int waterLvlupr = analogRead(Wupr); // add mapping if required
  while (waterLvlupr < waterLvlempty) {
    ++i; // increment i by 1
    delay(timeIntervalFlush);
    waterLvlupr = analogRead(Wupr); // add mapping if required
    if (i >= flush_max_its) {
      break;
    }
  }

  i = 0;
  digitalWrite(PP, HIGH);
  digitalWrite(Vlwr, LOW);
  while (waterLvllwr > waterLvlmax) {
    ++i; // increment i by 1
    delay(timeIntervalFlush);
    waterLvllwr = analogRead(Wlwr); // add mapping if required
    if (i >= flush_max_its) {
      break;
    }
  }

  i = 0;
  digitalWrite(Vupr, LOW);
  while (waterLvlupr > waterLvlmax) {
    ++i; // increment i by 1
    delay(timeIntervalFlush);
    waterLvlupr = analogRead(Wupr); // add mapping if required
    if (i >= flush_max_its) {
      break;
    }
  }

  digitalWrite(PP, LOW);
}

void loop() {
  sensorsNormalOperation(); // read all sensors every 15 mins
  delay(10000); // allow time for data processing

  roofactuators();

  while (Serial.available() > 0) {
    roofactuators();
    delay(1000); // allow time for data to be sent to Serial monitor
    
    if (Serial.read() == flushMode_tag) {
      flushing();
    }
  }
  
  delay(5000);
}
