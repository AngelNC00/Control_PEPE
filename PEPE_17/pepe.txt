/* UNIVERSIDAD AUTONOMA METROPOLITANA

Descripción: Control del Robot PEPE utilizando ARDUINO.             

M en C Omar Lucio Cabrera Jiménez        MAY 2017    */

#include<Servo.h>

Servo servoCbzaNo;
Servo servoCbzaSi;

int incrServoCbzaNo = 5;
int incrServoCbzaSi = 5;

unsigned long milisActual = 0;
unsigned long milisAnterior = 0;

long intervalo = 250;

int posServoCbzaNo = 90;
int posServoCbzaSi = 90;

int bzoder = LOW;
int bzoizq = LOW;

int cbz_no = LOW;
int cbz_si = LOW;
int cmdnvo = 64;
int cmdant = 64;
  
void setup()  {
  Serial.begin(9600);   // Comunicación Serie 
  for (int Pin = 8; Pin <= 13; Pin++) 
    pinMode(Pin, OUTPUT); // Pines de salida 
  //servoCbzaNo.attach(6);
  pinMode(6, OUTPUT);
  servoCbzaSi.attach(5);
}

void vehiculo (int a, int b, int c, int d)  {
  digitalWrite(10, a);
  digitalWrite(11, b);
  digitalWrite(12, c);
  digitalWrite(13, d);
}  

void paro(){
  vehiculo(LOW, LOW, LOW, LOW);
  delay(50);
}
  
void loop() 
{   
  if (Serial.available() > 0)     
  {
    cmdnvo = Serial.read();    // Lectura de comando:
    
    switch (cmdnvo) 
    {      
      case 'D':  // Avanza
        if (cmdnvo != cmdant) 
          paro();  
        vehiculo(HIGH, LOW, HIGH, LOW);
        break;
        
      case 'I':  // Reversa
        if (cmdnvo != cmdant)    
          paro();
        vehiculo(LOW, HIGH, LOW, HIGH); 
        break;
        
      case 'R':  // Vuelta a la derecha
        if (cmdnvo != cmdant)    
          paro(); 
        vehiculo(LOW, HIGH, HIGH, LOW);           
        break;
        
      case 'A':  // Vuelta a la izquierda  
        if (cmdnvo != cmdant)
          paro(); 
        vehiculo(HIGH, LOW, LOW, HIGH);           
        break;
        
      case 'Z':  // Brazo izquierdo
        delay(100);
        if (bzoizq == 0)  {
          digitalWrite(9, HIGH);
          bzoizq = 1;
        }
        else  {
          digitalWrite(9, LOW);
          bzoizq = 0;
        }
        break;

      case 'E': // Brazo derecho
        delay(100); 
        if (bzoder == 0)  {
          digitalWrite(8, HIGH);
          bzoder = 1;
        }
        else  {
          digitalWrite(8, LOW);
          bzoder = 0;
        }
        break; 

      case 'S':  // Cabeza SI
        delay(100);  
        if (cbz_si == 0)  
        { 
          digitalWrite(7, HIGH);
          cbz_si = 1;
        }
        else 
        {
          digitalWrite(7, LOW);
          cbz_si = 0;
        }
        break;      

      case 'N':  // Cabeza NO
        delay(100);
        digitalWrite(6,HIGH);
        delay(100);
        digitalWrite(6,LOW);
        break;
                 
      default:  {  // Desactivar las salidas:        
        paro();
      }
    }
    cmdant = cmdnvo;
  }  
  
  if ( cbz_no == HIGH)
  {   
     milisActual = millis();
     if(milisActual - milisAnterior > intervalo)
     { 
        posServoCbzaNo += incrServoCbzaNo;
        if(posServoCbzaNo == 150 || posServoCbzaNo == 30)    
           incrServoCbzaNo *= -1;
        servoCbzaNo.write (posServoCbzaNo);
        milisAnterior = milisActual;
     }
  } 

  if ( cbz_si == HIGH)
  {   
     milisActual = millis();
     if(milisActual - milisAnterior > intervalo)
     { 
        posServoCbzaSi += incrServoCbzaSi;
        if(posServoCbzaSi == 150 || posServoCbzaSi == 30)    
           incrServoCbzaSi *= -1;
        servoCbzaSi.write (posServoCbzaSi);
        milisAnterior = milisActual;
     }
  } 
}
