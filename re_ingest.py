import configparser
from genericpath import exists
import logging
import csv
from uuid import uuid4
import requests
import json


class Ingestor:
    """An object for absorbing invalid data and re-submitting it to deltaDNA.

    `project_id` is a guid that corresponds to the unity project receiving the data
    `env_name` is the _name_ of the environment (by default 'production')
    """

    def __init__(self, project_id: str, env_name: str = "production"):

        self.url = f"https://collect.analytics.unity3d.com/api/analytics/collect/v1/projects/{project_id}/environments/{env_name}"

        self.success_file = open("success.csv", "a")
        self.source_file = open("missedJson.csv", "a")
        self.logger = logging.getLogger("ingestor")

    def do_the_thing(self, target_file):
        "iterate through the target file submitting each event"
        if not exists(target_file):
            self.logger.error("Target file does not exist, aborting")
            return

        with open(target_file, "r") as file:
            reader = csv.DictReader(file)

            for row in reader:
                json_d = json.loads(row["EVENT_JSON"])
                if "eventParams" not in json_d:
                    json_d = _inflate_json(json_d)
                    json_d["eventUUID"] = str(uuid4())
                    self._send_event(json_d)

    def _send_event(self, json_d):
        "Sends and event and updates the output files"

        writer = csv.writer(self.source_file)
        success_writer = csv.writer(self.success_file)

        try:
            r = requests.post(self.url, json=json_d)
            self.logger.info(f"{json_d['userID']} - {r.status_code}")
            if r.status_code != 204:
                writer.writerow([json_d["userID"]])
            else:
                success_writer.writerow([json_d["userID"]])
        except Exception as err:
            writer.writerow([json_d["userID"]])
            self.logger.error("ERROR %s - %s", json_d["userID"], err)


def _inflate_json(json_d) -> dict:
    new_json = {"eventParams": json_d}
    keys = [
        "eventTimestamp",
        "eventVersion",
        "userID",
        "sessionID",
        "eventName",
        "eventUUID",
        "unityInstallationID",
        "unityPlayerID",
    ]
    for key in keys:
        if key in new_json["eventParams"]:
            value = new_json["eventParams"].pop(key)
            new_json[key] = value

    enriched_keys = [
        "collectInsertedTimestamp",
        "msSinceLastEvent",
        "eventLevel",
        "gaUserAcquisitionChannel",
        "gaUserAgeGroup",
        "gaUserCountry",
        "gaUserGender",
        "gaUserStartDate",
        "eventDate",
        "eventID",
        "mainEventID",
        "timezoneOffset",
    ]

    for key in enriched_keys:
        if key in new_json["eventParams"]:
            new_json["eventParams"].pop(key)

    return new_json


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    cfg_path = "resource/reingest.cfg"
    config = configparser.ConfigParser()
    config.read(filenames=[cfg_path])

    ing = Ingestor(config["DEFAULT"]["project_id"], config["DEFAULT"]["environment_id"])
    ing.do_the_thing(config["DEFAULT"]["target_file"])
