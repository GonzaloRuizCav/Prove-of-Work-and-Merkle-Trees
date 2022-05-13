from typing import Optional, List
import hashlib,sys
import random
import hashlib
import numpy as np

def verify(obj: str, proof: str, commitment: str) -> bool:
    proof_list = proof.split(',')
    if proof_list[-1] == commitment and proof_list[0] == obj:
        return True
    else:
        return False

class Prover:
    def __init__(self):
        pass
    
    def SHA(s):
        return hashlib.sha256(s.encode()).hexdigest()
    
    def GetTree(self):
        return self.tree

	# Build a merkle tree and return the commitment
    def build_merkle_tree(self, objects: List[str]) -> str:
        if objects == None:
            return None
        else:
            Num_Of_Objects = int(2**np.ceil(np.log2(len(objects))))
            while len(objects) < Num_Of_Objects:
                objects.append("%")
            Tree = {}
            for i in range(len(objects) * 2 - 1, 0, -1):
                if i >= len(objects):
                    Tree[i] = Prover.SHA(objects[i - len(objects)])
                else:
                    # We calculate the hash of the parent node by the sum of the child nodes
                    IndexLeft = i * 2
                    IndexRight = i * 2 + 1
                    # Retrieve the hashes from Tree
                    Tree[i] = Prover.SHA(Tree[IndexLeft] + Tree[IndexRight])
            # Build the commitment
            commitment = Tree[1]
            self.tree = Tree
            self.objects = objects
            return commitment
            
    def get_leaf(self, index: int) -> Optional[str]:
        objects = self.objects       
        # The index is a leaf if its less than the length of the objects
        if index < len(objects) and self.objects[index] != '%':
            return self.objects[index]
        else:
            return None

            
    def generate_proof(self, index: int) -> Optional[str]:
        if self.get_leaf(index) == None:
            return None
        else:
            index_dict = len(self.tree) - index
            path = []
            # path.append(self.objects[index])
            while index_dict >= 1:
                path.append(self.tree[index_dict])
                if index_dict % 2 == 0:
                    index_dict = index_dict / 2
                else:
                    index_dict = (index_dict - 1) / 2
            
            return self.get_leaf(index) + "," + ",".join([str(item) for item in path])

                
objects = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
Tree = Prover()
commitment = Tree.build_merkle_tree(objects)
proof = Tree.generate_proof(1)
print(verify('b',proof, commitment))