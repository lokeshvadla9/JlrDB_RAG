import sys
from config import config
from prompts import sql_prompt, synthesis_prompt

# LangChain Imports
from langchain_community.utilities import SQLDatabase
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain_ollama import ChatOllama

# =====================================================================
# 1. Load Infrastructure Config from Config Object
# =====================================================================
print(f"Connecting to SQL Server: {config.DB_SERVER} | Database: {config.DB_NAME}...")

db = SQLDatabase.from_uri(
    config.get_db_uri(),
    include_tables=[
        "tblCar", "tblOrder", "tblCustomer", 
        "tblSalesTransaction", "tblEmployee", 
        "tblMaintenanceRecord", "tblServiceRecord", "tblWarranty",
        "tblPart", "tblInventory", "tblSupplier"
    ],
    sample_rows_in_table_info=2
)

print(f"Connected successfully to tables: {db.get_usable_table_names()}\n")

# Initialize ChatOllama with values from config
llm = ChatOllama(
    base_url=config.OLLAMA_BASE_URL,
    model=config.OLLAMA_MODEL,
    temperature=config.OLLAMA_TEMPERATURE
)

execute_query_tool = QuerySQLDataBaseTool(db=db)

# =====================================================================
# 2. Conversational Logic
# =====================================================================
def format_chat_history(history_list):
    if not history_list:
        return "None"
    formatted = []
    for turn in history_list[-3:]:
        formatted.append(f"User: {turn['question']}\nAI: {turn['answer']}")
    return "\n".join(formatted)

def generate_sql_query(inputs):
    question = inputs["question"]
    chat_history_str = format_chat_history(inputs.get("chat_history", []))
    table_info = db.get_table_info()
    
    prompt = sql_prompt.format(
        table_info=table_info, 
        question=question,
        chat_history=chat_history_str
    )
    response = llm.invoke(prompt)
    
    query = response.content.strip()
    if query.startswith("```sql"):
        query = query[6:]
    if query.startswith("```"):
        query = query[3:]
    if query.endswith("```"):
        query = query[:-3]
    return query.strip()

def summarize_answer(inputs):
    chat_history_str = format_chat_history(inputs.get("chat_history", []))
    prompt = synthesis_prompt.format(
        question=inputs["question"],
        query=inputs["query"],
        result=inputs["result"],
        chat_history=chat_history_str
    )
    response = llm.invoke(prompt)
    return response.content.strip()

# =====================================================================
# 3. Interactive Execution Loop
# =====================================================================
def run_app():
    print("=" * 60)
    print(f" JLR Database Chatbot [{config.OLLAMA_MODEL}] Ready!")
    print("=" * 60)

    chat_history = []

    while True:
        try:
            user_input = input("\nAsk a question: ")
            if user_input.strip().lower() in ["exit", "quit", "q"]:
                break
            if user_input.strip().lower() in ["clear", "reset"]:
                chat_history = []
                print("🧹 Chat memory cleared!")
                continue
            if not user_input.strip():
                continue

            print("\nThinking & querying database...")
            
            query = generate_sql_query({"question": user_input, "chat_history": chat_history})
            raw_result = execute_query_tool.invoke(query)
            final_answer = summarize_answer({
                "question": user_input, 
                "query": query, 
                "result": raw_result, 
                "chat_history": chat_history
            })

            print("\n[Generated T-SQL]:")
            print(f"  {query}")

            print("\n[Final Response]:")
            print(f"  {final_answer}")

            chat_history.append({"question": user_input, "answer": final_answer})

        except Exception as e:
            print(f"\nExecution Error: {e}")

if __name__ == "__main__":
    run_app()