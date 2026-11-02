document.addEventListener("DOMContentLoaded", function () {
    const ruleKey = document.getElementById("id_rule_key");
    const nameField = document.getElementById("id_name");
    const descriptionField = document.getElementById("id_description");
    const messageField = document.getElementById("id_message");
    const thresholdField = document.getElementById("id_threshold_percent");

    if (!ruleKey || !nameField || !descriptionField || !messageField) {
        return;
    }

    const ruleDetails = {
        expenses_exceed_income: {
            name: "Expenses Exceed Income",
            description: "Identifies when a student's total expenses exceed their recorded income.",
            threshold: 80,
            message: "Your expenses are higher than your income. Review your spending, prioritise essential expenses, and look for ways to reduce unnecessary costs."
        },

        moderate_expense_ratio: {
            name: "Moderate Spending",
            description: "Identifies when a student's expenses remain below the configured percentage of their income.",
            threshold: 80,
            message: "You are keeping your expenses within the configured spending threshold. Continue monitoring your budget and setting aside money for savings."
        },

        no_income_recorded: {
            name: "No Income Recorded",
            description: "Identifies when a student has recorded expenses but no income for the current period.",
            threshold: 80,
            message: "You have recorded expenses but no income. Update your income details to help FinanceWise provide more accurate financial insights."
        },

        budget_exceeded: {
            name: "Budget Exceeded",
            description: "Identifies when spending in a budget category exceeds its allocated budget.",
            threshold: 80,
            message: "You have exceeded your budget in a spending category. Review your transactions and adjust your remaining spending where possible."
        },

        no_active_savings_goal: {
            name: "No Active Savings Goal",
            description: "Identifies when a student has no active savings goals.",
            threshold: 80,
            message: "Consider creating a savings goal. Setting a clear target and deadline can help you develop consistent saving habits."
        },

        savings_goal_reached: {
            name: "Savings Goal Reached",
            description: "Identifies when a student's savings reach or exceed a goal's target amount.",
            threshold: 80,
            message: "Congratulations! You have reached your savings goal. Consider setting another financial goal to continue building your savings."
        },

        savings_goal_target_date_passed: {
            name: "Savings Goal Overdue",
            description: "Identifies savings goals whose target dates have passed before the target amount was reached.",
            threshold: 80,
            message: "Your savings goal has passed its target date. Review your progress and consider setting a more realistic deadline."
        },

        savings_goal_approaching: {
            name: "Savings Goal Approaching",
            description: "Identifies savings goals whose target dates are approaching.",
            threshold: 80,
            message: "Your savings goal deadline is approaching. Review how much you still need to save and plan your remaining contributions."
        },

        no_recommendations: {
            name: "General Financial Guidance",
            description: "Provides general financial guidance when no other recommendation rule is triggered.",
            threshold: 80,
            message: "Keep tracking your income and expenses, review your budget regularly, and work towards your savings goals."
        }
    };

    let manuallyEdited = false;

    [nameField, descriptionField, messageField].forEach(function (field) {
        field.addEventListener("input", function () {
            manuallyEdited = true;
        });
    });

    ruleKey.addEventListener("change", function () {
        const selectedRule = ruleDetails[ruleKey.value];

        if (!selectedRule) {
            return;
        }

        // Populate fields when a rule is selected.
        // The admin can edit them afterwards.
        nameField.value = selectedRule.name;
        descriptionField.value = selectedRule.description;
        messageField.value = selectedRule.message;

        if (thresholdField) {
            thresholdField.value = selectedRule.threshold;
        }

        manuallyEdited = false;
    });
});
