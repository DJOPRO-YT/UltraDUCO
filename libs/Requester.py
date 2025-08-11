import os
from socket import socket
import requests as rq

class Requester:
    def __init__(self,outputting):
        self.socket = socket()
        self.pool_data = None
        self.ip = None
        self.port = None
        self.en_out = outputting
    
    def FastConnection(self):
        rq0 = rq.get("https://server.duinocoin.com/getPool")
        if rq0.ok:
            self.pool_data = rq0.json()
            self.ip = self.pool_data["ip"]
            self.port = self.pool_data["port"]
            self.socket.connect((str(self.ip),int(self.port)))
            self.pool_data["version"] = self.socket.recv(100).decode().replace("\n","")
            if self.en_out:
                print("Connected To Pool :",self.pool_data["name"])
            return True
        return False
    
    def GetPoolData(self):
        if self.pool_data:
            return self.pool_data

    def RequestJOB(self,username,mining_key,dif="LOW"):
        self.socket.send(bytes("JOB,"+ str(username) + "," + dif + "," + str(mining_key),encoding="utf8"))
        if self.en_out:
            print("Job Requested Succcessfully, Waiting for Responce ...")
        job = self.socket.recv(1024).decode().rstrip("\n")
        job = job.split(",")
        if self.en_out:
            print("Got the Responce from the pool !")
        return job

    def ValidationJOBResults(self,result,hashrate,miner_name):
        self.socket.send(bytes(str(result) + "," + str(hashrate) + "," + miner_name,encoding="utf8"))
        if self.en_out:
            print("Requested Validation Result Successfully, Waiting Responce ...")
        r = self.socket.recv(1024).decode().rstrip("\n")
        if self.en_out:
            print("Got the Responce from the pool !")
        return r       
