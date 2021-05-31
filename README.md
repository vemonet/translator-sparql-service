# SPARQL endpoint for Translator services  

A SPARQL endpoint to serve NCATS Translator services as SPARQL custom functions. Built with [rdflib-endpoint](https://github.com/vemonet/rdflib-endpoint)

Access the SPARQL service endpoint at https://service.translator.137.120.31.102.nip.io/sparql

OpenAPI docs at https://service.translator.137.120.31.102.nip.io

Translator APIs integrated:

* https://nodenormalization-sri.renci.org/docs

## Available functions 📬

**<a href="https://yasgui.triply.cc/#query=PREFIX%20umtranslator%3A%20%3Chttps%3A%2F%2Fw3id.org%2Fum%2Ftranslator%2F%3E%0ASELECT%20%3Fentity%20%3Flabel%20WHERE%20%7B%0A%20%20%20%20BIND(%22MONDO%3A0005146%22%20AS%20%3Fentity)%0A%20%20%20%20BIND(umtranslator%3Alabel(%3Fentity)%20AS%20%3Flabel)%0A%7D&endpoint=https%3A%2F%2Fservice.translator.137.120.31.102.nip.io%2Fsparql&requestMethod=GET&tabTitle=Query%209&headers=%7B%7D&contentTypeConstruct=application%2Fn-triples%2C*%2F*%3Bq%3D0.9&contentTypeSelect=application%2Fsparql-results%2Bjson%2C*%2F*%3Bq%3D0.9&outputFormat=table">Try the queries on YASGUI</a>**

### Get label  for entity

From a CURIE, or URI following this pattern: https://identifiers.org/NAMESPACE:ID

```SPARQL
PREFIX umtranslator: <https://w3id.org/um/translator/>
SELECT ?entity ?label WHERE {
    BIND("MONDO:0005146" AS ?entity)
    BIND(umtranslator:get_label(?entity) AS ?label)
}
```

### Get preferred ID

From a CURIE, or URI following this pattern: https://identifiers.org/NAMESPACE:ID

```SPARQL
PREFIX umtranslator: <https://w3id.org/um/translator/>
SELECT ?entity ?pref_id WHERE {
    BIND("MONDO:0005146" AS ?entity)
    BIND(umtranslator:pref_id(?entity) AS ?pref_id)
}
```

### Try a federated query

Use this federated query to retrieve labels from any other SPARQL endpoint supporting federated queries.

**From another SPARQL endpoint**

```SPARQL
PREFIX umtranslator: <https://w3id.org/um/translator/>
SELECT * WHERE
{
  SERVICE <https://service.translator.137.120.31.102.nip.io/sparql> {
    SELECT ?entity ?label WHERE {
        BIND("MONDO:0005146" AS ?entity)
        BIND(umtranslator:get_label(?entity) AS ?label)
    }
  }
}
```

**From the RDFLib SPARQL endpoint**

⚠️ RDFLib has a few limitation related to federated queries:

* Unfortunately, the `PREFIX` keyword does not work with federated queries in RDFLib, so we need to write the full URIs

* The latest version of RDFLib (`5.0.0 `) only recognize **lowercase `service`**. This will be fixed in the next versions.

Run this federated query on this RDFLib endpoint to resolve drug/disease labels retrieved from the Nanopublication network:

```SPARQL
SELECT DISTINCT ?label ?subject ?object (<https://w3id.org/um/translator/get_label>(str(?subject)) AS ?subjectLabel) (<https://w3id.org/um/translator/get_label>(str(?object)) AS ?objectLabel)
WHERE {
  	service <http://virtuoso.np.dumontierlab.137.120.31.101.nip.io/sparql> {
        SELECT * WHERE {
            GRAPH ?np_assertion {
              ?association <http://www.w3.org/2000/01/rdf-schema#label> ?label ;
                <http://www.w3.org/1999/02/22-rdf-syntax-ns#subject> ?subject ;
                <http://www.w3.org/1999/02/22-rdf-syntax-ns#predicate> ?predicate ;
                <http://www.w3.org/1999/02/22-rdf-syntax-ns#object> ?object .
              optional {
                ?association <https://w3id.org/biolink/vocab/relation> ?relation .
              }
              optional {
                ?association <https://w3id.org/biolink/vocab/provided_by> ?provided_by .
              }
              optional {
                ?association <https://w3id.org/biolink/vocab/association_type> ?association_type .
              }
              ?subject <https://w3id.org/biolink/vocab/category> ?subject_category .
              ?object <https://w3id.org/biolink/vocab/category> ?object_category .
            }
            filter ( ?subject_category = <https://w3id.org/biolink/vocab/Drug> || ?subject_category = <https://w3id.org/biolink/vocab/ChemicalSubstance> )
            filter ( ?object_category = <https://w3id.org/biolink/vocab/Disease> )
            GRAPH ?np_head {
                ?np_uri <http://www.nanopub.org/nschema#hasAssertion> ?np_assertion .
            }
                ?np_uri <http://purl.org/dc/terms/creator> <https://orcid.org/0000-0002-7641-6446> .
            	filter NOT EXISTS { ?creator <http://purl.org/nanopub/x/retracts> ?np_uri }
        } LIMIT 5
  	}
}
```

> Note: Adding this filter make the federated query crash in RDFLib (works with Fuseki functions):
>
> ```SPARQL
>             GRAPH <http://purl.org/nanopub/admin/graph> {
>                 ?np_uri <http://purl.org/nanopub/admin/hasValidSignatureForPublicKey> ?pubkey .
>             }
> ```

## Install and run ✨️

1. Install dependencies

```bash
pip install -r requirements.txt
```

2. Run the server on http://localhost:8000

```bash
uvicorn main:app --reload --app-dir app
```

## Or run with docker 🐳

Checkout the `Dockerfile` to see how the image is built, and run it with the `docker-compose.yml`:

```bash
docker-compose up -d --build
```

Or build and run with docker:

```bash
docker build -t rdflib-endpoint .
```

Run on http://localhost:8080

```bash
docker run -p 8080:80 rdflib-endpoint
```
