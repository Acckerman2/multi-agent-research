# 🕵️‍♂️ Multi-Agent Research System

A fully automated, multi-agent AI system built with Python, LangChain, and Mistral AI. This project utilizes a team of specialized AI agents to autonomously search the web, scrape content, write a comprehensive research report, and critically evaluate the final output. 

It also includes a sleek, dark-and-orange-themed Streamlit user interface for an improved user experience.

## ✨ Features

- **Search Agent:** Scours the web to find the most recent and relevant information on any given topic.
- **Reader/Scraper Agent:** Selects the top resource from the search results and scrapes the detailed content.
- **Writer Agent:** Compiles the raw search and scraped data into a structured, professional report (Introduction, Key Findings, Conclusion, Sources).
- **Critic Agent:** Reviews the writer's report, providing a score out of 10, highlighting strengths, and suggesting areas for improvement.
- **Web UI:** An easy-to-use Streamlit frontend to interact with the pipeline and view the step-by-step progress.

## 🛠️ Tech Stack

- **Python** (Core language)
- **LangChain & LangChain Agents** (Multi-agent orchestration)
- **Mistral AI** (LLM provider)
- **Streamlit** (Web Interface)
- **python-dotenv** (Environment variable management)

## 📁 Project Structure

```text
├── app.py             # Streamlit UI application
├── pipline.py         # Main execution pipeline connecting all agents
├── agent.py           # Defines the LLM, agents, and prompts (Writer/Critic chains)
├── tools.py           # Custom tools for web searching and scraping
├── requirements.txt   # Python dependencies
└── README.md          # Project documentation
```

## 🚀 Getting Started

### 1. Prerequisites
Ensure you have Python 3.8+ installed on your system.

### 2. Installation
Clone the repository and install the required dependencies:

```bash
git clone <your-repo-url>
cd multi-agent-system
pip install -r requirements.txt
```

### 3. Environment Variables
This project requires API keys to function (e.g., Mistral AI, and whatever search API you use in `tools.py`). Create a `.env` file in the root directory:

```env
MISTRAL_API_KEY=your_mistral_api_key_here
```

### 4. Running the Application

**Option A: Streamlit UI (Recommended)**
To run the graphical interface, use:
```bash
streamlit run app.py
```

**Option B: Terminal Interface**
To run the CLI version directly:
```bash
python pipline.py
```

## 🧠 How it Works

1. **Input:** The user provides a topic.
2. **Search:** `create_search_agent()` triggers `web_search` to find context.
3. **Scrape:** `create_scrape_agent()` triggers `scrape_url` to deep-dive into the best link.
4. **Draft:** The `writer_chain` structures a detailed markdown report based on gathered context.
5. **Review:** The `critic_chain` evaluates the report and returns constructive feedback.

## 📜 License
[MIT License](LICENSE)