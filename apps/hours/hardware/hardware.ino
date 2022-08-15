#include <EasyHTTP.h>
#include <Wire.h>
#include <PN532_I2C.h>
#include <PN532.h>
#include <NfcAdapter.h>


// PN532 I2C
PN532_I2C pn532i2c(Wire);
PN532 nfc(pn532i2c);
volatile bool connected = false;

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
  uint8_t uuid[16]; // Buffer to try and find the uuid (128 bits or 16 octets)

  boolean success = false;

  while (!connected)
    connected = connect();

  if (connected) {
        while (!success) {
            success = readUUID(*uuid);
            if (success) {
                postData(*uuid)
            }
        }

  }
}

bool readUUID(uint8_t data[16]) {
  // Wait for an ISO14443A type cards (Mifare, etc.).  When one is found
  // 'uid' will be populated with the UID, and uidLength will indicate
  // if the uid is 4 bytes (Mifare Classic) or 7 bytes (Mifare Ultralight)

  uint8_t uid[7];
  uint8_t uidLength;                        // UID size (4 or 7 bytes depending on card type) Mifare Classic is 4 bytes
  uint8_t currentblock;                     // Counter to keep track of which block we're on
  bool authenticated = false;               // Flag to indicate if the sector is authenticated
  bool success = false;

  uint8_t keyuniversal[6] = { 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF }; // Keyb on NDEF and Mifare Classic should be the same

  success = nfc.readPassiveTargetID(PN532_MIFARE_ISO14443A, &uid[0], &uidLength);


  // If the card is detected, print the UID
  if (success)
  {
    Serial.println("Card Detected");
    Serial.print("Size of UID: "); Serial.print(uidLength, DEC);
    Serial.println(" bytes");
    Serial.print("UID: ");
    for (uint8_t i = 0; i < uidLength; i++)
    {
      Serial.print(" 0x"); Serial.print(uid[i], HEX);
    }
    Serial.println("");
    Serial.println("");

    if (uidLength != 4) return false;
    if (uidLength == 4) {
      Serial.println("Seems to be a Mifare Classic card (4 byte UID)");

      for (currentblock = 0; currentblock < 64; currentblock++) {  // Try to go through all 16 sectors (each having 4 blocks
        if (nfc.mifareclassic_IsFirstBlock(currentblock)) authenticated = false;  // Check if this is a new block so that we can reauthenticate
        if (!authenticated) {  // If the sector hasn't been authenticated, do so first
          // Starting of a new sector ... try to to authenticate
          Serial.print("------------------------Sector ");
          Serial.print(currentblock/4, DEC);
          Serial.println("-------------------------");
          if (currentblock == 0) {
              // This will be 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF for Mifare Classic (non-NDEF!)
              // or 0xA0 0xA1 0xA2 0xA3 0xA4 0xA5 for NDEF formatted cards using key a,
              // but keyb should be the same for both (0xFF 0xFF 0xFF 0xFF 0xFF 0xFF)
              success = nfc.mifareclassic_AuthenticateBlock (uid, uidLength, currentblock, 1, keyuniversal);
          } else {
              // This will be 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF for Mifare Classic (non-NDEF!)
              // or 0xD3 0xF7 0xD3 0xF7 0xD3 0xF7 for NDEF formatted cards using key a,
              // but keyb should be the same for both (0xFF 0xFF 0xFF 0xFF 0xFF 0xFF)
              success = nfc.mifareclassic_AuthenticateBlock (uid, uidLength, currentblock, 1, keyuniversal);
          }

          if (success) {
            authenticated = true;
          } else {
            Serial.println("Authentication error");
          }
        }

        if (authenticated) { // Dump the data into the 'data' array
          success = nfc.mifareclassic_ReadDataBlock(currentblock, data);
          if (success) {
            // Read successful
            Serial.print("Block ");Serial.print(currentblock, DEC);
            if (currentblock < 10) {
              Serial.print("  ");
            } else {
              Serial.print(" ");
            }
            // Dump the raw data
            nfc.PrintHexChar(data, 16);
          } else {
            // Oops ... something happened
            Serial.print("Block ");Serial.print(currentblock, DEC);
            Serial.println(" unable to read this block");
          }
        }
      }
    }
    connected = connect();
  } else {
    // PN532 probably timed out waiting for a card
    Serial.println("Timed out waiting for a card");
  }

  return false;
}


bool connect() {
    nfc.begin();
    // Connected, show version
    uint32_t versiondata = nfc.getFirmwareVersion();
    if (! versiondata) {
        Serial.println("PN53x card not found!");
        return false;
    }

    //port
    Serial.print("Found chip PN5"); Serial.println((versiondata >> 24) & 0xFF, HEX);
    Serial.print("Firmware version: "); Serial.print((versiondata >> 16) & 0xFF, DEC);
    Serial.print('.'); Serial.println((versiondata >> 8) & 0xFF, DEC);

    // Set the max number of retry attempts to read from a card
    // This prevents us from waiting forever for a card, which is
    // the default behaviour of the PN532.
    // I think we want to wait forever tbh.
    // nfc.setPassiveActivationRetries(0xFF);

    // configure board to read RFID tags
    nfc.SAMConfig();

    Serial.println("Waiting for card (ISO14443A Mifare)...");
    Serial.println("");

    return true;
}

void postData(uint8_t data[]) {
    DynamicJsonDocument doc(32);
    String payload = "";

    doc["UUID"] = "";
    for (int i = 0; i < 16; i++) {
        doc["UUID"] = doc["UUID"] + i.str()
    }

    serializeJson(doc, payload);

    String response = http.post("/hours/card", "{ \"UUID\" : \"14466e66-b880-4b24-8e9b-e4ed69b38e85\" }");
    Serial.println(response);
}
