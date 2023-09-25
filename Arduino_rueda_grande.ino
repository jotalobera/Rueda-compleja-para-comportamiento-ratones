
// include the library code:
#include <LiquidCrystal.h>
#include <SPI.h>
#include <SD.h>
////////////////////////////////////////// DEFINE ////////////////////////////////////////////////////////////////

#define muestreo 10000
#define pi 3.1415926535
#define cant_ranuras 15
#define radio_rueda 55/10 //en centimetros
#define dist_ranuras (2*pi*radio_rueda/cant_ranuras) 
#define pin_encoder_1 0
#define pin_encoder_2 2
#define pin_encoder_3 3
#define pin_reset_R1 A2
#define pin_reset_R2 A1
#define pin_reset_R3 A0

////////////////////////////////////////// VARIABLES ////////////////////////////////////////////////////////////////

//Encoder
unsigned long int cuentas_ranuras_R1=0,cuentas_ranuras_R2=0,cuentas_ranuras_R3=0,cant_datos=0;
int flag_encoder_1=0;
volatile long tiempo_escritura=0,tiempo_actual=0;
volatile float vueltas_R1=0,vueltas_R2=0,vueltas_R3=0;
volatile unsigned long debounce_1 = 0,debounce_2 = 0,debounce_3 = 0; // Tiempo del rebote.

//VARIABLES PARA LCD
const int rs = 9, en = 8, d4 = 5, d5 = 4, d6 = 10, d7 = 6;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);


// VARIABLES PARA SD
const int chipSelect = 7;


////////////////////////////////////////// CONFIG Y LOOP ////////////////////////////////////////////////////////////////

void setup()
{
    long int suma_media=0;
    int val=0;
    
    //INICIO SERIAL
    Serial.begin(9600); 
    
    //INICIO LCD -- FILAS Y COLUMNAS DE LCD
    lcd.begin(20, 4);
    // MENSAJES ESTATICOS
    lcd.setCursor(0, 0);
    lcd.print("Rueda1");;
    lcd.setCursor(7, 0);
    lcd.print("Rueda2");
    lcd.setCursor(14, 0);
    lcd.print("Rueda3");
    
    //VARIABLES ENCODER
    pinMode(pin_encoder_1,INPUT);    
    pinMode(pin_encoder_2,INPUT);    
    pinMode(pin_encoder_3,INPUT);    
    attachInterrupt(0, Counter_2, RISING); //pin 2 es interrupcion 0 ; pin 3 interrup 1
    attachInterrupt(1, Counter_3, RISING); //pin 2 es interrupcion 0 ; pin 3 interrup 1
    
    //INICIO TARJETA SD
    delay(3000);
    lcd.setCursor(0, 3);
    lcd.print("Iniciando SD");
    delay(1000);
    if (!SD.begin(chipSelect)) {
      lcd.setCursor(0, 3);
      lcd.print("Error tarjeta SD");
      while (1);
    }
    lcd.setCursor(0, 3);
    lcd.print("Tarjeta Ok    ");
}


