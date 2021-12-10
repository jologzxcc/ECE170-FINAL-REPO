// ProportionalControl.pde
// -*- mode: C++ -*-
//
// Make a single stepper follow the analog value read from a pot or whatever
// The stepper will move at a constant speed to each newly set posiiton, 
// depending on the value of the pot.
//
// Copyright (C) 2012 Mike McCauley
// $Id: ProportionalControl.pde,v 1.1 2011/01/05 01:51:01 mikem Exp mikem $

#include <AccelStepper.h>


#define motorPin1  A0      // IN1 on the ULN2003 driver
#define motorPin2  A1      // IN2 on the ULN2003 driver
#define motorPin3  A2     // IN3 on the ULN2003 driver
#define motorPin4  A3     // IN4 on the ULN2003 driver
#define MotorInterfaceType 4
#define ANALOG_IN A4

AccelStepper stepper = AccelStepper(MotorInterfaceType, motorPin1, motorPin3, motorPin2, motorPin4);



void setup()
{  
  Serial.begin(9600);
  stepper.setMaxSpeed(1000);
}

void loop()
{
  // Read new position
  int analog_in = analogRead(ANALOG_IN);
  int map_values = map(analog_in, 0, 2038, 0 , 1024);
  Serial.println(map_values);
  stepper.moveTo(map_values);
  stepper.setSpeed(1000);
  stepper.runSpeedToPosition();
}
