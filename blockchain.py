import hashlib
import json
from time import time
import matplotlib.pyplot as plt
import networkx as nx

class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.create_block(previous_hash='1', proof=100)  # Genesis block

    def create_block(self, proof, previous_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'entries': self.current_transactions,  # Changed key name to 'entries'
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }
        self.current_transactions = []
        self.chain.append(block)
        return block

    def new_entry(self, person_id, time_entered):
        """
        Creates a new entry representing a person entering the premise
        :param person_id: <str> ID of the person
        :param time_entered: <int> Unix timestamp of when the person entered
        :return: <int> The index of the block that will hold this entry
        """
        self.current_transactions.append({
            'person_id': person_id,
            'time_entered': time_entered,
        })
        return self.last_block['index'] + 1

    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        return self.chain[-1]

    def proof_of_work(self, last_proof):
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

def visualize_blockchain(blockchain:Blockchain):
    G = nx.DiGraph()

    for block in blockchain.chain:
        G.add_node(block['index'], label=f"Block {block['index']}")

    for i in range(1, len(blockchain.chain)):
        G.add_edge(blockchain.chain[i-1]['index'], blockchain.chain[i]['index'])

    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=1000, node_color='skyblue', font_size=12, font_weight='bold', arrows=False)
    plt.title("Blockchain")
    plt.show()

# Example usage:
if __name__ == "__main__":

    # Instantiate the Blockchain
    blockchain = Blockchain()

    # Example entries (people entering the premise)
    blockchain.new_entry(person_id="Alice", time_entered=int(time()))
    blockchain.new_entry(person_id="Bob", time_entered=int(time()))        

    # Mine a new block
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)
    previous_hash = blockchain.hash(last_block)
    block = blockchain.create_block(proof, previous_hash)

    print("Blockchain:", blockchain.chain)

    # Additional test blocks
    for i in range(3):
        # Example entries (people entering the premise)
        blockchain.new_entry(person_id=f"Person_{i+3}", time_entered=int(time()))

        # Mine a new block
        last_block = blockchain.last_block
        last_proof = last_block['proof']
        proof = blockchain.proof_of_work(last_proof)
        previous_hash = blockchain.hash(last_block)
        block = blockchain.create_block(proof, previous_hash)

    print("Blockchain after 2 entries:", blockchain.chain)

    visualize_blockchain(blockchain)
