from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from users.forms import RegisterForm
from django.core.exceptions import PermissionDenied
from functools import wraps
from django.db import transaction
from django.db.models import Q, Sum
from django.views.decorators.http import require_POST
from finance.models import Transaction, Category, Budget, SavingsGoal
from finance.forms import CategoryForm, TransactionForm, BudgetForm,SavingsGoalForm
from learning.models import LearningContent, QuizQuestion
from learning.forms import LearningContentForm
from django.utils import timezone
from .classification_service import classify_student_spending
from datetime import date


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
    today = timezone.localdate()


    monthly_transactions = Transaction.objects.filter(
        user=request.user,
        date__year=today.year,
        date__month=today.month
    )

    monthly_income = (
        monthly_transactions.filter(type="income")
        .aggregate(total=Sum("amount"))["total"] or 0
    )

    monthly_expenses = (
        monthly_transactions.filter(type="expense")
        .aggregate(total=Sum("amount"))["total"] or 0
    )

    available_balance = monthly_income - monthly_expenses

    spending_analysis = classify_student_spending(
        user=request.user,
        year=today.year,
        month=today.month
    )

    context = {
        "monthly_income": monthly_income,
        "monthly_expenses": monthly_expenses,
        "available_balance": available_balance,
        "spending_analysis": spending_analysis,
    }

    return render(request, "user.html", context)



# Display the transactions page.
# Retrieve only the currently logged-in student's records 
#and passes them to the template for rendering.
@login_required
def transactions(request):
    student_transactions = Transaction.objects.filter(
        user=request.user
    ).select_related("category").order_by("-date")

    return render(request, "transactions.html", {
        "transactions": student_transactions
    })

# Display the form for adding a transaction.
@login_required
def add_transaction(request):

    if request.method == "POST":

        form = TransactionForm(request.POST)

        if form.is_valid():

            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()

            messages.success(
                request,
                "Transaction saved successfully."
            )

            return redirect("transactions")

    else:
        form = TransactionForm()

    return render(
        request,
        "add_transaction.html",
        {"form": form}
    )

# Retrieve only the currently logged-in student's records 
#and passes them to the template for rendering.
@login_required
def budgets(request):
    student_budgets = Budget.objects.filter(
        user=request.user
    ).select_related("category").order_by("-start_date")

    return render(request, "budgets.html", {
        "budgets": student_budgets
    })

# Display the form for creating a budget.
@login_required
def create_budget(request):

    if request.method == "POST":

        form = BudgetForm(request.POST)

        if form.is_valid():

            budget = form.save(commit=False)
            budget.user = request.user
            budget.save()

            messages.success(
                request,
                "Budget saved successfully."
            )

            return redirect("budgets")

    else:
        form = BudgetForm()

    return render(
        request,
        "create_budget.html",
        {"form": form}
    )

# Edit an existing transaction
@login_required
def edit_transaction(request, transaction_id):

    transaction = get_object_or_404(
        Transaction,
        id=transaction_id,
        user=request.user #ensures you only edit your own record
    )

    if request.method == "POST":
        form = TransactionForm(
            request.POST,
            instance=transaction
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Transaction updated successfully."
            )

            return redirect("transactions")

    else:
        form = TransactionForm(instance=transaction)

    return render(
        request,
        "add_transaction.html",
        {
            "form": form,
            "editing": True
        }
    )


# Delete an existing transaction
@login_required
@require_POST
def delete_transaction(request, transaction_id):

    transaction = get_object_or_404(
        Transaction,
        id=transaction_id,
        user=request.user
    )

    transaction.delete()

    messages.success(
        request,
        "Transaction deleted successfully."
    )

    return redirect("transactions")


# Edit an existing budget
@login_required
def edit_budget(request, budget_id):

    budget = get_object_or_404(
        Budget,
        id=budget_id,
        user=request.user
    )

    if request.method == "POST":
        form = BudgetForm(
            request.POST,
            instance=budget
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Budget updated successfully."
            )

            return redirect("budgets")

    else:
        form = BudgetForm(instance=budget)

    return render(
        request,
        "create_budget.html",
        {
            "form": form,
            "editing": True
        }
    )


