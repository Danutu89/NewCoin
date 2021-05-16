import json
from merkle import MerkleHash
from transaction import Transaction
from Crypto.Hash import SHA256
from time import time


class Block(object):
    __slots__ = [
        "transactions",
        "time",
        "index",
        "prevHash",
        "proofNonce",
        "hashInitial",
        "hash",
        "__hashObj",
        "__dict__",
    ]

    def __init__(self, transactions=[], time=time(), index=0, prevHash="") -> None:
        self.transactions = transactions
        self.time = time
        self.index = index
        self.prevHash = prevHash
        self.proofNonce = 0
        self.hashInitial = 0
        self.hash, self.__hashObj = "", ""

    def calculateHash(self):

        if len(self.transactions) == 1:
            hashTransactions = self.transactions[0].hash

        else:
            hashTransactions = MerkleHash(
                [x.hash for x in self.transactions]
            ).calculate()

        hashString = (
            str(self.time)
            + self.prevHash
            + str(self.index)
            + str(self.proofNonce)
            + hashTransactions
        )
        hashEncoded = json.dumps(hashString, sort_keys=True).encode()
        hashed = SHA256.new(hashEncoded)
        return hashed.hexdigest(), hashed

    def mine(self, difficulty):
        initialHash = "".join([str(self.hashInitial) for x in range(0, difficulty)])

        while self.hash[0:difficulty] != initialHash:
            self.proofNonce += 1
            self.hash, self.__hashObj = self.calculateHash()

        print(f"New block mined: {self.hash}")
        print(f"Nonce: {self.proofNonce}")

    def parseDict(self):
        blockDict = {}
        for attr in filter(lambda a: a.startswith("_") == False, self.__slots__):
            blockDict[attr] = str(self.__getattribute__(attr))

        return blockDict

    @staticmethod
    def importFromDict(obj):
        block = Block()

        for key in obj.keys():
            block.__setattr__(key, obj[key])
            block.transactions = Transaction.importFromDict(obj["transactions"])
            block.hash, block.__hashObj = block.calculateHash()

        return block
