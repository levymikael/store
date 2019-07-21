from bottle import route, run, template, static_file, get, post, delete, request
from sys import argv
import json
import pymysql
import store

connection = pymysql.connect(host='localhost',
                     user='root',
                     password='root',
                     db='store',
                     charset='utf8',
                     cursorclass=pymysql.cursors.DictCursor)



@get("/admin")
def admin_portal():
	return template("pages/admin.html")



@get("/")
def index():
    return template("index.html")


@get('/js/<filename:re:.*\.js>')
def javascripts(filename):
    return static_file(filename, root='js')


@get('/css/<filename:re:.*\.css>')
def stylesheets(filename):
    return static_file(filename, root='css')


@get('/images/<filename:re:.*\.(jpg|png|gif|ico)>')
def images(filename):
    return static_file(filename, root='images')


@post('/category')
def add_category():
    category_name = request.forms.get("name")
    with connection.cursor() as cursor:
            sql = "select category from category WHERE category = '{}'".format(category_name)
            cursor.execute(sql)
            result= cursor.fetchone()
            try:
                if result['category'] == category_name:
                    return json.dumps({"STATUS": "fail", "MSG": "", "CODE": 404})
            except:

                adding_category = 'INSERT INTO category (category) VALUES( % s) '
                val = (category_name)
                cursor.execute(adding_category, val)
                connection.commit()
                return json.dumps(category_name)



@get('/categories')
def show_category():
    with connection.cursor() as cursor:
        sql = "SELECT category FROM category"
        cursor.execute(sql)
        result = cursor.fetchall( )

    return json.dumps(result)


@delete('/categories/<id>')
def delete_category(id):
    with connection.cursor() as cursor:
        sql = "select cat_id from category WHERE cat_id = {}".format(id)
        cursor.execute(sql)

        result = cursor.fetchone()


        try:
            if int(id) == int(result['cat_id']):
                sql_t = "DELETE from category WHERE cat_id = {}".format(id)
                cursor.execute(sql_t)
                connection.commit()
                result = cursor.fetchone()

                return json.dumps({"STATUS": "success", "MSG": "category deleted successfully", "CODE": 201})
        except:

            return json.dumps({"STATUS": "fail", "MSG": "Category not found", "CODE": 404})


run(host='localhost', port=7040)

