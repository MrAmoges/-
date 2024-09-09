import psycopg2

db_name = 'Style'
user = 'postgres'
host = 'localhost'
port = 5432
password = '9004'

connect = psycopg2.connect(database=db_name, user=user, port=port, host=host, password=password)
cursor = connect.cursor()


def check_user(telegram_id):
    db_name = 'Style'
    user = 'postgres'
    host = 'localhost'
    port = 5432
    password = '9004'

    connect = psycopg2.connect(database=db_name, user=user, port=port, host=host, password=password)
    cursor = connect.cursor()

    cursor.execute(f" SELECT telegram_id FROM users WHERE telegram_id = {telegram_id}; ")

    user = cursor.fetchone()

    if user:
        return True
    
    else:
        return False
    


def register_user(username, phone_number, telegram_id):
    db_name = 'Style'
    user = 'postgres'
    host = 'localhost'
    port = 5432
    password = '9004'
    

    connect = psycopg2.connect(database=db_name, user=user, port=port, host=host, password=password)
    cursor = connect.cursor()

    cursor.execute(
        """
        INSERT INTO users 
        (user_name, phone_number, telegram_id) 
        VALUES (%s, %s, %s);""", (username, phone_number, telegram_id)
    )

    connect.commit()
    connect.close()



def add_feedback(telegram_id, user_feedback):
    connect = psycopg2.connect(database=db_name, user=user, port=port, host=host, password=password)
    cursor = connect.cursor()
    
    cursor.execute(" INSERT INTO feedback (telegram_id, user_feedback) VALUES (%s, %s);", (telegram_id, user_feedback))

    connect.commit()
    connect.close()


def delete_feedback(telegram_id):
    connect = psycopg2.connect(database=db_name, user=user, port=port, host=host, password=password)
    cursor = connect.cursor()

    cursor.execute('DELETE FROM feedback WHERE telegram_id= %s ;', (telegram_id,))

    connect.commit()
    connect.close()


def select_user_orders(telegram_id):
    connect = psycopg2.connect(database=db_name, user=user, port=port, host=host, password=password)
    cursor = connect.cursor()

    cursor.execute('SELECT * FROM orders WHERE telegram_id=%s;', (telegram_id,))

    data = cursor.fetchall()

    return data


def add_product(product_name, product_desc, product_photo, product_price):
    connect = psycopg2.connect(database=db_name, user=user, port=port, host=host, password=password)
    cursor = connect.cursor()

    cursor.execute("INSERT INTO products (product_name, description, photo, product_price) VALUES (%s, %s, %s, %s);", 
                   (product_name, product_desc, product_photo, product_price))
    
    connect.commit()
    connect.close()


def delete_product_by_name(product_name):
    connect = psycopg2.connect(database=db_name, user=user, port=port, host=host, password=password)
    cursor = connect.cursor()

    cursor.execute("DELETE FROM products WHERE product_name=%s;", (product_name,))

    connect.commit()
    connect.close()
    

def add_product_to_basket(telegram_id, product_name, product_amount, total_price, location):
    connect = psycopg2.connect(database=db_name, user=user, port=port, host=host, password=password)
    cursor = connect.cursor()

    cursor.execute("INSERT INTO basket (telegram_id, product_name, product_amount, total_price, location) VALUES (%s, %s, %s, %s, %s);", (telegram_id, product_name, product_amount, total_price, location))

    connect.commit()
    connect.close()


def delete_product_from_basket(telegram_id):
    connect = psycopg2.connect(database=db_name, user=user, port=port, host=host, password=password)
    cursor = connect.cursor()

    cursor.execute("DELETE FROM basket WHERE telegram_id=%s;", (telegram_id,))

    connect.commit()
    connect.close()


def select_all_products():
    connect = psycopg2.connect(database=db_name, user=user, port=port, host=host, password=password)
    cursor = connect.cursor()

    cursor.execute("SELECT * FROM products;")
    data = cursor.fetchall()

    return data



def select_current_product_by_name(product_name):
    connect = psycopg2.connect(database=db_name, user=user, port=port, host=host, password=password)
    cursor = connect.cursor()

    cursor.execute("SELECT * FROM products WHERE product_name=%s;", (product_name))
    data = cursor.fetchall()

    return data



def select_products_name():
    connect = psycopg2.connect(database=db_name, user=user, port=port, host=host, password=password)
    cursor = connect.cursor()

    cursor = connect.cursor("SELECT producy_name FROM products;")
    data = cursor.fetchall()

    cursor.execute