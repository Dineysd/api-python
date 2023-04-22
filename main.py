# -*- coding: utf-8 -*-
import math
from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///produtos.db'
db = SQLAlchemy(app)


class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    codigo_produto = db.Column(db.Integer, nullable=False)
    codigo_fornecedor = db.Column(db.Integer, nullable=False)
    descricao_produto = db.Column(db.String(100), nullable=False)
    codigo_embalagem = db.Column(db.String(20))
    descricao_embalagem = db.Column(db.String(50))
    quantidade_embalagem = db.Column(db.Integer)
    codigo_barra = db.Column(db.String(20))
    estoque_baixo = db.Column(db.Integer)
    quantidade_caixa = db.Column(db.Integer)
    saldo_estoque = db.Column(db.Integer)
    permite_vender = db.Column(db.String(10))
    reservado = db.Column(db.String(10))
    peso = db.Column(db.String(10))
    status = db.Column(db.String(10))
    codigo_marca = db.Column(db.String(20))
    preco_custo = db.Column(db.Float)

    #preco = db.Column(db.Float, nullable=False)

with app.app_context():
    db.create_all()
    


@app.route('/produtos', methods=['POST'])
def criar_produto():
    barcode = request.json['codigo_barra']
    existing_product = Produto.query.filter_by(codigo_barra=barcode).first()
    if existing_product:
        return jsonify({'error': 'A product with the same barcode already exists.'}), 409
    
    novo_produto = Produto(codigo_produto=request.json['codigo_produto'], 
        descricao_produto=request.json['descricao_produto'], 
        codigo_fornecedor=request.json['codigo_fornecedor'],
        codigo_embalagem=request.json['codigo_embalagem'],
        descricao_embalagem=request.json['descricao_embalagem'],
        quantidade_embalagem=request.json['quantidade_embalagem'],
        codigo_barra=request.json['codigo_barra'],
        estoque_baixo=request.json['estoque_baixo'],
        quantidade_caixa=request.json['quantidade_caixa'],
        saldo_estoque=request.json['saldo_estoque'],
        permite_vender=request.json['permite_vender'],
        reservado=request.json['reservado'],
        peso=request.json['peso'],
        status=request.json['status'],
        codigo_marca=request.json['codigo_marca'],
        preco_custo=request.json['preco_custo'])
    db.session.add(novo_produto)
    db.session.commit()
    return jsonify({'id': novo_produto.id})


@app.route('/', methods=['GET'])
def index():
    return render_template('test.html')

@app.route('/produtos/paginacao', methods=['GET'])
def listar_produtos():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    produtos = Produto.query.paginate(page=page, per_page=per_page)
    result = []
    for produto in produtos.items:
        produto_data = {
            'id': produto.id,
            'codigo_produto': produto.codigo_produto,
            'codigo_fornecedor': produto.codigo_fornecedor,
            'descricao_produto': produto.descricao_produto,
            'codigo_embalagem': produto.codigo_embalagem,
            'descricao_embalagem': produto.descricao_embalagem,
            'quantidade_embalagem': produto.quantidade_embalagem,
            'codigo_barra': produto.codigo_barra,
            'estoque_baixo': produto.estoque_baixo,
            'quantidade_caixa': produto.quantidade_caixa,
            'saldo_estoque': produto.saldo_estoque,
            'permite_vender': produto.permite_vender,
            'reservado': produto.reservado,
            'peso': produto.peso,
            'status': produto.status,
            'codigo_marca': produto.codigo_marca,
            'preco_custo': produto.preco_custo
        }
        result.append(produto_data)
    return jsonify({'produtos': result})

@app.route('/produtos', methods=['GET'])
def listar_produtos_central():
    # Define a quantidade de produtos exibidos por página
    produtos_por_pagina = 50

    # Obtém a página atual a partir da URL (se não houver, assume como 1)
    pagina_atual = request.args.get('pagina', 1, type=int)

    # Obtém a lista de produtos da página atual
    produtos = Produto.query.paginate(page=pagina_atual, per_page=produtos_por_pagina)

    # Calcula o número total de páginas
    total_paginas = produtos.total // produtos_por_pagina
    if produtos.total % produtos_por_pagina != 0:
        total_paginas += 1

    return render_template('lista_produtos.html', produtos=produtos, pagina_atual=pagina_atual, total_paginas=total_paginas)


@app.route('/produtos/<int:id>', methods=['GET'])
def buscar_produto(id):
    produto = Produto.query.get(id)
    if produto:
        return jsonify({'id': produto.id, 'nome': produto.nome, 'preco': produto.preco})
    return jsonify({'mensagem': 'Produto não encontrado.'}), 404

@app.route('/produtos/<int:id>', methods=['PUT'])
def atualizar_produto(id):
    produto = Produto.query.get(id)
    if not produto:
        return jsonify({'mensagem': 'Produto não encontrado.'}), 404
    produto.nome = request.json['nome']
    produto.preco = request.json['preco']
    db.session.commit()
    return jsonify({'mensagem': 'Produto atualizado com sucesso.'})


@app.route('/produtos/<int:id>', methods=['DELETE'])
def deletar_produto(id):
    produto = Produto.query.get(id)
    if not produto:
        return jsonify({'mensagem': 'Produto não encontrado.'}), 404
    db.session.delete(produto)
    db.session.commit()
    return jsonify({'mensagem': 'Produto deletado com sucesso.'})


if __name__ == '__main__':
     app.run(host="0.0.0.0", port=5000, debug=True)



