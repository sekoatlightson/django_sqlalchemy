from django.shortcuts import render
from sqlalchemy import create_engine
import os
from copy import deepcopy
from jinjasql import JinjaSql
#from six import string_types

basepath = os.path.dirname(os.path.abspath(__file__))

def quote_sql_string(value):
    '''
    If `value` is a string type, escapes single quotes in the string
    and returns the string enclosed in single quotes.
    '''
    if isinstance(value, str):
        new_value = str(value)
        new_value = new_value.replace("'", "''")
        return "'{}'".format(new_value)
    return value


def get_sql_from_template(query, bind_params):
    if not bind_params:
        return query
    params = deepcopy(bind_params)
    for key, val in params.items():
        params[key] = quote_sql_string(val)
    return query % params


def apply_sql_template(template, parameters):
    '''
    Apply a JinjaSql template (string) substituting parameters (dict) and return
    the final SQL.
    '''
    j = JinjaSql(param_style='pyformat')
    query, bind_params = j.prepare_query(template, parameters)
    return get_sql_from_template(query, bind_params)


def get_context_dic(engine,query):
    res = engine.execute(query)
    header = res.keys()
    results = []
    for rows in res.fetchall():
        row_dic = {}
        for key, value in zip(header,rows):
            row_dic[key] = value
        results.append(row_dic)
    #list(res)
    return header,results
    

def index(request):
    engine = create_engine('sqlite:///'+ os.path.join(basepath,'sqlite-sakila.sq'))
    #query = 'select title, rental_rate from film'
    header, results = get_context_dic(engine,query)
    context = {
        'columns': header,
        'rows' : results
    }

    return render(request, 'rental/rental_list.html', context)


def search(request):
    parameters = request.GET
    parameters = { 'rental_rate': request.GET.get('rental_rate'), 'length': request.GET.get('length')}
    print(parameters)
    engine = create_engine('sqlite:///'+ os.path.join(basepath,'sqlite-sakila.sq'))
    #query = 'select title, rental_rate , length from film'
    template = """
    SELECT title, rental_rate, length
    FROM film
    WHERE title <> ''
    {% if rettal_rate %} 
    AND rental_rate  < {{ rental_rate }}
    {% endif %}   
    {% if length %}
    AND length < {{ length }}
    {% endif %}
    """
    # parameters = {
    #     "rental_rate" : 3.0,
    #     "length" : 100
    # }

    query = apply_sql_template(template, parameters)
    print(query)
    header, results = get_context_dic(engine,query)
    context = {
        'columns': header,
        'rows' : results
    }

    # parameterを含むフルパス
    path_1 = request.get_full_path()
    print(path_1)

    # queryパラーメタの取得
    parameter = request.GET
    print(parameter)
    return render(request, 'rental/rental_list.html', context)
