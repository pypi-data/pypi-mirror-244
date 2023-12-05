from solana.rpc.api import Client
from solana.transaction import Transaction
from solana.blockhash import BlockhashCache
from solders.keypair import Keypair
from solders.transaction import VersionedTransaction
from solders.message import to_bytes_versioned, Message
from solders.instruction import Instruction


def create_client(url):
    return Client(url)


def to_solami(price):
    return price * 1_000_000_000


def from_solami(price):
    return float(price) / 1_000_000_000


def get_keypair_from_base58_secret_key(private_key_base58):
    return Keypair.from_base58_string(private_key_base58)


def run_solana_transaction(client, sender_key_pair, transaction_buffer):
    transaction = Transaction.deserialize(bytes(transaction_buffer))
    transaction.sign(sender_key_pair)
    response = None
    try:
        response = client.send_transaction(transaction, sender_key_pair)
    except Exception as e:
        print("An error occurred:", e)
    return response


def run_solana_versioned_transaction(client, sender_key_pair, transaction_buffer):
    transaction = VersionedTransaction.from_bytes(bytes(transaction_buffer))
    signature = sender_key_pair.sign_message(to_bytes_versioned(transaction.message))
    signed_tx = VersionedTransaction.populate(transaction.message, [signature])
    print(signed_tx)
    block = client.get_latest_blockhash().value
    print(block)
    print(dir(signed_tx))
    print(transaction.message.instructions)
    instructions = [
        Instruction.from_json(instru.to_json())
        for instru in transaction.message.instructions
    ]
    signed_tx.message = Message.new_with_blockhash(
            instructions,
            sender_key_pair.pubkey(), block)
    response = None
    try:
        response = client.send_transaction(
            signed_tx
        )
    except Exception as e:
        print("An error occurred:", e)
    return response
