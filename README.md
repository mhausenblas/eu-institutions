#Institutions of the European Union

This is a LOD dataset about 'Institutions of the European Union' originally deployed on [GAE](http://eu-institutions.appspot.com/).

Michael and Anja from the [LATC Support Action](http://latc-project.eu/) are developing and maintaining it.

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

### Using the JSON data from within a Web page

The site is [CORS-enabled](http://enable-cors.org/), so you can directly use the data in your Web page. For a simple example how to use the JSON data from within a Web page, see the '[standalone json](https://github.com/mhausenblas/eu-institutions/blob/master/usage/standalone-json.html)' HTML file.

### Using the CSV data in a Google spreadsheet

Import the [CSV data](http://eu-institutions.appspot.com/format/csv) in a Google spreadsheet.

### Dataset metadata

The dataset is described using [VoID](http://www.w3.org/TR/void/). See the [about.html](https://github.com/mhausenblas/eu-institutions/blob/master/about.html) file or via '[.well-known/void](http://eu-institutions.appspot.com/.well-known/void)' on the site itself.

## License

This software is Public Domain.