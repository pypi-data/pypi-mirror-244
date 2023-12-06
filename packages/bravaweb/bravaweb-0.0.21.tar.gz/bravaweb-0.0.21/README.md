# BravaWeb Framework for ASGI Server

Framework para aplicações WEB baseada em Python3 ASGI  (_Asynchronous Server Gateway Interfac_  em  Uvicorn), com possibilidade de utilização de Template em Html (Mako Templates).

Veja Documentação em:

Uvicorn: https://www.uvicorn.org/
Mako Templates: https://www.makotemplates.org/

# Instalação
Instalação utilizando Pip
```bash
pip install bravaweb
```
Git/Clone
```
git clone https://github.com/robertons/bravaweb
cd bravaweb
pip install -r requirements.txt
python setup.py install
```

# Primeiros Passos

Inicie seu projeto conforme estrutura abaixo


```bash
app
├── ...
├── configuration                           		
│   ├── __init__.py          
│   └── api.py                   
└── server.py
```

O arquivo de configurações deve conter os seguintes dados:

| variável     		  |    tipo     | obrigatório |  descrição       			        |
|-------------------|-------------|-------------|-------------------------------|
| directory       	| string      | sim         | Caminho Projeto     		     	|
| encoding 		  	  | string      | sim         | Codificação    				        |
| date_format     	| string      | sim         | Formato data             		  |
| short_date_format | string      | sim         | Formato data curta            |
| token 			      | string      | sim         | Token codificação Authorization Header    |
| domains      		  | array       | sim         | Domínios autorizados a acessar|
| access_exceptions | array       | sim         | Rotas e Exceções de acesso   	|
| routes 			      | array       | sim         | Rotas do Projeto      		    |


```python

configuration/__init__.py

# -*- coding: utf-8 -*-

from configuration import api

```


```python

configuration/api.py

# -*- coding: utf-8 -*-

import os

# Directory
directory = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

# Api Encoding
encoding = "utf-8"

# Date Format
date_format = "%d/%m/%Y %H:%M:%S"
short_date_format = "%d/%m/%Y"

# Token Authorization
token = "JWT-Token-Project"

# Authorized Domains Origin/Referrer
domains = [
    "https://www.dominio.com.br",
    "https://alias.dominio.com.br",
]

# Exceptions Routes
access_exceptions = [

    {'path': '(^/default/)','referer': '*'},

    {'path': '(/rota/especifica/)','referer': '(^https://dominio.especifico.com.br/)'},

    {'path': '*', 'referer': "(^https://outro.dominio.com.br/)|(^https://adicional.dominio.com.br/)"},
]

routes = [
    ("{controller}/{area}/{module}/{action}/{id}", '(^/admin/)|(^/panel/)',
    ("{controller}/{module}/{action}/{id}", ""),
]

```

**Definições:**

**domains**:  lista array de strings, com domínios que tem acesso a api, o teste é feito baseado no origin e/ou referrer de cada requisição.

**access_exceptions**: é possivel que algumas rotas sejam abertas para qualquer requisição, ou mesmo que alguma rota seja especifica para algum domínio. A lista deve conter um dicionário com as chaves path e referer onde:

	path: é referente ao caminho da rota
	referer: origem da requisição

Ambos os valores aceitam * para todos ou expressão regular para teste de string.

**routes**:  lista com tuplas que definem as rotas padrões do projeto. Bravaweb esta preparado para até 4 níveis de profundidade que definem, Controlador, Area, Modulo, Ação e mais um nível **opcional** para captação de ID, a prioridade das regras é sequencial, portanto as regras específicas devem vir primeiro. A tupla é definida assim:

	0: a captação de cada parte da profundidade para carregamento
	1: expressão regular para identificar a regra

Por padrão os valores de rota do ambiente são:

    controller = None
    area = None
    module = "default"
    action="index"
    id = None

Por fim vamos  criar a execução do projeto que vai tratar as requisições e processar as rotas.

