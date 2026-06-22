import datetime
import json
import hashlib
from flask import Flask, jsonify

class Blockchain:
    def __init__(self):
        #กลุ่มของบล็อก
        self.chain = [] #ลิสที่เก็บบล็อกทั้งหมด
        self.transactions = 0 #จำนวนธุรกรรมที่เกิดขึ้นในบล็อก
        self.create_block(nonce=1, previous_hash='0') #สร้างบล็อกแรก
        # self.create_block(nonce=10, previous_hash='00') #สร้างบล็อกที่สอง
        # self.create_block(nonce=20, previous_hash='000') #สร้างบล็อกที่สาม
    #สร้างบล็อกใหม่และเพิ่มลงใน chain
    def create_block(self, nonce, previous_hash):
        #เก็บส่วนประกอบของบล็อก
        block = {
            "index": len(self.chain) + 1,
            "timestamp":str(datetime.datetime.now()),
            "nonce": nonce,
            "data": self.transactions,
            "previous_hash": previous_hash
        }
        self.chain.append(block)
        return block
    
    #ให้บริการข้อมูลของบล็อกล่าสุด
    def get_previous_block(self):
        return self.chain[-1]
    
    def hash(self, block):
        #เรียงข้อมูลของบล็อกเป็นสตริงและเข้ารหัสด้วย SHA-256
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def proof_of_work(self, previous_nonce):
        new_nonce = 1
        check_proof = False #เช็คว่าหมายเลข nonce ถูกต้องหรือไม่

        #แก้โจทย์ทางคณิตศาสตร์เพื่อหาหมายเลข nonce ที่ถูกต้อง
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_nonce**2 - previous_nonce**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_nonce += 1
        return new_nonce

    #ตรวจสอบความถูกต้องของบล็อก
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index] #block ที่กำลังตรวจสอบ
            if block['previous_hash'] != self.hash(previous_block):
                return False
            
            previous_nonce = previous_block['nonce'] #nonce ของบล็อกก่อนหน้า
            nonce = block['nonce'] # nonce ของบล็อกปัจจุบัน
            hashoperation = hashlib.sha256(str(nonce**2 - previous_nonce**2).encode()).hexdigest()
            if hashoperation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True

#web server
app = Flask(__name__)
blockchain = Blockchain()

#routing
@app.route('/')
def hello():
    return "<h1>Hello, Blockchain!</h1>"

@app.route('/get_chain', methods=['GET'])
def get_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }
    return jsonify(response), 200

@app.route('/mining')
def mining_block():
    amount = 1000000 #จำนวนโทเคนที่ได้จากการขุด
    blockchain.transactions += amount  #เพิ่มจำนวนธุรกรรมในบล็อก
    #pow
    previous_block = blockchain.get_previous_block()
    previous_nonce = previous_block['nonce']
    #nonce
    nonce = blockchain.proof_of_work(previous_nonce)
    #previous hash
    previous_hash = blockchain.hash(previous_block)
    #new block
    block=blockchain.create_block(nonce, previous_hash)
    response = {
        'message': 'Mining successful',
        'data': block['data'],
        'index': block['index'],
        'timestamp' : block['timestamp'],
        'nonce': block['nonce'],
        'previous_hash': block['previous_hash']
    }
    return jsonify(response), 200

@app.route('/is_valid', methods=['GET'])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {'message': 'The blockchain is valid.'}
    else:
        response = {'message': '**The blockchain is not valid.**'}
    return jsonify(response), 200

#run server
if __name__ == '__main__':
    app.run(debug=True)



