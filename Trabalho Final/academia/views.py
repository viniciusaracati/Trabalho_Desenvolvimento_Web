from academia import app
from academia import management
from academia import models
from flask import render_template, redirect, url_for, request, flash
import datetime,time




@app.route('/') 
@app.route('/home')
def home():
	#verifica o tipo de usuario para determinar para qual tipo de pagina ele vai
	if management.usuario_tipo == 'cliente':
		return render_template('normal_index.html', usuario = management.usuario_logado)

	elif management.usuario_tipo == 'admin':
		return render_template('admin_index.html', usuario = management.usuario_logado)

@app.route('/layout/admin')
def layout_admin():
    return render_template('layout_admin.html', usuario = management.usuario_logado)

@app.route('/layout/cliente')
def layout_cliente():
    return render_template('layout_cliente.html', usuario = management.usuario_logado)




#Rotas usuarios
@app.route('/usuarios')
def usuarios():
	#verifica tipo do usuario para saber se ele tem permissão para acessar essa pagina
	if management.usuario_tipo == 'admin':
		return render_template('admin_usuarios.html', usuario = management.usuario_logado, listaUsuario = management.recebeUsuarios())


@app.route('/usuarios/cadastrar')
def cadastro_usuario():

	if management.usuario_tipo == 'cliente':
		return render_template('normal_cadastro_usuario.html', usuario = management.usuario_logado)

	elif management.usuario_tipo == 'admin':
		return render_template('admin_cadastro_usuario.html', usuario = management.usuario_logado)


# Função para cadastrar usuario cliente 
@app.route('/usuarios/executarCadastroCliente', methods = ['GET','POST'])
def executar_cadastro_cliente():

	#Verifica se o metodo é post, se for recebemos os valores do formulario
	if(request.method == 'POST'):
		nome = request.form.get('cad_nome')
		dataNascimento = request.form.get('cad_dataNascimento')
		cpf = request.form.get('cad_cpf')
		rg = request.form.get('cad_rg')
		rua = request.form.get('cad_rua')
		numero = request.form.get('cad_numero')
		bairro = request.form.get('cad_bairro')
		cidade = request.form.get('cad_cidade')
		estado = request.form.get('cad_estado')        
		email = request.form.get('cad_email')
		senha = request.form.get('cad_senha')

		#verifica se os campos estão preenchidos, se estiverem, ele é inserido e vai para a pagina principal, caso contrario ele volta para a pagina de cadastro
		if nome and dataNascimento and cpf and rg and rua and numero and bairro and cidade and estado and email and senha:
			management.inserirUsuario(nome, dataNascimento, cpf, rg , rua, numero, bairro, cidade, estado, email, senha,'cliente');			
			return redirect(url_for('home'))
		else:
			return redirect(url_for('cadastro_usuario'))

	


# Função para cadastrar usuario Admin
@app.route('/usuarios/executarCadastroAdmin', methods = ['GET','POST'])
def executar_cadastro_admin():

	if(request.method == 'POST'):
		nome = request.form.get('cad_nome')
		dataNascimento = request.form.get('cad_dataNascimento')
		cpf = request.form.get('cad_cpf')
		rg = request.form.get('cad_rg')
		rua = request.form.get('cad_rua')
		numero = request.form.get('cad_numero')
		bairro = request.form.get('cad_bairro')
		cidade = request.form.get('cad_cidade')
		estado = request.form.get('cad_estado')        
		email = request.form.get('cad_email')
		senha = request.form.get('cad_senha')
		tipo = request.form.get('cad_tipo')

		if nome and dataNascimento and cpf and rg and rua and numero and bairro and cidade and estado and email and senha and tipo:
			management.inserirUsuario(nome, dataNascimento, cpf, rg , rua, numero, bairro, cidade, estado, email, senha, tipo);
			return redirect(url_for('usuarios'))
		else:
			return redirect(url_for('cadastro_usuario'))



@app.route('/usuarios/editar/<int:id>', methods = ['GET','POST'])
def editar_usuario(id):

	#verifica tipo do usuario para saber se ele tem permissão para acessar essa pagina
	if management.usuario_tipo == 'admin':

		usuario = models.Usuario.query.filter_by(idUsuario = id).first()

		if(request.method == 'POST'):

			nome = request.form.get('cad_nome')
			dataNascimento = request.form.get('cad_dataNascimento')
			cpf = request.form.get('cad_cpf')
			rg = request.form.get('cad_rg')
			rua = request.form.get('cad_rua')
			numero = request.form.get('cad_numero')
			bairro = request.form.get('cad_bairro')
			cidade = request.form.get('cad_cidade')
			estado = request.form.get('cad_estado')        
			email = request.form.get('cad_email')
			senha = request.form.get('cad_senha')
			tipo = request.form.get('cad_tipo')

			if nome and dataNascimento and cpf and rg and rua and numero and bairro and cidade and estado and email and senha and tipo:
				management.editarUsuario(usuario,nome, dataNascimento, cpf, rg , rua, numero, bairro, cidade, estado, email, senha, tipo);
				return redirect(url_for('usuarios'))
		



		return render_template('admin_editar_usuario.html', usuario = management.usuario_logado, listaUsuario = usuario)


