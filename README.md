## Webapp/API Desafio PontoTel
### Por onde começar ?

Estas instruções darão à você uma cópia do projeto rodando em sua máquina local para testes e feedback. Todas as instruções para baixar e rodar a aplicação se encontram abaixo!
### Pré-requisitos

```
Docker
```
```
HTTPie
```

### Rodando a aplicação com Docker!

Execute o seguinte comando para obter uma cópia da aplicação em seu localhost:

```
$ docker run -d -p 8000:5000 --rm wadsongarbes/pontotel:latest
```

Em seguida, acesse http://localhost:8000


## API Endpoints

|  URL | Métodos | Descrição |
| -------- | ------------- | --------- |
| `/api/cotacoes/<int:id>` | GET, PUT, DELETE  | Visualizar cotação específica , alterar cotação, deletar cotação |
| `/api/cotacoes` | GET, POST  | Ver todas as cotações, cadastrar cotação |
| `/api/usuarios/<int:id>` | GET, PUT  | Visualizar usuario específico, alterar usuário |
| `/api/usuarios` | GET, POST, PUT  | Ver todas os usuários, cadastrar usurios, alterar usuários |

## Acessando a API com um token

É necessário possuir um usuário para gerar um token para usar a API. Após criado seu usuário, instale o [HTTPie](https://httpie.org/#installation). É possivel então gerar um token com seu usuário e senha. Exemplo:

```
$ http --auth POST user:password http://localhost:8000/api/tokens
```

Pronto! O token tem duração de uma hora! Divirta-se!


## Construído com

* [Flask](https://flask.palletsprojects.com/en/1.1.x/) - Framework utilizado

## Dúvidas ?

Pergunte qualquer coisa na seção "Issue". Em caso de erros, poste o motivo e o log para uma melhor resposta!

* [Dúvidas](https://github.com/WadsonGarbes/pontotel/issues)

