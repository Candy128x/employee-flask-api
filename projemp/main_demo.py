from flask import Flask, jsonify, request
from flaskext.mysql import MySQL
from pobj import pobjl
import json

app = Flask(__name__)
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'qwerty'
app.config['MYSQL_DATABASE_DB'] = 'employee_db'
app.config['MYSQL_DATABASE_HOST'] = '127.0.0.1'
mysql.init_app(app)
logger = pobjl('dev-env', 'debug')


@app.route('/', methods=['GET'])
@app.route('/home/', methods=['GET'])
def home():
    return 'Hello Developer :]'


def list_to_str(list_val):
    return ','.join(list_val)

def list_to_str_v2(list_val):
    res1 = '","'.join(map(str, list_val))
    return '"' + res1 + '"'

def list_to_str_v3(list_val):
    text = []
    for val in list_val:
        if isinstance(val, str):
            text.append(str(val))
        else:
            text.append(val)
    return ','.join(text)


def dict_to_str(dict_vals: dict):
    res1 = []
    for k, v in dict_vals.items():
        if isinstance(v, int):
            statement = str(k) + '=' + str(v)
        else:
            statement = str(k) + '="' + str(v) + '"'
        res1.append(statement)
    return ','.join(res1)


def db_query_exec(action, db_query) -> bool:
    db_conn = db_cursor = result = None
    try:
        logger.debug('---db_query: ---\n%s' % db_query)
        db_conn = mysql.connect()
        db_cursor = db_conn.cursor()
        db_cursor.execute(db_query)
        db_conn.commit()

        if 'insert' == action:
            result = db_cursor.lastrowid
        elif 'update' == action:
            result = True
        elif 'select' == action:
            # rows = cursor.fetchall()

            rows = db_cursor.fetchone()
            result = str(rows)

            # row_headers = [x[0] for x in db_cursor.description]  # this will extract row headers
            # rv = db_cursor.fetchall()
            # json_data = []
            # for result in rv:
            #     json_data.append(dict(zip(row_headers, result)))
            # result = json.dumps(json_data)

    except Exception as ex:
        logger.critical('---db_query_exec---EXCEPTION---', exc_info=True)
        raise Exeption
    finally:
        db_cursor.close()
        db_conn.close()
        return result

def api_response(status_code=400, status='failed', message=[], data=[]):
    """
    # -> API Response Common Function
    :param status_code:
    :param status: success / failed
    :param message:
    :param data:
    :return:
    """
    result = jsonify({'status_code': status_code, 'status': status, 'message': message, 'data': data})
    result.status_code = status_code
    return result


@app.route('/employee/create/', methods=['POST'])
def emp_create():
    try:
        api_code, api_status, msg, data = 400, 'failed', [], []
        req_params = request.json
        logger.debug('---req_params: ---\n%s' % req_params)
        # -> Validate Request Params
        if req_params:
            query_statement = 'INSERT INTO {table_name}({columns}) VALUES({values});'.format(table_name='employee_details',
                columns=list_to_str(list(req_params.keys())), values=list_to_str_v2(list(req_params.values())))
            is_created = db_query_exec('insert', query_statement)
            logger.debug('---is_created: ---\n%s' % is_created)
            if is_created:
                api_code = 201
                api_status = 'success'
                msg.append('Employee created successfully.')
                data.append({'employee_id': is_created})
        return api_response(api_code, api_status, msg, data)
    except Exception as ex:
        logger.critical('---emp_create---EXCEPTION---msg:---\n%s' % str(ex))
        logger.critical('---emp_create---EXCEPTION---info---', exc_info=True)
        raise Exception


@app.route('/employee/update/<int:id>/', methods=['PUT'])
def emp_update(id):
    try:
        api_code, api_status, msg, data = 400, 'failed', [], []
        req_params = request.json
        logger.debug('---emp_update---req_params: ---\n%s' % req_params)
        # -> Validate Request Params
        if req_params:
            query_statement = 'UPDATE {table_name} SET {columns_and_vals} WHERE {where_cond};'.format(table_name='employee_details',
                columns_and_vals=dict_to_str(req_params), where_cond=dict_to_str({'id': id}))
            is_updated = db_query_exec('update', query_statement)
            logger.debug('---is_updated: ---\n%s' % is_updated)
            if is_updated:
                api_code = 200
                api_status = 'success'
                msg.append('Employee updated successfully.')
        return api_response(api_code, api_status, msg, data)
    except Exception as ex:
        logger.critical('---emp_update---EXCEPTION---msg:---\n%s' % str(ex))
        logger.critical('---emp_update---EXCEPTION---info---', exc_info=True)
        raise Exception


@app.route('/employee/read/<int:id>/', methods=['GET'])
def emp_select_by_id(id):
    try:
        api_code, api_status, msg, data = 400, 'failed', [], []
        logger.debug('---emp_select_by_id---req_params---id: ---\n%s' % id)
        # -> Validate Request Params
        if id:
            query_statement = 'SELECT * FROM {table_name} WHERE {where_cond};'.format(table_name='employee_details', where_cond=dict_to_str({'id': id}))
            fetch_data = db_query_exec('select', query_statement)
            logger.debug('---fetch_data: ---\n%s' % fetch_data)
            if fetch_data:
                api_code = 200
                api_status = 'success'
                msg.append('Employee details fetch successfully.')
                data.append(fetch_data)
        return api_response(api_code, api_status, msg, data)
    except Exception as ex:
        logger.critical('---emp_select_by_id---EXCEPTION---msg:---\n%s' % str(ex))
        logger.critical('---emp_select_by_id---EXCEPTION---info---', exc_info=True)
        raise Exception


if __name__ == '__main__':
    app.run(debug=True)