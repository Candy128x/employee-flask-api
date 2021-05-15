from flask import Flask, jsonify, request
from flaskext.mysql import MySQL
from pobj import pobjl

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
    # return ','.join(list_val)
    return ','.join(map(str, list_val))

def list_to_str_v2(list_val):
    # return ','.join(list_val)
    res1 = '","'.join(map(str, list_val))
    return '"' + res1 + '"'


def insert_query(tbl_name: str, colms: list, vals: list) -> bool:
    db_conn = db_cursor = result = None
    try:
        db_query = 'INSERT INTO {table_name}({columns}) VALUES({values});'.format(table_name=tbl_name, columns=list_to_str(colms), values=list_to_str_v2(vals))
        # db_query = 'INSERT INTO {table_name}({columns}) VALUES(values);'.format(table_name=tbl_name, columns=list_to_str(colms), values=list_to_str(vals)
        logger.debug('---db_query: ---\n%s' % db_query)
        db_conn = mysql.connect()
        db_cursor = db_conn.cursor()
        db_cursor.execute(db_query)
        db_conn.commit()
        result = db_cursor.lastrowid
    except Exception as ex:
        logger.critical('---insert_query---EXCEPTION---', exc_info=True)
        raise Exeption
    finally:
        db_cursor.close()
        db_conn.close()
        return result


@app.route('/employee/create/', methods=['POST'])
def emp_create():
    try:
        result = None
        req_params = request.json
        logger.debug('---req_params: ---\n%s' % req_params)
        # -> Validate Request Params
        if req_params:
            is_created = insert_query('employee_details', list(req_params.keys()), list(req_params.values()))
            logger.debug('---is_created: ---\n%s' % is_created)
            if is_created:
                # result = jsonify({'message': ['Employee created successfully.']})
                result = jsonify('Employee created successfully.')
                result.status_code = 200
        return result
    except Exception as ex:
        logger.critical('---emp_create---EXCEPTION---msg:---\n%s' % str(ex))
        logger.critical('---emp_create---EXCEPTION---info---', exc_info=True)
        raise Exception

if __name__ == '__main__':
    app.run()