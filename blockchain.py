import datetime

class Blockchain:
    def __init__(self):
        #กลุ่มของบล็อก
        self.chain = [] #ลิสที่เก็บบล็อกทั้งหมด
        self.create_block(nonce=1, previous_hash='0') #สร้างบล็อกแรก

    #สร้างบล็อกใหม่และเพิ่มลงใน chain
    def create_block(self, nonce, previous_hash):
        #เก็บส่วนประกอบของบล็อก
        block = {
            "index": len(self.chain) + 1,
            "timestamp":str(datetime.datetime.now()),
            "nonce": nonce,
            "previous_hash": previous_hash
        }
        self.chain.append(block)
        return block

#ใช้งาน blockchain
blockchain = Blockchain()
print(blockchain.chain)