from django.test import TestCase

from datetime import date

from ..models import Portfolio, Project, Assumption, Loan

# Create your tests here.
class ModelTests(TestCase):

    def setUp(self):
        port = Portfolio.objects.create(name='PortTest') # returns queryset
        proj = Project.objects.create(portfolio=port, name='ProjTest')
        Assumption.objects.create(
            portfolio = port,
            project = proj,
            vacancy_rate=2.00,
            income_trend=3.00,
            expense_trend=4.00
            )
        Loan.objects.create(
            portfolio = port,
            project = proj,
            principal=150000,
            interest_rate=0.0525,
            amort_term=40,
            loan_term=40,
            closing_date=date(2016,3,25),
            first_pay_date=date(2016,4,25)
        )

    def test_deleting_proj_comp_keeps_higher(self):
        """
        If a ProjectComponent is deleted, the Project and Portfolio shouldn't be
        nor should other ProjectComponents
        """
        # Delete ProjectComponent
        proj = Project.objects.filter(name="ProjTest").first()
        Assumption.objects.filter(project=proj).delete()

        # Check if Loan, Project, and Portfolio still exists
        self.assertEquals(len(Loan.objects.all()), 1)
        self.assertEquals(len(Project.objects.all()), 1)
        self.assertEquals(len(Portfolio.objects.all()), 1)

    def test_deleting_proj_keeps_higher_not_lower(self):
        """
        If a Project is deleted, the Portfolio shouldn't be, but all the
        ProjectComponents should
        """
        port = Portfolio.objects.filter(name="PortTest").first()
        proj = Project.objects.filter(name="ProjTest").first()

        # Making ProjectComponent
        Assumption.objects.create(
            portfolio = port,
            project = proj,
            vacancy_rate=2.00,
            income_trend=3.00,
            expense_trend=4.00
            )

        # Delete Project
        proj.delete()

        # Check if ProjectComponent and Portfolio still exists
        self.assertEquals(len(Assumption.objects.all()), 0)
        self.assertEquals(len(Loan.objects.all()), 0)
        self.assertEquals(len(Portfolio.objects.all()), 1)

    def test_deleting_port_deletes_lower(self):
        """
        If a Portfolio is deleted, the Projects and ProjectComponents should be
        """
        port = Portfolio.objects.filter(name="PortTest").first()

        # Making lower objects
        proj = Project.objects.create(portfolio=port, name='ProjTest')
        Assumption.objects.create(
            portfolio = port,
            project = proj,
            vacancy_rate=2.00,
            income_trend=3.00,
            expense_trend=4.00
            )

        # Delete Portfolio
        port.delete()

        # Check if ProjectComponent and Project still exists
        self.assertEquals(len(Assumption.objects.all()), 0)
        self.assertEquals(len(Project.objects.all()), 0)
