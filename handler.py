"""
The handler script.

@author: Michael Hausenblas, http://sw-app.org/mic.xhtml#i
@since: 2011-05-06
@status: HTML and format API
"""
import sys
sys.path.insert(0, 'lib')
import logging
import cgi
import os
import platform
import urllib
import urllib2
import StringIO

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

from rdflib import Graph
from rdflib import Namespace
from rdflib import plugin
from rdflib.serializer import Serializer

import rdfjson


SUPPORTED_OUTPUT_FORMATS = ["rdf-xml", "ttl", "nt", "json"]

NAMESPACES = {	'void' : Namespace('http://rdfs.org/ns/void#'),
				'eui' : Namespace('http://institutions.publicdata.eu/#')
}

plugin.register("rdf-json-pretty", Serializer, "rdfjson.RdfJsonSerializer", "PrettyRdfJsonSerializer")


class NotFoundHandler(webapp.RequestHandler):
	def get(self):
		self.response.out.write(template.render('a404.html', None))
		
class MainHandler(webapp.RequestHandler):
	def get(self):
		self.response.out.write(template.render('index.html', None))

class FormatHandler(webapp.RequestHandler):
	def get(self, format):
		logging.info('[API] alternative format request for [%s] from IP [%s]' %(format, os.environ['REMOTE_ADDR']))
		
		if format in SUPPORTED_OUTPUT_FORMATS:
			g = Graph()
			g.bind('void', NAMESPACES['void'], True)
			g.bind('eui', NAMESPACES['eui'], True)
			g.parse(location = 'index.html', format="rdfa") # load the RDFa-based dataset
			
			if format == 'rdf-xml':
				self.response.headers['Content-Type'] = 'application/rdf+xml'
				self.response.out.write(g.serialize())
			elif format == 'ttl':
				self.response.headers['Content-Type'] = 'text/turtle'
				self.response.out.write(g.serialize(format="turtle"))
			elif format == 'nt':
				self.response.headers['Content-Type'] = 'text/plain'
				self.response.out.write(g.serialize(format="nt"))
			elif format == 'json':
				# based on https://bitbucket.org/okfn/openbiblio/src/tip/rdflib/
				self.response.headers['Content-Type'] = 'application/json'
				self.response.out.write(g.serialize(None, "rdf-json-pretty"))
		elif format =="":
			self.response.out.write("<div>Supported output formats:</div><ul>")
			for format in SUPPORTED_OUTPUT_FORMATS:
				self.response.out.write("".join(["<li>", "<a href='../format/", format, "'>", format , "</a></li>"]))
			self.response.out.write("</ul>")
		else:
			self.response.out.write(template.render('a404.html', None))