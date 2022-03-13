#include "SoftwareSerial.h"
SoftwareSerial loraSerial(2,3);
void setup() {
  Serial.begin(9600);
  loraSerial.begin(9600);
}
String msg;
void loop() {
 if(loraSerial.available()>0){
  msg = loraSerial.readString();
  Serial.println(msg);
 }
 }
