## Welcome to FRC-Scouting

The web server is hosted from a raspberry pi during competition which creates a PAN network, (Bluetooth network) to allow other devices to connect to the web server. Using a wifi network would be much better but would be a violation of rule C05 of the [FRC Event Rules Manual](https://firstfrc.blob.core.windows.net/frc2019/EventRules/EventRulesManual.pdf), bluetooth setup of this scouting system is not a violation of rule C05 as the wording is specific to WiFi wireless bands and standards. [Community interpretation](https://www.reddit.com/r/FRC/comments/67c7z4/bluetooth_at_competitions/) also supports the legality of using bluetooth networks in the stands.


### Installation
```
git clone https://github.com/AlexanderDefuria/FRC-Scouting.git
sudo apt-get install python3-pandas python3-pip
sudo pip3 install django==2.2 djangoajax==3.2 
```

### Image Installation


### Connecting to Bluetooth
To reach the server running off the raspberry pi one must first connect to to the PAN netwrok named raspberrypi by default. The steps to do so are different on each platform. 
#### Mobile
Simply connect as per usual with any other bluetooth device. On android one must change the settings of the connection to enable internet     access over bluetooth. Connect to 127.20.1.1/entry.
#### Windows & Linux
TODO

TODO 
from paper to electricity input from paper 
link with picture of a cat

