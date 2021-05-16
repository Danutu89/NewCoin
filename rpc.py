from wallet import Wallet, wallets
from block import Block
from transaction import Transaction
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.client import ServerProxy
from node import get_nodes, add_node
from chain import chain

server = None

PORT = 8301


class RpcServer:
    def __init__(self, server):
        self.server = server

    def ping(self):
        return True

    def get_blockchain(self):
        print("get blockchain")
        return chain.parseDict()

    def new_block(self, block):
        chain.addBlock(Block.parseDict(block))
        print("INFO", "Receive new block.")
        return True

    def get_transactions(self):
        return chain.getTransactions()

    def get_pending_transactions(self):
        array = chain.pendingTransactions
        transactionDict = []

        for item in array:
            transactionDict.append(item.parseDict())

        return transactionDict

    def get_accounts(self):

        walletsDict = wallets.parseDict()
        return walletsDict

    def new_transaction(self, transaction):
        print(transaction)
        chain.addPendingTransaction(Transaction.importOneFromDict(transaction))
        print("INFO", "Receive new unchecked transaction.")
        return True

    def blocked_transactions(self, txs):
        # TransactionDB().write(txs)
        print("INFO", "Receive new blocked transactions.")
        return True

    def add_node(self, address):
        add_node(address)
        return True

    def add_account(self, wallet):

        print("INFO", "Receive new wallet.")
        wallets.addWallet(Wallet.importFromDict(wallet))
        return True


class RpcClient:

    ALLOW_METHOD = [
        "get_transactions",
        "get_blockchain",
        "new_block",
        "new_transaction",
        "blocked_transactions",
        "ping",
        "add_node",
        "get_accounts",
        "get_pending_transactions",
    ]

    def __init__(self, node):
        self.node = node
        self.client = ServerProxy(node)

    def __getattr__(self, name):
        def noname(*args, **kw):
            if name in self.ALLOW_METHOD:
                return getattr(self.client, name)(*args, **kw)

        return noname


class BroadCast:
    def __getattr__(self, name):
        def noname(*args, **kw):
            cs = get_clients()
            rs = []
            for c in cs:
                try:
                    rs.append(getattr(c, name)(*args, **kw))
                except ConnectionRefusedError:
                    print(
                        "WARN",
                        "Contact with node %s failed when calling method %s , please check the node."
                        % (c.node, name),
                    )
                else:
                    print(
                        "INFO",
                        "Contact with node %s successful calling method %s ."
                        % (c.node, name),
                    )
            return rs

        return noname


def start_server(ip, port=8301):
    server = SimpleXMLRPCServer((ip, port))
    rpc = RpcServer(server)
    server.register_instance(rpc)
    server.serve_forever()


def get_clients():
    clients = []
    nodes = get_nodes()

    for node in nodes:
        clients.append(RpcClient(node))
    return clients
