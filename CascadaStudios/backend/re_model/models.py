from django.db import models
import uuid

# Create your models here.
class TimeStampedModel(models.Model):
    """
    An abstract base class to be inherited by all the other models that need to
    have unique IDs and be time stamped.
    """
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Portfolio(TimeStampedModel):
    """
    Each Portfolio contains Projects
    """
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"

class Project(TimeStampedModel):
    """
    Each Project contains ProjectComponents
    """
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)

    name = models.CharField(max_length=64)
    address = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.name}"

class ProjectComponentModel(TimeStampedModel):
    """
    An abstract base class for inheritance to make sure the rules for deletion
    of all the ProjectComponents is the same.
    """
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    class Meta:
        abstract = True

class Assumption(ProjectComponentModel):
    """
    Foundational constants for the functioning of Real Estate modeling
    """
    vacancy_rate = models.DecimalField(decimal_places=4, max_digits=6)
    income_trend = models.DecimalField(decimal_places=4, max_digits=6)
    expense_trend = models.DecimalField(decimal_places=4, max_digits=6)

class Loan(ProjectComponentModel):
    """
    Loans are the unit of debt for Sources in a project
    """
    name = models.CharField(max_length=64)
    principal = models.DecimalField(decimal_places=2, max_digits=15)
    interest_rate = models.DecimalField(decimal_places=4, max_digits=8)
    amort_term = models.IntegerField()
    loan_term = models.IntegerField()
    closing_date = models.DateTimeField()
    first_pay_date = models.DateTimeField()

    def __str__(self):
        return f"{self.name}"

class Unit(ProjectComponentModel):
    """
    The basic form of Income to the Project
    """
    count = models.IntegerField()
    rent = models.DecimalField(decimal_places=2, max_digits=10)
    beds = models.IntegerField()
    baths = models.DecimalField(decimal_places=2, max_digits=5)
    sqft = models.DecimalField(decimal_places=2, max_digits=15)
    description = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.beds}BR - {self.project}"

class UseLineItem(ProjectComponentModel):
    """
    Line Items are the most granular form of Uses and each can have a different
    tax treatment which will affect the rate of losses from the Project
    """
    name = models.CharField(max_length=64)
    amount = models.DecimalField(decimal_places=2, max_digits=15)

    TAX_CHOICES = (
        ("Depreciable", 'Depreciable'),
        ("Non-Depreciable", 'Non-Depreciable'),
        ("Expensed", 'Expensed'),
        ("Amortized", 'Amortized')
    )

    tax_treatment = models.CharField(max_length=15, choices=TAX_CHOICES)

    def __str__(self):
        return f"{self.name}"

class ExpenseLineItem(ProjectComponentModel):
    """
    Line Items are the most granular form of Expenses and each can have a different
    trending over the life of the Project. For now, we'll assume a flat trending from
    the Assumptions model
    """
    name = models.CharField(max_length=64)
    amount = models.DecimalField(decimal_places=2, max_digits=15)

    def __str__(self):
        return f"{self.name}"
