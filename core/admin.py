from django.contrib import admin

# Register your models here.
from .models import Loan
from .models import Proposal

admin.site.register(Loan)
admin.site.register(Proposal)
