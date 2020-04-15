from entity import *

import datetime # TODO: Remove


class Section(Entity):
    _columns  = ['title']
    _parents  = []
    _children = {'categories': 'Category'}
    _siblings = {}


class Category(Entity):
    _columns  = ['title']
    _parents  = ['section']
    _children = {'posts': 'Post'}
    _siblings = {}


class Post(Entity):
    _columns  = ['content', 'title']
    _parents  = ['category']
    _children = {'comments': 'Comment'}
    _siblings = {'tags': 'Tag'}


class Comment(Entity):
    _columns  = ['text']
    _parents  = ['post', 'user']
    _children = {}
    _siblings = {}


class Tag(Entity):
    _columns  = ['name']
    _parents  = []
    _children = {}
    _siblings = {'posts': 'Post'}


class User(Entity):
    _columns  = ['name', 'email', 'age']
    _parents  = []
    _children = {'comments': 'Comment'}
    _siblings = {}


if __name__ == "__main__":

    # print(psycopg2.__version__)
    all = Section.all()
    for i in all:
        print(i._columns, i.id, i.title, i.created, i.updated)


    # section = Section(2)
    # print(section.title)
    # section.delete()
    # print('1')
    # section = Section()
    #
    # section.delete()

    # section = Section(2)
    # user = User(1)
    # print('first')
    # section.title = "zalupa"
    # print(user.__dict__)
    # print(user.name, user.email)
    # section.save()
    # print(section.title, section.created, section.updated)
    # print(section.noattr)
    # print(section._fields)
    # section.title = 'small_zhopa_' + str(datetime.datetime.now())
    # section.save()
    # sec = Section(2)
    # print(sec.title) #, section.created, section.updated)
    # user = User()
    # user.name = "zalupa pomen'she"
    # print(user)

    # for section in Section.all():
        # print(section.title)
