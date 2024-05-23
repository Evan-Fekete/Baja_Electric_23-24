#include <Arduino.h>

extern const byte CH_ID;  // LoRa Channel ID

/*  
Formats the transmitting message and executes necessary AT commands.
Params:
  msg -> the message to be transmitted
*/
void sendTransmission(String msg) {
  String command = "AT+SEND=" + String(CH_ID) + "," + String(msg.length()) + "," + msg + "\r\n";
  if(Serial1.availableForWrite()) {
    Serial1.write(command.c_str());
  }
}