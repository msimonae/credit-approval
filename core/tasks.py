from celery import shared_task
from django.core.mail import send_mail
from time import sleep
from . import serializers
from rest_framework.compat import requests
import json
from django.db.migrations import serializer
from core.models import Proposal
from datetime import date
from uuid import UUID
from core.models import Loan

status = ('EM ANÁLISE')

@shared_task
def sleepy(duration):
    sleep(duration)
    return None

@shared_task
def send_email_task():
    sleep(10)
    print("Hello World")
    #send_mail('Celery Task Worked',
    #'This is proof the task worked',
    return None

def consultaComprometimento(dados):
    
    headers = {'x-api-key': 'SnAB7jQEFs1Ai8XtZdssa14gORT3jWPI7TWdXN97', 'Content-Type': 'application/json', 'charset': 'utf8'}
    url = 'https://challenge.noverde.name/commitment'
    data = json.dumps(dados)
    request1 = requests.post(url = url, data = data, headers = headers)
    print(data)
    resultado = request1.json()

    print(resultado.get('commitment'))
    commitment = resultado.get('commitment')
    print(commitment)
    assert commitment >= 0
    return commitment

def consultaScore(dados):
    headers = {'x-api-key': 'SnAB7jQEFs1Ai8XtZdssa14gORT3jWPI7TWdXN97', 'Content-Type': 'application/json', 'charset': 'utf8'}
    url = 'https://challenge.noverde.name/score'
    data = json.dumps(dados)
    print(data)
    request1 = requests.post(url = url, data = data, headers = headers)
    resultado = request1.json()

    print(resultado.get('score'))
    score = resultado.get('score')
    print(score)
    return score

def calculoValorParcela(dados, score, comprometimento):
    data = json.dumps(dados)
    print(data)
    print(dados['income'])
    salario = dados['income']
    print(salario)
    print(comprometimento)
    rendaDisponivel = float(salario) - (float(comprometimento) * float(salario))
    print(rendaDisponivel)
    assert int(dados['terms']) == 6 or int(dados['terms']) == 9 or int(dados['terms']) == 12
    QTDparcelas = int(dados['terms'])
    
    amount = float(dados['amount'])
    taxa = 0.0

# Verifica o comprometimento da renda disponível x valor parcela 
# Verificar a possibilidade de financiar com maior número de parcelas

