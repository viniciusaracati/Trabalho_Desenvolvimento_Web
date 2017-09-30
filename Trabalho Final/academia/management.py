from datetime import *
from academia import models
from academia import db



#Variavel local

usuario_logado = 'Admin'
usuario_tipo = 'admin'
id_logado = 0


#Funções


#inserções
def inserirUsuarioCliente(nome,dataNascimento,cpf,rg,rua,numero,bairro,cidade,estado,email,senha):
	#cria novo e passa os dados
	novoUsuario = models.Usuario(nome,dataNascimento,cpf,rg,rua,numero,bairro,cidade,estado,email,senha,'cliente')
	#adiciona ao banco
	db.session.add(novoUsuario)
	#realiza a ação
	db.session.commit()

def inserirUsuarioAdmin(nome,dataNascimento,cpf,rg,rua,numero,bairro,cidade,estado,email,senha):
	#cria novo e passa os dados
	novoUsuario = models.Usuario(nome,dataNascimento,cpf,rg,rua,numero,bairro,cidade,estado,email,senha,'admin')
	#adiciona ao banco
	db.session.add(novoUsuario)
	#realiza a ação
	db.session.commit()


def inserirAcademia(nome,cnpj,rua,numero,bairro,cidade,estado,email):
	#cria novo e passa os dados
	novaAcademia = models.Academia(nome,cnpj,rua,numero,bairro,cidade,estado,email)
	#adiciona ao banco
	db.session.add(novaAcademia)
	#realiza a ação
	db.session.commit()

def inserirPlano(nome,descricao,valor,validade):
	#cria novo e passa os dados
	novoPlano = models.Plano(nome,descricao,valor,validade)
	#adiciona ao banco
	db.session.add(novoPlano)
	#realiza a ação
	db.session.commit()

def inserirPlanosAcademia(academia, plano):
	#adiciona plano em academia(nas referencias)
	academia.planos.append(plano)
	#realiza ação
	db.session.commit()


def inserirInscricao(usuario, academia, plano):

	#verifica se a academia e plano inseridos estão relacionados, se estiverem, será feito a inscrição, 	
	if(verificaPlanosAcademia(plano,academia) == True):		
		#pegar data de vencimento
		dataVencimento = adicionarVencimento(plano.Validade)
		#cria novo e passa os dados
		novaInscricao = models.Inscricao(dataVencimento)
		#adiciona ao banco
		db.session.add(novaInscricao)
		#realiza a ação
		db.session.commit()

		#adicionar referencia da inscição nova em: usuario, academia, plano
		usuario.inscricoes.append(novaInscricao)
		academia.inscricoes.append(novaInscricao)
		plano.inscricoes.append(novaInscricao)

		#realiza a ação
		db.session.commit()






#verificações 

#Verificações de Relações, será utilizado na exclusão, verifica se os valores no banco, possuem relações com algum outro
def verificaRelacoesUsuario(id):
	existeUsurio = models.Inscricao.query.filter_by(idUsuario = id).first()
	if(existeUsurio is None):
		return False
	else:	
		return True


def verificaRelacoesAcademia(id):
	
	academia_local = models.Academia.query.filter_by(idAcademia = id).first()

	#Se academia não esta relacionada a nenhum plano
	if(academia_local.planos == []):
		#caso nao esteja, verifica se esta em relacionada em inscricao				
		existeAcademia = models.Inscricao.query.filter_by(idAcademia = id).first()
		#se nao tiver retorna falso
		if(existeAcademia is None):
			return False
		else:
			#se tiver retorna true
			return True

	else:
		return True

	


