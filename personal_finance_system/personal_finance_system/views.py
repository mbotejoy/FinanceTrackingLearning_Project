from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from users.forms import RegisterForm
from django.core.exceptions import PermissionDenied
from functools import wraps

def landing(request):
    return render(request, 'landing.html')

User = get_user_model()
def is_admin(user):
    return (
        user.is_authenticated
        and user.role == "admin"
        and user.is_staff
    )

# Unauthorized users receive a 403 Forbidden response 
# instead of being redirected to a dashboard they might not be permitted to access
def admin_required(view_func):
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        if not is_admin(request.user):
            raise PermissionDenied

        return view_func(request, *args, **kwargs)

    return wrapper


@admin_required
def admin_dashboard(request):

    context = {
        "total_users": User.objects.count(),
        "total_students": User.objects.filter(
            role="student"
        ).count(),
        "total_admins": User.objects.filter(
            role="admin",
            is_staff=True
        ).count(),
    }

    return render(
        request,
        "admin_dashboard.html",
        context
    )
#retrieves registered users from your existing users database table
@admin_required
def admin_users(request):

    users = User.objects.all().order_by("-date_joined")

    context = {
        "users": users,
        "total_users": users.count(),
    }

    return render(request, "admin_users.html", context)

@login_required
def user(request):
    if is_admin(request.user):
        return redirect("admin_dashboard")
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


def dashboard_redirect(user):
    if is_admin(user):
        return redirect("admin_dashboard")

    return redirect("home")


def login_view(request):

    # Redirect users who are already logged in.
    if request.user.is_authenticated:
        return dashboard_redirect(request.user)

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

            # Redirect according to the role stored in the database.
            return dashboard_redirect(user)

        messages.error(
            request,
            "Invalid email address or password."
        )

    return render(request, "login.html")

def logout_view(request):

    logout(request)

    return redirect("landing")


def register(request):

    #Already logged-in admin isn't sent to the student dashboard 
    #when they try to access the registration page.
    if request.user.is_authenticated:
        return dashboard_redirect(request.user)

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