import multiprocessing
import rpc
from chain import chain
from transaction import Transaction


def start_node(hostport="0.0.0.0:3009"):
    init_node()
    print("INFO", "Node initialize success.")
    host = ""
    port = 5000
    try:
        if hostport.find(".") != -1:
            host, port = hostport.split(":")
        else:
            host = "0.0.0.0"
            port = hostport
    except Exception:
        print(
            "ERROR", "params must be {port} or {host}:{port} , ps: 3009 or 0.0.0.0:3009"
        )
    p = multiprocessing.Process(target=rpc.start_server, args=(host, int(port)))
    p.start()
    print("INFO", "Node start success. Listen at %s." % (hostport,))


def init_node():
    from wallet import wallets

    """
    Download blockchain from node compare with local database and select the longest blockchain.
    """
    blockchain = rpc.BroadCast().get_blockchain()
    wallets_extern = rpc.BroadCast().get_accounts()
    pendingTransactions = rpc.BroadCast().get_pending_transactions()

    # If there is a blochain downloaded longer than local database then relace local's.
    for bc in blockchain:
        if len(bc) > len(chain.chain):
            chain.importFromDict(bc)

    for pt in pendingTransactions:
        if len(pt) > len(chain.pendingTransactions):
            chain.pendingTransactions = [Transaction.importOneFromDict(x) for x in pt]

    for wl in wallets_extern:
        if len(wl.keys()) > len(wallets.parseDict().keys()):
            wallets.importFromDict(wl)


def get_nodes():
    return ["http://127.0.0.1:5001", "http://127.0.0.1:5002"]


def add_node(address):
    ndb = None
    # all_nodes = ndb.find_all()
    if address.find("http") != 0:
        address = "http://" + address
    # all_nodes.append(address)
    # ndb.clear()
    # ndb.write(rm_dup(all_nodes))
    return address


def check_node(address):
    pass


def rm_dup(nodes):
    return sorted(set(nodes))


if __name__ == "__main__":
    start_node(3009)
