from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from academia import db
from sqlalchemy import and_

class Usuario(db.Model):
	idUsuario = db.Column(db.Integer, primary_key = True)
	Nome = db.Column(db.String(150))
	DataNascimento = db.Column(db.String(20))
	Cpf = db.Column(db.String(20))
	Rg = db.Column(db.String(20))
	Rua = db.Column(db.String(150))
	Numero = db.Column(db.Integer)
	Bairro = db.Column(db.String(100)) 
	Cidade = db.Column(db.String(100))
	Estado = db.Column(db.String(100))
	Email = db.Column(db.String(150))
	Senha = db.Column(db.String(15))
	#cliente, admin
	Tipo = db.Column(db.String(15))

	#referencia incricoao
	inscricoes =   db.relationship(
		'Inscricao',
		backref='usuario',
		lazy = 'dynamic'
		)

	def __init__(self,nome,dataNascimento,cpf,rg,rua,numero,bairro,cidade,estado,email,senha,tipo):
		self.Nome = nome
		self.DataNascimento = dataNascimento
		self.Rg = rg
		self.Cpf = cpf
		self.Rua = rua
		self.Numero = numero
		self.Bairro = bairro
		self.Cidade = cidade
		self.Estado = estado
		self.Email = email
		self.Senha = senha
		self.Tipo = tipo 


#Relacionamento entre academia e planos
PlanosAcademia = db.Table('PlanosAcademia',
 	db.Column('idAcademia', db.Integer, db.ForeignKey('academia.idAcademia')),
 	db.Column('idPlano', db.Integer, db.ForeignKey('plano.idPlano'))
 	)


class Academia(db.Model):
	idAcademia = db.Column(db.Integer, primary_key = True)
	Nome = db.Column(db.String(150))
	Cnpj = db.Column(db.String(20))
	Rua = db.Column(db.String(150))
	Numero = db.Column(db.Integer)
	Bairro = db.Column(db.String(100))
	Cidade = db.Column(db.String(100))
	Estado = db.Column(db.String(100))
	Email = db.Column(db.String(150))

	#referencia planoAcademia
	planos = db.relationship(

		'Plano',

		secondary = PlanosAcademia,

		backref = db.backref(
			'academia',
			lazy = 'dynamic'))

	#referencia incricao
	inscricoes =   db.relationship(
		'Inscricao',
		backref='academia',
		lazy = 'dynamic'
		)

	def __init__(self,nome,cnpj,rua,numero,bairro,cidade,estado,email):
		self.Nome = nome
		self.Cnpj = cnpj
		self.Rua = rua
		self.Numero = numero
		self.Bairro = bairro
		self.Cidade = cidade
		self.Estado = estado
		self.Email = email

class Plano(db.Model):
	idPlano = db.Column(db.Integer, primary_key = True)
	Nome = db.Column(db.String(50))
	Descricao = db.Column(db.String(150))
	Valor = db.Column(db.Float)
	#dias
	Validade = db.Column(db.Integer)

	
	#referencia incricao
	inscricoes =   db.relationship(
		'Inscricao',
		backref='plano',
		lazy = 'dynamic'
		)

	def __init__(self, nome,descricao,valor,validade):
		self.Nome = nome
		self.Descricao = descricao
		self.Valor = valor
		self.Validade = validade



#relacionamento entre usuario, academia, plano, juntamente com o parametro proprio 'DataVencimento'
class Inscricao(db.Model):
	idInscricao = db.Column(db.Integer, primary_key = True)
	idUsuario = db.Column(db.Integer, db.ForeignKey('usuario.idUsuario'))
	idAcademia = db.Column(db.Integer, db.ForeignKey('academia.idAcademia'))
	idPlano = db.Column(db.Integer, db.ForeignKey('plano.idPlano'))
	DataVencimento = db.Column(db.Date)

	def __init__(self, datavencimento):
		#basta adicionar a data, as chaves estrangeiras serão preenchidas com a passagem da relação
		self.DataVencimento = datavencimento