# Verifica o comprometimento da renda disponível x valor parcela 
# Verificar a possibilidade de financiar com maior número de parcelas

    if score >= 900 and (QTDparcelas == 6 or QTDparcelas == 9 or QTDparcelas == 12) :

        if QTDparcelas == 6 :
            taxa = 0.039

        if QTDparcelas == 9 :
            taxa = 0.042

        if QTDparcelas == 12 :
            taxa = 0.045

        VALParcela = amount * ((1 + taxa ) ** QTDparcelas) * taxa / ((1 + taxa) ** QTDparcelas - 1 )

        if rendaDisponivel < VALParcela:
            status = "RECUSADO"
        else: status = "APROVADO"
            
        if rendaDisponivel < VALParcela:
            QTDparcelas = 9
        
        if QTDparcelas == 6 :
            taxa = 0.039

        if QTDparcelas == 9 :
            taxa = 0.042

        if QTDparcelas == 12 :
            taxa = 0.045

        if QTDparcelas == 9:
            VALParcela = amount * ((1 + taxa ) ** QTDparcelas) * taxa / ((1 + taxa) ** QTDparcelas - 1 )

            if rendaDisponivel < VALParcela:
                QTDparcelas = 12

                if QTDparcelas == 6 :
                    taxa = 0.039

                if QTDparcelas == 9 :
                    taxa = 0.042

                if QTDparcelas == 12 :
                    taxa = 0.045

                if QTDparcelas == 12:
                    VALParcela = amount * ((1 + taxa ) ** QTDparcelas) * taxa / ((1 + taxa) ** QTDparcelas - 1 )
                    if rendaDisponivel < VALParcela:
                        status = "RECUSADO"
                    else: 
                        status = "APROVADO"    

    if (score >= 800 and score <= 899) and (QTDparcelas == 6 or QTDparcelas == 9 or QTDparcelas == 12) :

        if QTDparcelas == 6 :
            taxa = 0.047

        if QTDparcelas == 9 :
            taxa = 0.050

        if QTDparcelas == 12 :
            taxa = 0.053

        VALParcela = amount * ((1 + taxa ) ** QTDparcelas) * taxa / ((1 + taxa) ** QTDparcelas - 1 )

        if rendaDisponivel < VALParcela:
            status = "RECUSADO"
        else: status = "APROVADO"
            
        if rendaDisponivel < VALParcela:
            QTDparcelas = 9
        
        if QTDparcelas == 6 :
            taxa = 0.047

        if QTDparcelas == 9 :
            taxa = 0.050

        if QTDparcelas == 12 :
            taxa = 0.053

        if QTDparcelas == 9:
            VALParcela = amount * ((1 + taxa ) ** QTDparcelas) * taxa / ((1 + taxa) ** QTDparcelas - 1 )

            if rendaDisponivel < VALParcela:
                QTDparcelas = 12

                if QTDparcelas == 6 :
                    taxa = 0.047

                if QTDparcelas == 9 :
                    taxa = 0.050

                if QTDparcelas == 12 :
                    taxa = 0.053

                if QTDparcelas == 12:
                    VALParcela = amount * ((1 + taxa ) ** QTDparcelas) * taxa / ((1 + taxa) ** QTDparcelas - 1 )
                    if rendaDisponivel < VALParcela:
                        status = "RECUSADO"
                    else: 
                        status = "APROVADO"

    if (score >= 700 and score <= 799) and (QTDparcelas == 6 or QTDparcelas == 9 or QTDparcelas == 12):

        if QTDparcelas == 6 :
            taxa = 0.055

        if QTDparcelas == 9 :
            taxa = 0.058

        if QTDparcelas == 12 :
            taxa = 0.061

        VALParcela = amount * ((1 + taxa ) ** QTDparcelas) * taxa / ((1 + taxa) ** QTDparcelas - 1 )

        if rendaDisponivel < VALParcela:
            status = "RECUSADO"
        else: status = "APROVADO"
            
        if rendaDisponivel < VALParcela:
            QTDparcelas = 9
        
        if QTDparcelas == 6 :
            taxa = 0.055

        if QTDparcelas == 9 :
            taxa = 0.058

        if QTDparcelas == 12 :
            taxa = 0.061

        if QTDparcelas == 9:
            VALParcela = amount * ((1 + taxa ) ** QTDparcelas) * taxa / ((1 + taxa) ** QTDparcelas - 1 )

            if rendaDisponivel < VALParcela:
                QTDparcelas = 12

                if QTDparcelas == 6 :
                    taxa = 0.055

                if QTDparcelas == 9 :
                    taxa = 0.058

                if QTDparcelas == 12 :
                    taxa = 0.061

                if QTDparcelas == 12:
                    VALParcela = amount * ((1 + taxa ) ** QTDparcelas) * taxa / ((1 + taxa) ** QTDparcelas - 1 )
                    if rendaDisponivel < VALParcela:
                        status = "RECUSADO"
                    else: 
                        status = "APROVADO"
    
    if (score >= 600 and score <= 699) and (QTDparcelas == 6 or QTDparcelas == 9 or QTDparcelas == 12):

        if QTDparcelas == 6 :
            taxa = 0.064

        if QTDparcelas == 9 :
            taxa = 0.066

        if QTDparcelas == 12 :
            taxa = 0.069

        VALParcela = amount * ((1 + taxa ) ** QTDparcelas) * taxa / ((1 + taxa) ** QTDparcelas - 1 )

        if rendaDisponivel < VALParcela:
            status = "RECUSADO"
        else: status = "APROVADO"
            
        if rendaDisponivel < VALParcela:
            QTDparcelas = 9
        
        if QTDparcelas == 6 :
            taxa = 0.064

        if QTDparcelas == 9 :
            taxa = 0.066

        if QTDparcelas == 12 :
            taxa = 0.069

        if QTDparcelas == 9:
            VALParcela = amount * ((1 + taxa ) ** QTDparcelas) * taxa / ((1 + taxa) ** QTDparcelas - 1 )

            if rendaDisponivel < VALParcela:
                QTDparcelas = 12

                if QTDparcelas == 6 :
                    taxa = 0.064

                if QTDparcelas == 9 :
                    taxa = 0.066

                if QTDparcelas == 12 :
                    taxa = 0.069

                if QTDparcelas == 12:
                    VALParcela = amount * ((1 + taxa ) ** QTDparcelas) * taxa / ((1 + taxa) ** QTDparcelas - 1 )
                    if rendaDisponivel < VALParcela:
                        status = "RECUSADO"
                    else: 
                        status = "APROVADO"                    

    assert status == "APROVADO" or status == "RECUSADO" or "EM ANÁLISE"
    assert QTDparcelas == 6 or QTDparcelas == 9 or QTDparcelas == 12
    x = [status, QTDparcelas]
    return x

