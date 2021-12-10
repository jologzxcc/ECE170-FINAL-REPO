// ConstantSpeed.pde
// -*- mode: C++ -*-
//
// Shows how to run AccelStepper in the simplest,
// fixed speed mode with no accelerations
/// \author  Mike McCauley (mikem@airspayce.com)
// Copyright (C) 2009 Mike McCauley
// $Id: ConstantSpeed.pde,v 1.1 2011/01/05 01:51:01 mikem Exp mikem $

#include <AccelStepper.h>

#define motorPin1  A0      // IN1 on the ULN2003 driver
#define motorPin2  A1      // IN2 on the ULN2003 driver
#define motorPin3  A2     // IN3 on the ULN2003 driver
#define motorPin4  A3     // IN4 on the ULN2003 driver
#define MotorInterfaceType 4

AccelStepper stepper = AccelStepper(MotorInterfaceType, motorPin1, motorPin3, motorPin2, motorPin4);
void setup()
{  
   stepper.setMaxSpeed(1000);
   stepper.setSpeed(500);	
}

void loop()
{  
   stepper.runSpeed();
}
