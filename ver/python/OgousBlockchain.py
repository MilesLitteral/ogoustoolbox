import hashlib
import json
import socket
import requests
import urllib.request, json 
from time import time
from urllib.parse import urlparse
from uuid import uuid4
from flask import Flask, jsonify, request, render_template, redirect, Response


class Blockchain(object):
    def __init__(self):
        self.current_transactions = []
        self.chain = []
        self.nodes = set()
        self.users = []

        # Create the genesis block
        self.new_block(previous_hash=1, proof=100)

    def register_node(self, address):
        """
        Add a new node to the list of nodes
        :param address: <str> Address of node. Eg. 'http://192.168.0.5:5000'
        :return: None
        """
        #parsed_url = urlparse(address)
        #self.nodes.add(parsed_url.netloc)
        #address = socket.gethostbyname(socket.gethostname())
        self.nodes.add(address)

    def register_user(self, username, password):
        guess = password.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        self.users.add((username, guess_hash))

    def login(self, username, password):
        if self.users[username] is None:
            return "Error: Please supply a valid username", 400

        guess = password.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()

        if self.users[username] is guess_hash:
            return True
        else:
            return False    


    def auto_register_node(self):
        """
        Add a new node to the list of nodes
        :param address: <str> Address of node. Eg. 'http://192.168.0.5:5000'
        :return: None
        """
        #parsed_url = urlparse(address)
        #self.nodes.add(parsed_url.netloc)
        address = socket.gethostbyname(socket.gethostname())
        self.nodes.add(address)

    def valid_chain(self, chain):
        """
        Determine if a given blockchain is valid
        :param chain: <list> A blockchain
        :return: <bool> True if valid, False if not
        """

        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            print(f('{last_block}'))
            print(f('{block}'))
            print("\n-----------\n")
            # Check that the hash of the block is correct
            if block['previous_hash'] != self.hash(last_block):
                return False

            # Check that the Proof of Work is correct
            if not self.valid_proof(last_block['proof'], block['proof']):
                return False

            last_block = block
            current_index += 1

        return True

    def resolve_conflicts(self):
        """
        This is our consensus algorithm, it resolves conflicts
        by replacing our chain with the longest one in the network.
        :return: <bool> True if our chain was replaced, False if not
        """

        neighbours = self.nodes
        new_chain = None

        # We're only looking for chains longer than ours
        max_length = len(self.chain)

        # Grab and verify the chains from all the nodes in our network
        for node in neighbours:
            response = requests.get(f('http://{node}/chain'))

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                # Check if the length is longer and the chain is valid
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        # Replace our chain if we discovered a new, valid chain longer than ours
        if new_chain:
            self.chain = new_chain
            return True

        return False

    def new_block(self, proof, previous_hash=None):
        """
        Create a new Block in the Blockchain
        :param proof: <int> The proof given by the Proof of Work algorithm
        :param previous_hash: (Optional) <str> Hash of previous Block
        :return: <dict> New Block
        """

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        # Reset the current list of transactions
        self.current_transactions = []

        self.chain.append(block)
        return block

    def get_transaction(self, trans):
        print(self.chain)
        vs = self.chain[1]
        return vs

    def new_transaction(self, sender, recipient, amount):
        """
        Creates a new transaction to go into the next mined Block
        :param sender: <str> Address of the Sender
        :param recipient: <str> Address of the Recipient
        :param amount: <int> Amount
        :return: <int> The index of the Block that will hold this transaction
        """
        sender = socket.gethostbyname(socket.gethostname())
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
            'company': "The Farm"
        })

        return self.last_block['index'] + 1

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def hash(block):
        """
        Creates a SHA-256 hash of a Block
        :param block: <dict> Block
        :return: <str>
        """

        # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self, last_proof):
        """
        Simple Proof of Work Algorithm:
         - Find a number p' such that hash(pp') contains leading 4 zeroes, where p is the previous p'
         - p is the previous proof, and p' is the new proof
        :param last_proof: <int>
        :return: <int>
        """

        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        """
        Validates the Proof
        :param last_proof: <int> Previous Proof
        :param proof: <int> Current Proof
        :return: <bool> True if correct, False if not.
        """

        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"
        
# Instantiate the Node
app = Flask(__name__, static_path='/static')

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()

