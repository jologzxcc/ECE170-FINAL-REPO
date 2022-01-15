char data;

void setup() {
   Serial.begin(9600);
   pinMode(LED_BUILTIN,OUTPUT);
}

void loop() {
  
  if (Serial.available()>0){
    data = Serial.read();
    if (data == '1'){
      digitalWrite(LED_BUILTIN,HIGH);
      Serial.write("Led on");
    }
    if (data == '2'){
      digitalWrite(LED_BUILTIN,LOW);
      Serial.write("Led off");}
    else{
      Serial.write("invalid information");
    }
    }
}