O arquivo `server.py` na raiz deve ficar assim:

```python
#-*- coding: utf-8 -*-
import sys

import configuration

from bravaweb import App as application

```

Acesse o diretório  do seu projeto, e execute o comando  de serviço do ASGI, conforme documentação do Uvicorn, no exemplo abaixo ativamos o ambiente virtual onde os pacotes estão instalados:


```bash\
source ../env/bin/activate

uvicorn server:application --port 8080 --interface=asgi3 --workers 7 --proxy-headers --lifespan off --reload

```
O Resultado então será:

```bash\
INFO: Uvicorn running on http://127.0.0.1:8080 (Press CTRL+C to quit)
INFO: Started reloader process [82503] using statreload
INFO: Started server process [82505]
.
.
.
```

Neste momento sua aplicação estará em execução. Nós configuramos as rotas mas não desenvolvemos nenhuma delas portanto qualquer requisição na url http://127.0.0.1:8080 irá retornar 404.

# Hello World


Vamos iniciar aplicando a rota default, a pasta do projeto nesse momento deverá estar assim:
```bash
app
├── ...
├── configuration                           		
│   ├── __init__.py          
│   └── api.py        
├── controllers
│   └── default.py              
└── server.py
```
Conforme exemplificado a rota default(padrão) é

    controller = None
    area = None
    module = "default"
    action="index"
    id = None


O arquivo ficará assim:

```python

controllers/default.py

# -*- coding: utf-8 -*-
from bravaweb.controller import *

class DefaultController(Controller):

    @get
    async def index(self) -> Json:
        await View(self.enviroment, data={"mensagem": 'Olá Mundo'})

```

**Analisando a rota default:**

Nome do Controlador é default, por isso nome da classe é **Default**Controller, herdando o controlador do framework (Controller)

O metodo de request aceito para esta rota é o GET (*@get*) , mas POST (*@post*) , PUT(*@put*) e DELETE(*@delete*) também são aceitos. Uma requisição diferente do permitido para rota retorna Erro *405: Method not allowed*

O Framwork é baseado em ASGI (_Asynchronous Server Gateway Interface_) por isso ação index é assíncrona (async) .

A anotação é o tipo de resultado que essa rota irá retornar, posteriormente veremos sobre os tipos, no exemplo acima utilizamos Json.

Todos os dados da requisição, estão na *enviroment*, veremos mais logo a seguir.


Para melhor compreenção sobre as rotas , vejamos os exemplos abaixo baseado no arquivo de configuração acima:

# Criando e Configurando Rotas

Os padrões de rota é configurado no arquivo de configurações em routes. Você provavelmente fará isso somente uma vez, ou quando for necessária a criação de rotas específicas em seu projeto.  Abaixo segue alguns exemplos baseado na configuração que apresentamos.

## Exemplo 1

    GET -> api.dominio.com.br/admin/catalog/products/list

