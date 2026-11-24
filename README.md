# FinanceWise – Personal Finance Tracking and Learning System

## 1. Project Overview

**FinanceWise** is a web-based personal finance tracking and learning system designed to help young people in Kenya improve how they manage their money, develop responsible spending habits and make informed financial decisions.

The system combines personal finance tracking, machine learning techniques, predictive analysis and rule-based recommendations to provide users with insights into their financial behaviour.

FinanceWise goes beyond simply recording income and expenses. It analyses users' financial activities, identifies spending patterns, helps them monitor their budgets and savings goals, and recommends relevant financial learning materials based on their financial behaviour.

The overall goal is to promote financial awareness, responsible money management and better financial decision-making among Kenyan youth.

## 2. Problem Statement

Many young people experience difficulties managing their personal finances due to limited financial literacy, poor budgeting habits, uncontrolled spending and inadequate savings practices.

Some individuals struggle to:
- Keep track of their income and daily expenses.
- Understand where most of their money goes.
- Develop and maintain realistic budgets.
- Set and achieve savings goals.
- Identify unhealthy spending patterns.
- Make informed financial decisions.
- Access relevant financial education that addresses their personal financial challenges.

Traditional expense-tracking applications mainly focus on recording financial transactions and presenting summaries. They may not provide sufficient personalised insights or connect financial activities with relevant financial education.

FinanceWise addresses this gap by integrating financial tracking with intelligent analysis and financial learning.

## 3. Project Objectives

The main objective of FinanceWise is to develop a web-based personal finance tracking and learning system that uses classification, predictive analysis and rule-based recommendations to support better financial management among youth in Kenya.

The specific objectives are to:

1. Develop a platform that allows users to record, monitor and manage their income and expenses.
2. Implement a classification model to categorise users according to their spending behaviour.
3. Apply predictive analysis to identify potential future spending patterns and provide financial insights.
4. Implement a rule-based recommendation engine that generates personalised financial guidance.
5. Integrate financial literacy materials and quizzes to improve users' financial knowledge.
6. Provide dashboards and reports that help users understand their financial activities and progress.

## 4. Key System Features

### 4.1 User Registration and Authentication
- User registration and login.
- Secure authentication.
- Personalised user dashboards.
- User profile management.

### 4.2 Income and Expense Tracking
- Record income and allowances.
- Record daily expenses.
- Organise transactions using financial categories and subcategories.
- View transaction histories.
- Monitor monthly income and expenditure.

### 4.3 Budget Management
- Create personal budgets.
- Allocate spending limits to different categories.
- Monitor budget utilisation.
- Identify exceeded or nearly exhausted budgets.

### 4.4 Savings Goals Management
- Create personalised savings goals.
- Set target amounts and deadlines.
- Monitor savings progress.
- Identify completed and overdue goals.

### 4.5 Spending Behaviour Classification

FinanceWise incorporates a supervised machine learning classification component that categorises users according to their spending behaviour.

The classification categories include:
- **Low Spending:** Users whose spending behaviour falls within the low spending category.
- **Moderate Spending:** Users whose spending behaviour falls within the moderate spending category.
- **High Spending:** Users whose spending behaviour falls within the high spending category.

The classification process uses financial information and spending-related features to identify the user's spending behaviour.

The resulting classification helps the system provide more relevant financial insights and recommendations.

### 4.6 Predictive Analysis

The predictive analysis component uses historical financial information to identify spending patterns and estimate potential future financial trends.

It helps users:
- Understand their historical expenditure patterns.
- Identify changes in their spending behaviour.
- Gain insights into potential future expenditure.
- Make more informed budgeting decisions.

### 4.7 Rule-Based Recommendations

FinanceWise uses a rule-based recommendation engine to analyse users' financial activities and generate relevant financial guidance.

Recommendations may be triggered by conditions such as:
- Expenses exceeding recorded income.
- High spending ratios.
- Exceeded budgets.
- Missing or inactive savings goals.
- Approaching savings deadlines.
- Completed savings goals.

The system uses predefined financial rules to determine which recommendations are relevant to each user's financial situation.

### 4.8 Personalised Financial Learning

The learning module provides educational materials covering important personal finance topics, including:

- Budgeting.
- Saving.
- Debt management.
- Responsible spending.
- Financial fraud and scams.
- Introduction to investing.

The system also provides quizzes to assess users' understanding of financial concepts.

Learning materials can be recommended based on users' spending behaviour and financial activities, helping them access educational content relevant to their needs.

### 4.9 Financial Dashboards and Insights

FinanceWise provides dashboards that present financial information in an understandable format.

Users can view:
- Income and expenditure summaries.
- Spending patterns.
- Budget performance.
- Savings progress.
- Spending behaviour classification.
- Financial recommendations.
- Relevant learning materials.

