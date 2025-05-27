#include <WiFi.h>
#include <HTTPClient.h>
#include <ESP32Servo.h>
#include "secrets.h"

Servo servo;
int sensor = 36; // módulo de chuva
const int LDR = 33; // LDR
int ang = 0;

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  Serial.print("Conectando ao Wi-Fi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("Conectado!");
  servo.attach(18);
}

void loop() {
  int valor_luz = analogRead(LDR);
  int valor = analogRead(sensor);
  servo.write(ang);

  String estado_luz = valor_luz > 2000 ? "claro" : "escuro";

  if(valor > 3000){
    Serial.println("Seco");
    while(ang>0)
    {
      ang--;
      servo.write(ang);
      delay(15);
    }

  }
  else{
    Serial.println("Chuva");
    while(ang<110)
    {
      ang++;
      servo.write(ang);
      delay(15);
    }

  }

  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverName);
    http.addHeader("Content-Type", "application/json");

    String json = "{";
    json += "\"valor_chuva\":" + String(valor) + ",";
    json += "\"valor_luz\":" + String(valor_luz);
    json += "}";

    int httpResponseCode = http.POST(json);
    if (httpResponseCode > 0) {
      Serial.print("POST enviado, código: ");
      Serial.println(httpResponseCode);
    } else {
      Serial.print("Erro no POST: ");
      Serial.println(http.errorToString(httpResponseCode).c_str());
    }
    http.end();
  }

  delay(5000); // envia a cada 5 segundos
}
