int directionPinA = 12;  //LEFT
int pwmPinA = 3;
int brakePinA = 9;
#define echoPin 6
#define trigPin 5

int directionPinB = 13;  //RIGHT
int pwmPinB = 11;
int brakePinB = 8;

const int ledPin = 7;
int ledState = LOW;          
unsigned long previousMillis = 0;     
const long interval = 300; 

long duration; 
int distance; 
int speeds = 123;

void blink(){
  unsigned long currentMillis = millis();
  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;
    if (ledState == LOW) {
      ledState = HIGH;
    } else {
      ledState = LOW;
    }
    digitalWrite(ledPin, ledState);
  }
}

void setup() {
  pinMode(directionPinA, OUTPUT);    //Initiates Motor Channel A pin
  pinMode(brakePinA, OUTPUT);        //Initiates Brake Channel A pin
  pinMode(pwmPinA, OUTPUT);
  pinMode(directionPinB, OUTPUT);    //Initiates Motor Channel A pin
  pinMode(brakePinB, OUTPUT);        //Initiates Brake Channel A pin
  pinMode(pwmPinB, OUTPUT);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  Serial.begin(9600);
}

void loop(){
      digitalWrite(trigPin, LOW);
      delayMicroseconds(2);
      digitalWrite(trigPin, HIGH);
      delayMicroseconds(10);
      digitalWrite(trigPin, LOW);
      duration = pulseIn(echoPin, HIGH);
      distance = duration * 0.034 / 2;

    if (Serial.read()=='b'){
      digitalWrite(directionPinA, LOW);  //Establishes forward direction of Channel A
      digitalWrite(brakePinA, LOW);      //Disengage the Brake for Channel A
      analogWrite(pwmPinA, speeds);      //Spins the motor on Channel A at "speeds"
      digitalWrite(directionPinB, LOW); 
      digitalWrite(brakePinB, LOW);   
      analogWrite(pwmPinB, speeds);   
    }
    else if((Serial.read()=='f')&&(distance >= 10)){
      digitalWrite(directionPinA, HIGH); 
      digitalWrite(brakePinA, LOW);   
      analogWrite(pwmPinA, speeds);  
      digitalWrite(directionPinB, HIGH); 
      digitalWrite(brakePinB, LOW);   
      analogWrite(pwmPinB, speeds); 
    } 
    else if(Serial.read()=='s'||(distance < 10)){
      digitalWrite(brakePinA, HIGH);   
      digitalWrite(brakePinB, HIGH);
    }
    else if(Serial.read()=='r'){
      digitalWrite(directionPinA, HIGH); 
      digitalWrite(brakePinA, LOW);   
      analogWrite(pwmPinA, speeds);  
      digitalWrite(directionPinB, HIGH); 
      digitalWrite(brakePinB, LOW);   
      analogWrite(pwmPinB, speeds); 
    }
    else if(Serial.read()=='l'){
      digitalWrite(directionPinA, LOW); 
      digitalWrite(brakePinA, LOW);   
      analogWrite(pwmPinA, speeds);  
      digitalWrite(directionPinB, HIGH); 
      digitalWrite(brakePinB, LOW);   
      analogWrite(pwmPinB, speeds); 
    }
    if (Serial.read()=='x'){
      speeds = 60;
      blink();
      }
    else{
      speeds = 123;
    }

}
