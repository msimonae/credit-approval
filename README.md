# Credit-approval 


# Introdução
- A Noverde, sendo uma empresa de crédito pessoal, recebe diariamente milhares de solicitações de crédito.
- Cada solicitação passa por um processo de análise, um fluxo com várias etapas, onde o resultado de cada etapa (chamada de política de crédito) retorna um estado de "APROVADO" ou "NEGADO".
- Caso toda as políticas sejam aprovadas, o crédito é liberado.

# Desafio Noverde 

- Desenvolver uma aplicação backend para processar as requisições de crédito, disponibilizando para tal uma API com os seguintes endpoints:

# Requisitos Funcionais

## POST /loan
- Este endpoint é responsável por receber as requisições. Ao recebê-la, você deve armazear os dados enviados pelo cliente para processamento posterior, e gerar um ID (UUID) retornando-o imediatamente.

- O processamento dos dados enviados será executado em background (ex: Sidekiq em Ruby ou Celery em Python). As informações trocadas na requisição e na resposta, precisam ser formatadas em json,

## GET /loan/:id
- Este endpoint irá retornar o status atual da solicitação. Caso o processamento em background já tiver sido concluído, deve-se exibir o status como completed e o resultado no atributo result, caso contrário o status estará como processing.

## API de aprovação de crédito
- APIs de aprovação de crédito acesando Bureau de Crédito para calcular o scoring do cliente para avaliar o risco de crédito

## Políticas de Crédito

- As informações enviadas pelo cliente, são processadas pelo motor de crédito, que nada mais é que um conjunto de etapas (pipelines) com regras que podem negar aquela solicitação.

- Caso todas as etapas sejam processadas com sucesso, a solicitação será aprovada, caso contrário, recusada. O motor de crédito deve seguir a ordem de processamento abaixo:

### Política de Idade
- Aqui, deve-se verificar a idade informada pelo cliente. Caso ele seja menor de 18 anos, esta política irá recusar a solicitação.

### Política de Score

- Cada cliente possui um credit score, um valor que vai de 0 a 1000, sendo 1000 o melhor score e 0 o pior score.

- A consulta do score se dá através do serviço de score (API desenvolvida apenas para este teste). Detalhes da API abaixo:

- Cada cliente possui um credit score, um valor que vai de 0 a 1000, sendo 1000 o melhor score e 0 o pior score.

- A consulta do score se dá através do serviço de score (API desenvolvida apenas para este teste). Detalhes da API abaixo:

### POST https://challenge.noverde.name/score

- REQUEST HEADER

- Esta API utiliza autenticação via token. Você deve solicitar o token previamente através do e-mail dev@noverde.com.br

- x-api-key: $token_informado_por_email
- REQUEST BODY

 {
     "cpf": "12345678901"
 }
- RESPONSE BODY
 {
     "score": 800
 }

- Caso o score do cliente solicitado seja MENOR QUE 600 esta política irá recusar a solicitação.

### Política de Comprometimento

- A idéia do comprometimento de renda está em saber se o cliente conseguirá honrar com o pagamento da parcela, mediante o uso atual da renda.

- Exemplo: João possui uma renda de R$ 1.500,00/mês, porém, 80% dessa renda (R$ 1.200,00) já está comprometida com diversas contas, como luz, aluguel, carro, etc. Logo, se a parcela do empréstimo for maior que R$ 300,00, existe uma grande chance de João não honrar este compromisso.

- A renda comprometida pode ser consultada na seguinte API (desenvolvida exclusivamente para este desafio), que irá retornar a renda comprometida, em decimal, entre 0 e 1.

- POST https://challenge.noverde.name/commitment
- REQUEST HEADER
- Esta API utiliza autenticação via token. Você deve solicitar o token previamente através do e-mail dev@noverde.com.br

- x-api-key: $token_informado_por_email
- REQUEST BODY
 {
     "cpf": "12345678901"
 }
- Exemplo de resposta para 80% da renda comprometida:

- RESPONSE BODY
 {
     "commitment": 0.8
 }
- Após calcular o valor da parcela, deve-se verificar se este é maior que a renda comprometida. Em caso positivo, um novo cálculo com um período maior deve ser efetuado, visando diminuir o valor da parcela.

- Em cada novo cálculo, deve-se verificar se o valor da parcela ultrapassa a renda comprometida.

- Se todos os cálculos forem concluídos (em 6x, 9x e 12x) e mesmo assim a parcela ainda ultrapassar a renda comprometida, esta política deve recusar a solicitação.