def verificaRelacoesPlano(id):
	
	academias = models.Academia.query.all()
	verif = 0

	#percorre as academias
	for noA in academias:
		#verifica os planos relacionados a cada academia
		for noP in noA.planos:
			#verifica se o plano que queremos esta relacionado
			if noP.idPlano != id:
				#se nao tiver verif nao muda
				verif += 0
			else:
				#se tiver verif muda
				verif += 1

	#se verif == 0 significa que o plano nao estava relacionado com nenhuma academia, então procuramos se está nas inscrições, por segurança
	if(verif == 0):
		#caso nao esteja, verifica se esta relacionado em inscricao
		existePlano = models.Inscricao.query.filter_by(idPlano = id).first()
		#se não tiver retorna falso
		if(existePlano is None):
			return False
		else:
			return True
	else:
		#caso verif diferente de 0 então significa que o plano possui algum relacionamento
		return True



#verifica se a academia e o plano inserido em inscrição estão relacionados
def verificaPlanosAcademia(plano, academia):

	#percorre os planos da academias
	for no in academia.planos:
		#se existir o plano
		if no.idPlano == plano.idPlano:
			return True

	 #Apos percorrer todos os planos se nao encontrar retorna false
	return False


#edições

#editar funcionarios, recebe 1 usuario e os campos novos, e assim altera todos
def editarUsuario(usuario,novo_nome,nova_dataNascimento,novo_cpf,novo_rg,nova_rua,novo_numero,novo_bairro,nova_cidade,novo_estado,novo_email,nova_senha,novo_tipo):
	usuario.Nome = novo_nome
	usuario.DataNascimento = nova_dataNascimento
	usuario.Cpf = novo_cpf
	usuario.Rg = novo_rg
	usuario.Rua = nova_rua
	usuario.Numero = novo_numero
	usuario.Bairro = novo_bairro
	usuario.Cidade = nova_cidade
	usuario.Estado = novo_estado
	usuario.Email = novo_email
	usuario.Senha = nova_senha
	usuario.Tipo = novo_tipo
	db.session.commit()

def editarAcademia(academia,novo_nome,novo_cnpj,nova_rua,novo_numero,novo_bairro,nova_cidade,novo_estado,novo_email):
	academia.Nome = novo_nome
	academia.Cnpj = novo_cnpj
	academia.Rua = nova_rua
	academia.Numero = novo_numero
	academia.Bairro = novo_bairro
	academia.Cidade = nova_cidade
	academia.Estado = novo_estado
	academia.Email = novo_email
	db.session.commit()

def editarPlano(plano,novo_nome,nova_descricao,novo_valor,nova_validade):
	plano.Nome = novo_nome
	plano.Descricao = nova_descricao
	plano.Valor = novo_valor
	plano.Validade = nova_validade
	db.session.commit()


#exclusões

#recebe o id do que deseja excluir, mas antes de excluir, verifica se ele está em algum relacionamento, so podemos excluir se ele não estiver em nenhum relacionamento
def excluirUsuario(usuario):
	if (verificaRelacoesUsuario(usuario.idUsuario) == False):
		#exclui
		db.session.delete(usuario)
		#realiza a ação
		db.session.commit()

def excluirAcademia(academia):

	if (verificaRelacoesAcademia(academia.idAcademia) == False):
		#exclui
		db.session.delete(academia)
		#realiza a ação
		db.session.commit()

def excluirPlano(plano):
	if (verificaRelacoesPlano(plano.idPlano) == False): 
		#exclui
		db.session.delete(plano)
		#realiza a ação
		db.session.commit()


#É o unico que não interfere em relacionamentos ao ser excluido
def excluirInscricao(inscricao,usuario,academia,plano): 

	#remove a referencia de insricao em usuario, academia e plano
	usuario.inscricoes.remove(inscricao)
	academia.inscricoes.remove(inscricao)
	plano.inscricoes.remove(inscricao)
	
	#exclui inscricao 
	db.session.delete(inscricao)

	#realiza a ação
	db.session.commit()
	

def removerPlanosAcademia(academia,plano):
	#remove o plano das referencias da academia
	academia.planos.remove(plano)
	#realiza a ação
	db.session.commit()






#Função para definir a data de vencimento da inscrição
def adicionarVencimento(validade):
	#pega data atual do sistema
	atual = date.today()
	#retorna data atual mais a validade(dias), gerando a data de vencimento da inscricao
	return atual + timedelta(validade)
	