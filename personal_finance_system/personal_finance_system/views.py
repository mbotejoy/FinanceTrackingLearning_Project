from django.shortcuts import render

def landing(request):
    return render(request, 'landing.html')

def user(request):
    return render(request, 'user.html')

def transactions(request):
    return render(request, "transactions.html")


def add_transaction(request):
    return render(request, "add_transaction.html")


def budgets(request):
    return render(request, "budgets.html")


def create_budget(request):
    return render(request, "create_budget.html")


def savings_goals(request):
    return render(request, "savings_goals.html")


def create_savings_goal(request):
    return render(request, "create_savings_goal.html")


def financial_insights(request):
    return render(request, "financial_insights.html")


def learning(request):
    return render(request, "learning.html")


def quiz(request):
    return render(request, "quiz.html")


def recommendations(request):
    return render(request, "recommendations.html")


def login_view(request):
    return render(request, "login.html")


def register(request):
    return render(request, "register.html")