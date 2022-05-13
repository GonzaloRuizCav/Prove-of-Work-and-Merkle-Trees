# -*- coding: utf-8 -*-
import random
import hashlib
import time
import string

def GenerateWatermark():
    netID = "gr334"
    netID = netID.encode(encoding = 'ASCII')
    hashed_netID = hashlib.sha256(netID).hexdigest()
    hashed = bin(int(hashed_netID, 16))
    w = hashed[:10]
    w = w.replace('b', '0', 1)
    return w

def SHA(s: string) -> string:
    return hashlib.sha256(s.encode()).hexdigest()

def GenerateATry(w):
    C = list(bin(random.getrandbits(64)))[2:]
    while len(C) < 64:
        C.append('0')
    C = "".join(C)
    Final = w + C[:54]
    return Final

def GenerateACoin(w):
    C = list(bin(random.getrandbits(64)))[2:]
    while len(C) < 64:
        C.append('0')
    C = "".join(C)
    prov = w + C[:54]
    provisional = hex(int(prov,2))
    prov_hashed = hashlib.sha256(bytes.fromhex(provisional.lstrip("0x"))).hexdigest()
    prov_bin = bin(int(prov_hashed,16))
    return prov_bin[2:30], provisional.lstrip("0x")

def TestCoin(Coins):
    hashes = []
    for coin in Coins:
        prov_hashed = hashlib.sha256(bytes.fromhex(coin.lstrip("0x"))).hexdigest()
        prov_bin = bin(int(prov_hashed,16))[2:]
        hashes.append(prov_bin)
    element = hashes[0]
    AreEqual = True
    for h in hashes:
        if h[:28] != element[:28]:
            AreEqual = False
    if AreEqual:
        return True
    else:
        return False
        

StartTime = time.time()
n = 28
w = GenerateWatermark()
Dictionary = {}
# Generate the other collisions with c
k = 4

while True:
    Try, coin = GenerateACoin(w)
    if Try not in Dictionary.keys():
        Dictionary[Try] = [coin]
    else:
        Dictionary[Try].append(coin)
        if len(Dictionary[Try]) == 4:
            FinalCoins = Dictionary[Try]
            break

f = open('coin.txt', 'w')
for i in FinalCoins:
    f.write(i)
    f.write("\n")
f.close()

EndingTime = time.time() - StartTime
print("The time to generate a coin is: " + str(EndingTime))
print(TestCoin(FinalCoins))