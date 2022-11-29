"""File defining the entrypoint to this blockchain module."""
import json
import blockchain.simple_blockchain
import blockchain.structures as struct


def main():
    my_blockchain = blockchain.simple_blockchain.SimpleBlockchain()
    transactions = my_blockchain.make_transactions_buffer()
    my_blockchain.process_transactions_buffer(transactions)
    transactions = my_blockchain.make_transactions_buffer(5)
    incoming_chain = [my_blockchain.make_block(transactions)]
    my_blockchain.update_chain(incoming_chain)
    chainson = my_blockchain.export_chain()
    chain_copy = my_blockchain.load_exported_chain(chainson)
    print(chain_copy == my_blockchain.chain)


if __name__ == "__main__":
    main()
