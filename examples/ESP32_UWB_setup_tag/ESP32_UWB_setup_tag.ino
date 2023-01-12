// currently tag is module #5
// The purpose of this code is to set the tag address and antenna delay to default.
// this tag will be used for calibrating the anchors.
// Modified to run with STM32F103C8 (BluePill)
// Ludvig Syrén 3/1/2023
#include <SPI.h>
#include "DW1000Ranging.h"
#include "DW1000.h"

// connection pins
#define PIN_SPI_SCK = PB13;
#define PIN_SPI_MISO = PB14;
#define PIN_SPI_MOSI = PB15;
const uint8_t PIN_SS = PB12;   // spi select pin
const uint8_t PIN_RST = PA12; // reset pin
const uint8_t PIN_IRQ = PA11; // irq pin

// TAG antenna delay defaults to 16384
// leftmost two bytes below will become the "short address"
char tag_addr[] = "7D:00:22:EA:82:60:3B:9C";

void newRange()
{
  Serial.print(DW1000Ranging.getDistantDevice()->getShortAddress(), HEX);
  Serial.print(",");
  Serial.println(DW1000Ranging.getDistantDevice()->getRange());
}

void newDevice(DW1000Device *device)
{
  Serial.print("Device added: ");
  Serial.println(device->getShortAddress(), HEX);
}

void inactiveDevice(DW1000Device *device)
{
  Serial.print("delete inactive device: ");
  Serial.println(device->getShortAddress(), HEX);
}

void setup()
{
  Serial.begin(115200);
  delay(1000);
  pinMode(LED_BUILTIN, OUTPUT);
  //init the configuration
  DW1000Ranging.initCommunication(PIN_RST, PIN_SS, PIN_IRQ, PB15, PB14, PB13); //Reset, CS, IRQ pin

  DW1000Ranging.attachNewRange(newRange);
  DW1000Ranging.attachNewDevice(newDevice);
  DW1000Ranging.attachInactiveDevice(inactiveDevice);

// start as tag, do not assign random short address

  DW1000Ranging.startAsTag(tag_addr, DW1000.MODE_LONGDATA_RANGE_LOWPOWER, false);
}

void loop()
{
  digitalWrite(LED_BUILTIN, HIGH);
  DW1000Ranging.loop();
}