# Delete an existing budget
@login_required
@require_POST
def delete_budget(request, budget_id):

    budget = get_object_or_404(
        Budget,
        id=budget_id,
        user=request.user
    )

    budget.delete()

    messages.success(
        request,
        "Budget deleted successfully."
    )

    return redirect("budgets")

# Display only the logged-in student's savings goals.
@login_required
def savings_goals(request):

    goals = SavingsGoal.objects.filter(
        user=request.user
    ).order_by("target_date")

    return render(
        request,
        "savings_goals.html",
        {"goals": goals}
    )


# Create a new savings goal.

@login_required
def create_savings_goal(request):
    if request.method == "POST":
        form = SavingsGoalForm(request.POST)

        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user

            # Automatically assign the status for new goals
            if goal.current_amount >= goal.target_amount:
                goal.status = "completed"
            else:
                goal.status = "active"

            goal.save()

            messages.success(
                request,
                "Savings goal created successfully."
            )

            return redirect("savings_goals")

        messages.error(
            request,
            "Please correct the errors below and try again."
        )
    else:
        form = SavingsGoalForm()

    return render(
        request,
        "create_savings_goal.html",
        {"form": form}
    )


# Edit a savings goal.
@login_required
def edit_savings_goal(request, goal_id):

    goal = get_object_or_404(
        SavingsGoal,
        pk=goal_id,
        user=request.user
    )

    if request.method == "POST":
        form = SavingsGoalForm(request.POST, instance=goal)

        if form.is_valid():
            updated_goal = form.save(commit=False)

            if updated_goal.current_amount >= updated_goal.target_amount:
                updated_goal.status = "completed"

            updated_goal.save()

            messages.success(
                request,
                "Savings goal updated successfully."
            )

            return redirect("savings_goals")

    else:
        form = SavingsGoalForm(instance=goal)

    return render(
        request,
        "create_savings_goal.html",
        {
            "form": form,
            "goal": goal,
            "editing": True,
        }
    )


# Update the amount saved toward a goal.
@login_required
def update_savings_progress(request, goal_id):

    goal = get_object_or_404(
        SavingsGoal,
        pk=goal_id,
        user=request.user
    )

    if request.method == "POST":
        amount_text = request.POST.get("current_amount", "").strip()

        try:
            from decimal import Decimal, InvalidOperation

            current_amount = Decimal(amount_text)

            if not current_amount.is_finite():
                raise InvalidOperation

            if current_amount < 0:
                raise InvalidOperation

            if current_amount > goal.target_amount:
                messages.error(
                    request,
                    "The saved amount cannot exceed your target."
                )

            else:
                goal.current_amount = current_amount

                if current_amount >= goal.target_amount:
                    goal.status = "completed"
                elif goal.status == "completed":
                    goal.status = "active"

                goal.save(
                    update_fields=["current_amount", "status"]
                )

                messages.success(
                    request,
                    "Savings progress updated successfully."
                )

        except (InvalidOperation, ValueError):
            messages.error(
                request,
                "Enter a valid, non-negative amount."
            )

    return redirect("savings_goals")


# Delete a savings goal.
@login_required
@require_POST
def delete_savings_goal(request, goal_id):

    goal = get_object_or_404(
        SavingsGoal,
        pk=goal_id,
        user=request.user
    )

    goal.delete()

    messages.success(
        request,
        "Savings goal deleted successfully."
    )

    return redirect("savings_goals")

