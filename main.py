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


def write_private_config(account_info, bootstrap_info):
    config = {}
    config["account_info"] = [{f"0x{account}": key}
                              for account, key in account_info]
    config["bootstrap_info"] = bootstrap_info
    with open(f"{CWD}/private/private.yaml", "w") as f:
        f.write(yaml.dump(config, default_flow_style=False))
        print("Created private info at private/config.yaml . Keep this safe and give validator money using accounts in it.")


def write_public_config_for_bootstrap(accounts, bootstrap_enodes):
    config = create_default_config()
    genesis = create_default_genesis()
    genesis["alloc"] = {account: {"balance": DEFAULT_BALANCE}
                        for account in accounts}
    config["eth"]["genesis"] = genesis
    config["discovery"]["bootstrap_nodes"] = bootstrap_enodes
    with open(f"{CWD}/user/data/config/config.yaml", "w") as f:
        f.write(yaml.dump(config, default_flow_style=False))
        print("Created config.yaml at user/data/config")


def to_enode(ip, privkey):
    node_pubkey = privtopub_raw(privkey)
    enode = host_port_pubkey_to_uri(ip, 30303, node_pubkey).decode("utf-8")
    return enode


def ask_ips():
    example_ips = "11.22.33.44, 55.66.77.88, 123.123.123.123"
    question = (
        "Enter ips of your machines for bootstrap nodes"
        "(domain name not allowed),"
        f"separeted with comma ({example_ips}):"
    )
    answer = input(question)
    boostrap_ips_raw = answer if answer != "" else example_ips
    bootstrap_ips = boostrap_ips_raw.replace(" ", "").split(",")
    return bootstrap_ips


def show_bootstrap_deploy_guide(bootstrap_info):
    for ip, privhex in bootstrap_info.items():
        print("Deploy this bootstrap node on", ip)
        print(f"""
        ```
        docker run -d \\
            -v $PWD/data/config:/root/.config/pyethapp \\
            -p 30303:30303 \\
            -p 30303:30303/udp \\
            -p 8545:8545 \\
            --name pyethapp \\
            ethresearch/pyethapp-research:alpine \\
            pyethapp -c "node.privkey_hex={privhex}" run
        ```""")


def create_config_for_bootstrap():
    bootstrap_ips = ask_ips()
    bootstrap_info = {ip: token_hex(32) for ip in bootstrap_ips}

    account_private_keys = [token_hex(32) for _ in range(NUM_ACCOUNTS)]
    accounts = [encode_hex(privtoaddr(key)) for key in account_private_keys]
    accounts_info = zip(accounts, account_private_keys)

    bootstrap_enodes = [to_enode(ip, key)
                        for ip, key in bootstrap_info.items()]

    write_private_config(accounts_info, bootstrap_info)
    write_public_config_for_bootstrap(accounts, bootstrap_enodes)

    show_bootstrap_deploy_guide(bootstrap_info)


if __name__ == '__main__':
    create_config_for_bootstrap()
