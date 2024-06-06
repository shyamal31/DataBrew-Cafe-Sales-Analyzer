# DataBrew-Cafe-sales-Analyzer
An innovative LLM application for a local cafe, employing Langchain and RAG to deliver direct, natural language responses to fetch queries on the cafe sales database. It also helps to provide some advanced insights and reasoning on data. 


## File Structure:

Data: This folder contains the cafe data
llm_app.py: A llm chatbot application made with streamlit
sql_connection.py: Connects the LLM pipeline to a SQL database, where the data is stored
model_test.py: Logic of LLM is written using langchain framework

## Installation and Setup guide

1. Clone this github repository to your local machine.
   ```shell
   git clone https://github.com/shyamal31/DataBrew-Cafe-sales-Analyzer.git
   ```
2. Install the required dependancies
   ```shell
   pip3 install -r requirements.txt
   ```
3. Make sure to push all the data into an SQL database. Here I used MYSQL Workbench. Modify the database details(username, password, port, database name etc.)
4. Run streamlit chatbot application
  ```shell
  streamlit run llm_app.py
  ```
<img width="870" alt="image" src="https://github.com/shyamal31/DataBrew-Cafe-sales-Analyzer/assets/57554284/270c2dc3-d7d4-434a-99c9-5891936b3165">
