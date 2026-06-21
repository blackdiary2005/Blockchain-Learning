import datetime

class Blockchain:
    def __init__(self):
        #กลุ่มของบล็อก
        self.chain = [] #ลิสที่เก็บบล็อกทั้งหมด
        self.create_block(nonce=1, previous_hash='0') #สร้างบล็อกแรก
        self.create_block(nonce=2, previous_hash='10') #สร้างบล็อกที่สอง
        self.create_block(nonce=3, previous_hash='20') #สร้างบล็อกที่สาม
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
    
    #ให้บริการข้อมูลของบล็อกล่าสุด
    def get_previous_block(self):
        return self.chain[-1]

#ใช้งาน blockchain
blockchain = Blockchain()
print(blockchain.get_previous_block())