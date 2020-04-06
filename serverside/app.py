from flask import Flask,request,render_template , jsonify
import os
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

CURRENT_DIR=os.getcwd()
CURRENT_DIR = os.path.join(CURRENT_DIR, 'Images')

dir = os.path.join('D:\\code\\practices\\nextjs\\imgeUploadproject\\clientside\\public' , 'Images')

app = Flask(__name__)
CORS(app)
app.config["IMAGE_UPLOADS"] = dir

# Data Base
basedir = os.path.abspath(os.path.dirname(__file__))

# DataBase
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACKER_MODIFICATION'] = False


# init db
db = SQLAlchemy(app)

# init ma
ma = Marshmallow(app)



# Product class/model
class ImageModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    imagepath = db.Column(db.String(200))

    def __init__(self, imagepath):
        self.imagepath = imagepath

# product schema
class ImageSchema(ma.Schema):
    class Meta:
        fields = ('id', 'imagepath')

# init schema
image_schema = ImageSchema()
images_schema = ImageSchema(many=True) 



db.create_all()






# store image to directory and database
@app.route('/upload',methods=['POST'])
def uploadImage():
    if request.method == 'POST':
        if request.files:
            image = request.files['image']
            path = str(os.path.join('Images', image.filename))
            image.save(os.path.join(app.config["IMAGE_UPLOADS"], image.filename))

            imgpath = path.replace('\\' , '/')
            new_img_path = ImageModel(imgpath)
            db.session.add(new_img_path)
            db.session.commit()

            return image_schema.jsonify(new_img_path)
    return jsonify({'msg':'no image found'})

@app.route('/storedimages', methods=['GET'])
def storedimages():
    images_path = ImageModel.query.all()
    result = images_schema.dump(images_path)
    return jsonify(result)
@app.route('/hello', methods=['GET'])
def get():
    return jsonify({'msg': 'hello'})



if __name__ == '__main__':
    app.run(debug=True)
