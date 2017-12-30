# User Flow

1. Create Keystore
2. Choose your roles: [normal_node, miner, validator]

## Prerequisite

docker installed

## Normal node

```
docker run -d \
    -v $PWD/data/config:/root/.config/pyethapp \
    -v $PWD/data/log:/root/log \
    --name pyethapp \
    ethresearch/pyethapp \
    /usr/local/bin/pyethapp \
    --log-file /root/log/log.txt run

docker logs -f pyethapp
```


## Miner

```
docker run -d \
    -v $PWD/data/config:/root/.config/pyethapp \
    -v $PWD/data/log:/root/log \
    --name pyethapp \
    ethresearch/pyethapp \
    /usr/local/bin/pyethapp \
    -m 50 --log-file /root/log/log.txt run

docker logs -f pyethapp
```

## Validator

```
docker run -d \
    -v $PWD/data/config:/root/.config/pyethapp \
    -v $PWD/data/log:/root/log \
    --name pyethapp \
    ethresearch/pyethapp \
    /usr/local/bin/pyethapp \
    --validate 1 --deposit 5000 -m 0 --password /root/.config/pyethapp/password.txt
    --log-file /root/log/log.txt run

docker logs -f pyethapp
```