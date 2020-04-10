from entity import *


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

    section = Section(2)
    # user = User(1)
    print('first')
    # section.title = "zalupa"
    # print(user.__dict__)
    # print(user.name, user.email)
    # section.save()
    print(section.title, section.created, section.updated)
    # print(section.noattr)
    # print(section._fields)
    section.title = 'zhopa_pomenbshe'
    section.save()
    # print(section.title, section.created, section.updated)
    # user = User()
    # user.name = "zalupa pomen'she"
    # print(user)

    # for section in Section.all():
        # print(section.title)
