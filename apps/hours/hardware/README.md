## HARDWARE
This is the hardware for the hours app. 

It runs on ESP32-C3 using the PN532 NFC RFID module.

### Plan
1. Tap NFC/RFID tag to PN532
2. Read UUID from card
3. POST UUID to SWISS Hours
4. SWISS returns status (in/out/error) 
5. Display status on integrated RGB LED

### Docs
- [PN532 NXP Datasheet](https://www.nxp.com/docs/en/nxp/data-sheets/PN532_C1.pdf)
- [FOSS PN532 Library](https://warlord0blog.wordpress.com/2021/10/09/esp32-and-nfc-over-i2c)
- [Wiring and Arduino Examples](http://wiki.sunfounder.cc/index.php?title=PN532_NFC_RFID_Module#Test_under_I2C_Mode)
- [Arduino to ESP32C3 Pin Mapping](https://github.com/espressif/arduino-esp32/blob/master/variants/esp32c3/pins_arduino.h)
- [ESP32-C3-DevKit-M1 Docs](https://docs.espressif.com/projects/esp-idf/en/latest/esp32c3/hw-reference/esp32c3/user-guide-devkitm-1.html)

