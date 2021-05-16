from wallet import wallets
from block import Block
from transaction import Transaction
from time import time
from datetime import datetime
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256


class Chain(object):
    __slots__ = [
        "chain",
        "pendingTransactions",
        "mineDifficulty",
        "mineReward",
        "blockSize",
        "blockValidity",
    ]

    def __init__(self) -> None:
        self.chain = [self.addGenesisBlock()]
        self.pendingTransactions = []
        self.mineDifficulty = 4
        self.mineReward = 50
        self.blockSize = 4
        self.blockValidity = 1

    @property
    def isValid(self):
        for i in range(2, len(self.chain)):

            currentBlock = self.chain[i]
            prevBlock = self.chain[i - 1]

            if currentBlock.prevHash != prevBlock.hash:
                print("Chain not valid.")
                return False

            if currentBlock.hashInitial != prevBlock.hashInitial:
                print("Chain not valid.")
                return False

            # hashOperation = SHA256.new(
            #     str(
            #         int(currentBlock.proofNonce) ** 2 - int(prevBlock.proofNonce) ** 2
            #     ).encode()
            # ).hexdigest()

            # if hashOperation[: int(self.mineDifficulty)] != str(
            #     int(currentBlock.hashInitial) * int(self.mineDifficulty)
            # ):
            #     print("Chain not valid.")
            #     return False

            newPrevBlockHash, newPrevBlockHashObj = prevBlock.calculateHash()

            if newPrevBlockHash != currentBlock.prevHash:
                print("Chain not valid.")
                return False

            prevBlock.hash, prevBlock.__hashObj = newPrevBlockHash, newPrevBlockHashObj

        return True

    def getPrevBlock(self):
        return self.chain[-1]

    def addBlock(self, block):
        if len(self.chain) == 0:
            block.prevHash = "none"
        else:
            block.prevHash = self.getPrevBlock().hash

        self.chain.append(block)

    def addPendingTransaction(self, transaction):
        self.pendingTransactions.append(transaction)

    def completePendingTransactions(self, start, end):
        for t in self.pendingTransactions:
            t.completeTranfer()
        self.pendingTransactions = (
            self.pendingTransactions[:start] + self.pendingTransactions[end:]
        )

    def mine(self, miner):
        lengthPending = len(self.pendingTransactions)

        if lengthPending < self.blockSize:
            print("Can`t mine without transactions.")
            return

        endSlice = self.blockSize

        if endSlice > lengthPending:
            endSlice = lengthPending - 1

        transactions = self.pendingTransactions[0 : self.blockSize]
        transactionsTemp = transactions

        for index, t in enumerate(transactionsTemp):
            if t.isValid == False:
                transactions.__delitem__(index)

        prevHash = self.getPrevBlock().hash

        newBlock = Block(transactions, time(), len(self.chain), prevHash)

        newBlock.mine(self.mineDifficulty)

        self.addBlock(newBlock)
        self.completePendingTransactions(0, self.blockSize)
        print(f"Mined transactions: {[x.hash for x in transactions]}")

        newTransaction = Transaction("Mine Reward", miner, self.mineReward)
        self.addPendingTransaction(newTransaction)

    def addTransaction(self, sender, receiver, amount, passphrase):
        senderWallet = None
        receiverWallet = None

        try:
            senderWallet = wallets.getWallet(sender)
        except:
            print("No sender wallet found.")
            return

        try:
            receiverWallet = wallets.getWallet(receiver)
        except:
            print("No receiver wallet found.")
            return

        if senderWallet.balance < int(amount):
            print("Insufficient funds.")
            return

        try:
            senderKey = RSA.import_key(senderWallet.privateKey, passphrase)
        except:
            print("Invalid passphrase")
            return

        if not sender or not receiver or not amount:
            print("No arguments")
            return

        transaction = Transaction(sender, receiver, amount)

        transaction.signTransaction(senderKey)

        if not transaction.isValid:
            print("Transaction not valid")
            return

        self.addPendingTransaction(transaction)
        return transaction

    def parseDict(self):
        chainJson = []

        for block in self.chain:
            blockDict = block.parseDict()
            transactionsJson = []
            for transaction in block.transactions:
                transactionsJson.append(transaction.parseDict().copy())

            blockDict["transactions"] = transactionsJson

            chainJson.append(blockDict)

        return chainJson

    def importFromDict(self, array):
        parsedArray = []

        for item in array:
            block = Block.importFromDict(item)
            parsedArray.append(block)

        checkChain = Chain()
        checkChain.chain = parsedArray

        if checkChain.isValid == True:
            self.chain = parsedArray

    def addGenesisBlock(self) -> Block:
        return Block(
            [Transaction("me", "you", 10)],
            datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
            0,
            "none",
        )

    def getTransactions(self):
        transactions = []

        for block in self.chain:
            transactions.extend(block.transactions.parseDict())

        return transactions


chain = Chain()
