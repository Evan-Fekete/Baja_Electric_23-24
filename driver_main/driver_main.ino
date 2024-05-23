#include <Arduino.h>
#include "transmitter.h"
#include "sensors.h"

const byte RXD1 = 16;   // LoRa RX pin
const byte TXD1 = 17;   // LoRa TX pin
const byte CH_ID = 1;   // LoRa Channel ID

float fuelLevel;
unsigned int speed;
unsigned int rpm;
float brakePressure;
char gearPosition = 'P';

void setup() {
  Serial.begin(115200);
  Serial1.begin(115200, SERIAL_8N1, RXD1, TXD1);
}

void loop() {
  sendTransmission("hello");
}