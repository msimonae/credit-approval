from rest_framework import serializers
from .models import Loan
from .models import Proposal

class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ('id', 'name', 'cpf', 'birthdate', 'amount', 'terms', 'income')

class ProposalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proposal
        fields = ('id', 'loan_id', 'status', 'result', 'refused_policy', 'amount', 'terms')

