#Institutions of the European Union

This is a LOD dataset about 'Institutions of the European Union' originally deployed on [GAE](http://eu-institutions.appspot.com/).

## Using


Go to [sparql.org](http://sparql.org/sparql.html) and paste in the following query:

	prefix owl: <http://www.w3.org/2002/07/owl#>
	prefix dct: <http://purl.org/dc/terms/> 
	prefix eui: <http://institutions.publicdata.eu/#>

	select * from <http://www.w3.org/2007/08/pyRdfa/extract?uri=http%3A%2F%2Feu-institutions.appspot.com> where {

	 ?org a eui:EU_Institution ;
	      dct:title ?name ;
	      owl:sameAs ?alias .
	}
