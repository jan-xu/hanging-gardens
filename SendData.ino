int led = 0;
int durationInput = 0;

void setup() {
  // put your setup code here, to run once:
  // sine wave
  Serial.begin(9600);
  pinMode(led, OUTPUT);

  // blink LED
  pinMode(13, OUTPUT);
}


void data1(int d) {  
  Serial.println(1); // tag
  Serial.println(100); // data
}

void data2(int sec) {
  Serial.println(2); // tag
  Serial.println(200); // data
}




void loop() {
  // put your main code here, to run repeatedly:
  data1(1000);
  data2(durationInput);

  delay(5000);
  }
