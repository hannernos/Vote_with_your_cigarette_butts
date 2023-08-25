import pandas as pd
from sqlalchemy import create_engine
# pip install pandas
# pip install SQLAlchemy
from qt_display.msgDTO import msg_instance

import json

class QuestionDataFrame:
    _instance = None


    def __init__(self):
        self._data = None
        with open('mykey.json', 'r') as config_file:
            self.config = json.load(config_file)

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(QuestionDataFrame, cls).__new__(cls)
            cls._instance._init_data()
        return cls._instance

    def _init_data(self):
        self._data = pd.DataFrame(columns=['question_ID', 'content', 'group', 'category', 'optionA', 'optionB', 'type'])
    
    def load_data_from_mysql(self):
        try:

            connection_str = self.config["db_connection"]
            engine = create_engine(connection_str)
            group_value = 3

            query = "SELECT * FROM question WHERE `group` = {}".format(group_value)
            self._data = pd.read_sql(query, engine)
            
            # question id -> 1부터로 재조정->할경우 투표마다 (min_id-1)더해서 보내줘야함
            min_id = self._data['question_ID'].min()
            self._data['question_ID'] = self._data['question_ID'] - (min_id - 1)
            msg_instance.question_offset = min_id - 1

        except Exception as err:
            print("Error: {}".format(err))

    @property
    def data(self):
        return self._data

question_df_instance = QuestionDataFrame()

if __name__ == "__main__":
    df_instance = QuestionDataFrame()
    df_instance.load_data_from_mysql()

    print(df_instance.data)
