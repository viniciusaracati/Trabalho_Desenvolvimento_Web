from academia import db
from academia import models
from academia import management
import unittest

#funções para testar

#função para verificar se os dados do usuário estão corretos, tem como parametro o self , o usuario a ser verificado e os campos
def verificaCamposUsuarios(self,usuario, nome,dataNascimento,cpf,rg,rua,numero,bairro,cidade,estado,email,senha,tipo):
	self.assertEqual(usuario.Nome, nome)		
	self.assertEqual(usuario.DataNascimento, dataNascimento)
	self.assertEqual(usuario.Cpf, cpf)
	self.assertEqual(usuario.Rg, rg)
	self.assertEqual(usuario.Rua, rua)
	self.assertEqual(usuario.Numero,numero)
	self.assertEqual(usuario.Bairro,bairro)
	self.assertEqual(usuario.Cidade,cidade)
	self.assertEqual(usuario.Estado,estado)
	self.assertEqual(usuario.Email,email)
	self.assertEqual(usuario.Senha,senha)	
	self.assertEqual(usuario.Tipo, tipo)

#função para verificar se os dados da academia estão corretos, tem como parametro o self , a academia a ser verificada e os campos
def verificaCamposAcademia(self,academia, nome,cnpj,rua,numero,bairro,cidade,estado,email):
	self.assertEqual(academia.Nome, nome)		
	self.assertEqual(academia.Cnpj, cnpj)
	self.assertEqual(academia.Rua, rua)
	self.assertEqual(academia.Numero,numero)
	self.assertEqual(academia.Bairro,bairro)
	self.assertEqual(academia.Cidade,cidade)
	self.assertEqual(academia.Estado,estado)
	self.assertEqual(academia.Email,email)

#função para verificar se os dados do plano estão corretos, tem como parametro o self , o plano a ser verificado e os campos
def verificaCamposPlano(self,plano,nome,descricao,valor,validade):
	self.assertEqual(plano.Nome, nome)
	self.assertEqual(plano.Descricao, descricao)
	self.assertEqual(plano.Valor, valor)
	self.assertEqual(plano.Validade, validade)

#função para verificar se os dados de inscrições estão corretos
def verificaCamposInscricao(self,inscricao,idUsuario, idAcademia, idPlano):
	self.assertEqual(inscricao.idUsuario, idUsuario)
	self.assertEqual(inscricao.idAcademia, idAcademia)
	self.assertEqual(inscricao.idPlano, idPlano)




