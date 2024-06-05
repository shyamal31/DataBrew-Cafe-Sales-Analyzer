from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from langchain.prompts import ChatPromptTemplate
# from langchain.chat_models import AzureChatOpenAI
from langchain_openai import OpenAI,ChatOpenAI
from sqlalchemy import create_engine
from langchain.sql_database import SQLDatabase 
from dotenv import load_dotenv
from getpass import getpass
import os
from sql_connection import cntdb

class own_data():

    def __init__(self, Database, LLM):
        self.Database = Database
        self.LLM = LLM

    def get_schema(self,_):
        return self.Database.get_table_info()

    
    def prsql_query(self, User_Input):
        sql_template = """Based on the table schema below, question, write a SQL query that would answer the user's question.:
        {schema}
        Question: {question} 
        SQL Query:"""
        prompt = ChatPromptTemplate.from_template(sql_template)

        model = self.LLM

        sql_response = (
            RunnablePassthrough.assign(schema = self.get_schema)
            | prompt
            | model.bind(stop = ["\nSQLResult:" ])
            | StrOutputParser()
        )
     
        try:
            results = sql_response.invoke({"question": User_Input})
        except Exception as e:
            results = str(e)
        return sql_response, results
    
    def prtext_query(self, User_Input):
        template = """Based on the table schema below, question, sql query and sql response, write a natural language response. :
        {schema}
        Question: {question}
        SQL Query: {query}
        SQL Response: {response}
        AI Response:"""
        prompt_response= ChatPromptTemplate.from_template(template)

        sql_response,query_res = self.prsql_query(User_Input)
        model = self.LLM

        full_chain = (
            RunnablePassthrough.assign(query = sql_response)
            | RunnablePassthrough.assign(
                schema = self.get_schema,
                response = lambda x: self.Database.run(x['query']),
            )
            | prompt_response
            | model
        )
        try:
            resultsf = full_chain.invoke({"question": User_Input})
        except Exception as e:
            resultsf = str(e)
        return resultsf, query_res

def cntopenai():
    load_dotenv()   
    openai_api_key = os.getenv("OPENAI_API_KEY") or getpass("Enter your OpenAI key: ")
    llm = ChatOpenAI(model_name = "gpt-4", openai_api_key = openai_api_key)
    return llm


if __name__ == "__main__":
    llm = cntopenai()
    db= cntdb()
    model = own_data(db,llm)

    # print(model.prtext_query("Please find number of unique products."))
    # print(model.prtext_query("Please tell me which is the highest selling product by sales"))
    # print()
    # print(model.prsql_query("Please tell me which is the highest selling product by sales"))

    # print(model.prtext_query("For each category list top 5 best selling items by sales"))
    # print(model.prtext_query("For each product category, list top 5 best selling products by total amount of sales"))
    # print()
    # print(model.prsql_query("list top 5 best selling items from each category of products"))
    # print(model.prtext_query("which special product has made highest sales by amount? give me the name of the product and in which season it has made the sale"))
    # print(model.prsql_query("which special product has made highest sales by amount? give me the name of the product and in which season it has made the sale"))

    #can it generate multiple query and answers?
    # Also what is the amount of total purchase throughout the year ny this customer
    response, sql_query = model.prtext_query("can you tell me which customer has made highest amount of purchase on a single day and what did he/she buy?")
    print(f'Model Response{response.content}')
    print(f'SQL QUERY: {sql_query}')
    # print(model.prtext_query("Can you tell me the detail of customer who made highest purchase of Muffin in July 2023?"))
    # print(model.prtext_query("can you tell me which customer has made highest amount of purchase on a single day? also can you tell me overall purchase made by that customer over the entire year?"))
    # print(model.prsql_query("can you tell me which customer has made highest amount of purchase on a single day? also can you tell me overall purchase made by that customer over the entire year?"))

        
    
    
