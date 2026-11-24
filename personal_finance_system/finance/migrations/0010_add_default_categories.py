
from django.db import migrations


def create_default_categories(apps, schema_editor):

    Category = apps.get_model("finance", "Category")

    default_categories = {
        "income": [
            "Salary",
            "Allowance",
            "Business Income",
            "Freelance Income",
            "Gift",
        ],

        "expense": [
            "Food",
            "Transport",
            "Rent",
            "Tuition",
            "Entertainment",
            "Shopping",
            "Utilities",
            "Healthcare",
        ],

        "savings": [
            "Emergency Fund",
            "Personal Savings",
            "Education Savings",
            "Travel Savings",
        ],

        "investment": [
            "Stocks",
            "Bonds",
            "Money Market Fund",
            "Fixed Deposits",
        ],

        "debt_repayment": [
            "Student Loan",
            "Personal Loan",
            "Credit Card",
            "Fuliza",
        ],
    }

    for category_type, names in default_categories.items():

        for name in names:

            Category.objects.get_or_create(
                name=name,
                type=category_type,
                user=None
            )


class Migration(migrations.Migration):

    dependencies = [
        ("finance", "0009_category_user_alter_category_type"),
    ]

    operations = [
        migrations.RunPython(
            create_default_categories,
            migrations.RunPython.noop
        ),
    ]