# Display financial insights for the logged-in user.
@login_required
def financial_insights(request):
    today = timezone.localdate()

    # Get this month's transactions for the logged-in user.
    monthly_transactions = Transaction.objects.filter(
        user=request.user,
        date__year=today.year,
        date__month=today.month
    )

    # Calculate monthly income and expenses.
    monthly_income = (
        monthly_transactions
        .filter(type="income")
        .aggregate(total=Sum("amount"))["total"] or 0
    )

    monthly_spending = (
        monthly_transactions
        .filter(type="expense")
        .aggregate(total=Sum("amount"))["total"] or 0
    )

    # Find the category with the highest spending this month.
    highest_category = (
        monthly_transactions
        .filter(type="expense", category__isnull=False)
        .values("category__name")
        .annotate(total=Sum("amount"))
        .order_by("-total")
        .first()
    )

    highest_spending_category = (
        highest_category["category__name"]
        if highest_category
        else "No Data"
    )

    highest_category_amount = (
        highest_category["total"]
        if highest_category
        else 0
    )

    # Prepare spending totals for the last six calendar months.
    spending_trend = []

    for offset in range(5, -1, -1):
        month_index = today.year * 12 + (today.month - 1) - offset
        year = month_index // 12
        month = month_index % 12 + 1

        month_spending = (
            Transaction.objects.filter(
                user=request.user,
                type="expense",
                date__year=year,
                date__month=month
            )
            .aggregate(total=Sum("amount"))["total"] or 0
        )

        spending_trend.append({
            "label": date(year, month, 1).strftime("%b %Y"),
            "total": month_spending,
        })

    # Estimate next month's spending using the average of
    # the previous three completed calendar months.
    previous_months = []

    for offset in range(1, 4):
        month_index = today.year * 12 + (today.month - 1) - offset
        year = month_index // 12
        month = month_index % 12 + 1

        previous_spending = (
            Transaction.objects.filter(
                user=request.user,
                type="expense",
                date__year=year,
                date__month=month
            )
            .aggregate(total=Sum("amount"))["total"] or 0
        )

        previous_months.append(previous_spending)

    predicted_spending = sum(previous_months) / 3

    # Find the largest monthly value to scale the trend bars.
    max_trend_spending = max(
        (item["total"] for item in spending_trend),
        default=0
    )

    context = {
        "monthly_income": monthly_income,
        "monthly_spending": monthly_spending,
        "highest_spending_category": highest_spending_category,
        "highest_category_amount": highest_category_amount,
        "predicted_spending": predicted_spending,
        "spending_trend": spending_trend,
        "max_trend_spending": max(max_trend_spending, 1),
    }

    return render(
        request,
        "financial_insights.html",
        context
    )


# Display the financial learning page.
@login_required
def learning(request):
    lessons = LearningContent.objects.filter(
        is_published=True
    ).order_by("topic", "title")

    return render(
        request,
        "learning.html",
        {"lessons": lessons}
    )

# Allow user to read a lesson in detail.
@login_required
def lesson_detail(request, lesson_id):
    lesson = get_object_or_404(
        LearningContent,
        pk=lesson_id,
        is_published=True
    )

    return render(
        request,
        "lesson_detail.html",
        {"lesson": lesson}
    )

#Allows the user to take a quiz
@login_required
def quiz(request):
    topics = LearningContent.TOPIC_CHOICES

    selected_topic = request.GET.get(
        "topic",
        request.POST.get("topic", "budgeting")
    )

    valid_topics = [value for value, label in topics]

    if selected_topic not in valid_topics:
        selected_topic = "budgeting"

    questions = list(
        QuizQuestion.objects.filter(
            topic=selected_topic,
            is_published=True
        ).order_by("id")
    )

    if request.method == "POST":
        if not questions:
            messages.error(
                request,
                "There are no published questions for this topic yet."
            )
            return redirect("quiz")

        score = 0
        results = []

        for question in questions:
            submitted_answer = request.POST.get(
                f"question_{question.id}",
                ""
            )

            is_correct = (
                submitted_answer == question.correct_answer
            )

            if is_correct:
                score += 1

            results.append({
                "question": question,
                "selected_answer": submitted_answer,
                "is_correct": is_correct,
                "correct_answer": question.correct_answer,
                "explanation": question.explanation,
            })

        percentage = round((score / len(questions)) * 100)

        return render(
            request,
            "quiz.html",
            {
                "topics": topics,
                "selected_topic": selected_topic,
                "questions": questions,
                "results": results,
                "score": score,
                "total_questions": len(questions),
                "percentage": percentage,
                "submitted": True,
            }
        )

    return render(
        request,
        "quiz.html",
        {
            "topics": topics,
            "selected_topic": selected_topic,
            "questions": questions,
            "submitted": False,
        }
    )



# Display personalized recommendations.
@login_required
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