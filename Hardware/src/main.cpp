#include <Arduino.h>
#include "Wire.h"
#include "SerialTransfer.h"
#include <Servo.h>
#include <AccelStepper.h>



SerialTransfer myTransfer;
Servo myservo;

const int dir_pin = 3;
const int step_pin = 4;
const int stepsPerRevolution = 200;

int claw = 0;
int angle1 = 0;
int angle2 = 0;
int depth = 0;

AccelStepper stepper_depth(AccelStepper:: DRIVER, step_pin, dir_pin);

void setup(){
  
  Serial.begin(115200);
  myTransfer.begin(Serial);
  myservo.attach(A0); 
  stepper_depth.setMaxSpeed(2000);
  stepper_depth.setAcceleration(2000);
  
}

void loop(){

      if(myTransfer.available()){
            // for(uint16_t i=0; i < myTransfer.bytesRead; i++){
            //       myTransfer.packet.txBuff[i] = myTransfer.packet.rxBuff[i];
            //       }
            claw = myTransfer.packet.rxBuff[0];      
            angle1 = myTransfer.packet.rxBuff[4];
            angle2 = myTransfer.packet.rxBuff[8];
            depth = myTransfer.packet.rxBuff[12];
            myTransfer.sendData(myTransfer.bytesRead);
      }

     

//////////////////////////  SERVO 1 CODE  ///////////////////////////////////////////////////////////////////
      
      
      int mapped_claw = map(claw, 200, 0, 0, 120);
      myservo.write(mapped_claw);


///////////////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////  MOTOR 1 CODE  /////////////////////////////////////////////////////////////////
      
      //  myservo.write(motor1);

///////////////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////  MOTOR 2 CODE  /////////////////////////////////////////////////////////////////
      
      // myservo.write(motor2);

///////////////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////  MOTOR 3 CODE  /////////////////////////////////////////////////////////////////
     
//      stepper_depth.moveTo(2000);
//      stepper_depth.runToPosition();
      if(depth > 1){
      //       stepper_depth.setCurrentPosition(0);
      // while(stepper_depth.currentPosition() != depth * 5){
      //       stepper_depth.setSpeed(1000);
      //       stepper_depth.run();
      //       }
      stepper_depth.moveTo(-(depth * 20));
      stepper_depth.runToPosition();
      
      }

///////////////////////////////////////////////////////////////////////////////////////////////////////////
      
}



