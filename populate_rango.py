import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'tango_with_django_project.settings')

import django
django.setup()
from rango.models import Category, Page

def populate():

    view = {"python_pages": 128,
            "django_pages": 64,
            "other_pages": 32}

    like = {"python_pages": 64,
            "django_pages": 32,
            "other_pages": 16}



    python_pages = [
    {"title": "Official Python Tutorial",
     "url":"http://docs.python.org/2/tutorial/",
     "views": view["python_pages"],
     "likes": like["python_pages"]},

    {"title": "How to Think like a Computer Scientist",
     "url": "http://www.greenteapress.com/thinkpython/",
     "views": view["python_pages"],
     "likes": like["python_pages"]},

    {"title": "Learn Python in 10 Minutes",
     "url": "http://www.korokithakis.net/tutorials/python/",
     "views": view["python_pages"],
     "likes": like["python_pages"]}]

    django_pages = [
    {"title": "Official Django Tutorial",
     "url":"https://docs.djangoproject.com/en/1.9/intro/tutorial01/",
     "views": view["django_pages"],
     "likes": like["django_pages"]},

    {"title": "Django Rocks",
     "url": "http://www.djangorocks.com/",
     "views": view["django_pages"],
     "likes": like["django_pages"]},

    {"title": "How to Tango with Django",
     "url": "http://www.tangowithdjango.com/",
     "views": view["django_pages"],
     "likes": like["django_pages"]}]

    other_pages = [
        {"title": "Bottle",
         "url":"http://bottlepy.org/docs/dev/",
         "views": view["other_pages"],
         "likes": like["other_pages"]},

        {"title": "Flask",
         "url": "http://flask.pocoo.org",
         "views": view["other_pages"],
         "likes": like["other_pages"]}]

    cats = {"Python": {"pages": python_pages},
            "Django": {"pages": django_pages},
            "Other Frameworks": {"pages": other_pages} }

    for cat, cat_data in cats.items():
        c = add_cat(cat)

        for p in cat_data["pages"]:
            add_page(c, p["title"], p["url"], p["views"], p["likes"])

    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print("- {0} - {1}".format(str(c), str(p)))

def add_page(cat, title, url, views = 0, likes = 0):

    p = Page.objects.get_or_create(category=cat, title=title)[0]
    p.url = url
    p.views = views
    p.likes = likes
    p.save()
    return p

def add_cat(name):
    c = Category.objects.get_or_create(name=name)[0]
    c.save()
    return c

# First executed code here:
if __name__ == '__main__':
    print("Starting Rango population script...")
    populate()