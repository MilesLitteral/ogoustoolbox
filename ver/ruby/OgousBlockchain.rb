require 'hashlib'
require 'json'
require 'requests'
require 'net/http'

#Ogous Functionality
class Blockchain()
	@current_transactions = []
	@chain = []
	@nodes = []
	@users = []

	def initialize(self)
        self.current_transactions = []
        self.chain = []
        self.nodes = set()
        self.users = []
        self.new_block(1,100)
	end
		
	def register_node(self, addr)
		self.nodes.push(addr)
	end

	def register_user(self, username, password)
		#TBA
	end

    def auto_register_user(self)
        self.nodes.push(address)
    end

    def valid_chain(self, chain)
        last_block = chain[0]
        current_index = 1

        while current_index < len(chain)
            block = chain[current_index]
            print(f('{last_block}'))
            print(f('{block}'))
            print("\n-----------\n")
            # Check that the hash of the block is correct
            if block['previous_hash'] != self.hash(last_block):
                return False
            end

            # Check that the Proof of Work is correct
            if not self.valid_proof(last_block['proof'], block['proof']):
                return False
            end
            last_block = block
            current_index += 1
        end

        return True
    end

    def resolve_conflicts(self)
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
                end
            end
        end

        # Replace our chain if we discovered a new, valid chain longer than ours
        if new_chain:
            self.chain = new_chain
            return True
        end
        return False
    end

    def new_block(self, proof, previous_hash=nil)

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
    end

    def get_transaction(self, trans)
        print(self.chain)
        vs = self.chain[1]
        return vs
    end

    def new_transaction(self, sender, recipient, amount)

        sender = socket.gethostbyname(socket.gethostname())
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
            'company': "The Farm"
        })

        return self.last_block['index'] + 1
    end

    @property
    def last_block(self)
        return self.chain[-1]
    end

    @staticmethod
    def hash(block)
        # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()
    end

    def proof_of_work(self, last_proof)

        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        end
        return proof
    end

    @staticmethod
    def valid_proof(last_proof, proof)
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"
    end
end

#Define Rails Functionality here
#app.start()