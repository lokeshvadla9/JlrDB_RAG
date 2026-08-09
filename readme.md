# 🚗 JLR Database Text-to-SQL RAG Chatbot

A hands-on practice project for querying a Microsoft SQL Server database using Natural Language. Powered by **Ollama**, **LLaMA 3.1**, and **LangChain**, this application translates user questions into syntactically correct T-SQL queries, executes them against a local JLR database, and returns conversational answers with short-term memory.

---

## 📽️ Demo & Sample Output

> Watch the chatbot in action below:

🎥 **[Output GIF (output.gif)](./output.gif)**


---

## 🏗️ Architecture & Pipeline

![Architecture Diagram](./Architecture.jpg)

### Key Features
* 🧠 **Conversational Memory**: Remembers context across follow-up questions (e.g., *"Who bought the most expensive car?"* ──► *"What is their email address?"*).
* 🛡️ **T-SQL Protection Rules**: Built-in prompt guardrails preventing common SQL Server `GROUP BY`, `JOIN`, and subquery syntax errors.
* ⚙️ **Configurable Infrastructure**: Environment variables decoupled via `.env` and `config.py` for database credentials and model settings.
* ⚡ **100% Local & Private**: Runs completely offline using Ollama without sending sensitive database data to external cloud APIs.

---

## 📂 Project Structure

```text
JLRDB_RAG/
│
├── .env                # Infrastructure & DB credentials configuration
├── .gitignore          # Git ignore rules
├── config.py           # Configuration loader
├── prompts.py          # T-SQL schema rules, memory prompts & few-shot examples
├── app.py              # Main execution loop & database chain
├── requirements.txt    # Python dependencies
└── output.GIF          # Demo output video/media file
```

## 🚀 Getting Started

### Step 1: Virtual Environment Setup
```bash
python -m venv venv
# Windows:
.\venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Pull Ollama Model & Run Application
```bash
ollama pull llama3.1
python app.py
```

---

## 💬 Sample Test Questions

* **Sales**: *"Which car company and model generated the highest total revenue?"*
* **Extreme Subquery**: *"List all customers who bought the costliest car and what is that car?"*
* **Inventory**: *"Which parts are currently low in stock or need reordering?"*
* **Follow-up Memory**:
  1. *"Who was the top customer by total spending?"*
  2. *"What is their email address?"*

---

## 🚀 Future Enhancements & Roadmap

1. **Decoupled Data Architecture (ETL Pipeline)**:
   * Build an **Apache Airflow** or **SSIS** ETL pipeline to extract production database tables into compressed flat files (**Parquet** / CSV).
   * Run natural language queries against the exported flat files using **DuckDB** to prevent hitting live production databases directly.
2. **Custom Interactive Chat Web UI**:
   * Replace the CLI console interface with a modern web dashboard built using **Streamlit**, **Gradio**, or **FastAPI + React**.
   * Display interactive data tables, query response benchmarks, and syntax-highlighted SQL execution paths.
3. **Enhanced Prompt Accuracy via Schema-RAG / Few-Shot Indexing**:
   * Store complex SQL query pairs in a local Vector Database (**ChromaDB** or **Qdrant**).
   * Dynamically retrieve and inject the most relevant T-SQL query examples based on user intent for complex multi-table joins.
4. **AST Query Validation & Security**:
   * Integrate an Abstract Syntax Tree (AST) parser (such as `sqlglot`) to strictly validate generated T-SQL prior to execution.
   * Reject non-`SELECT` statements (`DROP`, `DELETE`, `UPDATE`) and automatically enforce query timeout limits.