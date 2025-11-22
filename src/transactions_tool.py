"""
Financial Transactions Summary Tool

Organized by Taiga user stories:

User Story 1 – Load and Clean Transaction Data
User Story 2 – Generate Overall Financial Summary
User Story 3 – Monthly Summary Report
User Story 4 – Customer Summary
User Story 5 – Top Customers by Spending
User Story 6 – Visualizations (Monthly Net Amount & other plots)
User Story 7 – Modular Function Design (all functions + main workflow)
User Story 8 – Documentation (this header + docstrings + comments)

Run the whole tool with:
    python src/transactions_tool.py
"""

import os
import pandas as pd
import matplotlib.pyplot as plt


# ---------------------------------------------------------------------
# Shared configuration (used by several user stories)
# ---------------------------------------------------------------------

# Folder where this script lives (src/)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# CSV file path: ../data/financial_transactions.csv
CSV_PATH = os.path.join(BASE_DIR, "..", "data", "financial_transactions.csv")

# Where to save plots (same folder as this script)
PLOT_DIR = BASE_DIR


# =====================================================================
# User Story 1 – Load and Clean Transaction Data
# =====================================================================

def load_and_clean_transactions(csv_path: str = CSV_PATH) -> pd.DataFrame:
    """
    Load the financial transactions CSV file and perform basic cleaning.

    Steps:
    1. Load CSV into a pandas DataFrame.
    2. Convert 'date' to datetime.
    3. Standardize the 'type' column (lowercase, stripped).
    4. Drop rows missing critical values: date, amount, type.

    Returns:
        Cleaned pandas DataFrame.
    """
    print(f"[US1] Loading transactions from: {csv_path}")
    df = pd.read_csv(csv_path)

    # 2. Convert date column
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # 3. Clean 'type' column
    df["type"] = df["type"].astype(str).str.lower().str.strip()

    # 4. Drop rows missing key fields
    before = len(df)
    df.dropna(subset=["date", "amount", "type"], inplace=True)
    after = len(df)

    print(f"[US1] Rows before cleaning: {before}")
    print(f"[US1] Rows after cleaning : {after}")
    return df


# =====================================================================
# User Story 2 – Generate Overall Financial Summary
# =====================================================================
# Task 23 update
def generate_overall_financial_summary(df: pd.DataFrame) -> dict:
    """
    Calculate high-level metrics for the entire dataset.

    Returns:
        Dictionary with total_transactions, total_credit, total_debit,
        net_amount, avg_amount, max_amount, min_amount.
    """
    total_transactions = len(df)
    total_credit = df[df["amount"] > 0]["amount"].sum()
    total_debit = df[df["amount"] < 0]["amount"].sum()
    net_amount = df["amount"].sum()
    avg_amount = df["amount"].mean()
    max_amount = df["amount"].max()
    min_amount = df["amount"].min()

    summary = {
        "total_transactions": total_transactions,
        "total_credit": total_credit,
        "total_debit": total_debit,
        "net_amount": net_amount,
        "avg_amount": avg_amount,
        "max_amount": max_amount,
        "min_amount": min_amount,
    }

    print("\n[US2] Overall Financial Summary")
    print("--------------------------------")
    print(f"Total Transactions       : {summary['total_transactions']}")
    print(f"Total Credit             : {summary['total_credit']:.2f}")
    print(f"Total Debit              : {summary['total_debit']:.2f}")
    print(f"Net Amount               : {summary['net_amount']:.2f}")
    print(f"Average Transaction Amt  : {summary['avg_amount']:.2f}")
    print(f"Max Transaction Amount   : {summary['max_amount']:.2f}")
    print(f"Min Transaction Amount   : {summary['min_amount']:.2f}")

    return summary


# =====================================================================
# User Story 3 – Monthly Summary Report
# =====================================================================

def generate_monthly_summary_report(df: pd.DataFrame) -> pd.DataFrame:
    """
   Group transactions by year-month and compute:

        * total_credit
        * total_debit
        * transaction_count
        * net_amount

    Returns:
        DataFrame indexed by year_month with the above metrics.
    """
    df["year_month"] = df["date"].dt.to_period("M")
    summary = df.groupby("year_month").agg(
        total_credit=("amount", lambda x: x[x > 0].sum()),
        total_debit=("amount", lambda x: x[x < 0].sum()),
        transaction_count=("amount", "count"),
        net_amount=("amount", "sum"),
    )

    # Convert PeriodIndex to string for easier printing/plotting
    summary.index = summary.index.astype(str)

    print("\n[US3] Monthly Summary Report (first 5 rows)")
    print("-------------------------------------------")
    print(summary.head())

    return summary


# =====================================================================
# User Story 4 – Customer Summary
# =====================================================================

