#include <Arduino.h>

extern const byte CH_ID;  // LoRa Channel ID

/*  
Formats the transmitting message and executes necessary AT commands.
Params:
  CH_ID -> the reciever's ID
  msg -> the message to be transmitted
*/
void sendTransmission(String msg) {
  String command = "AT+SEND=" + String(CH_ID) + "," + String(msg.length()) + "," + msg + "\r\n";
  while (!Serial1.availableForWrite());
  Serial1.write(command.c_str());
  Serial.println("Sent: " + command);
  delay(300);
}