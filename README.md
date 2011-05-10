#Institutions of the European Union

This is a LOD dataset about 'Institutions of the European Union' originally deployed on [GAE](http://eu-institutions.appspot.com/).

## Using



### SPARQL Query Example

Go to [sparql.org](http://sparql.org/sparql.html) and paste in the following query that list all organisations, their names and links to Wikipedia:

	PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
	PREFIX owl: <http://www.w3.org/2002/07/owl#>
	PREFIX org: <http://www.w3.org/ns/org#>
	PREFIX dct: <http://purl.org/dc/terms/> 

	SELECT ?org ?name ?alias FROM <http://eu-institutions.appspot.com/format/rdf-xml> WHERE {

	 ?euib rdfs:subClassOf org:Organization .
	 ?org a ?euib ;
	      dct:title ?name ;
	      owl:sameAs ?alias .
	}

### Using the data as JSON from a Web page
TBD ...

### Using the data in a Google spreadsheet
TBD ...
