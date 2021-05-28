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
    BIND(umtranslator:label(?entity) AS ?label)
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

```SPARQL
PREFIX umtranslator: <https://w3id.org/um/translator/>
SELECT * WHERE
{
  SERVICE <https://service.translator.137.120.31.102.nip.io/sparql> {
    SELECT ?entity ?label WHERE {
        BIND("MONDO:0005146" AS ?entity)
        BIND(umtranslator:label(?entity) AS ?label)
    }
  }
}
```

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
