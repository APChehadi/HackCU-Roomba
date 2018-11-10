#include <SoftwareSerial.h>
//* RX is digital pin 10 (connect to TX of other device - iRobot DB25
// pin 2)
//* TX is digital pin 11 (connect to RX of other device - iRobot DB25
// pin 1)
#define rxPin 0
#define txPin 1
// set up a new software serial port:
SoftwareSerial softSerial = SoftwareSerial(rxPin, txPin);
int inByte = 0; // incoming serial byte
/*************************************************************
SETUP
*************************************************************/
void setup()
{
delay(2000); // Needed to let the robot initialize
// define pin modes for software tx, rx pins:
 pinMode(rxPin, INPUT);
 pinMode(txPin, OUTPUT);
// start the the SoftwareSerial port 57600 bps (robot’s default)
 softSerial.begin(115200);
// start hardware serial port
  Serial.begin(115200);
  softSerial.write(128); // This command starts the OI.
  softSerial.write(131); // set mode to safe (see p.7 of OI manual)
}
/*************************************************************
LOOP
*************************************************************/
void loop()
{
 //serial.write(ana
 softSerial.write(142); // requests the OI to send a packet of
 // sensor data bytes
 softSerial.write(3); // request cliff sensor value specifically
 delay(250); // poll sensor 4 times a second
 if (softSerial.available() > 0) {
 inByte = softSerial.read();
 }
 Serial.println(inByte);
}
