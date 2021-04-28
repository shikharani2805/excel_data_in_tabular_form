from flask import Flask, render_template, request
from flask_paginate import Pagination, get_page_args, get_page_parameter
from flask_pymongo import PyMongo
import pandas as pd
import json

app = Flask(__name__)

app.config['MONGO_URI'] = "mongodb://localhost:27017/web_excel_db"

mongo = PyMongo(app)

df = pd.read_excel("task_S.xlsx")
data = df.to_dict(orient = 'records')
columnNames = df.columns.values
# data = json.loads(df.to_json(orient='records'))

# mongo.db.web_excel_data.insert_many(data)

def get_users(offset=0, per_page=20):

    return data[offset: offset + per_page]

@app.route('/')
def index():

    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')

    total = len(data)

    pagination_users = get_users(offset=offset, per_page=per_page)

    pagination = Pagination(page=page,
                            per_page=per_page,
                            total=total,
                            css_framework='bootstrap4')

    return render_template('index.html',
                           data=pagination_users,
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           colnames=columnNames)


# @app.route('/')
# def excel_data():
#
#     data1 = pd.read_excel("task_S.xlsx")
#
#     data_json = json.loads(data1.to_json(orient='records'))
#
#     mongo.db.web_excel_data.insert_many(data_json)
#
#     excel_data =  data1.to_html()
#
#
#     return render_template('index.html',table=excel_data)



if __name__ == "__main__":
    app.run(debug=True)




