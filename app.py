from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configurando o MySQL no SQLAlchem
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:senha_mysql@localhost/flask_crud'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo do banco de dados
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    posicao = db.Column(db.String(20), nullable=False)

with app.app_context():
    db.create_all()

@app.route("/")
def index():
    items = Item.query.all()
    return render_template("index.html", items=items)

@app.route("/cadastrar", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        nome = request.form["nome"]
        idade = request.form["idade"]
        posicao = request.form["posicao"]
        new_item = Item(nome=nome, idade=int(idade), posicao=posicao)
        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("cadastrar.html")

@app.route("/editar/<int:id>", methods=["GET", "POST"])
def update(id):
    item = Item.query.get_or_404(id)
    if request.method == "POST":
        item.nome = request.form["nome"]
        item.idade = int(request.form["idade"])
        item.posicao = request.form["posicao"]
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("editar.html", item=item)

@app.route("/deletar/<int:id>")
def delete(id):
    item = Item.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
