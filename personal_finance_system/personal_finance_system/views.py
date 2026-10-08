from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from users.forms import RegisterForm
from django.core.exceptions import PermissionDenied
from functools import wraps
from django.db import transaction
from django.db.models import Q
from django.views.decorators.http import require_POST
from finance.models import Transaction, Category
from finance.forms import CategoryForm
from learning.models import LearningContent
from learning.forms import LearningContentForm


# Display the public landing page.
def landing(request):
    return render(request, 'landing.html')

User = get_user_model()
# Check whether a user has administrator privileges.
def is_admin(user):
    return (
        user.is_authenticated
        and user.role == "admin"
        and user.is_staff
    )

# Unauthorized users receive a 403 Forbidden response 
# instead of being redirected to a dashboard they might not be permitted to access
# Protect a view so only logged-in administrators can access it.
def admin_required(view_func):
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        # Reject non-admin users before running the protected view.
        if not is_admin(request.user):
            raise PermissionDenied

        return view_func(request, *args, **kwargs)

    return wrapper


# Show administrator dashboard counts.
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

# List users with optional search and role or status filters.
@admin_required
def admin_users(request):

    users = User.objects.all().order_by("-date_joined")

    # Get search and filter values
    search = request.GET.get("search", "").strip()
    role = request.GET.get("role", "")
    status = request.GET.get("status", "")

    # Search by first name, last name, or email
    if search:
        users = users.filter(
            Q(first_name__icontains=search)
            | Q(last_name__icontains=search)
            | Q(email__icontains=search)
            | Q(username__icontains=search)
        )

    # Filter by role
    if role in ["student", "admin"]:
        users = users.filter(role=role)

    # Filter by status
    if status == "active":
        users = users.filter(is_active=True)

    elif status == "inactive":
        users = users.filter(is_active=False)

    context = {
        "users": users,
        "total_users": User.objects.count(),
        "total_students": User.objects.filter(role="student").count(),
        "active_users": User.objects.filter(is_active=True).count(),
        "search": search,
        "selected_role": role,
        "selected_status": status,
    }

    return render(request, "admin_users.html", context)

# Activate or deactivate an eligible student account.
@admin_required
@require_POST
def toggle_user_status(request, user_id):

    account = get_object_or_404(User, pk=user_id)

    # Only student accounts can be changed here.
    if (
        account.role != "student"
        or account.is_staff
        or account.is_superuser
    ):
        messages.error(
            request,
            "Administrator and privileged accounts cannot be changed here."
        )
        return redirect("admin_users")

    # Change account status
    account.is_active = not account.is_active
    account.save(update_fields=["is_active"])

    status = "activated" if account.is_active else "deactivated"

    messages.success(
        request,
        f"{account.email} has been {status} successfully."
    )

    return redirect("admin_users")

# Display a confirmation page and delete an eligible student account.
@admin_required
def admin_delete_user(request, user_id):

    account = get_object_or_404(User, pk=user_id)

    # Prevent deletion of administrators and privileged accounts
    if (
        account.pk == request.user.pk
        or account.role != "student"
        or account.is_staff
        or account.is_superuser
    ):
        messages.error(
            request,
            "Administrator accounts cannot be deleted here."
        )
        return redirect("admin_users")

    if request.method == "POST":

        email = account.email

        # Delete user and related records together
        with transaction.atomic():
            account.delete()

        messages.success(
            request,
            f"The account {email} has been permanently deleted."
        )

        return redirect("admin_users")

    return render(
        request,
        "admin_delete_user.html",
        {"account": account}
    )

@admin_required
def admin_transactions(request):

    transactions = Transaction.objects.select_related(
        "user", "category"
    ).all()

    search = request.GET.get("search", "").strip()
    transaction_type = request.GET.get("type", "")
    category_id = request.GET.get("category", "")
    start_date = request.GET.get("start_date", "")
    end_date = request.GET.get("end_date", "")

    # Search transactions by user or description
    if search:
        transactions = transactions.filter(
            Q(user__first_name__icontains=search)
            | Q(user__last_name__icontains=search)
            | Q(user__email__icontains=search)
            | Q(description__icontains=search)
        )

    # Filter by transaction type
    if transaction_type in ["income", "expense"]:
        transactions = transactions.filter(type=transaction_type)

    # Filter by category
    if category_id.isdigit():
        transactions = transactions.filter(category_id=int(category_id))

    # Filter by dates
    from datetime import date

    try:
        if start_date:
            transactions = transactions.filter(
                date__gte=date.fromisoformat(start_date)
            )

        if end_date:
            transactions = transactions.filter(
                date__lte=date.fromisoformat(end_date)
            )
    except ValueError:
        pass

    context = {
        "transactions": transactions,
        "categories": Category.objects.all().order_by("name"),
        "total_transactions": transactions.count(),
        "search": search,
        "selected_type": transaction_type,
        "selected_category": category_id,
        "start_date": start_date,
        "end_date": end_date,
    }

    return render(
        request,
        "admin_transactions.html",
        context
    )
