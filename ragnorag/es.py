from elasticsearch import Elasticsearch
import os

os.environ["ELASTIC_ENDPOINT"] = (
    "https://serverless-lab-abe759.es.us-east-1.aws.elastic.cloud:443"
)
os.environ["ELASTIC_API_KEY"] = (
    "WUFKSDVaVUJJdmpfRlh1QmpNRFo6Qk9pU3hOLW4zRm05b1JwMWFiZ3VaZw=="
)

es = Elasticsearch(
    os.environ["ELASTIC_ENDPOINT"],
    api_key=os.environ["ELASTIC_API_KEY"],
)

# Define the index name
INDEX_NAME = "wikipedia"


def ask(question):
    print("asking question")
    print(question)
    response = es.search(
        index=INDEX_NAME,
        body={
            "size": 1,
            "query": {"semantic": {"field": "semantic_content", "query": question}},
            "highlight": {
                "fields": {
                    "semantic_content": {"order": "score", "number_of_fragments": 1}
                }
            },
        },
    )

    print("Hits", response)

    hits = response["hits"]["hits"]

    if not hits:
        print("No hits found")
        return None

    answer = hits[0]["highlight"]["semantic_content"][0]
    section = hits[0]["_source"]

    return {"answer": answer, "section": section}
