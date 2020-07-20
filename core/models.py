from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
import uuid

# Create your models here.

class Loan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    cpf = models.CharField(max_length=11)
    birthdate = models.DateField()
    amount = models.DecimalField(
        validators=[MinValueValidator(1000), MaxValueValidator(4000)], decimal_places=2, max_digits=10
    )
    terms = models.IntegerField()
    income = models.DecimalField(decimal_places=2, max_digits=10)

    def __str__(self):
        return self.all


class Proposal(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)   
    loan_id = models.ForeignKey(Loan, on_delete=models.CASCADE)
    status = models.CharField(max_length=15)
    result = models.CharField(max_length=15, null=True)
    refused_policy = models.CharField(max_length=15, default = "", null=True)
    amount = models.FloatField(null=True)
    terms = models.IntegerField(null=True)

    def __str__(self):
        return self.all