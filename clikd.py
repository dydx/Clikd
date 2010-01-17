import os

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

# database model to store clicks
class Click( db.Model ):
    user = db.UserProperty()
    date = db.DateTimeProperty( auto_now_add = True )

# request handler to process clicks
class ClickLog( webapp.RequestHandler ):
    def post( self ):
        click = Click()

        if users.get_current_user():
            click.user = users.get_current_user()

        click.put()
        self.redirect( '/' )

# request handler to serve web document and handle data
class MainPage( webapp.RequestHandler ):
    def get( self ):
        clicks_query = Click.all()
        clicks = db.GqlQuery("SELECT * FROM Click").count()

        if users.get_current_user():
            url = users.create_logout_url( self.request.uri )
            url_linktext = 'Logout'
        else:
            url = users.create_login_url( self.request.uri )
            url_linktext = 'Login'

        template_values = {
            'clicks': clicks,
            'url': url,
            'url_linktext': url_linktext,
            }

        path = os.path.join( os.path.dirname( __file__ ), 'index.html')
        self.response.out.write( template.render( path, template_values ))

application = webapp.WSGIApplication(
    [('/', MainPage),
     ('/click', ClickLog)],
     debug=True)

def main():
    run_wsgi_app( application )

if __name__ == "__main__":
    main()
