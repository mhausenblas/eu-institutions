"""
The main GAE script.

@author: Michael Hausenblas, http://sw-app.org/mic.xhtml#i
@since: 2011-05-06
@status: inital version
"""
import sys
import os
import logging
import cgi
import platform

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from handler import *


application = webapp.WSGIApplication([
						(r'/format/(.*)$', FormatHandler),
						(r'/', MainHandler),
						(r'/.*', NotFoundHandler)
					],
					debug=False)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
	main()
