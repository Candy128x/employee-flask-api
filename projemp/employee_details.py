from flask import flash, jsonify, request
from helper.db_helper import mysql
from app import app
import pymysql


# class EmployeeDetails:


def create_employee():
    db_conn = cursor = None
    try:
        _json = request.json
    except Exeption as ex:
        print(ex)