'''Generic Requests'''
@app.route('/getmethod/<jsdata>', methods=['GET'])
def get_javascript_data(jsdata):
    return jsdata

@app.route('/postmethod/<jsdata>')
def get_post_javascript_data(jsdata):
    jso = {'tool' : jsdata}
    print(jso)
    return jsonify(jso)

@app.route('/receiver', methods = ['POST'])
def worker():
    # read json + reply
    data = request.get_json()
    result = ''

    for item in data:
        # loop over every row
        result += str(item['make']) + '\n'

    print(result) 
    return result


@app.route('/mine/<jsdata>', methods=['GET'])
def mine(jsdata):
    # We run the proof of work algorithm to get the next proof...
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)
    '''reg_node()'''

    # We must receive a reward for finding the proof.
    # The sender is "0" to signify that this node has mined a new coin.
    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1,
    )

    # Forge the new Block by adding it to the chain
    #http://maps.googleapis.com/maps/api/geocode/json?address=google

    block = blockchain.new_block(proof)
    y = str(blockchain.get_transaction(1))
    print("Transaction 1: " +  y)
    jsx = json.loads(jsdata)
    
    print(jsx['tname'])
    if 'ttype' in jsx:
        jso = {'tool' : jsx['tname'],
        'tool_type' : jsx['ttype'],
        'tool_project' : jsx['tproj'],}
    elif 'tproj' in jsx and 'ttype' in jsx is True:
        jso = {'tool' : jsx['tname'],
        'tool_type' : jsx['ttype'],
        'tool_project' : jsx['tproj'],}
    else:
        jso = {'tool' : jsx['tname'],
        'tool_type' : None,
        'tool_project' : None,}

    response = {
        'Tool_name': jso['tool'],
        'Tool_type': jso['tool_type'],
        'Tool_Project': jso['tool_project'],
        'order_index': block['index'],
        'transactions': block['transactions'],
        'block_proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('AGJS.html')

@app.route('/api/register', methods=['POST'])
def APIregister():
    json_data = request.json
    user = User(
        email=json_data['email'],
        password=json_data['password']
    )
    try:
        db.session.add(user)
        db.session.commit()
        status = 'success'
    except:
        status = 'this user is already registered'
    db.session.close()
    return jsonify({'result': status})

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    # Check that the required fields are in the POST'ed data
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400

    # Create a new Transactionblock_string = json.dumps(block, sort_keys=True).encode()
    '''block_string = json.dumps(block, sort_keys=True).encode()
    hashlib.sha256(block_string).hexdigest()'''
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])

    response = {'message': f('Transaction will be added to Block {index}')}
    return jsonify(response), 201


@app.route('/register', methods=['GET'])
def register():
    blockchain.auto_register_node()
    response = {
        'message': 'New node appended to list',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response),200

@app.route('/login', methods=['POST'])
def login():
    values = request.get_json()
    nodes = values.get('nodes')

    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201

#write original contracts
@app.route('/message', methods=['POST'])
def message():
    
    values = request.get_json()

    # We run the proof of work algorithm to get the next proof...
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)
    '''reg_node()'''

    # We must receive a reward for finding the proof.
    # The sender is "0" to signify that this node has mined a new coin.
    blockchain.new_transaction(
        sender=values.get('sender'),
        recipient=values.get('recipient'),
        amount=values.get('amt'),
    )

    # Forge the new Block by adding it to the chain
    block = blockchain.new_block(proof)

    response = {
        'message': values.get('message'),
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200

'''def reg_node():
	with requests.get(socket.gethostbyname(socket.gethostname(), stream=True) as r:
	    blockchain.register_node(r.raw._original_response.fp.raw._sock.getpeername()[0])'''

@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()
    nodes = values.get('nodes')

    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201

@app.route('/nodes/autoregister', methods=['GET'])
def auto_register_nodes():
    blockchain.auto_register_node()

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201


@app.route('/nodes/list', methods=['GET'])
def list_nodes():
	'''for n in nodes:
		print n'''

	response = {
        'message': 'List of all nodes',
        'total_nodes': list(blockchain.nodes),
    }
	return jsonify(response),200

@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain
        }

    return jsonify(response), 200


if __name__ == '__main__':
	#debug host='0.0.0.0'
    #socket.gethostbyname(socket.gethostname())
	app.run(host=socket.gethostbyname(socket.gethostname()), port=500)
