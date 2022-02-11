import conf


class Post:
    def __init__(self, msg=' ', att=conf.att):
        self.msg = msg
        self.att = att

    def GetAtt(self, hashtag):
        return {'message': self.msg + hashtag, 'attachments': self.att}
