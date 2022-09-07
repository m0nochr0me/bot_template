# Telegram Bot template

Some boilerplate code I use to create telegram bots.

### Stack

- AIOgram
- Beanie
- MongoDB
- Motor

### Setup

- Edit `compose.yaml` to configure mongo and redis

- Set credentials in `config.secret.yaml`

- Review general settings in `config.yaml`

### Run

```shell
docker-compose -f compose.yaml up
```

```shell
python main.py
```