from uuid import uuid4
import time
import json
from random import randint, choice, uniform
import string
from faker import Faker
fake = Faker()

platforms = ['Android', 'iOS', 'Windows']


def generate_time(start_time=None):
    """
        Generates a timestamp between start_time and end_time
        - param: start_time int
        - return: event_time int
    """

    if start_time is None:
        start_time = time.mktime(time.strptime("1/7/2022 12:30 PM", '%d/%m/%Y %I:%M %p'))
    end_time = time.time()
    event_time = uniform(start_time,end_time)
    
    return event_time

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    """
        Generates a random string with six chars
    """

    return ''.join(choice(chars) for _ in range(size))

def get_init():
    """
        Creates a mocked init of game
        - return json
    """

    with open('./utils/countries.json', 'r') as f:
        countries = json.load(f)

    return {
        "event-type" : "init",
        "time": generate_time(),
        "user-id": str(uuid4()),
        "country": choice(list(countries.keys())),
        "platform": choice(platforms)
    }

def get_match(user_a, user_b):
    """
        Creates a mocked match with user_a and user_b
        - params:
            user_a: json
            user_b: json
        - return json
    """
    return {
        "event-type" : "match",
        "time": generate_time(min([user_a['time'],user_b['time']])),
        "user-a": user_a['user-id'],
        "user-b": user_b['user-id'],
        "user-a-postmatch-info": {
            "coin-balance-after-match": randint(0, 100),
            "level-after-match": randint(0, 100),
            "device": id_generator(),
            "platform": user_a['platform']
        },
        "user-b-postmatch-info": {
            "coin-balance-after-match": randint(0, 100),
            "level-after-match": randint(0, 100),
            "device": id_generator(),
            "platform": user_b['platform']
        },
        "winner": choice([user_a['user-id'],user_b['user-id']]),
        "game-tier": randint(1,5),
        "duration": randint(1,1000)
        
    }

def get_in_app_purchase(user):
    """
        Creates a mocked in app purchase request object
        - params:
            user: json
        - return json
    """
    return {
        "event-type" : "in-app-purchase",
        "time": generate_time(user['time']),
        "purchase_value": round(uniform(0.09, 99.99), 2),
        "user-id": user['user-id'],
        "product-id":id_generator(size=randint(1, 100))
    }