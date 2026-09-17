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

    # Admin
    path("admin/", admin.site.urls),

    # Landing Page
    path("", views.landing, name="landing"),

    # UserDashboard
    path("userdashboard/", views.user, name="home"),


    # Authentication
    path("login/", views.login_view, name="login"),
    path("register/", views.register, name="register"),


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
]