def validaPoliticaIdade(idade):
    if idade >= 18:
        return True
    else:
        return False

    return True

def converteNascimentoEmIdade(dtNascimentoStr):
    import datetime
    """
    Recebe a data de nascimento e retorna a idade
    """
    dtNascimentoData = datetime.datetime.strptime(dtNascimentoStr, '%Y-%m-%d').date()
    diferenca = (date.today() - dtNascimentoData)
    result = int((diferenca.days / 365))
    return result

@shared_task
def consultas_bureau_task(serializer):
    statusSolicitacao = "processing"
    dados = serializer
    UUID = dados['id']
    amount = float(dados['amount'])
    print(dados)

    idade = converteNascimentoEmIdade(dados["birthdate"])
    y = []
    y =[None, None]

    if validaPoliticaIdade(idade) == False:
        status = "RECUSADO"
        refused_policy = "age"
        y[0] = "RECUSADO"
        y[1] = None
        amount = None

    elif consultaScore(dados) < 600:
        status = "RECUSADO"
        refused_policy = "score"
        y[0] = "RECUSADO"
        y[1] = None
        amount == None

    elif consultaComprometimento(dados) == 1:
        status = "RECUSADO"
        refused_policy = "commitment"
        y[0] = "RECUSADO"
        y[1] = None
        amount == None
        
    else:
        y = calculoValorParcela(dados, consultaScore(dados), consultaComprometimento(dados))      
        print(y)
        status = y[0]
        QTDparcelas = y[1]

        if status == "RECUSADO":
            refused_policy = "commitment"
            y[0] = "RECUSADO"
            y[1] = None
            amount == None

    print(y[0])
    print(y[1])
    

    data = json.dumps(dados)    
    statusSolicitacao = "completed"
    if statusSolicitacao == "completed":
        if status == "RECUSADO":
            resultSolicitacao = "refused"
            amount = None
            terms = None
        if status == "APROVADO":
            resultSolicitacao = "approved"
            refused_policy = None    

    print(status)

    if amount == None:
        assert amount == None
    
    assert statusSolicitacao == "processing" or statusSolicitacao == "completed"
    assert resultSolicitacao == "approved" or resultSolicitacao == "refused" or resultSolicitacao == None
    assert refused_policy == None or refused_policy == "age" or refused_policy == "score" or refused_policy == "commitment"

    if statusSolicitacao == "completed":
        resposta = Proposal(status=statusSolicitacao, result=resultSolicitacao, refused_policy=refused_policy, amount=amount, terms=y[1], loan_id=Loan(serializer['id']))
        resposta.save()        
    return True