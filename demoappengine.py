import webapp2
import cgi
import datetime
import urllib
import os
import jinja2

from google.appengine.ext import db

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'])


class BlogPost(db.Model):
    title = db.StringProperty()
    content = db.StringProperty()
    name = db.StringProperty()

def BlogPostKey():
    return db.Key.from_path('Blog','default_blog')


class MainPage(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('templates/index.html')
        template_values = { "posts": BlogPost.all() }

        self.response.write(template.render(template_values))


class AddPost(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('templates/addPost.html')
        self.response.write(template.render())

    def post(self):
        title = self.request.get('title')
        content = self.request.get('content')
        newpost = BlogPost(parent=BlogPostKey())
        newpost.title = title
        newpost.content = content

        name = self.request.get('name')
        newpost.name = name

        newpost.put()
        self.redirect('/')


app = webapp2.WSGIApplication([('/', MainPage),
                               ('/AddPost',AddPost)],
                              debug=True)