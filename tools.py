import requests
from dotenv import load_dotenv
import os
from langchain.tools import tool
from bs4 import BeautifulSoup
from tavily import TavilyClient
from rich import print

load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def web_search(query: str) -> str:
    """Search the web for recent and relevant information in the topic .retrun title and url and snippet"""

    tavily_response = tavily.search(query=query, max_results=5)

    out = []

    for result in tavily_response["results"]:
      out.append(
       f"Title: {result['title']}\nURL: {result['url']}\nSnippet: {result['content'][:300]}\n"
     )

    return "\n_______\n".join(out)

@tool
def scrape_url(url: str) -> str:
    """Scrape and return clean text content from a given URL for deeper reading."""
    try:
        resp = requests.get(url, timeout=8, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(resp.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()
        return soup.get_text(separator=" ", strip=True)[:3000]
    except Exception as e:
        return f"Could not scrape URL: {str(e)}"
    

   
  

