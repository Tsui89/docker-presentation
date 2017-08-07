#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import requests
import json
import logging
import argparse
import types  

logging.getLogger().setLevel(logging.DEBUG)
logging.debug("debug mode enabled")
OPENTSDB_HTTP_API = os.getenv('OPENTSDB_HTTP_API') or 'localhost:4242'
OPENTSDB_VALUE_TYPE = "long"
url = "http://%s/api/put" % OPENTSDB_HTTP_API
session = requests.Session()


def _opentsdb_line_to_json(line):
    parts = line.split()
    tags = {}
    for tag in parts[4:]:
        key, value = tag.split('=')
        tags[key] = value
    value = parts[3]
    if value.lstrip('-').isdigit():
        if OPENTSDB_VALUE_TYPE == 'long':
            value = long(value)
        return {
            'metric': parts[1],
            'timestamp': int(parts[2]),
            'value': value,
            'tags': tags
        }
    elif "." in value :
        value = float(value)
        return {
                'metric': parts[1],
                'timestamp': int(parts[2]),
                'value': value,
                'tags': tags
        }



def _opentsdb_send(metric):
    try:
        response = session.post(url, data=json.dumps(metric))
        if response.status_code == 204:
            print 'send success'
        else:
            print 'send failed: ' + str(response)
    except requests.exceptions.RequestException as e:
        print 'send failed'
        print e.message


def _test():
    print _opentsdb_line_to_json(
        'put goldwind.kafka.raw_binary.offset.processed 1494988590 591865736 host=pc foo=bar a=b')
    print _opentsdb_line_to_json(
        'put goldwind.kafka.raw_binary.offset.processed 1494988590 591865736 host=pc')
    print _opentsdb_line_to_json(
        'put goldwind.kafka.raw_binary.offset.processed 1494988590 591865736')
    print _opentsdb_line_to_json(
        'put goldwind.kafka.raw_binary.offset.processed 1494988590 haha host=pc')


if __name__ == '__main__':
    while True:
        line = raw_input()
        if not line.startswith("put "):
            print 'error: ',line
            continue
        print line
        json_metric = _opentsdb_line_to_json(line)
        print json.dumps(json_metric)
        _opentsdb_send(json_metric)

