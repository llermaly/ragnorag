from elasticsearch import Elasticsearch
import os

os.environ["ELASTIC_ENDPOINT"] = (
    "your_endpoint_here"  # Replace with your actual endpoint
)
os.environ["ELASTIC_API_KEY"] = "your_api_key_here"  # Replace with your actual API key

es = Elasticsearch(
    os.environ["ELASTIC_ENDPOINT"],
    api_key=os.environ["ELASTIC_API_KEY"],
)

INDEX_NAME = "wikipedia"


def create_inference_endpoint():
    es.options(request_timeout=60, max_retries=3, retry_on_timeout=True).inference.put(
        task_type="sparse_embedding",
        inference_id="wiki-inference",
        body={
            "service": "elasticsearch",
            "service_settings": {
                "adaptive_allocations": {"enabled": True},
                "num_threads": 1,
                "model_id": ".elser_model_2",
            },
            "chunking_settings": {
                "strategy": "sentence",
                "max_chunk_size": 25,
                "sentence_overlap": 0,
            },
        },
    )


def create_index_mapping():
    """Create Elasticsearch index with mapping"""
    mapping = {
        "mappings": {
            "properties": {
                "title": {"type": "text"},
                "section_name": {"type": "text"},
                "content": {"type": "text", "copy_to": "semantic_content"},
                "wiki_link": {"type": "keyword"},
                "image_url": {"type": "keyword"},
                "section_order": {"type": "integer"},
                "semantic_content": {
                    "type": "semantic_text",
                    "inference_id": "wiki-inference",
                },
            }
        }
    }

    # Create the index with the mapping
    if es.indices.exists(index=INDEX_NAME):
        es.indices.delete(index=INDEX_NAME)

    es.indices.create(index=INDEX_NAME, body=mapping)


def load_messi_article():
    """Load Messi article sections into Elasticsearch"""

    # Define article metadata
    title = "Lionel Messi"
    wiki_link = "https://en.wikipedia.org/wiki/Lionel_Messi"
    image_url = "https://upload.wikimedia.org/wikipedia/commons/b/b4/Lionel-Messi-Argentina-2022-FIFA-World-Cup_%28cropped%29.jpg"

    # Define sections as array of objects
    sections = [
        {
            "section_name": "Introduction",
            "content": """Lionel Andrés "Leo" Messi (Spanish pronunciation: [ljoˈnel anˈdɾes ˈmesi] ⓘ; born 24 June 1987) is an Argentine professional footballer who plays as a forward for and captains both Major League Soccer club Inter Miami and the Argentina national team. Widely regarded as one of the greatest players of all time, Messi set numerous records for individual accolades won throughout his professional footballing career such as eight Ballon d'Or awards and eight times being named the world's best player by FIFA. He is the most decorated player in the history of professional football having won 45 team trophies, including twelve Big Five league titles, four UEFA Champions Leagues, two Copa Américas, and one FIFA World Cup. Messi holds the records for most European Golden Shoes (6), most goals in a calendar year (91), most goals for a single club (672, with Barcelona), most goals (474), hat-tricks (36) and assists (192) in La Liga, most assists (18) and goal contributions (32) in the Copa América, most goal contributions (21) in the World Cup, most international appearances (191) and international goals (112) by a South American male, and the second-most in the latter category outright. A prolific goalscorer and creative playmaker, Messi has scored over 850 senior career goals and has provided over 380 assists for club and country.""",
        },
        {
            "section_name": "Early Career at Barcelona",
            "content": """Born in Rosario, Argentina, Messi relocated to Spain to join Barcelona at age 13, and made his competitive debut at age 17 in October 2004. He gradually established himself as an integral player for the club, and during his first uninterrupted season at age 22 in 2008–09 he helped Barcelona achieve the first treble in Spanish football. This resulted in Messi winning the first of four consecutive Ballons d'Or, and by the 2011–12 season he would set La Liga and European records for most goals in a season and establish himself as Barcelona's all-time top scorer. The following two seasons, he finished second for the Ballon d'Or behind Cristiano Ronaldo, his perceived career rival. However, he regained his best form during the 2014–15 campaign, where he became the all-time top scorer in La Liga, led Barcelona to a historic second treble, and won a fifth Ballon d'Or in 2015. He assumed Barcelona's captaincy in 2018 and won a record sixth Ballon d'Or in 2019. During his overall tenure at Barcelona, Messi won a club-record 34 trophies, including ten La Liga titles and four Champions Leagues, among others. Financial difficulties at Barcelona led to Messi signing with French club Paris Saint-Germain in August 2021, where he would win the Ligue 1 title during both of his seasons there. He joined Major League Soccer club Inter Miami in July 2023.""",
        },
        {
            "section_name": "International Career",
            "content": """An Argentine international, Messi is the national team's all-time leading goalscorer and most-capped player. His style of play as a diminutive, left-footed dribbler, drew career-long comparisons with compatriot Diego Maradona, who described Messi as his successor. At the youth level, he won the 2005 FIFA World Youth Championship and gold medal in the 2008 Summer Olympics. After his senior debut in 2005, Messi became the youngest Argentine to play and score in a World Cup in 2006. Assuming captaincy in 2011, he then led Argentina to three consecutive finals in the 2014 FIFA World Cup, the 2015 Copa América and the Copa América Centenario, all of which they would lose. After initially announcing his international retirement in 2016, he returned to help his country narrowly qualify for the 2018 FIFA World Cup, which they would exit early. Messi and the national team finally broke Argentina's 28-year trophy drought by winning the 2021 Copa América, which helped him secure his seventh Ballon d'Or that year. He then led Argentina to win the 2022 Finalissima, as well as the 2022 FIFA World Cup, his country's third overall world championship and first in 36 years. This followed with a record-extending eighth Ballon d'Or in 2023, and a victory in the 2024 Copa América.""",
        },
        # Add more sections as needed...
    ]

    # Load each section as a separate document
    for i, section in enumerate(sections):
        document = {
            "title": title,
            "section_name": section["section_name"],
            "content": section["content"],
            "wiki_link": wiki_link,
            "image_url": image_url,
            "section_order": i,
        }

        # Index the document
        es.index(index=INDEX_NAME, document=document)

    # Refresh the index to make documents searchable immediately
    es.indices.refresh(index=INDEX_NAME)


def cleanup():
    es.indices.delete(index=INDEX_NAME, ignore_unavailable=True)
    es.options(ignore_status=[400, 404]).inference.delete(inference_id="wiki-inference")


if __name__ == "__main__":
    print("Cleaning up")
    cleanup()
    print("Creating inference endpoint")
    create_inference_endpoint()
    print("Creating index and mappings")
    create_index_mapping()
    print("Loading data")
    load_messi_article()
