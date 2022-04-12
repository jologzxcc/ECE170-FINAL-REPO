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
    for(uint16_t i=0; i < myTransfer.bytesRead; i++){
      myTransfer.packet.txBuff[i] = myTransfer.packet.rxBuff[i];
      }

//////////////////////////  SERVO CODE  ///////////////////////////////////////////////////////////////////
      
      claw = myTransfer.packet.rxBuff[0];
      int mapped_claw = map(claw, 200, 0, 0, 120);
      myservo.write(mapped_claw);

///////////////////////////////////////////////////////////////////////////////////////////////////////////

      myTransfer.sendData( myTransfer.bytesRead);

     }       
  }


