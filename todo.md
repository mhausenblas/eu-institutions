# Actions

## Michael

 1. DONE list of institutions in HTML based on [official EU page](http://europa.eu/institutions/inst/index_en.htm)
 2. DONE mark up in RDFa
 3. DONE Make URI's explict
 4. DONE add rdflib and provide alternative formats: RDF/XML, Turtle, JSON, etc. 
 5. DONE SPARQL interface
 6. DONE: VoID description (also: .well-known/void)
 7. OPEN: locations of all orgs
 8. OPEN: redirect from  http://institutions.publicdata.eu with Soeren

## Anja

 1. DONE modelling using [org vocab](http://www.epimorphics.com/public/vocabulary/org.html) etc. creating examples in models.ttl
 2. DONE interlinking targets (conceptual)
 3. OPEN: complete 'Decentralised Bodies'

## Ideas

### EU data cloud

Create a EU data cloud ala LOD cloud, taking into account stuff from [CKAN](http://ckan.net/tag/europe) and the datasets we do in LATC WP2 (base: diagram from D1.6.1)

### Geolocation

Show I&B on a geographical map. When using the DBpedia SPARQL endpoint Michael only found lat/long for two institutions, EC and EP with:

	select distinct * where {<http://dbpedia.org/resource/European_Parliament> <http://www.w3.org/2003/01/geo/wgs84_pos#lat> ?o }