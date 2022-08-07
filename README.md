## Welcome to FRC-Scouting

### Timeline
Updates to 2022 version will be occuring until approximately Mid-November. These updates will be mostly visual.
Mid-November Dev will be purged of all 2022 specfic references and templated to be ready for 2023 game.
Until The start of 2023 most changes will be general and applicable to future versions.
Start of 2023 will freeze and release 2022 Version
Upon the release of the 2023 FRC season begin creating game specific models and forms in dev.

### Raspberry Pi PAN Deployment (Bluetooth Access)

The web server is hosted from a raspberry pi during competition which creates a PAN network, (Bluetooth network) to allow other devices to connect to the web server. Using a wifi network would be much better but would be a violation of rule C05 of the [FRC Event Rules Manual](https://firstfrc.blob.core.windows.net/frc2019/EventRules/EventRulesManual.pdf), bluetooth setup of this scouting system is not a violation of rule C05 as the wording is specific to WiFi wireless bands and standards. [Community interpretation](https://www.reddit.com/r/FRC/comments/67c7z4/bluetooth_at_competitions/) also supports the legality of using bluetooth networks in the stands.

A use tutorial can be found at https://swiss-scouting.ca/entry/tutorial/

#### Installation
Download the appropriate .deb release from the main repository and run ``` sudo apt install ./FRC-Scouting-xxxxx ``` to proceed with a full production ready installation.

#### Source Setup Linux
```
git clone https://github.com/AlexanderDefuria/FRC-Scouting.git
sudo apt-get install $(cat ./debian/dependencies.txt | tr '\n' ' ')
sudo python3 -m venv ./venv
sudo ./venv/bin/pip3 install -r ./requirements.txt
```

#### Running The Server
<details>
<summary> Development </summary>
To run in Django's development mode ``` python3 manage.py runserver ```. To have it available from other devices record the ip address produced by ``` ipconfig ```. After running ``` sudo python3 manage.py 0.0.0.0:80 ``` navigate to the ip address from the other device. Ensure your firewall allows incoming connections over port 80.
</details>
<details>
<summary> Production </summary>
To run in production follow this [guide from Digital Ocean](https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-16-04) to setup basic http access using nginx and gunicorn. 
</details>

#### Connecting to Bluetooth
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
