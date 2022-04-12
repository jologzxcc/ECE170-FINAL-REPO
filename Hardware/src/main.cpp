#include <Arduino.h>
#include "Wire.h"
#include "SerialTransfer.h"
#include <Servo.h>


SerialTransfer myTransfer;
Servo myservo; 

void setup(){
  Serial.begin(115200);
  myTransfer.begin(Serial);
  myservo.attach(9);  
  
}

void loop(){

  if(myTransfer.available()){
    // send all received data back to Python
    for(uint16_t i=0; i < myTransfer.bytesRead; i++){
      myTransfer.packet.txBuff[i] = myTransfer.packet.rxBuff[i];
    }

    int claw = myTransfer.packet.txBuff[4];
    myTransfer.sendData(claw);
    delay(5);
    myservo.write(claw);            
    delay(5);       

     }       
  }