- Exemplo
- João solicitou um empréstimo de R$ 2.500,00 para pagar em 6 parcelas. A renda de João é de R$ 1.500,00, mas 80% desta renda está comprometida, sobrando R$ 300,00.

- O sistema calculou a parcela de R$ 500,00. Visto que essa parcela ultrapassa os R$ 300,00, o sistema irá fazer um novo cálculo, porém com 9 parcelas ao invés de 6 como solicitado por João.

- Ao efetuar este cálculo, chegou-se no valor da parcela de R$ 350,00.

- Este valor ainda é maior que os R$ 300,00 que João consegue pagar. Logo, o sistema tenta um novo cálculo, porém agora com 12 parcelas, chegando a um valor de parcela de R$ 280,00.

- Como este valor é menor que R$ 300, esta será a oferta informada para João: R$ 2.500,00 de empréstimo a serem pagos em 12 vezes de R$ 280,00.

- Taxas de Juros
- Abaixo estão as taxas de juros mensais praticadas para este desafio. Estas taxas são relacionadas ao score do cliente + a quantidade de parcelas da oferta.

|   Score    | 6 parcelas  | 9 parcelas |12 parcelas |
| :------------:|:---------------:|:---------------:|:-----:|
|  900 ou mais  | 3,9% | 4,2% | 4,5% |
|  800 a 899    | 4,7% | 5,0% | 5,3% |
|  700 a 799    | 5,5% | 5,8% | 6,1% |
|  600 a 699    | 6,4% | 6,6% | 6,9% |


- Cálculo da Parcela
- O cálculo da parcela (chamado de PMT) leva em consideração 3 variáveis:

- Valor Presente (PV) - é o valor solicitado pelo cliente
- Número de parcelas ou períodos (n) - quantidade de parcelas, neste desafio pode ser apenas 6, 9 ou 12.
- Taxa de juros (i) - a taxa de juros praticada de acordo com a tabela descrita em "Taxas de Juros".


# Requisitos Não funcionais e Técnicos
- Aplicação desenvolvida em Python 3.8.4, Django 3.0.8 e Django Rest-framework 3.11.0 persistndo em um Sistema Gerenciador de Banco de Dados Postgres 12.3, Redis 5.0.9 como Broker, Celery 4.4.6 com Worker para gerenciar filas de processamento assíncrono e o front-end, um simples Html com ReactJS,JavaScripts e CCS.
- Infraestrutura na plataforma em nuvem Heroku hospedando os seguintes recursos :

## Tecnologia utilizadas:
## Backend - API Restfull
### Django  3.0.8  
### Django Rest-framework  3.11.0
### Django-filter   3.2.0  
### Celery  4.4.6  - como Worker
### Redis  5.0.9 - como Broaker
### Banco de dados - Postgres 12.3

## Frontend
### Html,Javascript, React JS e CCS

![Arquitetura da Solução](https://github.com/msimonae/credit-approval/blob/master/Arquitetura.jpg)

# Processo de instalação 

## git clone https://github.com/msimonae/credit-approval.git
## Instalar o Python 3.8.4 - https://www.python.org/downloads/
## pip install -r requirements.txt , onde requirements.txt localizado na raiz do projeto
## Instalar Redis local - https://redis.io/download ou Heroku veja como instalar no site do Heroku - https://devcenter.heroku.com/categories/heroku-redis
## Instalar o Postgres 12.3 - local https://www.postgresql.org/download/ 
### Alterar o arquivo setting.py para :
DATABASES = {
        'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'NOME DA BASE',
        'USER': 'USUARIO',
        'PASSWORD': 'SENHA',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }

}

### Confirar no Heroku - https://devcenter.heroku.com/categories/heroku-postgres

# Testar as APIs 

## POST /loan
### Este endpoint é responsável por receber as requisições :   
### https://credit-approval.herokuapp.com/loan/  
### Abaixo uma consulta no Postman :
![Via Postman: Inserindo os dados análise: ](https://github.com/msimonae/credit-approval/blob/master/Arquitetura.jpg)

## Gerou um uuid = b14813c5-5a29-4fd2-af7a-9bf842414e99

## GET /loan/:id

# Este endpoint irá retornar o status atual da solicitação. 

### ttps://credit-approval.herokuapp.com/loan/b14813c5-5a29-4fd2-af7a-9bf842414e99

### Abaixo uma consulta no Postman :

![Via Postman - Consulta de crédito : ](https://github.com/msimonae/credit-approval/blob/master/Arquitetura.jpg)
