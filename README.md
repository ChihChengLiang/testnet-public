# Creator flow

1. Get ready for some machines for bootstrap nodes. We need the ips in next step.
2. `docker run -it --rm -v $PWD:/root ethresearch/pyethapp-research:alpine python /root/main.py`
3. Copy `user/` to remote servers, deploy bootstrap nodes as instructed
4. Distribute `user/` to friends 🎉