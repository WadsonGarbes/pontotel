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

É necessário possuir um usuário para gerar um token para usar a API. Instale o [HTTPie](https://httpie.org/#installation). É possivel então gerar um token com seu usuário e senha. Exemplo:

```
$ http POST http://localhost:8000/api/usuarios login="username" email="username@domain.com" senha="123"
```

```
$ http --auth username:123 POST http://localhost:8000/api/tokens
```

O comando acima irá gerar seu token de acesso. Ele possui uma hora de duração. Para maior praticidade, guarde-o em uma variavel com o seguinte comando

```
$ export TOKEN=<seu_token>
```

Acesse um dos endpoints da seguinte maneira:

```
$ http GET http://localhost:8000/api/usuarios Authorization:"Bearer $TOKEN"
```


## Construído com

* [Flask](https://flask.palletsprojects.com/en/1.1.x/) - Framework utilizado

## Dúvidas ?

Pergunte qualquer coisa na seção "Issue". Em caso de erros, poste o motivo e o log para uma melhor resposta!

* [Dúvidas](https://github.com/WadsonGarbes/pontotel/issues)

