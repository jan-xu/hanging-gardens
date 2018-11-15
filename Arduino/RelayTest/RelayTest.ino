void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(13, OUTPUT);
  pinMode(12, OUTPUT);
  pinMode(11, OUTPUT);
  pinMode(10, OUTPUT);
}

void testRelayModule1() {
//for (int i = 0; i < 5; i = i+1) {
    digitalWrite(13, LOW);
    //delay(1000);
    //digitalWrite(13, HIGH);
    //delay(1000);
 // }
}

void testRelayModule2() {
  for (int i = 0; i < 5; i = i+1) {
    digitalWrite(12, LOW);
    delay(1000);
    digitalWrite(12, HIGH);
    delay(1000);
  }
}

void testRelayModule3() {
//for (int i = 0; i < 5; i = i+1) {
    digitalWrite(13, HIGH);
    delay(1000);
    //digitalWrite(13, HIGH);
    //delay(1000);
 // }
}
void loop() {
  // put your main code here, to run repeatedly:

  testRelayModule1();
  testRelayModule2();
  testRelayModule3();
}
