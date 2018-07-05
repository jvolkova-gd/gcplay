
import logging
import json
from collections import namedtuple

from gcplay.config import Config
from google.cloud import pubsub_v1
from google.api_core.exceptions import AlreadyExists

from gcplay.botgen import BotGen

# init connect

cfg = Config()

cfg.init_connect()

publisher = pubsub_v1.PublisherClient()

# create topic
topic_id = publisher.topic_path(cfg.get("main", "project_id"),
                                cfg.get("pub", "topic_id"))


try:
    topic = publisher.create_topic(topic_id)
    logging.info('Topic created: {}'.format(topic))

except AlreadyExists:
    logging.info("Topuc %s already exist", topic_id)


# init BotGen
params_list = ["bots", "users", "cats", "duration"]
BotgenArgs = namedtuple("BotGenArgs", params_list)

args = BotgenArgs(*[int(cfg.get("botgen", i)) for i in params_list])

result = BotGen(args).execute()

for item in result:
    # decode by event
    for num, event in enumerate(json.loads(item)):
        print("line %s %s", num, event)
        # Data must be a bytestring
        data = str(event).encode('utf-8')
        publisher.publish(topic_id, data=data, ip=event.get("ip"))
