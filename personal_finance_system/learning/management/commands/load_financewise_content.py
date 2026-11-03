# Code creates 6 lessons and 30 quizzes with 5 questions each
from django.core.management.base import BaseCommand
from learning.models import LearningContent, QuizQuestion


class Command(BaseCommand):
    help = "Load initial FinanceWise lessons and quiz questions"

    def handle(self, *args, **options):

        # --------------------------------------------------
        # 1. PRELOADED LESSONS
        # --------------------------------------------------

        lessons = [
            {
                "title": "Understanding Budgeting and Expense Tracking",
                "topic": "budgeting",
                "description": (
                    "Learn how to plan your income, control expenses "
                    "and create a realistic student budget."
                ),
                "content": """
BUDGETING AND EXPENSE TRACKING

1. What is a budget?

A budget is a financial plan showing how you expect to receive and
spend money over a particular period. A monthly budget helps you
understand whether your income can cover your needs, wants and
savings goals.

2. Why is budgeting important?

Budgeting helps you:
- Understand where your money goes.
- Avoid unnecessary spending.
- Prioritise essential expenses.
- Prepare for unexpected costs.
- Work towards financial goals.

3. Understanding income and expenses

Income is money you receive. For a student, this could include
pocket money, family support, a part-time job or business income.

Expenses are the costs you pay. Examples include food, transport,
rent, tuition, internet bundles and entertainment.

Expenses can be grouped into needs and wants.

Needs are essential expenses, such as food, accommodation and
transport to university. Wants are optional purchases, such as
frequent entertainment outings or non-essential shopping.

4. Creating a student budget

Start by calculating your expected monthly income. List your
expenses and estimate how much you need for each category.

For example, a student receiving KES 15,000 per month might plan:

Food: KES 5,000
Transport: KES 3,000
Accommodation contribution: KES 3,000
Internet and communication: KES 1,000
Savings: KES 2,000
Other expenses: KES 1,000

Total planned allocation: KES 15,000.

These amounts are examples. Your own budget should reflect your
actual income, needs and circumstances.

5. Tracking expenses

Record each transaction as you spend. Include the date, category,
amount and payment method where appropriate.

For example, record a KES 250 lunch or a KES 100 transport payment.
M-Pesa messages, bank statements and receipts can help you check
your records.

6. Reviewing your budget

Compare actual spending with planned spending regularly.
If you spend more than planned on entertainment, you may need to
reduce other optional expenses or adjust your budget.

A budget is not meant to prevent all enjoyment. It helps you make
intentional decisions about your money.

ACTIVITY

List your expected monthly income and your five largest expenses.
Estimate how much you can save after paying for essential needs.
Review your actual spending at the end of the month.
""",
                "is_published": True,
            },
            {
                "title": "Building Savings Habits and Setting Financial Goals",
                "topic": "saving",
                "description": (
                    "Learn how to set achievable savings goals, build "
                    "consistent habits and prepare for unexpected costs."
                ),
                "content": """
SAVING AND FINANCIAL GOALS

1. What is saving?

Saving means setting aside part of your money for future use
instead of spending all the money you receive.

Savings can help you pay for planned expenses, handle emergencies
and work towards long-term goals.

2. Why should students save?

Students may save for books, tuition-related costs, a laptop,
professional training, accommodation or unexpected expenses.

Having savings can reduce the need to borrow whenever an
unplanned expense occurs.

3. Setting SMART savings goals

A useful financial goal should be:

Specific: Know exactly what you are saving for.
Measurable: Decide how much money you need.
Achievable: Choose an amount you can realistically save.
Relevant: Make sure the goal matters to you.
Time-bound: Set a target date.

For example, saving KES 6,000 for study materials in six months
requires saving KES 1,000 each month.

4. Pay yourself first

Consider setting aside a planned amount as soon as you receive
your income. You can then plan your remaining money around your
essential expenses.

The amount should be realistic. Saving a small amount consistently
may be more sustainable than setting an unrealistic target.

5. Emergency savings

An emergency fund is money reserved for unexpected expenses,
such as urgent transport, essential repairs or an unforeseen bill.

Start with a manageable target and increase your savings when
your financial circumstances allow.

6. Where can you keep savings?

Depending on your needs, you might consider a bank savings
account or another regulated savings service.

Compare fees, access requirements, security and applicable
terms before choosing a provider.

Do not confuse savings with money you have already committed
to immediate expenses.

7. Common saving challenges

Unexpected costs, impulse purchases and irregular income can make
saving difficult.

You can respond by reviewing your budget, setting reminders,
reducing avoidable expenses and adjusting your target when needed.

ACTIVITY

Choose one financial goal. Write the total amount required,
your target date and the amount you need to save each month.
""",
                "is_published": True,
            },
            {
                "title": "Understanding Loans and Managing Debt",
                "topic": "debt",
                "description": (
                    "Understand borrowing costs, repayment obligations "
                    "and how to make informed borrowing decisions."
                ),
                "content": """
UNDERSTANDING LOANS AND MANAGING DEBT

1. What is a loan?

A loan is money borrowed from a lender with an agreement to
repay it under specified conditions.

Borrowing creates an obligation. Before accepting a loan, you
should understand the repayment amount, due date, charges and
consequences of late payment.

2. Understanding the cost of borrowing

The principal is the original amount borrowed.

Interest is the cost charged for borrowing money. Other charges
may also apply, depending on the lender and loan product.

For example, if you borrow KES 5,000 and the total repayment
required is KES 5,600, the additional borrowing cost is
KES 600, assuming no other payments or charges.

Always check the actual terms rather than assuming that the
advertised amount is the total cost.

3. Mobile loans

Mobile-based borrowing can be convenient, but easy access may
encourage repeated borrowing.

Before accepting a mobile loan, check:
- The total repayment amount.
- The repayment deadline.
- Interest and other applicable charges.
- Late-payment consequences.
- Whether repayment fits your budget.

Do not borrow simply because a loan is available.

4. Responsible borrowing

Borrow only when there is a clear reason and a realistic
repayment plan.

Consider whether the expense is necessary, whether alternatives
exist and whether repayment will interfere with essential costs
such as food, accommodation or tuition.

Avoid taking a new loan without carefully considering how it
will affect existing obligations.

5. Managing existing debt

List your outstanding loans, balances, repayment dates and
required payments.

Prioritise required repayments while protecting essential living
expenses. If you cannot pay on time, contact the lender through
official channels to understand your available options.

Do not ignore repayment notices or rely on taking another loan
without assessing the consequences.

6. Credit records

Repayment behaviour may affect your credit history, depending
on the lender and applicable reporting arrangements.

Check your records through authorised channels if you believe
there is an error.

ACTIVITY

Before accepting a loan, write down the amount you will receive,
the total repayment, the due date and the source of repayment.
If you cannot explain how you will repay it, reconsider borrowing.
""",
                "is_published": True,
            },
            {
                "title": "Making Better Spending Decisions",
                "topic": "spending",
                "description": (
                    "Learn to distinguish needs from wants, manage "
                    "impulse purchases and make informed spending choices."
                ),
                "content": """
MAKING BETTER SPENDING DECISIONS

1. Needs versus wants

Needs are expenses required for basic living or essential
responsibilities. Examples include food, necessary transport,
accommodation and required learning materials.

Wants are purchases that may improve comfort or enjoyment but
are not essential. Examples might include optional subscriptions,
frequent entertainment outings or upgrading a device that still
works well.

The distinction depends on your circumstances.

2. Opportunity cost

When you spend money on one thing, you may give up the chance
to use that money for something else.

For example, spending KES 1,500 on an unplanned purchase may
leave less money available for books or savings.

Thinking about opportunity cost helps you compare alternatives
before making a purchase.

3. Impulse spending

Impulse spending occurs when you buy something without
sufficient planning or consideration.

Promotions, social pressure, convenience and online shopping
can encourage unnecessary purchases.

Try waiting before making non-essential purchases. Ask whether
you need the item, whether it fits your budget and whether you
would still choose it after some time.

4. Comparing prices

Compare the total cost, quality, durability and usefulness of
similar products.

The cheapest option is not always the best value. Consider
whether a product meets your needs and whether additional
costs may arise later.

5. Digital spending

Small digital purchases, subscriptions and mobile payments
can accumulate over time.

Review recurring payments and transaction records regularly.
Cancel services you no longer need, where applicable.

6. Social pressure

You do not have to match other people's spending habits.
Friends may have different incomes, responsibilities and
financial goals.

Set spending limits that reflect your circumstances.

7. Practical decision-making

Before spending, consider:
- Is this a need or a want?
- Can I afford it without missing essential expenses?
- Does it fit my budget?
- Is there a less expensive suitable alternative?
- Will this purchase affect my savings goal?

ACTIVITY

Choose one recent non-essential purchase. Consider whether it
was planned, whether it fitted your budget and what alternative
use you could have made of the money.
""",
                "is_published": True,
            },
            {
                "title": "Protecting Yourself from Financial Fraud",
                "topic": "fraud",
                "description": (
                    "Recognise common financial scams and learn how "
                    "to protect your money and personal information."
                ),
                "content": """
PROTECTING YOURSELF FROM FINANCIAL FRAUD

1. What is financial fraud?

Financial fraud involves deception intended to obtain money,
financial benefits or sensitive information unlawfully.

Fraudsters may contact people through phone calls, SMS,
messaging applications, social media, email or fake websites.

2. Common warning signs

Be cautious when a message:
- Claims you have won a prize you did not enter to win.
- Demands immediate payment to receive a reward.
- Requests your PIN, password or one-time verification code.
- Promises unusually high or guaranteed investment returns.
- Uses threats or pressure to make you act quickly.
- Contains suspicious links or impersonates a trusted organisation.

These warning signs should prompt you to verify the claim
independently.

3. Protecting M-Pesa and bank accounts

Never share your PIN or password with another person.

Do not disclose one-time verification codes to callers or
messages claiming to be customer support.

Verify unusual payment requests using official contact details.
Check recipient details carefully before confirming a transfer.

Use official applications and websites rather than links
provided in unexpected messages.

4. Fake investment opportunities

Be careful of schemes promising guaranteed profits, unusually
high returns or rewards for recruiting additional participants.

Before investing, independently verify the provider's identity
and regulatory status through the relevant official authorities.
Do not rely solely on testimonials or screenshots of profits.

5. Protecting personal information

Avoid sharing sensitive financial details publicly.
Use strong, unique passwords where passwords are required,
and secure your devices.

Do not install applications from untrusted sources or grant
unnecessary permissions to unknown applications.

6. What to do if you suspect fraud

Stop communicating with the suspected fraudster and do not
send additional money.

Contact your bank, mobile money provider or relevant service
through its official channels as soon as possible.

Preserve relevant messages, transaction references and other
evidence. Report the incident to the appropriate authorities.

If you shared a password or other credentials, take appropriate
steps to secure the affected account.

ACTIVITY

Review an unexpected financial message. Identify any warning
signs and explain how you would verify it before responding.
""",
                "is_published": True,
            },
            {
                "title": "Introduction to Investing",
                "topic": "investing",
                "description": (
                    "Learn basic investment concepts, risk and return, "
                    "diversification and the importance of research."
                ),
                "content": """
INTRODUCTION TO INVESTING

1. What is investing?

Investing means committing money to an asset or financial
product with the expectation of receiving a return or achieving
a financial goal.

Returns are not guaranteed. The value of an investment can
increase or decrease, and some investments can result in losses.

2. Saving versus investing

Savings are generally intended to preserve money and make it
available when needed.

Investing involves taking some level of risk in pursuit of
potential returns.

Money needed for immediate expenses should not be exposed
to investment risks that could prevent you from meeting those
obligations.

3. Risk and return

Risk refers to the possibility that an investment will produce
a different outcome from what you expect, including losing money.

Potential returns differ between products. Higher advertised
returns do not automatically make an investment suitable.

Consider your financial goals, time horizon, ability to tolerate
losses and understanding of the product.

4. Diversification

Diversification means spreading investments across different
assets or investment types rather than relying entirely on one.

It can reduce exposure to the poor performance of a single
investment, although it cannot eliminate all investment risk.

5. Understanding investment options

Different products have different terms, risks, costs and
requirements. Examples may include government securities,
regulated collective investment schemes and shares.

Research the product and provider before committing money.
Check official information about applicable fees, withdrawal
conditions and risks.

6. Avoiding investment scams

Be cautious of guaranteed profits, pressure to invest quickly
and schemes that depend heavily on recruiting new participants.

Verify providers and their regulatory status independently.
Never invest money solely because a friend or online influencer
claims to have made a profit.

7. Investing responsibly

Start by understanding your budget, managing high-cost debt
and building appropriate savings for essential expenses.

Only consider investing money that fits your circumstances and
financial goals. Seek qualified advice when necessary.

ACTIVITY

Identify one financial goal and decide whether it is short-term
or long-term. Explain what you would need to research before
choosing a suitable savings or investment product.
""",
                "is_published": True,
            },
        ]

        # --------------------------------------------------
        # 2. PRELOADED QUIZ QUESTIONS
        # --------------------------------------------------

        questions = [
            # BUDGETING: 5 QUESTIONS
            {
                "topic": "budgeting",
                "question_text": "What is the main purpose of a budget?",
                "option_a": "To spend all the money received",
                "option_b": "To plan income and expenses",
                "option_c": "To avoid recording purchases",
                "option_d": "To increase borrowing",
                "correct_answer": "B",
                "explanation": (
                    "A budget helps you plan how to allocate income "
                    "to expenses, savings and financial goals."
                ),
            },
            {
                "topic": "budgeting",
                "question_text": (
                    "Which of the following is generally a need for a student?"
                ),
                "option_a": "A new luxury watch",
                "option_b": "An optional gaming subscription",
                "option_c": "Food for daily meals",
                "option_d": "Frequent unplanned outings",
                "correct_answer": "C",
                "explanation": (
                    "Food is generally an essential living expense."
                ),
            },
            {
                "topic": "budgeting",
                "question_text": (
                    "A student receives KES 10,000 and spends KES 7,500. "
                    "How much remains?"
                ),
                "option_a": "KES 1,500",
                "option_b": "KES 2,000",
                "option_c": "KES 2,500",
                "option_d": "KES 3,500",
                "correct_answer": "C",
                "explanation": (
                    "KES 10,000 minus KES 7,500 leaves KES 2,500."
                ),
            },
            {
                "topic": "budgeting",
                "question_text": (
                    "Which is the best way to understand where your money goes?"
                ),
                "option_a": "Rely on memory alone",
                "option_b": "Record and review transactions",
                "option_c": "Ignore small purchases",
                "option_d": "Avoid checking payment records",
                "correct_answer": "B",
                "explanation": (
                    "Recording transactions makes spending easier "
                    "to monitor and compare with a budget."
                ),
            },
            {
                "topic": "budgeting",
                "question_text": (
                    "What should you do if your actual spending repeatedly "
                    "exceeds your budget?"
                ),
                "option_a": "Ignore the difference",
                "option_b": "Borrow automatically",
                "option_c": "Stop tracking expenses",
                "option_d": "Review spending and adjust the budget",
                "correct_answer": "D",
                "explanation": (
                    "Reviewing your expenses helps identify where "
                    "changes may be needed."
                ),
            },

            # SAVING: 5 QUESTIONS
            {
                "topic": "saving",
                "question_text": "What does saving mean?",
                "option_a": "Spending all available income",
                "option_b": "Setting money aside for future use",
                "option_c": "Borrowing money every month",
                "option_d": "Buying items on impulse",
                "correct_answer": "B",
                "explanation": (
                    "Saving involves reserving some money for future "
                    "needs or financial goals."
                ),
            },
            {
                "topic": "saving",
                "question_text": (
                    "A student wants to save KES 6,000 in six months. "
                    "How much should they save each month if contributions "
                    "are equal?"
                ),
                "option_a": "KES 500",
                "option_b": "KES 750",
                "option_c": "KES 1,000",
                "option_d": "KES 2,000",
                "correct_answer": "C",
                "explanation": (
                    "KES 6,000 divided by six months equals "
                    "KES 1,000 per month."
                ),
            },
            {
                "topic": "saving",
                "question_text": (
                    "What is the purpose of an emergency fund?"
                ),
                "option_a": "To fund every entertainment purchase",
                "option_b": "To increase unnecessary borrowing",
                "option_c": "To cover unexpected expenses",
                "option_d": "To replace all monthly income",
                "correct_answer": "C",
                "explanation": (
                    "An emergency fund provides money for unexpected "
                    "expenses when they arise."
                ),
            },
            {
                "topic": "saving",
                "question_text": (
                    "Which is an example of a SMART savings goal?"
                ),
                "option_a": "I will become rich someday",
                "option_b": "I will save KES 3,000 in three months",
                "option_c": "I will spend less whenever possible",
                "option_d": "I will save an unknown amount",
                "correct_answer": "B",
                "explanation": (
                    "The goal identifies a specific amount and a "
                    "clear time frame."
                ),
            },
            {
                "topic": "saving",
                "question_text": (
                    "Which habit can help a student save consistently?"
                ),
                "option_a": "Saving only when money is left by chance",
                "option_b": "Ignoring financial goals",
                "option_c": "Spending before checking essential expenses",
                "option_d": "Setting aside a realistic amount regularly",
                "correct_answer": "D",
                "explanation": (
                    "Regular contributions based on a realistic plan "
                    "can help build a consistent saving habit."
                ),
            },

            # DEBT: 5 QUESTIONS
            {
                "topic": "debt",
                "question_text": "What is the principal of a loan?",
                "option_a": "The original amount borrowed",
                "option_b": "The borrower's monthly food budget",
                "option_c": "The lender's profit only",
                "option_d": "The repayment deadline",
                "correct_answer": "A",
                "explanation": (
                    "The principal is the original amount of money "
                    "borrowed before applicable interest and charges."
                ),
            },
            {
                "topic": "debt",
                "question_text": (
                    "You borrow KES 5,000 and must repay KES 5,600. "
                    "Assuming there are no other payments or charges, "
                    "what is the additional borrowing cost?"
                ),
                "option_a": "KES 100",
                "option_b": "KES 500",
                "option_c": "KES 600",
                "option_d": "KES 5,600",
                "correct_answer": "C",
                "explanation": (
                    "KES 5,600 minus KES 5,000 equals KES 600."
                ),
            },
            {
                "topic": "debt",
                "question_text": (
                    "What should you check before accepting a mobile loan?"
                ),
                "option_a": "Only the advertised loan amount",
                "option_b": "The total repayment and loan terms",
                "option_c": "Only the application's appearance",
                "option_d": "Whether your friends have borrowed",
                "correct_answer": "B",
                "explanation": (
                    "You should understand the total repayment, charges, "
                    "deadline and consequences of late payment."
                ),
            },
            {
                "topic": "debt",
                "question_text": (
                    "What is a responsible step when you cannot make "
                    "a loan repayment on time?"
                ),
                "option_a": "Ignore all communication",
                "option_b": "Automatically take another loan",
                "option_c": "Hide the problem from the lender",
                "option_d": "Contact the lender through official channels",
                "correct_answer": "D",
                "explanation": (
                    "Contacting the lender can help you understand "
                    "the available options and applicable terms."
                ),
            },
            {
                "topic": "debt",
                "question_text": (
                    "Why can repeated borrowing to repay previous loans "
                    "be risky?"
                ),
                "option_a": "It always eliminates interest",
                "option_b": "It guarantees more income",
                "option_c": "It can increase financial pressure and debt",
                "option_d": "It removes repayment obligations",
                "correct_answer": "C",
                "explanation": (
                    "Repeated borrowing can increase repayment obligations "
                    "and make it harder to manage existing debt."
                ),
            },

            # SPENDING: 5 QUESTIONS
            {
                "topic": "spending",
                "question_text": (
                    "Which is an example of impulse spending?"
                ),
                "option_a": "Buying an item unexpectedly without considering "
                "your budget",
                "option_b": "Planning food expenses in advance",
                "option_c": "Comparing prices before a purchase",
                "option_d": "Reviewing your monthly transactions",
                "correct_answer": "A",
                "explanation": (
                    "Impulse spending involves making an unplanned purchase "
                    "without sufficient consideration."
                ),
            },
            {
                "topic": "spending",
                "question_text": (
                    "What does opportunity cost mean in personal finance?"
                ),
                "option_a": "The price printed on a receipt",
                "option_b": "The money in a savings account",
                "option_c": "The cost of using a mobile application",
                "option_d": "The value of the next-best alternative given up",
                "correct_answer": "D",
                "explanation": (
                    "Opportunity cost represents what you give up when "
                    "you choose one option over another."
                ),
            },
            {
                "topic": "spending",
                "question_text": (
                    "What is a good response to pressure to spend "
                    "like your friends?"
                ),
                "option_a": "Borrow money immediately",
                "option_b": "Follow your budget and financial priorities",
                "option_c": "Spend all your savings",
                "option_d": "Ignore your essential expenses",
                "correct_answer": "B",
                "explanation": (
                    "Your spending decisions should reflect your own "
                    "income, responsibilities and financial goals."
                ),
            },
            {
                "topic": "spending",
                "question_text": (
                    "How can a student identify unnecessary recurring costs?"
                ),
                "option_a": "Avoid checking bank statements",
                "option_b": "Delete all financial records",
                "option_c": "Review subscriptions and regular payments",
                "option_d": "Make more unplanned purchases",
                "correct_answer": "C",
                "explanation": (
                    "Reviewing recurring payments helps identify services "
                    "that are no longer needed."
                ),
            },
            {
                "topic": "spending",
                "question_text": (
                    "What should you consider before making a non-essential "
                    "purchase?"
                ),
                "option_a": "Whether it fits your budget and priorities",
                "option_b": "Whether everyone else owns it",
                "option_c": "Whether you can hide the expense",
                "option_d": "Whether it uses all your remaining money",
                "correct_answer": "A",
                "explanation": (
                    "Considering affordability and priorities helps "
                    "prevent spending from interfering with essential needs."
                ),
            },

            # FRAUD: 5 QUESTIONS
            {
                "topic": "fraud",
                "question_text": (
                    "Someone calls claiming to be a mobile money agent "
                    "and asks for your PIN. What should you do?"
                ),
                "option_a": "Share the PIN to avoid account problems",
                "option_b": "Send the PIN through SMS",
                "option_c": "Refuse and verify the request through official "
                "channels",
                "option_d": "Share the PIN if the caller sounds convincing",
                "correct_answer": "C",
                "explanation": (
                    "Never disclose your PIN. Verify suspicious requests "
                    "through official service channels."
                ),
            },
            {
                "topic": "fraud",
                "question_text": (
                    "Which is a warning sign of a possible investment scam?"
                ),
                "option_a": "Clear information about applicable risks",
                "option_b": "Promises of guaranteed unusually high returns",
                "option_c": "An opportunity to read official documentation",
                "option_d": "Time to research before investing",
                "correct_answer": "B",
                "explanation": (
                    "Promises of unusually high or guaranteed returns "
                    "can be a warning sign of fraud."
                ),
            },
            {
                "topic": "fraud",
                "question_text": (
                    "You receive an unexpected message with a link asking "
                    "you to confirm your financial account details. "
                    "What is the safest response?"
                ),
                "option_a": "Click immediately",
                "option_b": "Enter your PIN to verify your account",
                "option_c": "Forward it to all your contacts",
                "option_d": "Avoid the link and verify through official channels",
                "correct_answer": "D",
                "explanation": (
                    "Unexpected links may lead to fraudulent websites. "
                    "Verify requests independently using official channels."
                ),
            },
            {
                "topic": "fraud",
                "question_text": (
                    "What should you do if you suspect an unauthorised "
                    "mobile money transaction?"
                ),
                "option_a": "Contact the provider through official channels "
                "and preserve relevant evidence",
                "option_b": "Delete every message immediately",
                "option_c": "Share your PIN with the suspected sender",
                "option_d": "Send more money to test the account",
                "correct_answer": "A",
                "explanation": (
                    "Promptly contacting the provider and preserving "
                    "transaction details can help you respond to the incident."
                ),
            },
            {
                "topic": "fraud",
                "question_text": (
                    "How should you check whether an investment provider "
                    "is authorised where authorisation is required?"
                ),
                "option_a": "Trust online comments alone",
                "option_b": "Rely only on a friend's recommendation",
                "option_c": "Check independently through relevant official "
                "authorities",
                "option_d": "Assume every social media advertisement is genuine",
                "correct_answer": "C",
                "explanation": (
                    "Independent verification through relevant official "
                    "authorities is safer than relying on advertisements "
                    "or testimonials."
                ),
            },

            # INVESTING: 5 QUESTIONS
            {
                "topic": "investing",
                "question_text": "What does investing involve?",
                "option_a": "Spending all income immediately",
                "option_b": "Committing money to an asset with the "
                "expectation of a return",
                "option_c": "Borrowing money without a repayment plan",
                "option_d": "Avoiding all financial decisions",
                "correct_answer": "B",
                "explanation": (
                    "Investing involves committing money with the "
                    "expectation of a return, while accepting applicable risks."
                ),
            },
            {
                "topic": "investing",
                "question_text": (
                    "What is investment risk?"
                ),
                "option_a": "A guarantee of profit",
                "option_b": "The amount of money you save each month",
                "option_c": "The possibility of an unexpected outcome, "
                "including a loss",
                "option_d": "A guarantee that your money cannot change in value",
                "correct_answer": "C",
                "explanation": (
                    "Investment risk includes the possibility that actual "
                    "results differ from expectations or that money is lost."
                ),
            },
            {
                "topic": "investing",
                "question_text": "What is diversification?",
                "option_a": "Spreading investments across different assets "
                "or investment types",
                "option_b": "Putting all investment money into one asset",
                "option_c": "Investing without research",
                "option_d": "Borrowing to fund every investment",
                "correct_answer": "A",
                "explanation": (
                    "Diversification reduces reliance on a single investment, "
                    "although it does not eliminate all risk."
                ),
            },
            {
                "topic": "investing",
                "question_text": (
                    "What should you do before investing in a financial product?"
                ),
                "option_a": "Invest because someone promised a guaranteed profit",
                "option_b": "Ignore all fees and withdrawal conditions",
                "option_c": "Use money needed for immediate essential expenses "
                "without considering the risk",
                "option_d": "Research the provider, risks, fees and terms",
                "correct_answer": "D",
                "explanation": (
                    "Understanding the provider, risks, fees and conditions "
                    "helps you make a more informed decision."
                ),
            },
            {
                "topic": "investing",
                "question_text": (
                    "Why is it important to understand your financial goals "
                    "before choosing an investment?"
                ),
                "option_a": "All investments have identical risks",
                "option_b": "Your goals and time horizon affect suitability",
                "option_c": "Investing always produces a profit",
                "option_d": "Financial goals eliminate investment risk",
                "correct_answer": "B",
                "explanation": (
                    "Your goals, time horizon and ability to tolerate losses "
                    "help determine which products may be suitable."
                ),
            },
        ]

        # --------------------------------------------------
        # 3. SAVE LESSONS WITHOUT CREATING DUPLICATES
        # --------------------------------------------------

        lessons_created = 0
        lessons_updated = 0

        for lesson_data in lessons:
            _, created = LearningContent.objects.update_or_create(
                topic=lesson_data["topic"],
                title=lesson_data["title"],
                defaults={
                    "description": lesson_data["description"],
                    "content": lesson_data["content"].strip(),
                    "is_published": lesson_data["is_published"],
                },
            )

            if created:
                lessons_created += 1
            else:
                lessons_updated += 1

        # --------------------------------------------------
        # 4. SAVE QUIZ QUESTIONS WITHOUT CREATING DUPLICATES
        # --------------------------------------------------

        questions_created = 0
        questions_updated = 0

        for question_data in questions:
            _, created = QuizQuestion.objects.update_or_create(
                topic=question_data["topic"],
                question_text=question_data["question_text"],
                defaults={
                    "option_a": question_data["option_a"],
                    "option_b": question_data["option_b"],
                    "option_c": question_data["option_c"],
                    "option_d": question_data["option_d"],
                    "correct_answer": question_data["correct_answer"],
                    "explanation": question_data["explanation"],
                    "is_published": True,
                },
            )

            if created:
                questions_created += 1
            else:
                questions_updated += 1

        # --------------------------------------------------
        # 5. DISPLAY RESULTS
        # --------------------------------------------------

        self.stdout.write(
            self.style.SUCCESS(
                "FinanceWise content loaded successfully!"
            )
        )

        self.stdout.write(
            f"Lessons created: {lessons_created}"
        )
        self.stdout.write(
            f"Lessons updated: {lessons_updated}"
        )
        self.stdout.write(
            f"Quiz questions created: {questions_created}"
        )
        self.stdout.write(
            f"Quiz questions updated: {questions_updated}"
        )