@app.route('/usuarios/excluir/<int:id>')
def excluir_usuario(id):

	if management.usuario_tipo == 'admin':

		usuario = models.Usuario.query.filter_by(idUsuario = id).first()

		management.excluirUsuario(usuario)

		return redirect(url_for('planos'))




#rotas planos
@app.route('/planos')
def planos():
	if management.usuario_tipo == 'admin':
		return render_template('admin_planos.html', usuario = management.usuario_logado, listaPlano = management.recebePlanos())


@app.route('/planos/adicionar')
def adicionar_plano():
	if management.usuario_tipo == 'admin':
		return render_template('admin_adicionar_plano.html', usuario = management.usuario_logado)



@app.route('/planos/executarAdicionarPlano', methods = ['GET','POST'])
def executar_adicionar_plano():

	if(request.method == 'POST'):
		nome = request.form.get('cad_nome')
		descricao = request.form.get('cad_descricao')
		valor = request.form.get('cad_valor')
		validade = request.form.get('cad_validade')

		if nome and descricao and valor and validade:
			management.inserirPlano(nome, descricao, valor, validade);
			return redirect(url_for('planos'))

		else:
			return redirect(url_for('adicionar_plano'))



@app.route('/planos/editar/<int:id>', methods = ['GET','POST'])
def editar_plano(id):
	if management.usuario_tipo == 'admin':

		plano = models.Plano.query.filter_by(idPlano = id).first()

		if(request.method == 'POST'):
			nome = request.form.get('cad_nome')
			descricao = request.form.get('cad_descricao')
			valor = request.form.get('cad_valor')
			validade = request.form.get('cad_validade')

			if nome and descricao and valor and validade:
				management.editarPlano(plano,nome, descricao, valor, validade);
				return redirect(url_for('planos'))
			

		return render_template('admin_editar_plano.html', usuario = management.usuario_logado, plano = plano)





@app.route('/planos/excluir/<int:id>')
def excluir_plano(id):
	if management.usuario_tipo == 'admin':

		plano = models.Plano.query.filter_by(idPlano = id).first()

		management.excluirPlano(plano)

		return redirect(url_for('planos'))


		

#rotas academias
@app.route('/academias')
def academias():
	if management.usuario_tipo == 'cliente':
		return render_template('normal_academias.html', usuario = management.usuario_logado, listaAcademia = management.recebeAcademias())

	elif management.usuario_tipo == 'admin':
		return render_template('admin_academias.html', usuario = management.usuario_logado, listaAcademia = management.recebeAcademias())


@app.route('/academias/adicionar')
def adicionar_academia():
	if management.usuario_tipo == 'admin':
		return render_template('admin_adicionar_academia.html', usuario = management.usuario_logado)


@app.route('/academias/executarAdicionarAcademia', methods = ['GET','POST'])
def executar_adicionar_academia():

	if(request.method == 'POST'):
		nome = request.form.get('cad_nome')
		cnpj = request.form.get('cad_cnpj')
		rua = request.form.get('cad_rua')
		numero = request.form.get('cad_numero')
		bairro = request.form.get('cad_bairro')
		cidade = request.form.get('cad_cidade')
		estado = request.form.get('cad_estado')
		email = request.form.get('cad_email')

		if nome and cnpj and rua and numero and bairro and cidade and estado and email:
			management.inserirAcademia(nome, cnpj, rua, numero, bairro, cidade, estado, email);
			return redirect(url_for('academias'))

		else:
			return redirect(url_for('adicionar_academia'))


@app.route('/academias/editar/<int:id>', methods = ['GET','POST'])
def editar_academia(id):

	if management.usuario_tipo == 'admin':

		academia = models.Academia.query.filter_by(idAcademia = id).first()

		if(request.method == 'POST'):
			nome = request.form.get('cad_nome')
			cnpj = request.form.get('cad_cnpj')
			rua = request.form.get('cad_rua')
			numero = request.form.get('cad_numero')
			bairro = request.form.get('cad_bairro')
			cidade = request.form.get('cad_cidade')
			estado = request.form.get('cad_estado')
			email = request.form.get('cad_email')

			if nome and cnpj and rua and numero and bairro and cidade and estado and email:
				management.editarAcademia(academia,nome, cnpj, rua, numero, bairro, cidade, estado, email);
				return redirect(url_for('academias'))


		return render_template('admin_editar_academia.html', usuario = management.usuario_logado, academia = academia)


@app.route('/academias/gerenciar_planos/<int:id>')
def gerenciar_planos_academia(id):
	if management.usuario_tipo == 'admin':
		academia = models.Academia.query.filter_by(idAcademia = id).first()		

		return render_template('admin_academia_gerenciar_planos.html', usuario = management.usuario_logado, planos = academia.planos, academia = academia)


