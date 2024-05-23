#include <Arduino.h>

const byte RXD1 = 16;
const byte TXD1 = 17;

void parseCommand(String &CH_ID, int &msgLength, String &cmd);

void setup() {
  Serial.begin(115200);
  Serial1.begin(115200, SERIAL_8N1, RXD1, TXD1);
}


void loop() {
  String CH_ID;
  int msgLength;
  String cmd;
  if (Serial1.available()) {
    parseCommand(CH_ID, msgLength, cmd);
    Serial.println(cmd);
  }
}

/*
Parses the incoming transmission.
Params:
  CH_ID -> a reference that will store the transmitter's ID
  msgLength -> a reference will store the length of the message
  cmd -> a reference that will store the message
*/
void parseCommand(String &CH_ID, int &msgLength, String &cmd) {
  String msg = "";
  // Reads in the message
  while (Serial1.available()) {
    msg = msg + (char) Serial1.read();
  }
  // removes first part of message
  msg = msg.substring(5);
  // splits string by comma
  int comma1 = msg.indexOf(',');
  int comma2 = msg.indexOf(',', comma1 + 1);
  int comma3 = msg.indexOf(',', comma2 + 1);
  // stores data into passed references
  CH_ID = msg.substring(0, comma1);
  msgLength = msg.substring(comma1 + 1, comma2).toInt();
  cmd = msg.substring(comma2 + 1, comma3);
}
