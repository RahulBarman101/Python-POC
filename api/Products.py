from flask_restful import Resource
from flask import request
import os
from app import app
import sqlite3

VALID_EXTENSIONS = ['jpg','jpeg','png','PNG','JPG','JPEG']
class Products(Resource):
    def __init__(self):
        self.conn = sqlite3.connect('products.db')
        self.cur = self.conn.cursor()

    def get(self):
        products = []
        for row in (self.cur.execute("SELECT * FROM products")):
            products.append({
                'name':row[0],
                'price':row[1],
                'quantity':row[2],
                'image_path':row[3],
                })
        return products,200

    def is_valid_extension(self,filename):
        extension = filename.split('.')[-1]
        if extension in VALID_EXTENSIONS:
            return True
        return False
        
    
    def post(self):
        file = request.files['file']
        filename = file.filename
        if not self.is_valid_extension(filename):
            return {"message":"Not a valid file"},400
        filepath = os.path.join(app.config['UPLOAD_FOLDER'],filename)
        file.save(filepath)
        self.cur.execute("INSERT INTO products (name,price,quantity,img_path) VALUES (?,?,?,?)",
        (
            request.form.get('name'),
            request.form.get('price'),
            request.form.get('quantity'),
            filepath,
        ))
        self.conn.commit()
        tmp = {
            "name": request.form.get('name'),
            "price": request.form.get('price'),
            "quantity": request.form.get('quantity'),
            "file": filepath
        }
        return tmp,200

    def put(self,id):
        sql = "UPDATE products SET %s = ? WHERE id = ?"
        if request.form.get('name'):
            self.cur.execute(sql%('name'),(request.form.get('name'),id))
            self.conn.commit()
        if request.form.get('price'):
            self.cur.execute(sql%('price'),(request.form.get('price'),id))
            self.conn.commit()
        if request.form.get('quantity'):
            self.cur.execute(sql%('quantity'),(request.form.get('quantity'),id))
            self.conn.commit()
        return {"message": "commited"},200
    
    def delete(self,id):
        sql = "DELETE FROM products WHERE id = ?"
        self.cur.execute(sql,id)
        self.conn.commit()
        return {"message": "deleted"}
        
        
    