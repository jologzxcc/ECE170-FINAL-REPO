#include <Arduino.h>
#include "Wire.h"
#include "SerialTransfer.h"
#include <Servo.h>


SerialTransfer myTransfer;
Servo myservo;
void setup(){
  Serial.begin(115200);
  myTransfer.begin(Serial);
  myservo.attach(A0);  
  
}

void loop(){

  if(myTransfer.available()){
    for(uint16_t i=0; i < myTransfer.bytesRead; i++){
      myTransfer.packet.txBuff[i] = myTransfer.packet.rxBuff[i];
      }

//////////////////////////  SERVO 1 CODE  ///////////////////////////////////////////////////////////////////
      
      int claw = myTransfer.packet.rxBuff[0];
      int mapped_claw = map(claw, 200, 0, 0, 120);
      myservo.write(mapped_claw);

///////////////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////  MOTOR 1 CODE  /////////////////////////////////////////////////////////////////
      
      // int motor1 = myTransfer.packet.rxBuff[4];
      // myservo.write(motor1);

///////////////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////  MOTOR 2 CODE  /////////////////////////////////////////////////////////////////
      
      // int motor2 = myTransfer.packet.rxBuff[8];
      // myservo.write(motor2);

///////////////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////  MOTOR 3 CODE  /////////////////////////////////////////////////////////////////
      
      // int motor3 = myTransfer.packet.rxBuff[12];
      // int mapped_motor3 = map(motor3, 250, 0, 0, 120);
      // myservo.write(mapped_motor3);

///////////////////////////////////////////////////////////////////////////////////////////////////////////

      myTransfer.sendData( myTransfer.bytesRead);

     }       
  }