#include <Arduino.h>
#include "Wire.h"
#include "SerialTransfer.h"
#include <Servo.h>


SerialTransfer myTransfer;
Servo myservo;
int claw = 0; 

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
      claw = myTransfer.packet.rxBuff[4];
      myservo.write(claw);            
        }
      int send_claw = myTransfer.packet.txBuff[4];
      myTransfer.sendData(send_claw);
     }       
  }


