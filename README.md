# Tweets collector

Collects tweets from [twitter](https://twitter.com/), classify them by a topic keyword, and sends to a topic subscriber.

### External modules

- [Tweepy](https://www.tweepy.org/) - An easy-to-use Python library for accessing the Twitter API.

- [Pika](https://pika.readthedocs.io/en/stable/) - Pika is a pure-Python implementation of the AMQP 0-9-1 protocol that tries to stay fairly independent of the underlying network support library.

### Setting up
```
$ python3 -m pip install -r requirements.txt
```

### Running
```
$ python3 collector.py

$ python3 classifier.py

$ python3 consumer.py

```