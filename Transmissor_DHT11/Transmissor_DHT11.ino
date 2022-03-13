#include "SoftwareSerial.h"
#include "DHT.h"
#define DHTPIN 8
#define DHTTYPE DHT11
SoftwareSerial loraSerial(2,3);
DHT dht(DHTPIN,DHTTYPE); //nome para o sensor
void setup(){
  Serial.begin(9600);
  loraSerial.begin(9600);
  dht.comeco();
  Serial.println("Umidade,Temperatura,Monoxido de Carbono");
}

void loop() {
  int sensorMQ7 = analogRead(A0);
  int umidade = dht.le_umidade();
  int temperatura = dht.ler_Temperatura();
  if (isnan(temperatura) || isnan(umidade)){
    loraSerial.print("Erro na Leitura");
    delay(2000);
  }
  else{
    Serial.println(String(umidade)+","+String(temperatura)+","+String(sensorMQ7));
    loraSerial.print(String(umidade)+","+String(temperatura)+","+String(sensorMQ7));
    delay(2000);
  }
}
