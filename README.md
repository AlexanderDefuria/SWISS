## Welcome to FRC-Scouting

The web server is hosted from a raspberry pi during competition which creates a PAN network, (Bluetooth network) to allow other devices to connect to the web server. Using a wifi network would be much better but would be a violation of rule C05 of the [FRC Event Rules Manual](https://firstfrc.blob.core.windows.net/frc2019/EventRules/EventRulesManual.pdf), bluetooth setup of this scouting system is not a violation of rule C05 as the wording is specific to WiFi wireless bands and standards. [Community interpretation](https://www.reddit.com/r/FRC/comments/67c7z4/bluetooth_at_competitions/) also supports the legality of using bluetooth networks in the stands.

### Image Installation
To download a prebuilt image visit https://download.swiss-scouting.ca/ and unzip then install the same way as any other raspbian installation. TODO Add thorough instructions here.


### Source Setup Linux
```
git clone https://github.com/AlexanderDefuria/FRC-Scouting.git
sudo apt-get install python3-pandas python3-pip
sudo pip3 install django==2.2 djangoajax==3.2 
```

### Running The Server
Presently there is no configuration for a permemnant server deployment and it must be run in Django's development mode. ``` python3 manage.py runserver 127.0.0.1:80 ``` To have it available from other devices on the local network follow the commands below. Record the ip address produced by ``` ipconfig``` and after running ```sudo python3 manage.py 0.0.0.0:80 ``` navigate to the ip address from the other device.

### Connecting to Bluetooth
To reach the server running off the raspberry pi one must first connect to to the PAN netwrok named raspberrypi by default. The steps to do so are different on each platform. 
<details>
    <summary> Mobile </summary>
    <br>
    <li> 1. Simply connect as per usual with any other bluetooth device. 
    <li> 2. On android one must change the settings of the connection to enable internet access over bluetooth. Connect to 127.20.1.1/entry.
</details>

<details>
    <summary> Windows </summary>
    <br>
    <img src="/docs/Step%202%20-%20Bluetooth%20in%20Windows%20Settings.png" width="32%" height="32%"> <img src="/docs/Step%203%20-%20Add%20A%20Device.png" width="32%" height="32%"> <img src="/docs/Step%204a%20-%20Change%20Adapter%20Settings.png" width="32%" height="32%">
    <img src="/docs/Step%204b%20-%20Network%20Connection%20Control%20Panel.png" width="32%" height="32%"> <img src="/docs/Step%205%20-%20View%20Bluetooth%20Network%20Devices.png" width="32%" height="32%"> <img src="/docs/Step%206%20-%20Connect%20To%20Access%20Point.png" width="32%" height="32%">
</details>

TODO 
from paper to electricity input from paper 
link with picture of a cat


### Viewing Images
Images can be rotated using the [Rotate Image Utility](https://github.com/AlexanderDeFuria/FRC-Scouting/blob/master/rotateImage.py) to correct landscape and portrait modes not being consistent.

### TODOs

 - [ ] Documentation
   - [ ] Explanation of each page/card
   - [ ] Mock scout match
   - [ ] Multiple levels of tutorials? One level will take around 5 minutes, the other 10 minutes, etc. (one of the tutorials can do a whole match scout with you)

BTC Address - 376g5uV5XF7pZGoyfEZnU6zEMLW4L6EHJs

Should add more to readme.
