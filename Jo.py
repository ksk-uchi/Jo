#!/usr/bin/python
# -*- coding: utf-8 -*-

from ConfigParser import ConfigParser
import requests
import json
import time


class Jo(object):
    def __init__(self):
        config = ConfigParser()
        config.read("config.ini")
        self.TOKEN = config.get("configuration", "token")
        self.header = {"X-TrackerToken": self.TOKEN}
        self.PROJECT_ID = config.get("configuration", "project_id")
        self.v5_url = "https://www.pivotaltracker.com/services/v5"

    def getTicketsByState(self, state):
        url = ("{0}/projects/{1}/stories"
               "?fields=current_state%2Cstory_type%2Cname"
               "&with_state={2}").format(self.v5_url, self.PROJECT_ID, state)
        r = requests.get(url, headers=self.header)
        return eval(r.text)

    def moveAfterId(self, target_id, after_this):
        header = self.header.copy()
        header.update({"Content-Type": "application/json"})
        payload = {
                "after_id": after_this,
                }
        url = "{0}/projects/{1}/stories/{2}".format(self.v5_url, self.PROJECT_ID, target_id)
        r = requests.put(url, data=json.dumps(payload), headers=header)
        return eval(r.text)

    def makeBunch(self, *args):
        states = {}
        zeros = []
        for arg in args:
            res = jo.getTicketsByState(arg)
            if len(res) > 0:
                states[arg] = res
            else:
                continue
            zeros.append(states[arg][0]["id"])

        for i in range(len(zeros)):
            if i == 0:
                continue
            res = self.moveAfterId(zeros[i], zeros[i-1])

        for state in states:
            for j in range(len(states[state])):
                if j == 0:
                    continue
                self.moveAfterId(states[state][j]["id"], states[state][j-1]["id"])

    def quickSort(self):
        pass

if __name__ == '__main__':
    jo = Jo()
    jo.makeBunch("delivered", "rejected", "finished", "started")
