#include <EasyHTTP.h>

// Network info
char* ssid = "wanderlust807";
char* password = "Its506VFast!";

String baseURL = "https://webhook.site/3fea52c4-898d-4c75-b2cb-15af71922012";

EasyHTTP http(ssid, password);

void setup() {
  Serial.begin(115200);
  http.connectWiFi();
  http.setBaseURL(baseURL);
}

void loop() {
  DynamicJsonDocument doc(32);
  String payload = "";

  doc["sensor"] = "gps";
  serializeJson(doc, payload);

  String response = http.post("/hours/card", "{ \"UUID\" : \"14466e66-b880-4b24-8e9b-e4ed69b38e85\" }");
  Serial.println(response);

  delay(100);
}
