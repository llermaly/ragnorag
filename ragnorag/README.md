# ragnorag

This is a Streamlit application that demonstrates how to create a Q&A system without relying on an LLM to generate answers.

For this example, we're using a Wikipedia article about Lionel Messi. The app uses Elasticsearch's semantic search to find the most relevant chunks of text to answer your questions.

## How it works

1. We load Wikipedia article sections into Elasticsearch
   - Each section becomes a separate document
   - Elasticsearch handles the sentence chunking for us
2. You ask a question through the Streamlit UI
3. Our app runs an Elasticsearch query to find the most relevant section and chunk
4. You get back:
   - The most relevant answer
   - Wikipedia article details
   - A "show more" button to see the full context

## Quickstart

1. First, install the project dependencies using Poetry:
```bash
poetry install
```

2. Set up your Elasticsearch credentials in `load_data.py`:
```python
os.environ["ELASTIC_ENDPOINT"] = "your_endpoint_here"
os.environ["ELASTIC_API_KEY"] = "your_api_key_here"
```

3. Load the demo data:
```bash
python load_data.py
```

4. Run the Streamlit app:
```bash
streamlit run ui.py
```

That's it! Start asking questions about Messi! 🚀⚽

## Components

- `ui.py`: The Streamlit UI that handles questions and displays answers with Wikipedia info
- `es.py`: Contains all the Elasticsearch query magic
- `load_data.py`: Handles loading the demo data into Elasticsearch
- `cleanup.py`: Contains methods to clean up everything when you're done

## Want to try with different Wikipedia articles?

Check out the `load_messi_article()` function in `load_data.py` - you can use it as a template to load other articles. Just make sure to update the title, wiki link, image URL, and content sections!