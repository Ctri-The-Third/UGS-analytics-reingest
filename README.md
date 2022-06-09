


[![PyTest](https://github.com/Ctri-The-Third/PythonTemplate/actions/workflows/main.yml/badge.svg)](https://github.com/Ctri-The-Third/PythonTemplate/actions/workflows/main.yml)

# Executive Summary

A tool for automatically re-submitting small numbers of events to the Unity Gaming Services - Analytics platform, using the Rest API documented [here](https://docs.unity.com/analytics/AnalyticsRestAPI.html)

- [Overview](#Overview)
- [Deployment](#Deploy)


# Overview

Takes a CSV with a column header "EVENT_JSON".  
The script assumes that each row in the column is the invalid event as recorded in the event browser, or exported via Data Access.



# Deployment

Ensure that `resource/reingest.cfg` file is populated, refer to the template for reference.

Just install the requirements and run the re_ingest.py script.