### 4.10 Administrative Dashboard

The administrative module allows administrators to manage and monitor the platform.

Administrative functions include:
- Managing registered users.
- Managing financial categories.
- Managing transactions.
- Managing learning materials.
- Managing quizzes and questions.
- Viewing financial and system-related summaries.

## 5. Machine Learning and Intelligent Components

FinanceWise integrates three main analytical and decision-support approaches.

| Component | Technique | Purpose |
|---|---|---|
| Classification | Supervised Machine Learning | Categorises users according to spending behaviour. |
| Predictive Analysis | Predictive Modelling | Analyses historical financial information to estimate spending trends. |
| Recommendation Engine | Rule-Based System | Generates financial guidance based on predefined conditions and user activities. |

These components work together to provide users with more meaningful financial insights rather than simply displaying transaction records.

## 6. Technologies Used

The project uses the following technologies:

| Technology | Purpose |
|---|---|
| Python | Backend development and machine learning implementation. |
| Django | Web application framework. |
| HTML5 | Structuring web pages. |
| CSS3 | Styling and interface design. |
| JavaScript | Client-side functionality and interactivity. |
| Bootstrap | Responsive user interface development. |
| MySQL | Relational database management. |
| Pandas | Dataset manipulation and analysis. |
| NumPy | Numerical computing. |
| Scikit-learn | Machine learning model development and evaluation. |
| Matplotlib | Data visualisation. |
| Seaborn | Statistical data visualisation. |
| Joblib | Saving and loading trained machine learning models. |
| Git and GitHub | Version control and source code management. |

## 7. How FinanceWise Works

The system follows a process that connects users' financial activities with analytical processing and personalised outputs.

**Step 1: Financial Data Input**

Users register and provide financial information by recording their income, expenses, budgets and savings goals.

**Step 2: Data Processing**

The system retrieves and processes the recorded financial information to calculate relevant financial indicators.

**Step 3: Spending Behaviour Classification**

The classification model analyses the relevant financial features and assigns a spending behaviour category.

**Step 4: Predictive Analysis**

The predictive component analyses historical financial data to identify spending patterns and estimate future trends.

**Step 5: Rule-Based Recommendation Generation**

The recommendation engine evaluates predefined financial conditions and generates appropriate financial guidance.

**Step 6: Personalised Financial Learning**

The system identifies relevant financial learning materials based on users' financial activities and spending behaviour.

**Step 7: Presentation of Results**

The user receives financial summaries, visual insights, classifications, predictions and recommendations through the FinanceWise dashboard.

## 8. Target Users

The primary target users of FinanceWise are young people in Kenya who want to improve their personal financial management skills.

The system is particularly intended for:
- University and college students.
- Young adults.
- Young professionals.
- Individuals interested in developing better financial habits.

Administrators are responsible for managing platform users, financial categories and educational content.

## 9. Project Scope

FinanceWise focuses on personal financial management and financial literacy.

The project covers:
- Personal income and expense tracking.
- Budget creation and monitoring.
- Savings goal management.
- Spending behaviour classification.
- Predictive financial analysis.
- Rule-based financial recommendations.
- Financial literacy learning materials.
- Financial quizzes and assessments.
- User and administrative dashboards.

The system is designed as a web-based application and is focused on supporting individual financial decision-making rather than providing professional financial advisory, banking or investment services.

## 10. Expected Benefits

FinanceWise is expected to:

1. Improve financial awareness among young people in Kenya.
2. Encourage responsible spending and budgeting habits.
3. Help users monitor and understand their financial behaviour.
4. Support consistent saving and financial goal setting.
5. Provide personalised financial insights and recommendations.
6. Improve access to relevant financial literacy materials.
7. Encourage informed financial decision-making.

## 11. Future Improvements

Potential future enhancements include:
- Integration with M-Pesa for automated transaction tracking.
- Mobile application development.
- Automated financial alerts and notifications.
- Enhanced financial forecasting capabilities.
- Additional financial literacy topics and interactive learning materials.
- Integration with additional financial data sources.

## 12. Project Significance

FinanceWise demonstrates how information systems, machine learning and financial education can be combined to address personal financial management challenges.

By integrating financial tracking, spending behaviour classification, predictive analysis and rule-based recommendations, the system aims to provide a more informative and educational approach to personal finance management.

Ultimately, FinanceWise seeks to empower young people in Kenya with the knowledge and insights needed to develop healthier financial habits and make better financial decisions.

---

**Project Name:** FinanceWise  
**Project Type:** Final Year Project – Bachelor of Business and Information Technology (BBIT)  
**Primary Focus:** Personal Finance Management and Financial Literacy  
**Target Population:** Youth in Kenya