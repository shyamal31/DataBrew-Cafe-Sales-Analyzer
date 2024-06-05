from sqlalchemy.engine.url import URL
from dotenv import load_dotenv
import os
from langchain.sql_database import SQLDatabase 
from sqlalchemy import create_engine

#database connection

def cntdb():
        load_dotenv()
        username = os.getenv("USERNAME")
        password = os.getenv("PASSWORD")
        port = os.getenv("PORT")
        database = os.getenv("DATABASE")
        connection_string = f'mysql+mysqlconnector://{username}:{password}@localhost:3306/{database}'
        print(connection_string)
        try:
            engine = create_engine(connection_string)
            connection = engine.connect()
            if connection:
                print('Connection successful')
                db = SQLDatabase.from_uri(connection_string)
                return db
            else:
                print('Not connected')
            
        except Exception as e:
            print("Connection failed:", e)

if __name__ == "__main__":
        db =cntdb()
        print(db.get_table_info())