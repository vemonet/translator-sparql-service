# SPARQL endpoint for Translator services  

A SPARQL endpoint to serve Translator API operations as SPARQL custom functions.

Translator API integrated:

* https://nodenormalization-sri.renci.org/docs

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

## Example queries

Get label  from CURIE:

```SPARQL
PREFIX umtranslator: <https://w3id.org/um/translator/>
SELECT ?entity ?label WHERE {
    BIND("MONDO:0005146" AS ?entity)
    BIND(umtranslator:label(?entity) AS ?label)
}
```

Get preferred ID (CURIE):

```SPARQL
PREFIX umtranslator: <https://w3id.org/um/translator/>
SELECT ?entity ?pref_id WHERE {
    BIND("MONDO:0005146" AS ?entity)
    BIND(umtranslator:pref_id(?entity) AS ?pref_id)
}
```

## Try a federated query 📬

Use this federated query to retrieve predicted treatments for a drug or disease (OMIM or DRUGBANK) from any other SPARQL endpoint supporting federated queries (note that this query use our test SPARQL endpoints, it might not be always up)

```SPARQL
PREFIX umtranslator: <https://w3id.org/um/translator/>
SELECT * WHERE
{
  SERVICE <https://translator-service.137.120.31.102.nip.io/sparql> {
    SELECT ?entity ?label WHERE {
        BIND("MONDO:0005146" AS ?entity)
        BIND(umtranslator:label(?entity) AS ?label)
    }
  }
}
```

