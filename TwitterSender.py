from TwitterAPI import TwitterAPI # pip install TwitterAPI
from credentials import *

twitter_api = TwitterAPI(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)


def tweet(msg, image, debug=False):
    file_image = open(image, 'rb')
    data = file_image.read()
    if debug:
        print(image, msg)
        return
    file_image.close()
    return twitter_api.request('statuses/update_with_media', {'status': msg}, {'media[]': data})