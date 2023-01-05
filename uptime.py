#!/usr/bin/env python3

import json
import subprocess

from flup.server.fcgi_fork import WSGIServer

def getUptime():
    machines = []
    result = []  # create an empty list to store the dictionaries

    output = subprocess.run(['ruptime','&&','rsh noc2.lab.praetor.tel ruptime'],stdout=subprocess.PIPE)
    output = output.stdout.decode()
    output = output.split("\n")

    for x in output:
        machines = x.split()
        if machines:
            machines_dict = {"name": machines[0], "status": machines[1]}
            result.append(machines_dict)  # append the dictionary to the result list

    return(result)  # return the result list

def main(environ,start_response):
    start_response('200 OK', [('Content-Type', 'application/json')])
    uptime = getUptime()
    status = json.dumps(uptime)
   
    return(status)

if __name__ == "__main__":
    WSGIServer(main, bindAddress=('127.0.0.1',9000)).run()
