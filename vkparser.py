import requests as req
import random
import pendulum
import time

import conf
from publication import Post


class VKParser:
    def __init__(self, token=conf.token, owner_id=conf.owner_id, v=conf.v, from_group=conf.from_group):
        self.posts = list()
        self.token = token
        self.owner_id = owner_id
        self.v = v
        self.from_group = from_group
        self.idOfOtherGroups = conf.idOfOtherGroups
        self.hashtags = conf.hashtags

    def Main(self):
        self.SearchPosts()
        self.PublishPosts()
        print('Всё')

    def SearchPosts(self):
        resp = []
        for idOfOtherGroup in self.idOfOtherGroups:
            time.sleep(2)
            resp = req.get('https://api.vk.com/method/wall.get',
                           params={'access_token': self.token, 'v': self.v, 'owner_id': idOfOtherGroup, 'count': 3})

            for publication in resp.json()['response']['items']:
                post = Post()
                print('SearchPosts', publication)
                if 'text' in publication:
                    post.msg = publication['text']

                if 'text' not in publication:
                    post.att = self.AttImg(publication['attachments'])

                self.posts.append(post)

    def PublishPosts(self):
        minutes = 1
        datePublication = time.mktime(pendulum.now().add(hours=1, minutes=minutes).timetuple())
        for post in self.posts:
            p = {'publish_date': datePublication}
            p.update(self.GetAtt(post.GetAtt(self.hashtags)))
            print(p)
            r = req.get('https://api.vk.com/method/wall.post', params=p)
            print(r)
            minutes += random.randint(30, 59)
            datePublication = time.mktime(pendulum.now().add(hours=1, minutes=minutes).timetuple())
            time.sleep(2)

    def GetAtt(self, postDict):
        postDict['v'] = self.v
        postDict['owner_id'] = self.owner_id
        postDict['access_token'] = self.token
        postDict['from_group'] = self.from_group
        return postDict

    def AttImg(self, att):
        return 'photo' + str(att[0]['photo']['owner_id']) + '_' + str(att[0]['photo']['id'])
