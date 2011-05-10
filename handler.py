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
import csv

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

import rdflib

from rdflib import Graph
from rdflib import Namespace
from rdflib import plugin
from rdflib.serializer import Serializer

import rdfjson
import rdfextras


SUPPORTED_OUTPUT_FORMATS = ["rdf-xml", "ttl", "nt", "json", "csv"]

NAMESPACES = {	'void' : Namespace('http://rdfs.org/ns/void#'),
				'eui' : Namespace('http://institutions.publicdata.eu/#')
}

# for RDF/JSON output:
plugin.register("rdf-json-pretty", Serializer, "rdfjson.RdfJsonSerializer", "PrettyRdfJsonSerializer")
# for SPARQL query support:
plugin.register('sparql', rdflib.query.Processor, 'rdfextras.sparql.processor', 'Processor')
plugin.register('sparql', rdflib.query.Result, 'rdfextras.sparql.query', 'SPARQLQueryResult')

class MainHandler(webapp.RequestHandler):
	def get(self):
		self.response.out.write(template.render('index.html', None))

class NotFoundHandler(webapp.RequestHandler):
	def get(self):
		self.error(404)
		self.response.out.write(template.render('a404.html', None))

class WellKnownVoIDHandler(webapp.RequestHandler):
	def get(self):
		self.redirect("/about/void.ttl")

class AboutHandler(webapp.RequestHandler):
	def get(self, details):
		if details == "void.ttl": # someone trying to directly or via .well-known/void GET the VoID file
			g = Graph()
			g.parse(location = 'about.html', format="rdfa") # load the RDFa-based dataset description
			self.response.headers['Content-Type'] = 'text/turtle'
			self.response.out.write(g.serialize(format="turtle"))
		else:
			self.response.out.write(template.render('about.html', None))

class UsageHandler(webapp.RequestHandler):
	def get(self, upath):
		if upath == 'json-example':
			self.response.out.write(template.render('usage/standalone-json.html', None))
		else:
			self.error(404)
			self.response.out.write(template.render('a404.html', None))

class QueryHandler(webapp.RequestHandler):
	def get(self, q):

		if q == '':
			self.response.out.write(template.render('query.html', None))
		elif q == 'exec':
			if not self.request.query_string == '':
				qstr = urllib.unquote_plus(self.request.get('qstr'))
				logging.info('[API] query request [%s] from IP [%s]' %(qstr, os.environ['REMOTE_ADDR']))
				g = Graph()
				g.parse(location = 'index.html', format="rdfa") # load the RDFa-based dataset
				res = g.query(qstr)
				for r in res:
					row = ""
					for v in r:
						row = "".join([row, v])
					self.response.out.write("".join(["<div style='font-size: 80%; margin: 1em 1em 1em 0;'>", str(row), "</div>"]))
		else:
			self.error(404)
			self.response.out.write(template.render('a404.html', None))

class FormatHandler(webapp.RequestHandler):
	def get(self, format):
		logging.info('[API] alternative format request for [%s] from IP [%s]' %(format, os.environ['REMOTE_ADDR']))
		
		if format in SUPPORTED_OUTPUT_FORMATS:
			g = Graph()
			g.bind('void', NAMESPACES['void'], True)
			g.bind('eui', NAMESPACES['eui'], True)
			g.parse(location = 'index.html', format="rdfa") # load the RDFa-based dataset
			
			self.response.headers.add_header("Access-Control-Allow-Origin", "*") # CORS-enabled
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
			elif format == 'csv':
				self.response.headers['Content-Type'] = 'text/csv'
				self.response.out.write(self.dump_csv(g))
		elif format =='':
			self.response.out.write("<div>Supported output formats or go back [<a href='/'>home</a>]:</div><ul>")
			for format in SUPPORTED_OUTPUT_FORMATS:
				self.response.out.write("".join(["<li>", "<a href='../format/", format, "'>", format , "</a></li>"]))
			self.response.out.write("</ul>")
		else:
			self.response.out.write(template.render('a404.html', None))
	
	def dump_csv(self, graph):
		outbuffer = StringIO.StringIO()
		csvdata = csv.writer(outbuffer, delimiter=',')
		qstr = """
		PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
		PREFIX owl: <http://www.w3.org/2002/07/owl#>
		PREFIX org: <http://www.w3.org/ns/org#>
		PREFIX dct: <http://purl.org/dc/terms/> 
		PREFIX foaf: <http://xmlns.com/foaf/0.1/> 
		PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
		PREFIX eui: <http://institutions.publicdata.eu/#>

		SELECT ?org ?name ?description ?hp ?wikipedia WHERE {
		 ?euib rdfs:subClassOf org:Organization .
		 ?org a ?euib ;
		      dct:title ?name ;
		      dct:description ?description ;
		      foaf:homepage ?hp ;
		      owl:sameAs ?wikipedia . 
		}
		"""
		
		try:
			res = graph.query(qstr)
			csvdata.writerow(["ORG_ID", "NAME", "DESCRIPTION", "HOMEPAGE", "WIKIPEDIA_LINK"])
			for r in res:
				csvdata.writerow(r)
		except csv.Error, e:
			logging.info('[API] CSV output error %s' %e)
			
		data = outbuffer.getvalue()
		outbuffer.close()
		return data