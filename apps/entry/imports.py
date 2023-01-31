import requests
import json
import os


params = dict(
    teamNumber = 4343
)


responce = requests.get(f'https://frc-api.firstinspires.org/v3.0/2020/teams', headers={
    'Authorization': f'Basic dm9ydGV4MTQ4OmFkY2E5ZDI5LTU3YWUtNDJiMi1hMTY3LWZjMDhiMzg2Mzg4OQ=='}, params=params).json()

responce = responce['teams'][0]['nameShort']

print(responce)