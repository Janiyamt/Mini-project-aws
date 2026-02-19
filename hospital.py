from flask import Flask, request, jsonify
import pymysql
#pip install pymysql

app = Flask(__name__)
products = []

# Database connection
connection = pymysql.connect(
    host='miniproject.c7aas8u6w0p5.ap-south-1.rds.amazonaws.com',
    user='admin',
    password='23455423',
    db='hospital',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

@app.route('/')
def hello_world():
    return 'Hello, World! Happy to see you'

@app.route('/welcome')
def welcome():
    return 'Welcome'

@app.route('/hospital', methods=['POST'])
def add_product():
    hospital_data = request.get_json()
    print("hospital data::",hospital_data)

    # Validate the product data
    if not all(key in hospital_data for key in ('name', 'email', 'mobile','address','location','pincode')):
        return jsonify({'message': 'Missing product data'}), 400

    #products.append(product_data)
    #return jsonify({'message': 'Product added successfully!'}), 201
    # Save product data to the database
    with connection.cursor() as cursor:
        sql = "INSERT INTO hospital1 (name, email, mobile,address,location,pincode) VALUES (%s, %s,%s, %s, %s,%s)"
        cursor.execute(sql, (hospital_data['name'], hospital_data['email'], int(hospital_data['mobile']),hospital_data['address'],hospital_data['location'], int(hospital_data['pincode'])))
    connection.commit()
    return jsonify({'message': 'Product added successfully!'}), 201

@app.route('/hospitals', methods=['GET'])
def get_products():
    #return jsonify({'products': products}), 200
    with connection.cursor() as cursor:
        sql = "SELECT * FROM hospital1"
        cursor.execute(sql)
        result = cursor.fetchall()
    return jsonify({'hospital': result}), 200

@app.route('/hospital/<int:code>', methods=['PUT'])
def update_product(code):
    hospital_data = request.get_json()

    # Validate the product data
    if not all(key in hospital_data for key in ('code', 'name', 'email', 'mobile','address','location','pincode')):
        return jsonify({'message': 'Missing product data which is required to process this request'}), 400

    # Update product data in the database
    with connection.cursor() as cursor:
        sql = "UPDATE hospital1 SET code = %s, name = %s,email = %s, mobile= %s,address= %s,location= %s,pincode= %s WHERE code = %s"
        cursor.execute(sql, (int(hospital_data['code']), hospital_data['name'], hospital_data['email'],int(hospital_data['mobile']),hospital_data['address'],hospital_data['location'],int(hospital_data['pincode']) , code))
    connection.commit()

    return jsonify({'message': 'Product updated successfully!'}), 200

@app.route('/hospital/<int:code>', methods=['DELETE'])
def delete_product(code):
    # Delete product from the database
    with connection.cursor() as cursor:
        sql = "DELETE FROM hospital1 WHERE code = %s"
        cursor.execute(sql, (int(code),))
    connection.commit()

    return jsonify({'message': 'Product deleted successfully!'}), 200




if __name__ == '__main__':
    app.run(host='0.0.0.0')
