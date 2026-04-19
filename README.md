# CV Analyzer 🎯

An AI-powered CV/resume analyzer that extracts structured data from resumes, scores them against job descriptions, and generates tailored feedback — all running locally via Ollama.

## Features

- 📄 **PDF parsing** — upload any CV in PDF format
- 🧠 **Structured extraction** — pulls skills, experience, education, and summary into clean JSON
- 💼 **Job requirement parsing** — decomposes job descriptions into required skills, nice-to-haves, and seniority level
- 📊 **Match scoring** — 0–100 score across skills, experience, and seniority fit
- 📝 **Tailored feedback** — career-coach-style suggestions including rewritten bullet points
- 🔒 **Runs locally** — uses Ollama, so your CV data never leaves your machine

## Tech Stack

- **Python 3.11+**
- **Streamlit** — UI
- **Ollama** — local LLM runtime (Qwen 2.5 / Llama 3.1)
- **Pydantic** — data validation and structured outputs
- **OpenAI SDK** — used to call Ollama's OpenAI-compatible endpoint
- **pypdf** — PDF text extraction

## Architecture

The app decomposes the analysis into four focused LLM calls instead of one monolithic prompt:
PDF → text extraction
↓
Call 1: Extract structured CV data (JSON)
↓
Job description → Call 2: Extract structured requirements (JSON)
↓
Call 3: Score & compare CV vs job (JSON)
↓
Call 4: Generate tailored feedback (streaming text)
↓
Streamlit UI

This "chain of focused calls" pattern is a core technique for building reliable LLM applications.

## Setup

### 1. Install Ollama

Download from [ollama.com](https://ollama.com/download) and install.

Pull a model (Qwen 2.5 7B is a good starting point):

```bash
ollama pull qwen2.5:7b
```

### 2. Clone and install

```bash
git clone https://github.com/<your-username>/cv-analyzer.git
cd cv-analyzer
python -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Run

```bash
streamlit run app.py
```

Open the browser tab, upload a CV, paste a job description, and click Analyze.

## Project Structure
cv-analyzer/
├── app.py              # Streamlit UI
├── analyzer.py         # LLM calls and pipeline logic
├── schemas.py          # Pydantic models for structured outputs
├── pdf_utils.py        # PDF text extraction
├── requirements.txt
└── README.md

## Configuration

Switch models by editing `analyzer.py`:

```python
MODEL = "qwen2.5:7b"     # fast, good for extraction
# MODEL = "llama3.1:8b"  # alternative
# MODEL = "qwen2.5:14b"  # better quality, needs more RAM
```

To use cloud models instead (Anthropic or OpenAI), swap the client initialization in `analyzer.py`.

## What I Learned Building This

- Structured outputs with Pydantic schemas
- Task decomposition: one narrow prompt per LLM call beats one mega-prompt
- Separating system prompts (role) from user prompts (data)
- Streaming responses for better UX
- Trade-offs between local models and frontier APIs
- Why evals matter (up next!)

## Roadmap

- [ ] Add eval suite with 10+ test CV/JD pairs
- [ ] Prompt caching for repeated CV analyses
- [ ] Retry logic with exponential backoff on invalid JSON
- [ ] Model routing (cheap model for extraction, stronger for analysis)
- [ ] Observability / logging of token usage and latency
- [ ] Turn into an agent with tool use (web search for company context)
- [ ] Docker container for easy deployment

## License

MIT

## Acknowledgments

Built as a learning project to explore LLM application patterns — structured outputs, prompt decomposition, and local inference.