# Show an administrator the details of a selected transaction.
@admin_required
def admin_transaction_details(request, transaction_id):

    transaction = get_object_or_404(
        Transaction.objects.select_related("user", "category"),
        pk=transaction_id
    )

    return render(
        request,
        "admin_transaction_details.html",
        {"transaction": transaction}
    )

# Show the student dashboard, or redirect administrators to theirs.
@login_required
def user(request):
    if is_admin(request.user):
        return redirect("admin_dashboard")
    return render(request, 'user.html')

# Display the transactions page.
def transactions(request):
    return render(request, "transactions.html")


# Display the form for adding a transaction.
def add_transaction(request):
    return render(request, "add_transaction.html")


# Display the budgets page.
def budgets(request):
    return render(request, "budgets.html")


# Display the form for creating a budget.
def create_budget(request):
    return render(request, "create_budget.html")


# Display the user's savings goals.
def savings_goals(request):
    return render(request, "savings_goals.html")


# Display the form for creating a savings goal.
def create_savings_goal(request):
    return render(request, "create_savings_goal.html")


# Display financial insights.
def financial_insights(request):
    return render(request, "financial_insights.html")


# Display the financial learning page.
def learning(request):
    return render(request, "learning.html")


# Display the quiz page.
def quiz(request):
    return render(request, "quiz.html")


# Display personalized recommendations.
def recommendations(request):
    return render(request, "recommendations.html")


# Send users to the dashboard that matches their role.
def dashboard_redirect(user):
    if is_admin(user):
        return redirect("admin_dashboard")

    return redirect("home")


# Authenticate users and redirect them to their dashboard.
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

# Log out the current user and return to the landing page.
def logout_view(request):

    logout(request)

    return redirect("landing")


# Register a new user and show the registration form.
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

@admin_required
def admin_categories(request):

    categories = Category.objects.all().order_by("type", "name")

    return render(
        request,
        "admin_categories.html",
        {"categories": categories}
    )


@admin_required
def admin_category_form(request, category_id=None):

    category = None

    if category_id is not None:
        category = get_object_or_404(Category, pk=category_id)

    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)

        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Category saved successfully."
            )
            return redirect("admin_categories")

    else:
        form = CategoryForm(instance=category)

    return render(
        request,
        "admin_category_form.html",
        {
            "form": form,
            "category": category
        }
    )


@admin_required
@require_POST
def admin_delete_category(request, category_id):

    category = get_object_or_404(Category, pk=category_id)

    if (
        category.transactions.exists()
        or category.budgets.exists()
    ):
        messages.error(
            request,
            "This category is in use and cannot be deleted."
        )
    else:
        category.delete()
        messages.success(
            request,
            "Category deleted successfully."
        )

    return redirect("admin_categories")

@admin_required
def admin_learning(request):

    lessons = LearningContent.objects.all()

    search = request.GET.get("search", "").strip()

    if search:
        lessons = lessons.filter(title__icontains=search)

    context = {
        "lessons": lessons,
        "total_lessons": lessons.count(),
        "search": search,
    }

    return render(request, "admin_learning.html", context)


@admin_required
def admin_learning_form(request, lesson_id=None):

    lesson = None

    if lesson_id is not None:
        lesson = get_object_or_404(
            LearningContent,
            pk=lesson_id
        )

    if request.method == "POST":
        form = LearningContentForm(
            request.POST,
            instance=lesson
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Learning content saved successfully."
            )

            return redirect("admin_learning")

    else:
        form = LearningContentForm(instance=lesson)

    return render(
        request,
        "admin_learning_form.html",
        {
            "form": form,
            "lesson": lesson,
        }
    )


@admin_required
@require_POST
def admin_delete_learning(request, lesson_id):

    lesson = get_object_or_404(
        LearningContent,
        pk=lesson_id
    )

    lesson.delete()

    messages.success(
        request,
        "Learning content deleted successfully."
    )

    return redirect("admin_learning")