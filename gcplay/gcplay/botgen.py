
import json
import random
import logging
from gcplay.config import Config
from datetime import datetime, timedelta
from collections import deque


class BotGen(object):

    def __init__(self, params):
        self.cfg = Config()
        self.params = params
        self.users = deque(range(0, 0 + self.params.users))
        self.bots = deque(range(250, 250 + self.params.bots))
        self.categories = deque(range(1000, 1000 + self.params.cats))
        self.actions = self.cfg.get("botgen", "categories").split(",")
        print(self.actions)
        print("started with parameters :", self.params)

    def random_user(self):
        return random.choice(self.users)

    def random_bot(self):
        return random.choice(self.bots)

    def random_cat(self):
        return random.choice(self.categories)

    def random_action(self):
        return random.choice(self.actions)

    @staticmethod
    def user2ip(user_id): return "172.10.{}.{}".format(
        int(user_id / 255), user_id % 255)

    @staticmethod
    def bot2ip(user_id): return "172.20.{}.{}".format(
        int(user_id / 255), user_id % 255)

    @staticmethod
    def rsec(dt): return int(dt.timestamp())

    @staticmethod
    def repack2json(ls):

        try:
            return list(map(lambda x: {'unix_time': x[0], 'category_id': x[1],
                             'ip': x[2], 'type': x[3]}, ls))
        except TypeError:
            logging.warning("war %s", ls)

    def write_as_json(self, ls):
        if ls:
            json_result = json.dumps(self.repack2json(ls), ensure_ascii=False,
                             separators=(',', ':'), indent=1)
            return json_result

    def get_bots_requests(self, ts, i):
        if i % 5 == 0:
            return [(str(self.rsec(ts)), self.random_cat(),
                     self.bot2ip(self.random_bot()),
                     self.actions[0]) for u in range(len(self.bots))]
        else:
            return [(str(self.rsec(ts)), self.random_cat(),
                     self.bot2ip(self.random_bot()),
                     self.random_action()) for u in range(len(self.bots))]

    def users_requests(self, ts, i):
        if i % 10 == 0:
            return [(str(self.rsec(ts)), self.random_cat(),
                     self.user2ip(self.users[u]),
                     self.actions[0]) for u in range(len(self.users))]

        self.users.rotate(i % len(self.users))
        return [(str(self.rsec(ts)), self.random_cat(),
                 self.user2ip(self.random_user()),
                 self.random_action()) for x in random.sample(
            self.users, int(len(self.users) / 4))]

    def execute(self):
        start_time = datetime.now()
        t1, t2 = start_time, start_time + timedelta(
            seconds=self.params.duration)
        counter = 0
        while t1 < t2:
            yield self.write_as_json(self.users_requests(t1, counter))
            t1 += timedelta(seconds=1)
            counter += 1
