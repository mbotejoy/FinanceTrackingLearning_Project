from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from users.forms import RegisterForm

def landing(request):
    return render(request, 'landing.html')

@login_required
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

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(
            request,
            email=email,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect("home")

        messages.error(
            request,
            "Invalid email address or password."
        )

    return render(request, "login.html")

def logout_view(request):

    logout(request)

    return redirect("landing")


def register(request):

    # Already logged-in users do not need to register again.
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            # Use the email as the username.
            user.username = user.email

            user.save()

            messages.success(
                request,
                "Account created successfully. Please sign in."
            )

            return redirect("login")

    else:
        form = RegisterForm()

    return render(
        request,
        "register.html",
        {"form": form}
    )