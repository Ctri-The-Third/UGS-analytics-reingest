import configparser
from genericpath import exists
import logging
import csv
from uuid import uuid1
import requests
import json


class Ingestor():
    "An object for absorbing invalid data and re-submitting it to deltaDNA"
    def __init__(self, project_id,env_name):
        self.url = f"https://collect.analytics.unity3d.com/api/analytics/collect/v1/projects/{project_id}/environments/{env_name}"


        self.success_file = open('success.csv', 'a')
        self.source_file = open('missedJson.csv', 'a')
        self.logger = logging.getLogger("ingestor")
    

    def do_the_thing(self,target_file):
        "iterate through the target file submitting each event"
        if not exists(target_file):
            self.logger.error("Target file does not exist, aborting")
            return 
    
        with open (target_file, 'r') as file:
            reader = csv.DictReader(file)
 
            
            for row in reader:
                json_d = json.loads(row["EVENT_JSON"])
                if "eventParams" not in json_d:
                    json_d = _inflate_json(json_d)
                    json_d["event_uuid"] = uuid1()
                    self._send_event(json_d)



    def _send_event(self,json_d):
        "Sends and event and updates the output files"

        writer = csv.writer(self.source_file)
        success_writer = csv.writer(self.success_file)

        try:
            r = requests.post(self.url, json = json_d)
            self.logger (f"{json_d['userID']} - {r.status_code}")
            if r.status_code != 204:
                writer.writerow([json_d['userID']])
            else:
                success_writer.writerow([json_d['userID']])
        except Exception as err:
            writer.writerow([json_d['userID']])
            self.logger.error("ERROR %s - %s",json_d['USERID'],err)


def _inflate_json(json_d) -> dict:
    new_json = {"eventParams" : json_d} 
    keys = ["eventTimestamp","eventVersion","userID","sessionID","eventName","eventUUID"]
    for key in keys:
        if key in new_json["eventParams"]:
            value = new_json["eventParams"].pop(key)
            new_json[key] = value
                
    return new_json        


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    config = 
    ugs_project_id = ""
    env_name = ''
    tar_file = r""

    ing = Ingestor(ugs_project_id, env_name)
    ing.do_the_thing(tar_file)