def generate_customer_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create a customer-level summary with:

        * total_spent
        * transaction_count
        * avg_amount

    Returns:
        DataFrame indexed by customer_id.
    """
    grouped = df.groupby("customer_id")["amount"]
    summary = pd.DataFrame({
        "total_spent": grouped.sum(),
        "transaction_count": grouped.count(),
        "avg_amount": grouped.mean()
    })

    print("\n[US4] Customer Summary (first 5 rows)")
    print("-------------------------------------")
    print(summary.sort_values("total_spent", ascending=False).head())

    return summary


# =====================================================================
# User Story 5 – Top Customers by Spending
# =====================================================================

def generate_top_customers_report(customer_summary_df: pd.DataFrame,
                                 n: int = 10) -> pd.DataFrame:
    """
    Select the top N customers by total_spent.

    Returns:
        DataFrame with top N customers sorted by total_spent (descending).
    """
    top_customers = (
        customer_summary_df
        .sort_values("total_spent", ascending=False)
        .head(n)
        .reset_index()
    )

    print(f"\n[US5] Top {n} Customers by Total Spent")
    print("--------------------------------------")
    print(top_customers)

    return top_customers


# =====================================================================
# User Story 6 – Visualizations
#   (Monthly Net Amount + additional charts)
# =====================================================================

def _ensure_plot_dir():
    """Internal helper to ensure the plot directory exists."""
    os.makedirs(PLOT_DIR, exist_ok=True)


def create_monthly_net_amount_chart(monthly_summary_df: pd.DataFrame) -> str:
    """
    [US6] Bar chart of monthly net amounts.

    Saves: monthly_net_amount.png in the src/ folder.
    """
    _ensure_plot_dir()
    output_path = os.path.join(PLOT_DIR, "monthly_net_amount.png")

    plt.figure(figsize=(10, 5))
    monthly_summary_df["net_amount"].plot(kind="bar")
    plt.title("Monthly Net Amount")
    plt.xlabel("Year-Month")
    plt.ylabel("Net Amount")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

    print(f"[US6] Saved monthly net amount chart to: {output_path}")
    return output_path


def create_monthly_credit_debit_chart(monthly_summary_df: pd.DataFrame) -> str:
    """
    [US6] Line chart of monthly total credit and total debit.

    Saves: monthly_credit_debit.png in the src/ folder.
    """
    _ensure_plot_dir()
    output_path = os.path.join(PLOT_DIR, "monthly_credit_debit.png")

    plt.figure(figsize=(10, 5))
    plt.plot(monthly_summary_df.index, monthly_summary_df["total_credit"],
             marker="o", label="Total Credit")
    plt.plot(monthly_summary_df.index, monthly_summary_df["total_debit"],
             marker="o", label="Total Debit")
    plt.title("Monthly Credit and Debit")
    plt.xlabel("Year-Month")
    plt.ylabel("Amount")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

    print(f"[US6] Saved monthly credit/debit chart to: {output_path}")
    return output_path


def create_transaction_amount_histogram(df: pd.DataFrame, bins: int = 50) -> str:
    """
    [US6] Histogram showing the distribution of transaction amounts.

    Saves: transaction_amount_hist.png in the src/ folder.
    """
    _ensure_plot_dir()
    output_path = os.path.join(PLOT_DIR, "transaction_amount_hist.png")

    plt.figure(figsize=(8, 5))
    plt.hist(df["amount"], bins=bins, edgecolor="black")
    plt.title("Distribution of Transaction Amounts")
    plt.xlabel("Amount")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

    print(f"[US6] Saved transaction amount histogram to: {output_path}")
    return output_path


def create_top_customers_chart(top_customers_df: pd.DataFrame) -> str:
    """
    [US6] Bar chart of top customers by total spent.

    Uses the DataFrame from User Story 5.

    Saves: top_customers.png in the src/ folder.
    """
    _ensure_plot_dir()
    output_path = os.path.join(PLOT_DIR, "top_customers.png")

    plt.figure(figsize=(10, 5))
    plt.bar(top_customers_df["customer_id"].astype(str),
            top_customers_df["total_spent"])
    plt.title("Top Customers by Total Spent")
    plt.xlabel("Customer ID")
    plt.ylabel("Total Spent")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

    print(f"[US6] Saved top customers chart to: {output_path}")
    return output_path


# =====================================================================
# User Story 7 – Modular Function Design (Main Workflow)
# =====================================================================

def main():
    """
    Orchestrate the full analysis by calling the user-story functions
    in a clear, modular order.
    """
    print("=== Financial Transactions Summary Tool ===")
    print(f"CSV Path: {CSV_PATH}")

    # US1 – Load & clean data
    df = load_and_clean_transactions()

    # US2 – Overall summary
    generate_overall_financial_summary(df)

    # US3 – Monthly summary report
    monthly_summary_df = generate_monthly_summary_report(df)

    # US4 – Customer summary
    customer_summary_df = generate_customer_summary(df)

    # US5 – Top customers by spending
    top_customers_df = generate_top_customers_report(customer_summary_df, n=10)

    # US6 – Visualizations
    create_monthly_net_amount_chart(monthly_summary_df)
    create_monthly_credit_debit_chart(monthly_summary_df)
    create_transaction_amount_histogram(df)
    create_top_customers_chart(top_customers_df)

    print("\n[US7] Main workflow executed successfully.")


# =====================================================================
# Script entry point
# =====================================================================

if __name__ == "__main__":
    main()
