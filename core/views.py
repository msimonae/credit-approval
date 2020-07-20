from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .tasks import sleepy, send_email_task
from rest_framework import status, viewsets
from .models import Loan
from .models import Proposal
from .serializers import LoanSerializer
from .serializers import ProposalSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .tasks import consultas_bureau_task
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

class JSONResponse(HttpResponse):
    # An HttpResponse that renders its content into JSON

    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


# Create your views here.
class LoanViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows to be viewed or edited.
    """
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

 # Create your views here.
class ProposalViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows to be viewed or edited.
    """
    queryset = Proposal.objects.all()
    serializer_class = LoanSerializer
   

# api_view

@api_view(['GET', 'POST'])
def loan_list(request):
    # API endpoint that allows member to be viewed or edited made by function.

    if request.method == 'GET':

        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        

    if request.method == 'POST':
        serializer = LoanSerializer(data=request.data)


        if serializer.is_valid():
            serializer.save()
            
            conteudo = serializer.data
            
            consultas_bureau_task.run(conteudo)

            
            return Response(conteudo['id'], status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#@csrf_exempt
def loan_detail(request, uuid):

    if request.method == 'GET':
        loan = Loan.objects.get(id=uuid) 
        serializer = LoanSerializer(loan)
        return JSONResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = LoanSerializer(loan, data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        return JSONResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        loan.delete()
        return HttpResponse(status=204)

def proposal_detail(request, uuid):

    if request.method == 'GET':
        proposal_det = Proposal.objects.get(loan_id=uuid)
        serializer = ProposalSerializer(proposal_det)
        return JSONResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = LoanSerializer(proposal_det, data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        return JSONResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        proposal_det.delete()
        return HttpResponse(status=204)

def index(request):
    sleepy
    return HttpResponse('<h1>Acesso somente via API RESTful</h1>')
