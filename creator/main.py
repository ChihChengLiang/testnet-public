import yaml
import json
import sys
import os
from getpass import getpass
from secrets import token_hex
from ethereum.utils import privtoaddr, encode_hex
from devp2p.crypto import privtopub as privtopub_raw, sha3
from devp2p.utils import host_port_pubkey_to_uri


CWD = os.path.dirname(sys.argv[0])
NUM_ACCOUNTS = 10
DEFAULT_BALANCE = "50000000000000000000000000000"
NUM_BOOTSTRAPS = 5


def create_default_genesis():
    genesis = {
        "nonce": "0x0000000000000056",
        "difficulty": "0x4000",
        "mixhash": "0x0000000000000000000000000000000000000000000000000000000000000000",
        "coinbase": "0x0000000000000000000000000000000000000000",
        "timestamp": "0x00",
        "parentHash": "0x0000000000000000000000000000000000000000000000000000000000000000",
        "extraData": "0x11bbe8db4e347b4e8c937c1c8370e4b5ed33adb3db69cbdb7a38e1e50b1b82fa",
        "gasLimit": "0x5f5e100",
        "alloc": {}
    }
    return genesis


def create_default_config():
    config = {}
    config["eth"] = {"network_id": 1307}

    config["jsonrpc"] = {
        "listen_host": '0.0.0.0',
        "listen_port": 8545
    }
    config["discovery"] = {
        "listen_port": 30303
    }
    config["discovery"]["bootstrap_nodes"] = []

    config["p2p"] = {
        "listen_port": 30303
    }
    return config


def write_private_config(account_private_keys, bootstrap_node_private_keys):
    config = {}
    config["account_private_keys"] = account_private_keys
    config["bootstrap_node_private_keys"] = bootstrap_node_private_keys
    with open(f"{CWD}/private/private.yaml", "w") as f:
        f.write(yaml.dump(config, default_flow_style=False))
        print("Created private info at private/config.yaml . Keep this safe and give validator money using accounts in it.")



def write_public_config_for_bootstrap(accounts, bootstrap_enodes):
    config = create_default_config()
    genesis = create_default_genesis()
    genesis["alloc"] = {account: {"balance": DEFAULT_BALANCE}
                        for account in accounts}
    config["genesis"] = genesis
    config["discovery"]["bootstrap_nodes"] = bootstrap_enodes
    with open(f"{CWD}/public/config.yaml", "w") as f:
        f.write(yaml.dump(config, default_flow_style=False))
        print("Created public info at public/config.yaml")
        print("1. You still need to configure the ips of real deployed bootstrap nodes.")
        print("2. Then distribute this file to your user.")


def to_enode(privkey):
    node_pubkey = privtopub_raw(privkey)
    enode = str(host_port_pubkey_to_uri('0.0.0.0', 30303, node_pubkey))
    enode_replaced =enode # enode.replace('0.0.0.0', '__INSERT_IP_HERE__')
    return enode_replaced



def create_config_for_bootstrap():
    bootstrap_node_private_keys = [
        token_hex(32) for _ in range(NUM_BOOTSTRAPS)]
    account_private_keys = [token_hex(32) for _ in range(NUM_ACCOUNTS)]
    accounts = [encode_hex(privtoaddr(key)) for key in account_private_keys]

    bootstrap_enodes = [to_enode(key) for key in bootstrap_node_private_keys]

    write_private_config(account_private_keys, bootstrap_node_private_keys)
    write_public_config_for_bootstrap(accounts, bootstrap_enodes)
    


if __name__ == '__main__':
    create_config_for_bootstrap()
