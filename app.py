from email.header import decode_header
from flask import *
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import redirect, secure_filename
import os

app = Flask(__name__)
UPLOAD_FOLDER = "static/styles/images"
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sqlite3.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


db = SQLAlchemy(app)


class Receipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    receipe_name = db.Column(db.String, unique=True, nullable=False)
    receipe_making = db.Column(db.String, unique=False, nullable=False)
    image_path = db.Column(db.String, unique=False, nullable=False)
    desc = db.Column(db.String, unique=False, nullable=False)


@app.route("/")
def homepage():
    isEmpty = len(Receipe.query.all()) == 0
    if isEmpty:
        return render_template("home.html", receipes=Receipe.query.all(), isEmpty=True)
    return render_template("home.html", receipes=Receipe.query.all(), id=Receipe.query.all()[0].id, isEmpty=False)


@app.route('/cb/<id>')
def cb(id):

    r = Receipe.query.filter_by(id=id)[0]
    return render_template("cb.html", receipe=r)


@app.route('/newrecipe', methods=["POST"])
def newRecipe():
    name = request.form.get("recipe_name")
    receipe_making = request.form.get("receipe_making")
    desc = request.form.get("desc")
    file = request.files["fileinput"]

    r1 = Receipe(receipe_name=name, receipe_making=receipe_making,
                 image_path="static\styles\images\{}".format(secure_filename(file.filename)), desc=desc)
    db.session.add(r1)
    db.session.commit()
    file.save(app.config['UPLOAD_FOLDER'] +
              os.sep + secure_filename(file.filename))
    return redirect(url_for("homepage"))


@app.route("/delete/<id>", methods=["POST"])
def delete(id):
    r = Receipe.query.filter_by(id=id)[0]
    os.remove(r.image_path)
    db.session.delete(r)
    db.session.commit()
    return redirect(url_for("homepage"))


if __name__ == '__main__':
    app.run(debug=True)