@app.route('/academias/selecionar_planos/<int:id>')
def selecionar_planos_academia(id):
	if management.usuario_tipo == 'admin':

		#recebe a academia com o id recebido
		academia = models.Academia.query.filter_by(idAcademia = id).first()
		#recebe todos os planos do banco
		planos = management.recebePlanos()

		#pega os planos que nao estão relacionados com a academia escolhida
		novo_plano = management.planosForaAcademia(academia,planos) 



		return render_template('admin_academia_selecionar_planos.html', usuario = management.usuario_logado, academia = academia, planos = novo_plano)


@app.route('/academias/selecionar_planos_executar/<int:id_academia>/<int:id_plano>')
def executar_selecionar_planos_academia(id_academia, id_plano):
	if management.usuario_tipo == 'admin':

		#recebe a academia com o id recebido
		academia = models.Academia.query.filter_by(idAcademia = id_academia).first()
		#recebe o plano com o id recebido
		plano = models.Plano.query.filter_by(idPlano = id_plano).first()		

		#faz a relção entre plano e academia
		management.inserirPlanosAcademia(academia, plano) 

		#retorna para a pagina que mostra os planos pertencentes a academia
		return render_template('admin_academia_gerenciar_planos.html', usuario = management.usuario_logado, planos = academia.planos, academia = academia)
		

@app.route('/academias/planos/<int:id_academia>')
def mostra_planos_academia(id_academia):
	if management.usuario_tipo == 'cliente':

		#recebe a academia do id recebido
		academia = models.Academia.query.filter_by(idAcademia = id_academia).first()

		return render_template('normal_planos_academia.html', usuario = management.usuario_logado, planos = academia.planos, academia = academia)


@app.route('/academias/excluir/<int:id>')
def excluir_academia(id):
	if management.usuario_tipo == 'admin':

		academia = models.Academia.query.filter_by(idAcademia = id).first()

		management.excluirAcademia(academia)

		return redirect(url_for('academias'))



#matricula
@app.route('/matricula/selecionaacademia')
def matricula_seleciona_academia():
	if management.usuario_logado != 'Visitante':
		return render_template('normal_matricula_academias.html', usuario = management.usuario_logado,  listaAcademia = management.recebeAcademias())
	else:
		return redirect(url_for('home'))



@app.route('/matricula/selecionaplano/<int:id_academia>')
def matricula_seleciona_plano(id_academia):
	if management.usuario_logado != 'Visitante':
		academia = models.Academia.query.filter_by(idAcademia = id_academia).first()
		return render_template('normal_matricula_planos.html', usuario = management.usuario_logado, planos = academia.planos, academia = academia)
	else:
		return redirect(url_for('home'))


@app.route('/matricula/executamatricula/<int:id_academia>/<int:id_plano>')
def matricula_executa_matricula(id_academia, id_plano):
	if management.usuario_logado != 'Visitante':
		academia = models.Academia.query.filter_by(idAcademia = id_academia).first()
		usuario = models.Usuario.query.filter_by(idUsuario = management.id_logado).first()
		plano = models.Plano.query.filter_by(idPlano = id_plano).first()
		management.inserirInscricao(usuario,academia,plano)
		return redirect(url_for('home'))

@app.route('/matricula/inscricoes')
def inscricoes():
	if management.usuario_tipo == 'admin':

		inscricoes = models.Inscricao.query.order_by(models.Inscricao.DataVencimento.asc()).all()

		listaMatricula = list()

		for a in inscricoes:

			usuario = models.Usuario.query.filter_by(idUsuario = a.idUsuario).first()
			academia = models.Academia.query.filter_by(idAcademia = a.idAcademia).first()
			plano = models.Plano.query.filter_by(idPlano = a.idPlano).first()

			nData = time.strptime(str(a.DataVencimento), "%Y-%m-%d")
			nData = datetime.date(*nData[0:3])
			nData = nData.strftime('%d/%m/%Y')

			matricula = (a.idInscricao, academia.idAcademia, academia.Nome, usuario.idUsuario, usuario.Nome, plano.idPlano, plano.Nome, plano.Validade, nData)
			listaMatricula.append(matricula)

		return render_template('admin_inscricoes.html', usuario = management.usuario_logado, listaMatricula = listaMatricula)


#login
@app.route('/login')
def login():
	
	if management.usuario_tipo == 'cliente':
		return render_template('normal_login.html', usuario = management.usuario_logado)

	elif management.usuario_tipo == 'admin':
		return render_template('admin_login.html', usuario = management.usuario_logado)



@app.route('/executarLogin', methods = ['GET','POST'])
def executar_login():

	if(request.method == 'POST'):

		email = request.form.get('email')
		senha = request.form.get('senha')

		usuario  = management.existeUsuario(email, senha)
		if usuario:			
			management.usuario_logado = usuario.Nome
			management.id_logado = usuario.idUsuario
			management.usuario_tipo = usuario.Tipo
			flash('Login executado com sucesso')
			return redirect(url_for('home'))

		else:			
			return redirect(url_for('login'))

#sair
@app.route('/sair')
def sair():
    management.usuario_logado = 'Visitante'
    management.usuario_tipo = 'cliente'
    management.id_logado = -1
    return redirect(url_for('home'))
