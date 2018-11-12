const int buttonPin = 2;     // the number of the pushbutton pin
int buttonState = 0;
int data = 0;

void setup() {
  // put your setup code here, to run once:
  
  Serial.begin(9600);
  pinMode(8, OUTPUT); // with switch
  pinMode(13, OUTPUT);
  pinMode(buttonPin, INPUT); // switch
}


void ButtonCheck() {  
  Serial.println(8); // button tag
  buttonState = digitalRead(buttonPin);
  if (buttonState == HIGH) {
    //Serial.println("button pushed");
    Serial.println(81);  // signal for button pushed
    digitalWrite(8, HIGH);
  }
  else {
    //Serial.println("button not pushed");
    Serial.println(80);
    digitalWrite(8, LOW);
  }
}


void loop() {
  // put your main code here, to run repeatedly:
  ButtonCheck();
  
  if (Serial.available()) {
    Serial.println(13); // tag 13
    data = Serial.read();
    Serial.println(130); // signal for feedback
    digitalWrite(13, LOW);
  }
    
  else {
    Serial.println(13); // tag13
    Serial.println(131);
    digitalWrite(13, HIGH);
  }
  delay(10000);
  }
