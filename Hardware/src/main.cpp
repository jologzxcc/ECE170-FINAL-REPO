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
Servo myservoClaw;
Servo myservoRotate;

#define motorInterfaceType 1

int claw = 0;
int angle1 = 0;
int angle2 = 0;
int depth = 0;
int rotation = 0;

AccelStepper stepper_depth = AccelStepper(motorInterfaceType, stepPinDepth, dirPinDepth);
AccelStepper stepper_1 = AccelStepper(motorInterfaceType, stepPin1, dirPin1);
AccelStepper stepper_2 = AccelStepper(motorInterfaceType, stepPin2, dirPin2);

void setup(){
  
  Serial.begin(115200);

  myTransfer.begin(Serial);
  myservoClaw.attach(A0); 
  myservoRotate.attach(A1); 

  stepper_depth.setMaxSpeed(3000);
  stepper_depth.setAcceleration(3000);
  
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
            rotation = myTransfer.packet.rxBuff[16];
            myTransfer.sendData(myTransfer.bytesRead);
      }

     

//////////////////////////  SERVO 1 CODE  ///////////////////////////////////////////////////////////////////
      
      // myservoClaw.write(100);

      // myservoRotate.write(10);

if(true){

      int mapped_claw = map(claw, 200, 0, 0, 100);
      myservoClaw.write(mapped_claw);

      if(rotation <= 70){
      myservoRotate.write(10);      
      }
      if(rotation > 70){
      myservoRotate.write(110);
      }
      
           
///////////////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////  MOTOR 1 CODE  /////////////////////////////////////////////////////////////////
      
      int step_angle1 = angle1 / 1.8;
      stepper_1.moveTo(-(step_angle1 * 4.5));
      stepper_1.run();

///////////////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////  MOTOR 2 CODE  /////////////////////////////////////////////////////////////////
      
      int step_angle2 = angle2 / 1.8;
      stepper_2.moveTo(step_angle2 * 2.25);
      stepper_2.run();

///////////////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////  MOTOR 3 CODE  /////////////////////////////////////////////////////////////////
     
      stepper_depth.moveTo(depth * 20);
      stepper_depth.run();
      
///////////////////////////////////////////////////////////////////////////////////////////////////////////
      }
}