A regra identificada é a primeira da lista, pois o path da request inicia com */admin/* conforme expressão regular da posição [1]  da tupla em *configuration.api.routes*:

    ("{controller}/{area}/{module}/{action}/{id}", '(^/admin/)|(^/panel/)'

O resultado da captação da rota conforme posição [0] da tupla será:

    controller = 'admin'
    area = 'catalog'
    module = 'products'
    action = 'list'

A estrutura para processamento desta rota devera ser:

```bash
app
├── ...    
├── controllers
│   └── admin
│   │	└── catalog
│   │	|	└── products.py                
```

O arquivo :

```python

controllers/admin/catalog/products.py

# -*- coding: utf-8 -*-
from bravaweb.controller import *

class ProductsController(Controller):

    @get
    async def list(self) -> Json:
        await View(self.enviroment, data=[{"prod_nome": 'Exemplo'}])

```

## Exemplo 2

    POST -> api.dominio.com.br/site/product/like/110

A regra identificada é a default (segunda da lista), pois o path da request **não** contempla as expressões regulares anteriores :

     ("{controller}/{module}/{action}/{id}", "")

O resultado da captação da rota conforme posição [0] da tupla será:

    controller = 'site'
    area = None
    module = 'product'
    action = 'like'
    id = 110

A estrutura para processamento desta rota devera ser:

```bash
app
├── ...    
├── controllers
│   └── site
│   │	└── product.py                
```

O arquivo:

```python

controllers/site/products.py

# -*- coding: utf-8 -*-
from bravaweb.controller import *

class ProductController(Controller):

    @post
    async def like(self) -> Json:
        await View(self.enviroment, data=[{"likes": 535}])

```

# Ambiente / Enviroment

A qualquer momento dentro do controlador é possivel acessar  os dados da requisição através de *self.enviroment* os dados disponíves são:

|Campo  | Tipo | descrição |
|--|--|--|
| origin | string | Origem ou Referrer da Requisição|
| remote_ip | string |  Ip do usuário|
| remote_uuid | string | UUID se informado no header |
| browser | string | Browser do usuário |
| accept_encoding |  string | tipos de codificação aceito pelo browser |
| method | string | metodo da requisição (GET, POST, PUT ou DELETE) |
| response_type| string | tipo de resposta esperada para requisição|
| authorization| string | Token JWT - Bearer enviado no Header|
| bearer| string | Token JWT decodificado |
| content_length| int | Tamanho da requisição |
| get| dict | Dados enviados por querystring |
| post| dict  | Dados enviados por post |
| body | bytes | Bytes do corpo da requisição |
| route | string | rota |
| controller | string | nome controlador |
| area  |  string | nome area do controlador |
| module  | string |  nome modulo do controlador |
| action  | string | nome da ação do modulo |
| id  | string | identificador da requisição |

Há disponível também, para casos de manipulação específica os dados brutos do ASGI:

|Campo  | descrição |
|--|--|
| headers | cabeçalho da requisição |
| scope | escopo da requisição |
| send | conexão com navegador |
| receive | dados recebidos  |

# Entradas e Pré-condições

Para maior segurança no processamento das rotas é possível e **recomendável** estabelecer as pré-condições daquela rota específica.  Caso a requisição não tenha o objeto ou objeto informado seja inválido, haverá erro de resposta com erro *412: Precondition Failed*

```python
    @post
    async def comment(self, id_product:int, comment:string ) -> Json:
	    sql_query = f"INSERT  INTO products_comments (prod_comment, id_product) VALUES ('{comment}',{id_product})";
	    .
		.
		.
        await View(self.enviroment, data=[{"added": true}])

```

Caso a request não contenha os parametros acima, a ação não será executada.

É possível requerer objetos específicos, Bravaweb realiza o cast automático dos dados enviados, no caso datetime o parametro de conversão esta estabelecido no arquivo de configuração nos campos *date_format* e *short_date_format*.

```python
from datetime import datetime
from decimal import Decimal
.

    @post
    async def comment(self, id_product:int, comment:string, date:datetime, stars:Decimal) -> Json:
	    .
		.
		.
	    .
		.
		.
        await View(self.enviroment, data=[{"added": true}])

```

#  View

Toda rota deve retornar uma view, que será baseada na anotação a action.
```python
        await View(self.enviroment, data=_response_data)
```

Bravaweb possui tratamento específico para respostas Json e HTML, ambos possuem um modelo ou carregamento de  template para resposta.

A View possui os seguintes campos de entrada

| entrada | obrigatório | tipo | descrição
|--|--|--|--|
| enviorment | sim | bravaweb.enviroment | ambiente da requisição
| data | sim | bytes-like, dict, list, string |  dados da resposta de acordo com anotação
| success | não | boolean | sucesso na execução da action
| token | não | string | auth token, caso não informado, havendo token no enviroment, o mesmo se repetirá
| task | não | dict, list, string | dados sobre execução em segundo plano
| error | não | dict, list, string | mensagem de erro


# Anotações e Tipos de Resposta


|tipo  | Entrada |
|--|--|
| Html | dict |
| Css | bytes-like object |
| Csv | bytes-like object |
| JavaScript | bytes-like object |
| Jpg | bytes-like object |
| Json | dict, list, string |
| Mp4 |bytes-like object  |
| Pdf | bytes-like object |
| Png |  bytes-like object|
| TextPlain | bytes-like object |
| Xml | bytes-like object |


# Json
O template Json é composto da seguinte forma:

Json = {
	    "token": "",
	    "success": True,
	    "date": "",
	    "itens": 0,
	    "data": [],
}

Onde os dados respondidos estarão dentro de "data".
```python
    @get
    async def index(self) -> Json:
        await View(self.enviroment, data=[{"added": true}])
```


#  HTML e Template Mako

Para mais informações sobre a criação de templates Mako acesse: https://www.makotemplates.org/

A estrutura das Views HTML desenvolvidas em Mako devem estar assim:

```bash
app
├── ...
├── configuration                           		  
├── controllers
├── views
│   └── shared   
│   |	└── default.html              
└── server.py
```

Quando não há uma view definida para rota, o template padrão a ser carregado será o default.

é possível  criar views específicas para cada rota conforme exemplo abaixo:

Rota: **/product/detail**

