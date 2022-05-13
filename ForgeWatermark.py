# -*- coding: utf-8 -*-
import random
import hashlib
import time
import string

def SHA(s: string) -> string:
    return hashlib.sha256(s.encode()).hexdigest()

def GenerateRandomWatermark():
    num_of_Letters = random.randint(2,3)
    num_of_Numbers = random.randint(1,10)
    nid = ""
    for j in range(num_of_Letters):
        nid = nid + random.choice(string.ascii_lowercase)
    for i in range(num_of_Numbers):
        nid = nid + str(random.randint(0,9))
    hashed_nid = hashed_nid.encode(encoding = 'ASCII')
    hashed_nid = SHA(nid)
    hashed = (bin(int(hashed_nid, 16))[2:]).zfill(256)
    w = hashed[:10]
    return w, nid

def GenerateWatermark():
    netID = "gr334"
    hashed_netID = SHA(netID)
    hashed = bin(int(hashed_netID, 16))
    w = hashed[:10]
    w = w.replace('b', '0', 1)
    return w


f = open('coin.txt', 'r')
Lines = f.readlines()
collisions = 0
while True:
    w, nid = GenerateRandomWatermark()
    Original = GenerateWatermark()
    if w == Original:
        Final_Watermark = nid
        break

f1 = open('forged_watermark.txt', 'w')
f1.write(nid)
f.close()
f1.close()