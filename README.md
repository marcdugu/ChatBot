# 🧠 ChatBot Project (Weaviate + LLM)

An intelligent, retrieval-augmented chatbot system that lets you ask **FAQ or product-related questions** and get **context-aware answers** powered by **Weaviate (vector database)** and a **large language model (LLM)** such as Together AI or OpenAI.

Weaviate handles all **embedding and semantic search** inside Docker, while your Jupyter notebook orchestrates the **retrieval + generation** flow.

---

## ⚙️ How It Works — Chatbot Workflow

Imagine you’ve uploaded your company’s documentation or FAQs into the system.
Now you ask:

> “How can I reset my product’s access key?”

Here’s what happens step by step 👇

### 🧩 1. The Question (User Input)

You type your question into the notebook (or future UI/chat interface).

* The question is treated as a **query vector** by Weaviate.
* No local embedding code is needed — Weaviate’s internal `text2vec` module handles embedding creation.

### 🔍 2. Retrieval from Weaviate

Weaviate receives the vectorized question and performs a **similarity search** in its database:

* It compares your question’s vector with the stored vectors of your product documents, FAQs, or manuals.
* The top-K most semantically relevant text chunks are returned (these are the “context snippets”).

This ensures the chatbot doesn’t “hallucinate” — it grounds its answers in real company data.

### 🧠 3. Context Assembly

The notebook collects those top-K snippets and builds a **context-rich prompt** for the LLM:

```
User Question:
"How can I reset my product’s access key?"

Relevant Context:
1. "Access keys can be reset from the account settings page..."
2. "To generate a new key, navigate to..."

Instruction:
"Using the information above, answer clearly and concisely."
```

### 💬 4. Generation (LLM)

That structured prompt is sent to the LLM (Together AI or OpenAI).

The model:

* Reads the context retrieved from Weaviate.
* Generates a natural language answer grounded in those snippets.
* The result might be:

  > “You can reset your access key from the Account Settings → Security tab, then select ‘Generate New Key’.”


* **Weaviate (Vector DB)** – runs inside Docker; handles all embeddings and semantic search.
* **LLM API (Together / OpenAI)** – provides reasoning and natural-language generation.
* **Notebook** – coordinates the flow: ask → retrieve → generate → display.

---

## 🧪 Typical Use Cases

* **FAQ Chatbot** – upload company FAQs, ask questions in natural language.
* **Product Support Assistant** – give product manuals or help docs as knowledge base.
* **Documentation Query Bot** – search through technical docs or reports conversationally.
* **Knowledge RAG Demo** – educational project showing real retrieval-augmented generation flow.

---

## 🚀 Quickstart

1. **Start Weaviate**

   ```bash
   docker compose up -d
   ```

   This starts the vector database with its embedding module.

2. **(Optional) Add LLM API Key**

   ```bash
   export TOGETHER_API_KEY=...
   # or
   export OPENAI_API_KEY=...
   ```

3. **Open Notebook**

   ```bash
   jupyter notebook ChatBot_Proj.ipynb
   ```

4. **Run through the cells**:

   * Create schema
   * Ingest your FAQ or product data
   * Ask questions and see retrieval + LLM responses

---


## 🧰 Tech Stack

* **Weaviate** – Vector database for storage, embeddings, and semantic search
* **Together AI / OpenAI** – Text generation (LLM)
* **Python + Jupyter** – Orchestration and experimentation
* **Docker Compose** – Environment setup for Weaviate and its modules


