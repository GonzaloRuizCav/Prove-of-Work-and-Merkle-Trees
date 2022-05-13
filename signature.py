import string
import random
import hashlib
import numpy as np
import time
from essential_generators import DocumentGenerator

# return the hash of a string
def SHA(s: string) -> string:
    return hashlib.sha256(s.encode()).hexdigest()

# transfer a hex string to integer
def toDigit(s: string) -> int:
    return int(s, 16)

# generate 2^d (si^{-1}, si) pairs based on seed r
def KeyPairGen(d: int, r: int) -> dict:
    pairs = {}
    random.seed(r)
    for i in range(1 << d):
        cur = random.randbytes(32).hex()
        while cur in pairs:
            cur = random.randbytes(32).hex()
        pairs[cur] = SHA(cur)
    return pairs

# Find the previous power of 2 of a number
def findPreviousPowerOf2(n):
    while (n & n - 1):
        n = n & n - 1
    return n


class MTSignature:
    def __init__(self, d, k):
        self.d = d
        self.k = k
        self.treenodes = [None] * (d+1)
        for i in range(d+1):
            self.treenodes[i] = [None] * (1 << i)
        self.sk = [None] * (1 << d)
        self.pk = None # same as self.treenodes[0][0]
        self.tree = None

    # Populate the fields self.treenodes, self.sk and self.pk. Returns self.pk.
    def KeyGen(self, seed: int) -> string:
        KeyPairs = KeyPairGen(self.d, seed)
        Leafs = list(KeyPairs.values())
        PreImages = list(KeyPairs.keys())
        if Leafs == None:
            return None
        else:
            self.sk = PreImages
            Tree = {}
            for i in range(len(Leafs) * 2 - 1, 0, -1):
                if i >= len(Leafs):
                    Tree[i] = Leafs[i - len(Leafs)]
                else:
                    # We calculate the hash of the parent node by the sum of the child nodes
                    IndexLeft = i * 2
                    IndexRight = i * 2 + 1
                    # Now we calculate the local index
                    # We find the previous power of 2 of a number. E.g, 15 will be output as 8
                    PowerOf2 = findPreviousPowerOf2(i)
                    # Then we substract that number - 1 to our indexes. This is equal to the number of elements any element
                    # Has in the levels above them
                    localIndex = i - PowerOf2
                    # Convert the localIndex to a 256 bit number
                    local_bin = '{:0256b}'.format(localIndex)
                    # Retrieve the hashes from Tree
                    Tree[i] = SHA(local_bin + Tree[IndexLeft] + Tree[IndexRight])
                # Populate self.TreeNodes
                Previous = findPreviousPowerOf2(i)
                localIndex = i - Previous
                depth = int(np.log2(Previous))
                self.treenodes[depth][localIndex] = Tree[i]
                # Need to implement it
            # Build the commitment
            self.tree = Tree
            self.pk = self.treenodes[0][0]
        return self.treenodes[0][0]

    # Returns the signature. The format of the signature is as follows: ([sigma], [SP]).
    # The first is a sequence of sigma values and the second is a list of sibling paths.
    # Each sibling path is in turn a d-length list of tree node values. 
    # All values are 64 bytes. Final signature is a single string obtained by concatentating all values.
    def Sign(self, msg: string) -> string:
        sigma = ""
        Paths = ""
        # Compute z_j
        for j in range(1, self.k + 1):
            # Endian_Number = j.to_bytes(256, "big")
            Endian_Number = (bin(j)[2:]).zfill(256)
            To_Be_Hashed = str(Endian_Number) + msg
            z_value = int(SHA(To_Be_Hashed),16)%(2**self.d)
            sigma_value = self.sk[z_value]
            # Compute the sigma_j values
            sigma = sigma + sigma_value
            # Compute the path from leaf z_j to the root
            Path = []
            Current_Depth = self.d
            while Current_Depth >= 0:
                if z_value % 2 == 0 and Current_Depth > 0:
                    SiblingNode = self.treenodes[Current_Depth][z_value + 1]
                    z_value = z_value // 2
                    Path.append(SiblingNode)
                elif z_value % 2 == 1 and Current_Depth > 0:
                    SiblingNode = self.treenodes[Current_Depth][z_value - 1]
                    z_value = (z_value - 1) // 2
                    Path.append(SiblingNode)
                Current_Depth -= 1
            Path_To_Append = "".join(Path)
            Paths = Paths + Path_To_Append
        sig = sigma + Paths
        return sig
    
    # Part 3.2: Forgery

    # Call this function to generate a random forged message. Estimated time: 15 seconds
    def ForgeSignature(self, m):
        signature = self.Sign(m)
        Collision = False
        gen = DocumentGenerator()
        while Collision == False:
            N = random.randint(0,20)
            # Generate random word
            Attempt = ''.join(random.choice(string.ascii_lowercase) for i in range(N))
            # Generate random gramatically correct sentence
            signature2 = self.Sign(Attempt)
            # Check for collisions and gramatical correctness
            if signature[0 : self.k * 64] == signature2[0 : self.k * 64]:
                Collision = True
                FinalMessage = Attempt
                print(self.Sign(m) == self.Sign(Attempt))
        f = open('forgery.txt', 'w')
        f.write(m)
        f.write("\n")
        f.write(Attempt)
        f.close()
        return signature
    
    # Call this function to generate a forged message that is also gramatically correct. Estimated time: 50 seconds
    def ForgeSignatureGramaticallyCorrect(self, m):
        signature = self.Sign(m)
        Collision = False
        gen = DocumentGenerator()
        while Collision == False:
            # Generate random gramatically correct sentence
            Attempt = gen.sentence()
            signature2 = self.Sign(Attempt)
            # Check for collisions and gramatical correctness
            if signature[0 : self.k * 64] == signature2[0 : self.k * 64]:
                Collision = True
                FinalMessage = Attempt
                print(self.Sign(m) == self.Sign(Attempt))
        f = open('forgery.txt', 'w')
        f.write(m)
        f.write("\n")
        f.write(Attempt)
        f.close()
        return signature
    
# Testing part, remove if necessary

# Code for part 3.1
S1 = MTSignature(2, 1)
S1.KeyGen(1)
sig = S1.Sign("I Love 5433")

# Code for part 3.2
r = 2022
S2 = MTSignature(10, 2)
S2.KeyGen(r)
Time = time.time()
S2.ForgeSignatureGramaticallyCorrect("I love to forge signatures")
EndingTime = time.time()
print("Time required to forge the message is: " + str(EndingTime - Time) + " seconds.")

