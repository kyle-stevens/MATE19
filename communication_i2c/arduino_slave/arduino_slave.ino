#include <Wire.h>
#include <string.h>
#include <stdio.h>
#define SLAVE 0x04

unsigned int pwm_motor_vals[8];


void setup() {
  Serial.begin(9600); //Start Serial output and commmunication at baud of 30720
  Wire.begin(SLAVE); //begin wired communication

  Wire.onReceive(receiveDataStream); //Define a callback function
}

void loop() {
  delay(10); //Delay, not necessary in all cases
}

void receiveDataStream(int byteCount) {
  char str[32]; //cstring for all hex characters


  
 
  //Start populating the new array of hex values
  int inputLength = 0;

  while (inputLength<32) {
    if(Wire.available()){
      str[inputLength] = Wire.read();
      if(str[inputLength]==NULL){
        break;
      }
      inputLength++;
    }
  }
  if(inputLength!=31){
    return;
  }
  //

  

  //begin delimiter use, declare the token char and the delimiter used
  char* token;
  const char s[2] = "~";
  token = strtok(str, s);
  int j = 0;
  while (token != NULL) {

    pwm_motor_vals[j] = Hex_to_UInt(token);
    token = strtok(NULL, s);

    j++;
  }
  return (0);

}

int Hex_to_UInt(char str[])
{
  return (int) strtol(str, 0, 16);
}

void Write_Motor_Vals(){
  for(int k=0;k<8;k++){
    Serial.print(pwm_motor_vals);
    Serial.print(" ");
  }
  Serial.println();
}
