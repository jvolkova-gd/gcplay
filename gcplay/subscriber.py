
from gcplay.publisher import run_publisher
from google.cloud import pubsub
from gcplay.config import Config, logger
from google.api_core.exceptions import AlreadyExists

def run_subscriber():
    cfg = Config()
    project_id = cfg.get("main", "project_id")
    subscriber = pubsub.SubscriberClient()
    topic_path = subscriber.topic_path(project_id, cfg.get("pub", "topic_id"))
    subscription_name = 'projects/{project_id}/subscriptions/{sub}'.format(
        project_id=project_id, sub=cfg.get("pub", "subscript_name"))

    try:
        subscriber.create_subscription(subscription_name, topic_path)
    except AlreadyExists:
        logger.info("Topic %s already exist", topic_path)

    def callback(message):
        logger.info("Message id: %s \t Message attribute ip: %s \t "
                    "Message data: %s \n", message.message_id,
                    message.attributes["ip"], message.data)
        message.ack()
    future = subscriber.subscribe(subscription_name, callback)
    future.result()

if __name__ == "__main__":
    run_publisher()
    run_subscriber()
