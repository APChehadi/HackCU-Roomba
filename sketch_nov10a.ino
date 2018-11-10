
#include <SoftwareSerial.h>

int rxPin = 3;
int txPin = 4;
int ledPin = 13;

SoftwareSerial Roomba(rxPin,txPin);

#define bumpright (sensorbytes[0] & 0x01)
#define bumpleft  (sensorbytes[0] & 0x02)

void setup() {
 pinMode(ledPin, OUTPUT);   // sets the pins as output
 Serial.begin(19200);
 Roomba.begin(19200);  
 digitalWrite(ledPin, HIGH); // say we're alive
 Serial.println ("Sending start command...");
 delay (1000);
  // set up ROI to receive commands  
 Roomba.write(128);  // START
 delay(150);
 Serial.println ("Sending Safe Mode command...");
 delay (1000);
 Roomba.write(131);  // CONTROL
 delay(150);
 digitalWrite(ledPin, LOW);  // say we've finished setup
 Serial.println ("Ready to go!");
 delay (5000);
}

void loop() {
 digitalWrite(ledPin, HIGH); // say we're starting loop
 Serial.println ("Go Forward");
 goForward();
 delay (500);
 Serial.println ("Halt!");
 halt();
 Serial.println ("Go Backwards");
 delay (500);
 goBackward();
 delay (500);
 Serial.println ("Halt!");
 halt();
 while(1) { } // Stop program
}

void goForward() {
 Roomba.write(137);   // DRIVE
 Roomba.write((byte)0x00);   // 0x00c8 == 200
 Roomba.write(0xc8);
 Roomba.write(0x80);
 Roomba.write((byte)0x00);
}



void goBackward() {
 Roomba.write(137);   // DRIVE
 Roomba.write(0xff);   // 0xff38 == -200
 Roomba.write(0x38);
 Roomba.write(0x01);
 Roomba.write((byte)0xF4);
}

void spin(){



  
}

void halt(){
byte j = 0x00;
Roomba.write(137);   
Roomba.write(j);   
Roomba.write(j);
Roomba.write(j);
Roomba.write(j);
}
