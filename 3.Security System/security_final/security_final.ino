//Prateek
//www.prateeks.in
#include <Arduino.h>
#include "wiring_private.h"
#include <WiFiNINA.h>
#include <Firebase_Arduino_WiFiNINA.h>

#define URL "test-e8b6a-default-rtdb.firebaseio.com"
#define Secret "AIzaSyAEs6ayyqojMgfiNl-p4OqdwfIS2ztGKaE"

const int buzzer = 9;

char ssid[] = "Sam";
char pass[] = "Samarth123";

FirebaseData Fire;
String path;

int count = 0;
char card_no[12];
int Buzz1 = 10;
int Buzz2 = 12;

String rfid_1 = "0"; 
String rfid_2 = "0";
String rfid_3 = "0";
String rfid_4 = "0";

Uart mySerial(&sercom0, 5, 6, SERCOM_RX_PAD_1, UART_TX_PAD_0);

// Attach the interrupt handler to the SERCOM
void SERCOM0_Handler() {
  mySerial.IrqHandler();
}

void path_define()
{
  path = "/rfid_security/id";
  //Serial.print(rfid_1);
  String rfid_data;
  if (Firebase.getString(Fire, path))
  {
    rfid_data = Fire.stringData();
  }
  //Serial.println(rfid_data);
  String rfid = String(rfid_data);
  //Serial.print(rfid);
  rfid_1 = rfid[0];
  rfid_2 = rfid[1];
  rfid_3 = rfid[2];
  rfid_4 = rfid[3];
}

void setup() {
  pinPeripheral(5, PIO_SERCOM_ALT);
  pinPeripheral(6, PIO_SERCOM_ALT);

  // Start my new hardware serial
  mySerial.begin(9600);
  pinMode(Buzz1, OUTPUT);
  pinMode(Buzz2,OUTPUT);
  Serial.begin(9600);
  Serial1.begin(9600);
  Serial.print("Connecting to Wi-Fi");
  int status = WL_IDLE_STATUS;
  while (status != WL_CONNECTED)
  {
    status = WiFi.begin(ssid, pass);
    Serial.print(".");
    delay(100);
  }
  Serial.println();
  Serial.print("Connected with IP: ");
  Serial.println(WiFi.localIP());
  Serial.println();

  Firebase.begin(URL, Secret, ssid, pass);
  Firebase.reconnectWiFi(true);
  path_define();
}

void alarm() {
  tone(Buzz1,1000);
  tone(Buzz2,1000);
  delay(2000);
  noTone(Buzz1);
  noTone(Buzz2);
  delay(2000);

  
//  delay(2000);
//  
//  delay(2000);
  Serial.print("A");
}

void loop() {
  

  if (Serial1.available()) {
    count = 0;
    while (Serial1.available() ) {
      card_no[count] = Serial1.read();
      count++;
      delay(10);
    }
    if (card_no[0] == '1' && card_no[1] == '3' && card_no[2] == '0' && card_no[3] == '0' && card_no[4] == 'A' && card_no[5] == '2' && card_no[6] == '8' && card_no[7] == '7' && card_no[8] == '5' && card_no[9] == '6' && card_no[10] == '6' && card_no[11] == '0' && rfid_1 == "0") {
      alarm();

    }
    if (card_no[0] == '1' && card_no[1] == '4' && card_no[2] == '0' && card_no[3] == '0' && card_no[4] == '4' && card_no[5] == '8' && card_no[6] == 'E' && card_no[7] == 'F' && card_no[8] == '9' && card_no[9] == 'C' && card_no[10] == '2' && card_no[11] == 'F' && rfid_2 == "0") {
      alarm();

    }
    if (card_no[0] == '1' && card_no[1] == '4' && card_no[2] == '0' && card_no[3] == '0' && card_no[4] == '4' && card_no[5] == '8' && card_no[6] == 'E' && card_no[7] == 'F' && card_no[8] == '9' && card_no[9] == '2' && card_no[10] == '2' && card_no[11] == '1' && rfid_3 == "0") {
      alarm();

    }
    if (card_no[0] == '1' && card_no[1] == '4' && card_no[2] == '0' && card_no[3] == '0' && card_no[4] == '4' && card_no[5] == '6' && card_no[6] == 'E' && card_no[7] == 'E' && card_no[8] == '1' && card_no[9] == '9' && card_no[10] == 'A' && card_no[11] == '5' && rfid_4 == "0") {
      alarm();

    }
  }
  if (mySerial.available()) {
    count = 0;
    while (mySerial.available() ) {
      card_no[count] = mySerial.read();
      count++;
      delay(10);
    }
    if (card_no[0] == '1' && card_no[1] == '3' && card_no[2] == '0' && card_no[3] == '0' && card_no[4] == 'A' && card_no[5] == '2' && card_no[6] == '8' && card_no[7] == '7' && card_no[8] == '5' && card_no[9] == '6' && card_no[10] == '6' && card_no[11] == '0' && rfid_1 == "0") {
      alarm();

    }
    if (card_no[0] == '1' && card_no[1] == '4' && card_no[2] == '0' && card_no[3] == '0' && card_no[4] == '4' && card_no[5] == '8' && card_no[6] == 'E' && card_no[7] == 'F' && card_no[8] == '9' && card_no[9] == 'C' && card_no[10] == '2' && card_no[11] == 'F' && rfid_2 == "0") {
      alarm();

    }
    if (card_no[0] == '1' && card_no[1] == '4' && card_no[2] == '0' && card_no[3] == '0' && card_no[4] == '4' && card_no[5] == '8' && card_no[6] == 'E' && card_no[7] == 'F' && card_no[8] == '9' && card_no[9] == '2' && card_no[10] == '2' && card_no[11] == '1' && rfid_3 == "0") {
      alarm();

    }
    if (card_no[0] == '1' && card_no[1] == '4' && card_no[2] == '0' && card_no[3] == '0' && card_no[4] == '4' && card_no[5] == '6' && card_no[6] == 'E' && card_no[7] == 'E' && card_no[8] == '1' && card_no[9] == '9' && card_no[10] == 'A' && card_no[11] == '5' && rfid_4 == "0") {
      alarm();

    }
  }
}
