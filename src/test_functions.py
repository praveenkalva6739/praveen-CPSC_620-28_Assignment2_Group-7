"""
Task 29 – Test All Functions Individually
This script imports functions from transactions_tool.py
and tests them one by one.
"""

from transactions_tool import (
    load_and_clean_transactions,
    generate_overall_financial_summary,
    generate_monthly_summary_report,
    generate_customer_summary,
    generate_top_customers_report,
    create_monthly_net_amount_chart,
    create_monthly_credit_debit_chart,
    create_transaction_amount_histogram,
    create_top_customers_chart,
)

print("==== TASK 29: TESTING ALL FUNCTIONS INDIVIDUALLY ====\n")

# US1 – Load & clean data
df = load_and_clean_transactions()
print("\nUS1 passed ✔\n")

# US2 – Overall summary
overall = generate_overall_financial_summary(df)
print("US2 passed ✔\n")

# US3 – Monthly summary
monthly_summary = generate_monthly_summary_report(df)
print("US3 passed ✔\n")

# US4 – Customer summary
customer_summary = generate_customer_summary(df)
print("US4 passed ✔\n")

# US5 – Top customers
top_customers = generate_top_customers_report(customer_summary, n=10)
print("US5 passed ✔\n")

# US6 – Charts
create_monthly_net_amount_chart(monthly_summary)
create_monthly_credit_debit_chart(monthly_summary)
create_transaction_amount_histogram(df)
create_top_customers_chart(top_customers)

print("US6 charts generated ✔\n")

print("\n==== TASK 29 COMPLETED SUCCESSFULLY ====")
