import tbaapiv3client as tba
from tbaapiv3client import ApiException
import json

configuration = tba.Configuration()
configuration.api_key['X-TBA-Auth-Key'] = 'TaaEaU05CN3V89QGeDEKDSPYtfsFTAX0L8aNgAmjSAecJd2GpX4Avj5gQLjKKKls'


district_api = tba.DistrictApi(tba.ApiClient(configuration))
event_api = tba.EventApi(tba.ApiClient(configuration))
district_key = '2019ont'


try:
    event_list = district_api.get_district_events_simple(district_key)
    # print(api_response)

    for event in event_list:
        # x = event.name()
        print(str(event))
        event = str(event).replace('"', "'")
        y = json.loads(str(event))
        print(y["year"])

except ApiException as e:
    print("Exception when calling TBAApi->get_status: %s\n" % e)
