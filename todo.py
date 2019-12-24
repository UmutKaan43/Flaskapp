from flask import Flask,render_template,redirect,url_for,request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/asus/Desktop/Python 2.seviye/Flask_orm/todo.db' # veri tabanının adresini kayıt ettik
#burası servera kuracagın zaman farklı adresini os kutuphanesinden çekmen gerekicek
db = SQLAlchemy(app) # burada ise Orm yapısını db altında canlanırdık bunu c# taki dbcontext gibi dusun

class Todo(db.Model): #orm içindeki model yapısından turetmiş olduk
    id = db.Column(db.Integer, primary_key=True) #1.anahtar oluşunu true yaptık, ve 1. parametre olarak tipini belirttiik[ aynı c# daki gibi azcık farklı]
    title= db.Column(db.String(80))# stringe max karater yazabiliyor
    copmlete = db.Column(db.Boolean)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/Add",methods=["POST"]) # sadece post yazarak ayarlayailiriz
def addTodo():
    oz = request.form.get("title")
    yeni = Todo(title=oz,copmlete=False)
    db.session.add(yeni)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/Goster")
def goster():
    #ele = Todo.query.filter_by(id=id).first() # şimdi burada where yaptık --> todo sınıfıtan id'si id ye eşit olanı al dedik (User.query.all()hepsini çeker)
    todos = Todo.query.all()
    return render_template("Goster.html",items=todos)

@app.route("/Complete/<int:id>")
def ok(id):
    todo = Todo.query.filter_by(id=id).first() # sadece o id ye sahip olanı çektik
    if todo!=None:
        #if todo.copmlete:
        #    todo.copmlete=False
        #else:
        #    todo.copmlete=True""" 
        todo.copmlete= not todo.copmlete # yukarıdaki işlemın tek satır hali           
        db.session.commit()
        return redirect(url_for("goster"))

@app.route("/Delete/<int:id>")
def dele(id):
    todo = Todo.query.filter_by(id=id).first()
    if todo!=None:
        db.session.delete(todo)
        db.session.commit()
        return redirect(url_for("goster"))

if __name__=="__main__":
    db.create_all() # bunu uygulama calısmadan bir onceki asamada yaptık, unutma ustteki kısım fonksiyonlar allta ise asıl main kısmı var
    # bu c# da hazır halde geliyor. create_all() oluşmuş tabloları birkez daha oluşturmaz
    app.run(debug=True)

