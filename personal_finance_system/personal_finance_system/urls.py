"""
URL configuration for personal_finance_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [

    #Django built-in admin
    path("admin/", admin.site.urls),
    #FinanceWise custom admin dashboard
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),


    # Landing Page
    path("", views.landing, name="landing"),

    # UserDashboard
    path("userdashboard/", views.user, name="home"),


    # Authentication
    path("login/", views.login_view, name="login"),
    path("register/", views.register, name="register"),
    path("logout/", views.logout_view, name="logout"),


    # Transactions
    path(
        "transactions/",
        views.transactions,
        name="transactions"
    ),

    path(
        "transactions/add/",
        views.add_transaction,
        name="add_transaction"
    ),
    path(
    "transactions/<int:transaction_id>/edit/",
    views.edit_transaction,
    name="edit_transaction"
    ),

    path(
    "transactions/<int:transaction_id>/delete/",
    views.delete_transaction,
    name="delete_transaction"
    ),


    # Budgets
    path(
        "budgets/",
        views.budgets,
        name="budgets"
    ),

    path(
        "budgets/create/",
        views.create_budget,
        name="create_budget"
    ),
    path(
    "budgets/<int:budget_id>/edit/",
    views.edit_budget,
    name="edit_budget"
    ),

    path(
    "budgets/<int:budget_id>/delete/",
    views.delete_budget,
    name="delete_budget"
    ),


    # Savings Goals
    path(
        "savings-goals/",
        views.savings_goals,
        name="savings_goals"
    ),

    path(
        "savings-goals/create/",
        views.create_savings_goal,
        name="create_savings_goal"
    ),

    path(
        "savings-goals/<int:goal_id>/edit/",
        views.edit_savings_goal,
        name="edit_savings_goal"
    ),

    path(
        "savings-goals/<int:goal_id>/progress/",
        views.update_savings_progress,
        name="update_savings_progress"
    ),

    path(
        "savings-goals/<int:goal_id>/delete/",
        views.delete_savings_goal,
        name="delete_savings_goal"
    ),


    # Financial Insights
    path(
        "financial-insights/",
        views.financial_insights,
        name="financial_insights"
    ),


    # Learning
    path(
        "learning/",
        views.learning,
        name="learning"
    ),


    # Quiz
    path(
        "quiz/",
        views.quiz,
        name="quiz"
    ),


    # Recommendations
    path(
        "recommendations/",
        views.recommendations,
        name="recommendations"
    ),

    path(
        "user/",
        views.user,
        name="user"
    ),

    # Manage Users
    path(
    "admin-dashboard/users/",
    views.admin_users,
    name="admin_users"
    ),
    #<int:user_id> is used so that Django knows which user
    #account to update
    path(
        "admin-dashboard/users/<int:user_id>/toggle-status/",
        views.toggle_user_status,
        name="toggle_user_status"
    ),
    # Admin Transaction Management
path(
    "admin-dashboard/transactions/",
    views.admin_transactions,
    name="admin_transactions"
),

path(
    "admin-dashboard/transactions/<int:transaction_id>/",
    views.admin_transaction_details,
    name="admin_transaction_details"
),
path(
    "admin-dashboard/users/<int:user_id>/delete/",
    views.admin_delete_user,
    name="admin_delete_user"
),
path(
    "admin-dashboard/categories/",
    views.admin_categories,
    name="admin_categories"
),

path(
    "admin-dashboard/categories/add/",
    views.admin_category_form,
    name="admin_category_add"
),

path(
    "admin-dashboard/categories/<int:category_id>/edit/",
    views.admin_category_form,
    name="admin_category_edit"
),

path(
    "admin-dashboard/categories/<int:category_id>/delete/",
    views.admin_delete_category,
    name="admin_category_delete"
),
path(
    "admin-dashboard/learning/",
    views.admin_learning,
    name="admin_learning"
),

path(
    "admin-dashboard/learning/add/",
    views.admin_learning_form,
    name="admin_learning_add"
),

path(
    "admin-dashboard/learning/<int:lesson_id>/edit/",
    views.admin_learning_form,
    name="admin_learning_edit"
),

path(
    "admin-dashboard/learning/<int:lesson_id>/delete/",
    views.admin_delete_learning,
    name="admin_learning_delete"
),

]
