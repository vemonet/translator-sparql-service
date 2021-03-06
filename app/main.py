from rdflib_endpoint import SparqlEndpoint

from rdflib.plugins.sparql.evalutils import _eval
from rdflib import Graph, Literal, RDF, URIRef
from rdflib.graph import ConjunctiveGraph
# from rdflib.namespace import Namespace

import requests

def translator_label(query_results, ctx, part, eval_part):
    """
    Concat 2 string and return the length as additional Length variable

    Query:
    PREFIX umtranslator: <https://w3id.org/um/translator/>
    SELECT ?entity ?label WHERE {
        BIND("MONDO:0005146" AS ?entity)
        BIND(umtranslator:get_label(?entity) AS ?label)
    }
    \f
    :param query_results:   An array with the query results objects
    :param ctx:             <class 'rdflib.plugins.sparql.sparql.QueryContext'>
    :param part:            Part of the query processed (e.g. Extend or BGP) <class 'rdflib.plugins.sparql.parserutils.CompValue'>
    :param eval_part:       Part currently evaluated
    :return:                the same query_results provided in input param, with additional results
    """
    argument1 = str(_eval(part.expr.expr[0], eval_part.forget(ctx, _except=part.expr._vars)))
    # argument2 = str(_eval(part.expr.expr[1], eval_part.forget(ctx, _except=part.expr._vars)))
    evaluation = []
    # identifiers = []
    # if argument1.startswith('https://identifiers.org/'):
    #     argument1 = argument1.replace('https://identifiers.org/', '')
    argument1 = argument1.replace("https://identifiers.org/", "").replace("https://go.drugbank.com/drugs/", "DRUGBANK:").replace("http://purl.obolibrary.org/obo/HP_", "HP:").replace("http://purl.obolibrary.org/obo/MONDO_", "MONDO:")

    # Resolve CURIEs label using https://nodenormalization-sri.renci.org/docs
    resolve_curies = requests.get('https://nodenormalization-sri.renci.org/get_normalized_nodes',
        params={'curie': [argument1]}).json()
    try:
        evaluation.append(resolve_curies[argument1]['id']['label'])
        # identifiers.append(resolve_curies[argument1]['id']['identifier'])
    except:
        print('No results for ' + argument1)

    # Append the results for our custom function
    for i, result in enumerate(evaluation):
        query_results.append(eval_part.merge({
            part.var: Literal(result), 
            # rdflib.term.Variable(part.var + 'Id'): Literal(identifiers[i])
        }))
    return query_results, ctx, part, eval_part

def translator_pref_id(query_results, ctx, part, eval_part):
    """
    Concat 2 string and return the length as additional Length variable

    Query:
    PREFIX umtranslator: <https://w3id.org/um/translator/>
    SELECT ?entity ?pref_id WHERE {
        BIND("MONDO:0005146" AS ?entity)
        BIND(umtranslator:pref_id(?entity) AS ?pref_id)
    }
    \f
    :param query_results:   An array with the query results objects
    :param ctx:             <class 'rdflib.plugins.sparql.sparql.QueryContext'>
    :param part:            Part of the query processed (e.g. Extend or BGP) <class 'rdflib.plugins.sparql.parserutils.CompValue'>
    :param eval_part:       Part currently evaluated
    :return:                the same query_results provided in input param, with additional results
    """
    argument1 = str(_eval(part.expr.expr[0], eval_part.forget(ctx, _except=part.expr._vars)))

    evaluation = []
    if argument1.startswith('https://identifiers.org/'):
        # Quick hack to support identifiers URIs
        argument1 = argument1.replace('https://identifiers.org/', '')

    # Resolve CURIEs label using https://nodenormalization-sri.renci.org/docs
    resolve_curies = requests.get('https://nodenormalization-sri.renci.org/get_normalized_nodes',
        params={'curie': [argument1]}).json()
    try:
        evaluation.append(resolve_curies[argument1]['id']['identifier'])
    except:
        print('No results for ' + argument1)

    # Append the results for our custom function
    for i, result in enumerate(evaluation):
        query_results.append(eval_part.merge({
            part.var: Literal(result),
        }))
    return query_results, ctx, part, eval_part


example_query = """Resolve labels:\n
```
PREFIX umtranslator: <https://w3id.org/um/translator/>
SELECT ?entity ?label WHERE {
    BIND("MONDO:0005146" AS ?entity)
    BIND(umtranslator:get_label(?entity) AS ?label)
}
```
Resolve preferred ID:\n
```
PREFIX umtranslator: <https://w3id.org/um/translator/>
SELECT ?entity ?pref_id WHERE {
    BIND("MONDO:0005146" AS ?entity)
    BIND(umtranslator:pref_id(?entity) AS ?pref_id)
}
```"""

# Start the SPARQL endpoint based on a RDFLib Graph
g = ConjunctiveGraph(
    identifier=URIRef('https://w3id.org/um/translator/graph/default'), 
)

app = SparqlEndpoint(
    graph=g,
    functions={
        'https://w3id.org/um/translator/get_label': translator_label,
        'https://w3id.org/um/translator/pref_id': translator_pref_id,
    },
    title="SPARQL endpoint for Translator services", 
    description="A SPARQL endpoint to serve NCATS Translator services. \n[Source code](https://github.com/vemonet/translator-sparql-service)",
    version="0.0.1",
    public_url='https://service.translator.137.120.31.102.nip.io/sparql',
    cors_enabled=True,
    example_query=example_query
)
