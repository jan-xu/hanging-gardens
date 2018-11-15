#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_TSL2561_U.h>

Adafruit_TSL2561_Unified tsl1 = Adafruit_TSL2561_Unified(TSL2561_ADDR_FLOAT, 12345);
Adafruit_TSL2561_Unified tsl2 = Adafruit_TSL2561_Unified(TSL2561_ADDR_FLOAT, 67890);

void displaySensorDetails(void)
{
  sensor_t sensor;
  tsl1.getSensor(&sensor);
  tsl2.getSensor(&sensor);
  Serial.println("------------------------------------");
  Serial.print  ("Sensor:       "); Serial.println(sensor.name);
  Serial.print  ("Driver Ver:   "); Serial.println(sensor.version);
  Serial.print  ("Unique ID:    "); Serial.println(sensor.sensor_id);
  Serial.print  ("Max Value:    "); Serial.print(sensor.max_value); Serial.println(" lux");
  Serial.print  ("Min Value:    "); Serial.print(sensor.min_value); Serial.println(" lux");
  Serial.print  ("Resolution:   "); Serial.print(sensor.resolution); Serial.println(" lux");  
  Serial.println("------------------------------------");
  Serial.println("");
  delay(500);
}

void configureSensor(void)
{
  tsl2.enableAutoRange(true);
  tsl2.setIntegrationTime(TSL2561_INTEGRATIONTIME_13MS); 
  Serial.print  ("Gain:         "); Serial.println("Auto");
  Serial.print  ("Timing:       "); Serial.println("13 ms");
  Serial.println("------------------------------------");
}


void setup(void) 
{
  Serial.begin(9600);
  Serial.println("Light Sensor Test"); Serial.println("");
  
  if(!tsl1.begin()){
    Serial.print("Ooops, Sensor 1 TSL2561 not detected ... Check your wiring or I2C ADDR!");
    while(1);
  }
    if(!tsl2.begin()){
    Serial.print("Ooops, Sensor 2 TSL2561 not detected ... Check your wiring or I2C ADDR!");
    while(1);
  }
  
  displaySensorDetails();
  
  configureSensor();

}

void loop(void) 
{  
  /* Get a new sensor event */ 
  sensors_event_t event;
  tsl1.getEvent(&event);
  /* Display results*/
  if (event.light)
  {
    Serial.print("Sensor 1: ");Serial.print(event.light); Serial.println(" lux");
    delay(500);
  }

     tsl2.getEvent(&event);
     if (event.light)
  {
    Serial.print("Sensor 2: ");Serial.print(event.light); Serial.println(" lux");
    delay(500);
  }
   

  else
  {
    /* If event.light = 0 lux the sensor is probably saturated
       and no reliable data could be generated! */
    Serial.println("Sensor overload");
  }

}
