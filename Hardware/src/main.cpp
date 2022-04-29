#include <Arduino.h>
#include "Wire.h"
#include "SerialTransfer.h"
#include <Servo.h>
#include <AccelStepper.h>

#define dirPinDepth 5
#define dirPin1 6
#define dirPin2 7

#define stepPinDepth 2
#define stepPin1 3
#define stepPin2 4

SerialTransfer myTransfer;
Servo myservo;

#define motorInterfaceType 1

int claw = 0;
int angle1 = 0;
int angle2 = 0;
int depth = 0;

AccelStepper stepper_depth = AccelStepper(motorInterfaceType, stepPinDepth, dirPinDepth);
AccelStepper stepper_1 = AccelStepper(motorInterfaceType, stepPin1, dirPin1);
AccelStepper stepper_2 = AccelStepper(motorInterfaceType, stepPin2, dirPin2);

void setup(){
  
  Serial.begin(115200);

  myTransfer.begin(Serial);
  myservo.attach(A0); 

  stepper_depth.setMaxSpeed(2000);
  stepper_depth.setAcceleration(2000);
  
  stepper_1.setMaxSpeed(4000);
  stepper_1.setAcceleration(4000);
  
  stepper_2.setMaxSpeed(4000);
  stepper_2.setAcceleration(4000);
  
}

void loop(){

      if(myTransfer.available()){
            claw = myTransfer.packet.rxBuff[0];      
            angle1 = myTransfer.packet.rxBuff[4];
            angle2 = myTransfer.packet.rxBuff[8];
            depth = myTransfer.packet.rxBuff[12];
            myTransfer.sendData(myTransfer.bytesRead);
      }

     

//////////////////////////  SERVO 1 CODE  ///////////////////////////////////////////////////////////////////
      
      
      int mapped_claw = map(claw, 200, 0, 0, 120);
      myservo.write(mapped_claw);

if(true){
///////////////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////  MOTOR 1 CODE  /////////////////////////////////////////////////////////////////
      
      int step_angle1 = angle1 / 1.8;
      stepper_1.moveTo(-(step_angle1 * 4.5));
      stepper_1.run();

///////////////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////  MOTOR 2 CODE  /////////////////////////////////////////////////////////////////
      
      // myservo.write(motor2);

///////////////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////  MOTOR 3 CODE  /////////////////////////////////////////////////////////////////
     
//      stepper_depth.moveTo(2000);
//      stepper_depth.runToPosition();
      
      //       stepper_depth.setCurrentPosition(0);
      // while(stepper_depth.currentPosition() != depth * 5){
      //       stepper_depth.setSpeed(1000);
      //       stepper_depth.run();
      //       }
      stepper_depth.moveTo(-(depth * 20));
      stepper_depth.run();
      
      

///////////////////////////////////////////////////////////////////////////////////////////////////////////
      }
}



