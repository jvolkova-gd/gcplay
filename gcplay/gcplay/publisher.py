
import json
from collections import namedtuple

from gcplay.config import Config, logger
from google.cloud import pubsub
from google.api_core.exceptions import AlreadyExists

from gcplay.botgen import BotGen

def run_publisher():
    # init connect
    cfg = Config()

    cfg.init_connect()

    publisher = pubsub.PublisherClient()
    # create topic
    topic_path = publisher.topic_path(cfg.get("main", "project_id"),
                                      cfg.get("pub", "topic_id"))


    try:
        topic = publisher.create_topic(topic_path)
        logger.info('Topic created: {}'.format(topic))

    except AlreadyExists:
        logger.info("Topic %s already exist", topic_path)


    # init BotGen
    params_list = ["bots", "users", "cats", "duration"]
    BotgenArgs = namedtuple("BotGenArgs", params_list)

    args = BotgenArgs(*[int(cfg.get("botgen", i)) for i in params_list])

    result = BotGen(args).execute()

    for item in result:
        # decode by event
        for num, event in enumerate(json.loads(item)):
            logger.info("line %s %s", num, event)
            # Data must be a bytestring
            data = str(event).encode('utf-8')
            publisher.publish(topic_path, data=data, ip=event.get("ip"))


if __name__ == "__main__":
    run_publisher()