```python
    @get
    async def index(self) -> Html:
        await View(self.enviroment, data=[{"added": true}])
```

**Template:**

```bash
app
├── ...
├── configuration                           		  
├── controllers
├── views
│   └── product   
│   |	└── detail
│   |	|	└── index.html  
│   └── shared                
└── server.py
```


# Decoradores

Bravaweb é compatível com encapsulamento através de decorador e a criação deve seguir o modelo abaixo:

**Decorador de Método Síncrono:**

```python
def decorator_example(f):
    def example_decorator(cls, **args) -> f:
        return f(cls, **args)
    return example_decorator
```

**Decorador de Método Assíncrono:**

```python
def decorator_example_async(f):
    async def example_decorator(cls, **args) -> f:
        return await f(cls, **args)
    return example_decorator
```

**O uso do decorador em um método síncrono  ficaria assim:**

```python
    @decorator_example
    def __init__(self):
        .
        .
```

**O uso do decorador em uma rota ficaria assim:**

```python
    @decorator_example_async
    async def index(self) -> Html:
        await View(self.enviroment, data=_response_data)
```


**É possível também criar decorar para um controlador inteiro, a função "decora" todos os métodos executáveis, observe que os métodos padrões de classe  __init__ e __del__ são métodos síncronos e por isso o decorador síncrono, e demais métodos (actions) com decorador assíncrono.**

```python
def decorator_example_klass():
    def decorate(cls):
        for attr in cls.__dict__:
            _method = getattr(cls, attr)
            if hasattr(_method, '__call__'):
                if attr == "__init__" or attr == "__del__":
                    setattr(cls, attr, example_decorator(_method))
                else:
                    setattr(cls, attr, decorator_example_async(_method))
        return cls
    return decorate
```

# Erros:

A qualquer momento no processamento da sua rota é possível responder  com as seguintes mensagens de erro:

| Metoto | Código de Resposta  | Mensagem |
|--|--|--|
| NoContent | 204  | 204: No Content
| Unauthorized | 401  | 401: Unauthorized
| NotFound | 404  | 404: Not Found
| NotAllowed | 405  | 405: Method not allowed
| PreconditionFailed | 412  | 412: Precondition Failed
| InternalError | 500  | 500: Internal Error

**Exemplo requisição de um arquivo pdf:**

```python

import os.path

    @get
    async def index(self, file_path:str) -> Pdf:
	    if os.path.exists(file_path):
			_file_data = open(file_path,'r')
	        await View(self.enviroment, data = _file_data.read())
	    else:
		    self.NotFound()
```


## License

MIT
