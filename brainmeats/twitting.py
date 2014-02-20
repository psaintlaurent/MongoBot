import twitter

from autonomic import axon, alias, help, Dendrite
from settings import NICK
from secrets import (TWIT_USER, TWIT_PASS, TWIT_ACCESS_TOKEN, TWIT_ACCESS_SECRET,
                     TWIT_CONSUMER_KEY, TWIT_CONSUMER_SECRET, TWIT_PAGE)


class Twitting(Dendrite):

    api = twitter.Api(consumer_key=TWIT_CONSUMER_KEY,
                   consumer_secret=TWIT_CONSUMER_SECRET,
                   access_token_key=TWIT_ACCESS_TOKEN,
                   access_token_secret=TWIT_ACCESS_SECRET)

    def __init__(self, cortex):
        super(Twitting, self).__init__(cortex)

    @axon
    @help("<show link to %s's twitter feed>" % NICK)
    def totw(self):
        return TWIT_PAGE

    @axon
    @help("MESSAGE <post to %s's twitter feed>" % NICK)
    def tweet(self, _message=False):
        if not self.values and not _message:
            self.chat("Tweet what?")
            return

        if not _message:
            message = ' '.join(self.values)
        else:
            message = _message
        
        try:
            status = self.api.PostUpdate(message)
        except Exception as e:
            return "Twitter error."

        if not _message:
            return 'Tweeted "%s"' % status.text

    @axon
    @help("ID <retrieve the tweet with ID>")
    def get_tweet(self, id=False):
        if not id:
            id = '+'.join(self.values)

        status = self.api.GetStatus(id)

        text = status.text
        screen_name = status.user.screen_name
        name = status.user.name
        if status.text:
            return '%s (%s) tweeted: %s' % (name, screen_name, text)