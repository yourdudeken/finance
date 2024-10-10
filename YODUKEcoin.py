import hashlib
import json
from time import time
from uuid import uuid4
from flask import Flask, jsonify, request


class Block:
    def __init__(self, index, timestamp, transactions, previous_hash, nonce=0):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = nonce

    def compute_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()


class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        self.create_block(previous_hash='1', nonce=100)

    def create_block(self, nonce, previous_hash=None):
        block = Block(
            index=len(self.chain) + 1,
            timestamp=time(),
            transactions=self.current_transactions,
            previous_hash=previous_hash or self.last_block.compute_hash(),
            nonce=nonce,
        )
        self.current_transactions = []
        self.chain.append(block)
        return block

    def get_last_block(self):
        return self.chain[-1]

    def add_transaction(self, sender, recipient, amount):
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })
        return self.get_last_block().index + 1

    def proof_of_work(self, last_proof):
        nonce = 0
        while not self.valid_proof(last_proof, nonce):
            nonce += 1
        return nonce

    def valid_proof(self, last_proof, nonce):
        guess = f'{last_proof}{nonce}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    def is_chain_valid(self):
        for index in range(1, len(self.chain)):
            previous_block = self.chain[index - 1]
            current_block = self.chain[index]

            if current_block.previous_hash != previous_block.compute_hash():
                return False

            if not self.valid_proof(previous_block.nonce, current_block.nonce):
                return False

        return True

def create_wallet():
    return str(uuid4()).replace('-', '')

app = Flask(__name__)

blockchain = Blockchain()

node_identifier = create_wallet()


@app.route('/mine', methods=['GET'])
def mine():
    last_block = blockchain.get_last_block()
    last_proof = last_block.nonce

    nonce = blockchain.proof_of_work(last_proof)

    blockchain.add_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1,
    )

    previous_hash = last_block.compute_hash()
    block = blockchain.create_block(nonce, previous_hash)

    response = {
        'message': 'New block forged',
        'index': block.index,
        'transactions': block.transactions,
        'nonce': block.nonce,
        'previous_hash': block.previous_hash,
    }
    return jsonify(response), 200


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400


    index = blockchain.add_transaction(
        values['sender'],
        values['recipient'],
        values['amount'],
    )

    response = {'message': f'Transaction will be added to block {index}'}
    return jsonify(response), 201


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': [block.__dict__ for block in blockchain.chain],
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200


@app.route('/chain/valid', methods=['GET'])
def is_chain_valid():
    is_valid = blockchain.is_chain_valid()
    return jsonify({'valid': is_valid}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
