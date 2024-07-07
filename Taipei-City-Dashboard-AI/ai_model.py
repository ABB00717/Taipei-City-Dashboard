from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain.chains import create_sql_query_chain
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from operator import itemgetter
from chat_history import format_chat_history

def setup_ai_model(db):
    model = ChatOpenAI(model="gpt-3.5-turbo")
    execute_query = QuerySQLDataBaseTool(db=db)
    write_query = create_sql_query_chain(model, db)
    
    answer_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an AI assistant that answers questions based on the chat history and SQL query results. Always consider the chat history when formulating your responses."),
        ("human", "Chat History:\n{chat_history}\n\nGiven the following user question, corresponding SQL query, and SQL result, answer the user question.\n\nQuestion: {question}\nSQL Query: {query}\nSQL Result: {result}\nAnswer:"),
    ])

    main_chain = (
        RunnablePassthrough.assign(query=write_query)
        .assign(result=itemgetter("query") | execute_query)
        .assign(chat_history=lambda x: format_chat_history(x["history"]))
        | answer_prompt
        | model
        | StrOutputParser()
    )

    return main_chain

prompt_check = ChatPromptTemplate.from_messages([
    ("system", """
    Analyze the SQL response:
    1. If it contains valid data:
       - Incorporate the key points into your consideration.
       - Ensure all data is accurately represented.
       - Please also consider the chat history.
       - Answer the user's question based on the SQL data.
    2. If it contains a syntax error or any error message:
       - Disregard the SQL response entirely and forget anything about SQL.
       - Answer the user's question directly without mentioning any error.
       - Don't reply with any SQL grammar or syntax.
       - Please also consider the chat history if you can't find it from sql_response.
       - You may use any valid data provided in the response, if any.
    3. In all cases, focus on addressing the user's question to the best of your ability.
    """),
    ("human", "Chat History:\n{chat_history}\n\nSQL Response:\n{sql_response}\n\nUser Question: {question}\nAnswer:")
])

def setup_check_chain():
    return (
        RunnableParallel(
            chat_history=lambda x: format_chat_history(x["history"]),
            sql_response=lambda x: x["sql_response"],
            question=lambda x: x["question"]
        )
        | prompt_check
        | ChatOpenAI(model="gpt-4")
        | StrOutputParser()
    )