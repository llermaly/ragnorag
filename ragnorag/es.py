from elasticsearch import Elasticsearch
import os

os.environ["ELASTIC_ENDPOINT"] = "YOUR_ELASTIC_ENDPOINT"
os.environ["ELASTIC_API_KEY"] = "YOUR_ELASTIC_API_KEY"

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
