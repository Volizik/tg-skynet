# import redis
# from dotenv import load_dotenv
#
# load_dotenv()
#
# host = os.environ.get('REDIS_HOST')
# port = os.environ.get('REDIS_PORT')
# db = os.environ.get('REDIS_DB')
store = {}

def store_message(user_id, message):
    # r = redis.Redis(host, port, db)
    # r.rpush(user_id, message)
    if user_id in store:
        store[user_id].append(message)
    else:
        store[user_id] = [message]

    return get_user_messages(user_id)

def get_user_messages(user_id):
    # r = redis.Redis(host, port, db)
    # messages = r.lrange(user_id, 0, -1)
    # return messages
    if user_id in store:
        return convert_messages_to_string(store[user_id])
    else:
        print(f'[STORE]: User {user_id} has no messages')
        return convert_messages_to_string([])


def convert_messages_to_string(list):
    return '\n '.join(list)