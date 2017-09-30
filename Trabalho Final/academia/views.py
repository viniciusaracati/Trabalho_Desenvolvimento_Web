from academia import app
from academia import management
from flask import render_template, redirect, url_for, request



@app.route('/') 
@app.route('/home')
def home():

	if management.usuario_tipo == 'normal':
		return render_template('normal_index.html', usuario = management.usuario_logado)

	elif management.usuario_tipo == 'admin':
		return render_template('admin_index.html', usuario = management.usuario_logado)




#Rotas usuarios
@app.route('/usuarios')
def usuarios():

	if management.usuario_tipo == 'admin':
		return render_template('admin_usuarios.html', usuario = management.usuario_logado)


@app.route('/usuarios/cadastrar')
def cadastro_usuario():

	if management.usuario_tipo == 'normal':
		return render_template('normal_cadastro_usuario.html', usuario = management.usuario_logado)

	elif management.usuario_tipo == 'admin':
		return render_template('admin_cadastro_usuario.html', usuario = management.usuario_logado)


@app.route('/usuarios/editar')
def editar_usuario():

	if management.usuario_tipo == 'admin':
		return render_template('admin_editar_usuario.html', usuario = management.usuario_logado)


@app.route('/usuarios/excluir')
def excluir_usuario():

	if management.usuario_tipo == 'admin':
		return redirect(url_for('planos'))




#rotas planos
@app.route('/planos')
def planos():
	if management.usuario_tipo == 'admin':
		return render_template('admin_planos.html', usuario = management.usuario_logado)


@app.route('/planos/adicionar')
def adicionar_plano():
	if management.usuario_tipo == 'admin':
		return render_template('admin_adicionar_plano.html', usuario = management.usuario_logado)


@app.route('/planos/editar')
def editar_plano():
	if management.usuario_tipo == 'admin':
		return render_template('admin_editar_plano.html', usuario = management.usuario_logado)


@app.route('/planos/excluir')
def excluir_plano():
	if management.usuario_tipo == 'admin':
		return redirect(url_for('planos'))


		

#rotas academias
@app.route('/academias')
def academias():
	if management.usuario_tipo == 'normal':
		return render_template('normal_academias.html', usuario = management.usuario_logado)

	elif management.usuario_tipo == 'admin':
		return render_template('admin_academias.html', usuario = management.usuario_logado)


@app.route('/academias/adicionar')
def adicionar_academia():
	if management.usuario_tipo == 'admin':
		return render_template('admin_adicionar_academia.html', usuario = management.usuario_logado)


@app.route('/academias/editar')
def editar_academia():
	if management.usuario_tipo == 'admin':
		return render_template('admin_editar_academia.html', usuario = management.usuario_logado)


@app.route('/academias/gerenciar_planos')
def gerenciar_planos_academia():
	if management.usuario_tipo == 'admin':
		return render_template('admin_academia_gerenciar_planos.html', usuario = management.usuario_logado)


@app.route('/academias/selecionar_planos')
def selecionar_planos_academia():
	if management.usuario_tipo == 'admin':
		return render_template('admin_academia_selecionar_planos.html', usuario = management.usuario_logado)

@app.route('/academias/planos')
def mostra_planos_academia():
	if management.usuario_tipo == 'normal':
		return render_template('normal_planos_academia.html', usuario = management.usuario_logado)


@app.route('/academias/excluir')
def excluir_academia():
	if management.usuario_tipo == 'admin':
		return redirect(url_for('academias'))



#matricula
@app.route('/matricula/selecionaacademia')
def matricula_seleciona_academia():
	if management.usuario_logado != 'isitante':
		return render_template('normal_matricula_academias.html', usuario = management.usuario_logado)



@app.route('/matricula/selecionaplano')
def matricula_seleciona_plano():
	if management.usuario_logado != 'isitante':
		return render_template('normal_matricula_planos.html', usuario = management.usuario_logado)



#login
@app.route('/login')
def login():
	
	if management.usuario_tipo == 'normal':
		return render_template('normal_login.html', usuario = management.usuario_logado)

	elif management.usuario_tipo == 'admin':
		return render_template('admin_login.html', usuario = management.usuario_logado)

#sair
@app.route('/sair')
def sair():
    management.usuario_logado = 'Visitante'
    management.usuario_tipo = 'normal'
    management.id_logado = -1
    return redirect(url_for('home'))
