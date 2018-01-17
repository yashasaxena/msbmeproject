// Initialize variables
// pins
int motorA_drive = 12;
int motorA_brake = 9; 
int motorA_speed = 3; 




void setup() {
  // put your setup code here, to run once:
  pinMode(motorA_drive, OUTPUT); //Initiates Motor Channel A pin
  pinMode(motorA_brake, OUTPUT); //Initiates Brake Channel A pin
  pinMode(motorA_speed, OUTPUT); //Initiates analog pin to control motor speed 

}

void loop() {
  // put your main code here, to run repeatedly:

}