#teste propriamente dito
class AcademiaTestCase(unittest.TestCase):

	def setUp(self):
		db.drop_all()		
		db.create_all()

	def testeUsuario(self):

		#inserindo usuarios
		management.inserirUsuarioCliente('Vinicius Lima', '22/22/2222', '243223', '123123123', 'Rua 2', 12, 'Centro', 'Aracati','Ceara', 'aaaa@gmail.com', 'senha1')
		management.inserirUsuarioAdmin('Admin', '22/22/2222', '243223', '123123123', 'Rua 2', 12, 'Centro', 'Aracati', 'Ceara' ,'aaaa@gmail.com', 'senha4')
		
		#obtem lista dos usuarios
		usuarios = models.Usuario.query.all()
		
		#verifica se os dados dos usuarios foram inseridos corretamente
		verificaCamposUsuarios(self,usuarios[0],'Vinicius Lima', '22/22/2222', '243223', '123123123', 'Rua 2', 12, 'Centro', 'Aracati','Ceara', 'aaaa@gmail.com', 'senha1','cliente')		
		verificaCamposUsuarios(self,usuarios[1],'Admin', '22/22/2222', '243223', '123123123', 'Rua 2', 12, 'Centro', 'Aracati', 'Ceara' ,'aaaa@gmail.com', 'senha4','admin')
		
		#editando usuario
		management.editarUsuario(usuarios[0],'Vinicius Lima', '22/22/2222', '243223', '123123123', 'Rua 2', 12, 'Centro', 'Aracati','Ceara', 'aabb@gmail.com', 's1231','cliente')
		management.editarUsuario(usuarios[1],'Administrador', '24/24/2424', '243223', '123123123', 'Rua 2', 15, 'Centro', 'Aracati', 'Ceara' ,'aaaa@gmail.com', 'senha4','admin')

		#obtem lista dos usuarios
		usuarios = models.Usuario.query.all()

		#Verifica se a edição funcionou corretamente
		verificaCamposUsuarios(self,usuarios[0],'Vinicius Lima', '22/22/2222', '243223', '123123123', 'Rua 2', 12, 'Centro', 'Aracati','Ceara', 'aabb@gmail.com', 's1231','cliente')
		verificaCamposUsuarios(self,usuarios[1],'Administrador', '24/24/2424', '243223', '123123123', 'Rua 2', 15, 'Centro', 'Aracati', 'Ceara' ,'aaaa@gmail.com', 'senha4','admin')

		#Tamanho Antes de Excluir
		tamanhoTotal = len(usuarios)

		#Excluindo usuario
		management.excluirUsuario(usuarios[0])
		management.excluirUsuario(usuarios[1])	

		#total de valores excluidos
		excluidos = 2

		#obtem lista dos usuarios
		usuarios = models.Usuario.query.all()

		#Verifica se os usuarios realmente foram excluidos
		self.assertEqual(len(usuarios), tamanhoTotal-excluidos)
		


	def testeAcademia(self):
		
		#inserindo academia
		management.inserirAcademia('muscle','123123','Rua A', 10, 'Centro','Aracati','Ceará','muscle@gmail.com')
		management.inserirAcademia('maromba','123435123','Rua A', 40, 'Centro','Aracati','Ceará','maromba@gmail.com')

		#obtem lista de academias
		academias = models.Academia.query.all()

		#verifica se os dados foram inseridos
		verificaCamposAcademia(self,academias[0],'muscle','123123','Rua A', 10, 'Centro','Aracati','Ceará','muscle@gmail.com')
		verificaCamposAcademia(self,academias[1],'maromba','123435123','Rua A', 40, 'Centro','Aracati','Ceará','maromba@gmail.com')

		#editando academia
		management.editarAcademia(academias[0],'muscle1','123456','Rua X', 20, 'Centro1','Fortim','Ceará','muscle@gmail.com')
		management.editarAcademia(academias[1],'maromba1','3435123','Rua B', 40, 'Centro1','Aracati','Ceará','maromba@gmail.com')

		#obtem lista de academias
		academias = models.Academia.query.all()

		#verifica se os dados foram editados
		verificaCamposAcademia(self,academias[0],'muscle1','123456','Rua X', 20, 'Centro1','Fortim','Ceará','muscle@gmail.com')
		verificaCamposAcademia(self,academias[1],'maromba1','3435123','Rua B', 40, 'Centro1','Aracati','Ceará','maromba@gmail.com')

		#tamanho antes de excluir
		tamanhoTotal = len(academias)

		#excluir academia
		management.excluirAcademia(academias[0])
		management.excluirAcademia(academias[1])

		#total de valores excluidos
		excluidos = 2

		#obtem lista de academias
		academias = models.Academia.query.all()
		

		#Verifica se a academia realmente foi excluida
		self.assertEqual(len(academias), tamanhoTotal-excluidos)
		




	def testePlano(self):

		#Inserir Plano
		management.inserirPlano('Plano 1','Direito à academia por 1 mês',90.00,15)
		management.inserirPlano('Plano 2','Direito à academia por 3 mês',210.00,30)

		#obtem lista de planos
		planos = models.Plano.query.all()

		#verifica se os dados foram inseridos corretamente
		verificaCamposPlano(self,planos[0],'Plano 1','Direito à academia por 1 mês',90.00,15)
		verificaCamposPlano(self,planos[1],'Plano 2','Direito à academia por 3 mês',210.00,30)

		#Editar Plano
		management.editarPlano(planos[0],'Plano 1','Direito à academia por 1 mês',90.00,30)
		management.editarPlano(planos[1],'Plano 3','Direito à academia por 4 mês',299.00,120)

		#obtem lista de planos
		planos = models.Plano.query.all()


		#verifica se os planos foram editados
		verificaCamposPlano(self,planos[0],'Plano 1','Direito à academia por 1 mês',90.00,30)
		verificaCamposPlano(self,planos[1],'Plano 3','Direito à academia por 4 mês',299.00,120)

		#tamanho antes de excluir
		tamanhoTotal = len(planos)

		#excluir academia
		management.excluirPlano(planos[0])
		management.excluirPlano(planos[1])

		#total de valores excluidos
		excluidos = 2

		#obtem lista de academias
		planos = models.Plano.query.all()
		

		#Verifica se a academia realmente foi excluida
		self.assertEqual(len(planos), tamanhoTotal-excluidos)
		
	


	def testePlanosAcademia(self):

		#inserindo academia e plano
		management.inserirAcademia('muscle','123123','Rua A', 10, 'Centro','Aracati','Ceará','muscle@gmail.com')
		management.inserirPlano('Plano 1','Direito à academia por 1 mês',90.00,30)

		#obtem lista de academias e planos
		academias = models.Academia.query.all()
		planos = models.Plano.query.all()

		#inserir plano no Relacionamento PlanosAcademia(academia recebe o plano)
		management.inserirPlanosAcademia(academias[0],planos[0])

		#verifica Relacionamento PlanosAcademia, vendo se o plano está na lista de referencias da academia
		self.assertEqual(academias[0].planos[0].idPlano, planos[0].idPlano) 

		#excluir plano no Relacionamento planosAcademia(o plano deixa de se relacionar com a academia)
		management.removerPlanosAcademia(academias[0],planos[0])

		#verifica que a relação do plano com academia foi removida(obs: '[]' significa vazio, como removeu a relação, a list de relações está vazia)
		self.assertEqual(academias[0].planos, []) 



	def testeInscricao(self):
		#inserindo usuario,  academia e plano
		management.inserirUsuarioCliente('Vinicius Lima', '22/22/2222', '243223', '123123123', 'Rua 2', 12, 'Centro', 'Aracati','Ceara', 'aaaa@gmail.com', 'senha1')
		management.inserirAcademia('muscle','123123','Rua A', 10, 'Centro','Aracati','Ceará','muscle@gmail.com')
		management.inserirPlano('Plano 1','Direito à academia por 1 mês',90.00,60)

		#obtem lista de usuarios, academias e planos
		usuarios = models.Usuario.query.all()
		academias = models.Academia.query.all()		
		planos = models.Plano.query.all()

		#inserir plano no Relacionamento PlanosAcademia(academia recebe o plano) (pois o plano tem que estar relacionado a academia para realizar a inscrição)
		management.inserirPlanosAcademia(academias[0],planos[0])

		#obtem lista de usuarios, academias e planos atualizados
		usuarios = models.Usuario.query.all()
		academias = models.Academia.query.all()		
		planos = models.Plano.query.all()

		#realizar inscricao
		management.inserirInscricao(usuarios[0],academias[0],planos[0])

		#obtem lista de usuarios, academias , planos e inscricoes atualizado
		usuarios = models.Usuario.query.all()
		academias = models.Academia.query.all()		
		planos = models.Plano.query.all()
		inscricoes = models.Inscricao.query.all()

		#verifica se a inscricao foi feita
		verificaCamposInscricao(self,inscricoes[0],usuarios[0].idUsuario, academias[0].idAcademia, planos[0].idPlano)

		#verifica se a relação foi preenchida
		self.assertEqual(usuarios[0].inscricoes[0].idInscricao, inscricoes[0].idInscricao)
		self.assertEqual(academias[0].inscricoes[0].idInscricao, inscricoes[0].idInscricao)
		self.assertEqual(planos[0].inscricoes[0].idInscricao, inscricoes[0].idInscricao)


		#Excluir inscricao
		management.excluirInscricao(inscricoes[0],usuarios[0],academias[0],planos[0])

		#obtem lista de usuarios, academias , planos e inscricoes atualizado
		usuarios = models.Usuario.query.all()
		academias = models.Academia.query.all()		
		planos = models.Plano.query.all()
		inscricoes = models.Inscricao.query.all()


		#verifica se a inscrição foi removida, como so tinha uma, ao excluir, vai ficar []
		self.assertEqual(inscricoes, [])


			




if __name__ == '__main__':
	unittest.main()