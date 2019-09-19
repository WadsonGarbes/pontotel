## Webapp/API Desafio PontoTel
### Por onde começar ?

Estas instruções darão à você uma cópia do projeto rodando em sua máquina local para testes e feedback. Todas as instruções para baixar e rodar a aplicação se encontram abaixo!
### Pré-requisitos

```
Shell Linux 
```
```
Python3.x
```
```
virtualenv
```
```
Este repositório
```

### Instalando

Por padrão, toda distribuição Linux acompanha Python2.7 e Python3.x. É possível verificar isto abrindo um shell em seu ambiente Linux e digitando:

```
$ python3 --version
```

A resposta deve ser:

```
Python 3.x.x
```

Daí então podemos começar a instalar as dependências para rodar a aplicação:

```
$ sudo apt install pip3
```

pip é o instalador de pacotes do python, necessário para instalação das dependências da aplicação

```
$ sudo apt install python3-venv
```

Responsável por isolar nossa aplicação da máquina "hospedeira", garantido um controle maior sobre as dependências da aplicação

```
$ git clone https://github.com/wadsongarbes/pontotel
```

baixe a aplicação e a armazene-a no repositório de mesmo nome (pontotel)

```
$ python3 -m venv ~/.virtualenvs/pontotel && . pontotel/bin/activate
```
cria e ativa um ambiente virtual

```
$ pip install -r requirements.txt
```
baixa as dependências do projeto


## Rodando a aplicação

Ative, caso ainda não esteja ativado, o ambiente virtual pontotel, assim será posível instalar todas as dependências do projeto sem afetar a máquina local!

```
(pontotel) $ export FLASK_APP=pontotel.py 
```

Rode o script que cria o banco:
```
(pontotel) $ . cria_banco.sh 
```

Rode o servidor

```
(pontotel) $ flask run
```

Acesse o link disponibilizado pelo servidor (http://127.0.0.1:5000) em seu navegador de preferência

## Cansei!

No shell onde o servidor está rodando, tecle `ctrl + c` e desative o ambiente virtual com

`(pontotel) $ deactivate`

## Construído com

* [Flask](https://flask.palletsprojects.com/en/1.1.x/) - Framework utilizado

## Dúvidas ?

Pergunte qualquer coisa na seção "Issue". Em caso de erros, poste o motivo e o log para uma melhor resposta!

* [Dúvidas](https://github.com/WadsonGarbes/pontotel/issues)