void loop()
{
    //CUENTA VUELTAS Y MUESTRO LCD
    tiempo_actual=millis();      
    int horas=0,minutos=0;
    
    //Rueda1
    lcd.setCursor(0, 0);
    lcd.print("Rueda1");;
    lcd.setCursor(0, 1);
    vueltas_R1=cuentas_ranuras_R1/30;
    lcd.print(int(vueltas_R1));
    //Rueda2  
    lcd.setCursor(7, 0);
    lcd.print("Rueda2");
    lcd.setCursor(7, 1);
    vueltas_R2=cuentas_ranuras_R2/30;
    lcd.print(int(vueltas_R2));
    //Rueda3
    lcd.setCursor(14, 0);
    lcd.print("Rueda3");
    lcd.setCursor(14, 1);
    vueltas_R3=cuentas_ranuras_R3/30;
    lcd.print(int(vueltas_R3));

    //LEO ENTRADAS ANALOGICAS
    if(analogRead(pin_reset_R1)>512){
      cuentas_ranuras_R1=0;
      lcd.setCursor(0, 1);
      vueltas_R1=cuentas_ranuras_R1/30;
      lcd.print(int(vueltas_R1));
      lcd.print("    ");
    }
    if(analogRead(pin_reset_R2)>512){
      cuentas_ranuras_R2=0;
      lcd.setCursor(7, 1);
      vueltas_R2=cuentas_ranuras_R2/30;
      lcd.print(int(vueltas_R2));
      lcd.print("    ");
    }
    if(analogRead(pin_reset_R3)>512){
      cuentas_ranuras_R3=0;
      lcd.setCursor(14, 1);
      vueltas_R3=cuentas_ranuras_R3/30;
      lcd.print(int(vueltas_R3));
      lcd.print("    ");
    }
    if(digitalRead (pin_encoder_1) && (micros()-debounce_1 > 500) && (flag_encoder_1==0)) { 
    // Vuelve a comprobar que el encoder envia una señal buena y luego comprueba que el tiempo es superior a 1000 microsegundos y vuelve a comprobar que la señal es correcta.
        debounce_1 = micros(); // Almacena el tiempo para comprobar que no contamos el rebote que hay en la señal.
        cuentas_ranuras_R1++;
        flag_encoder_1=1;
        }

    if(digitalRead (pin_encoder_1)==0){
      flag_encoder_1=0; 
    }
    if ((tiempo_actual-tiempo_escritura)>muestreo){
      //GUARDA DATOS
      File dataFile = SD.open("datalog.txt", FILE_WRITE);
      lcd.setCursor(18, 3);
      lcd.print("NO");
      String dataString = "";
      for (int i = 0; i < 3; i++) {
        if (i==0){ dataString += cuentas_ranuras_R1;dataString += ",";}
        if (i==1){ dataString += cuentas_ranuras_R2;dataString += ",";}
        if (i==2){ dataString += cuentas_ranuras_R3;
          if (dataFile) {
            dataFile.println(dataString);
            lcd.setCursor(0, 3);
            lcd.print("Dato N:");
            lcd.print(cant_datos);
            lcd.print("        ");
            cant_datos++;
          }
        }
      }  
    tiempo_escritura=millis();
    dataFile.close();
    }
    lcd.setCursor(18, 3);
    lcd.print("OK");
    lcd.setCursor(0, 2);
    lcd.print("Tiempo: ");
    if (tiempo_actual/3600000>0){
      horas=int(tiempo_actual/3600000);
      tiempo_actual=tiempo_actual-horas*3600000;
    }
    if (tiempo_actual/60000>0){
      minutos=int(tiempo_actual/60000);
      tiempo_actual=tiempo_actual-minutos*60000;
    }
    lcd.print(horas);
    lcd.print("h ");
    lcd.print(minutos);
    lcd.print("m ");
    lcd.print(tiempo_actual/1000);
    lcd.print("s ");
      
}  

////////////////////////////////////////// FUNCIONES ////////////////////////////////////////////////////////////////

void Counter_2(){
  if(  digitalRead (pin_encoder_2) && (micros()-debounce_2 > 500) ) { 
// Vuelve a comprobar que el encoder envia una señal buena y luego comprueba que el tiempo es superior a 1000 microsegundos y vuelve a comprobar que la señal es correcta.
        debounce_2 = micros(); // Almacena el tiempo para comprobar que no contamos el rebote que hay en la señal.
        cuentas_ranuras_R2++;
        }  // Suma el pulso bueno que entra.
} 

void Counter_3(){
  if(  digitalRead (pin_encoder_3) && (micros()-debounce_3 > 500) ) { 
// Vuelve a comprobar que el encoder envia una señal buena y luego comprueba que el tiempo es superior a 1000 microsegundos y vuelve a comprobar que la señal es correcta.
        debounce_3 = micros(); // Almacena el tiempo para comprobar que no contamos el rebote que hay en la señal.
        cuentas_ranuras_R3++;
        }  // Suma el pulso bueno que entra.
} 
