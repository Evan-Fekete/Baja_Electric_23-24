#include <Arduino.h>
#include "main.h"

const byte RXD1 = 16;   // LoRa RX pin
const byte TXD1 = 17;   // LoRa TX pin
const byte CH_ID = 1;   // LoRa Channel ID

float fuelLevel;
unsigned int speed;
unsigned int rpm;
float brakePressure;
char gearPosition = 'P';

unsigned long lastTransmissionTime;

void setup() {
  Serial.begin(115200);
  Serial1.begin(115200, SERIAL_8N1, RXD1, TXD1);
}

void loop() {
  // Update sensor data
  fuelLevel = updateFuelLevel();
  speed = updateSpeed();
  rpm = updateRPM();
  brakePressure = updateBrakePressure();
  gearPosition = updateGearPosition();

  // Send data to raspberry pi over serial port
  String msg = String(fuelLevel) + " " + String(speed) + " " + String(rpm) + " " + String(brakePressure) + " " + String(gearPosition);
  Serial.println(msg);
  
  // Transmit data every 300ms
  if (millis() - lastTransmissionTime >= 300) {
    sendTransmission(msg);
    lastTransmissionTime = millis();
  }
}