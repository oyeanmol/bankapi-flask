
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

# Fictional sample data for learning purposes
customers = [
    {
        "customer_id": 101,
        "name": "Rahul Sharma",
        "age": 28,
        "city": "Jaipur",
        "occupation": "Software Developer",
        "account_number": "BANK1001",
        "account_type": "Savings",
        "balance": 85000,
        "monthly_income": 55000,
        "monthly_expenses": 25000,
        "credit_score": 750,
        "loan_amount": 200000,
        "existing_debt": 50000,
        "transactions_count": 45,
        "branch": "Vaishali Nagar",
        "account_opening_date": "2021-05-12",
        "is_active": True,
        "kyc_verified": True
    },
    {
        "customer_id": 102,
        "name": "Priya Verma",
        "age": 24,
        "city": "Delhi",
        "occupation": "Teacher",
        "account_number": "BANK1002",
        "account_type": "Savings",
        "balance": 12000,
        "monthly_income": 28000,
        "monthly_expenses": 22000,
        "credit_score": 350,
        "loan_amount": 150000,
        "existing_debt": 120000,
        "transactions_count": 28,
        "branch": "Connaught Place",
        "account_opening_date": "2023-08-20",
        "is_active": True,
        "kyc_verified": True
    },
    {
        "customer_id": 103,
        "name": "Amit Patel",
        "age": 35,
        "city": "Ahmedabad",
        "occupation": "Business Owner",
        "account_number": "BANK1003",
        "account_type": "Current",
        "balance": 250000,
        "monthly_income": 180000,
        "monthly_expenses": 90000,
        "credit_score": 680,
        "loan_amount": 500000,
        "existing_debt": 180000,
        "transactions_count": 120,
        "branch": "Navrangpura",
        "account_opening_date": "2018-02-15",
        "is_active": True,
        "kyc_verified": True
    },
    {
        "customer_id": 104,
        "name": "Neha Singh",
        "age": 42,
        "city": "Jaipur",
        "occupation": "Accountant",
        "account_number": "BANK1004",
        "account_type": "Savings",
        "balance": 8000,
        "monthly_income": 35000,
        "monthly_expenses": 30000,
        "credit_score": 280,
        "loan_amount": 100000,
        "existing_debt": 95000,
        "transactions_count": 15,
        "branch": "Mansarovar",
        "account_opening_date": "2024-01-10",
        "is_active": False,
        "kyc_verified": False
    },
    {
        "customer_id": 105,
        "name": "Rohit Mehta",
        "age": 31,
        "city": "Mumbai",
        "occupation": "Data Analyst",
        "account_number": "BANK1005",
        "account_type": "Salary",
        "balance": 95000,
        "monthly_income": 85000,
        "monthly_expenses": 40000,
        "credit_score": 420,
        "loan_amount": 300000,
        "existing_debt": 220000,
        "transactions_count": 65,
        "branch": "Andheri",
        "account_opening_date": "2020-11-05",
        "is_active": True,
        "kyc_verified": True
    },
    {
        "customer_id": 106,
        "name": "Sneha Joshi",
        "age": 26,
        "city": "Jaipur",
        "occupation": "Doctor",
        "account_number": "BANK1006",
        "account_type": "Salary",
        "balance": 175000,
        "monthly_income": 120000,
        "monthly_expenses": 45000,
        "credit_score": 810,
        "loan_amount": 0,
        "existing_debt": 0,
        "transactions_count": 90,
        "branch": "C-Scheme",
        "account_opening_date": "2019-07-22",
        "is_active": True,
        "kyc_verified": True
    }
]

SORT_FIELDS = {
    "name", "age", "balance", "credit_score",
    "monthly_income", "loan_amount", "transactions_count"
}


def get_number(name, cast_type=float):
    """Read and validate an optional numeric query parameter."""
    value = request.args.get(name)

    if value is None:
        return None, None

    try:
        number = cast_type(value)
        if isinstance(number, bool):
            raise ValueError
        return number, None
    except (ValueError, TypeError):
        return None, f"'{name}' must be a valid {cast_type.__name__}."


def get_boolean(name):
    """Read and validate true/false query parameters."""
    value = request.args.get(name)

    if value is None:
        return None, None

    if value.lower() == "true":
        return True, None

    if value.lower() == "false":
        return False, None

    return None, f"'{name}' must be true or false."


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/customers", methods=["GET"])
def get_customers():
    result = customers.copy()

    # Exact-match string filters
    city = request.args.get("city")
    if city:
        result = [
            c for c in result
            if c["city"].lower() == city.lower()
        ]

    account_type = request.args.get("account_type")
    if account_type:
        result = [
            c for c in result
            if c["account_type"].lower() == account_type.lower()
        ]

    # Numeric filters
    numeric_filters = [
        ("credit_score_lt", int),
        ("credit_score_gt", int),
        ("min_balance", float),
        ("max_balance", float),
        ("min_age", int),
        ("max_age", int),
    ]

    values = {}

    for name, cast_type in numeric_filters:
        value, error = get_number(name, cast_type)

        if error:
            return jsonify({"error": error}), 400

        values[name] = value

    if values["credit_score_lt"] is not None:
        result = [
            c for c in result
            if c["credit_score"] < values["credit_score_lt"]
        ]

    if values["credit_score_gt"] is not None:
        result = [
            c for c in result
            if c["credit_score"] > values["credit_score_gt"]
        ]

    if values["min_balance"] is not None:
        result = [
            c for c in result
            if c["balance"] >= values["min_balance"]
        ]

    if values["max_balance"] is not None:
        result = [
            c for c in result
            if c["balance"] <= values["max_balance"]
        ]

    if values["min_age"] is not None:
        result = [
            c for c in result
            if c["age"] >= values["min_age"]
        ]

    if values["max_age"] is not None:
        result = [
            c for c in result
            if c["age"] <= values["max_age"]
        ]

    # Boolean filters
    active, error = get_boolean("active")
    if error:
        return jsonify({"error": error}), 400

    if active is not None:
        result = [c for c in result if c["is_active"] == active]

    kyc_verified, error = get_boolean("kyc_verified")
    if error:
        return jsonify({"error": error}), 400

    if kyc_verified is not None:
        result = [
            c for c in result
            if c["kyc_verified"] == kyc_verified
        ]

    # Sorting
    sort_by = request.args.get("sort_by")
    order = request.args.get("order", "asc").lower()

    if order not in ("asc", "desc"):
        return jsonify({
            "error": "'order' must be 'asc' or 'desc'."
        }), 400

    if sort_by:
        if sort_by not in SORT_FIELDS:
            return jsonify({
                "error": "Invalid sort_by field.",
                "allowed_fields": sorted(SORT_FIELDS)
            }), 400

        result.sort(
            key=lambda customer: customer[sort_by],
            reverse=(order == "desc")
        )

    return jsonify({
        "count": len(result),
        "filters_applied": request.args.to_dict(),
        "customers": result
    })


@app.route("/stats", methods=["GET"])
def get_stats():
    total = len(customers)

    return jsonify({
        "total_customers": total,
        "active_customers": sum(c["is_active"] for c in customers),
        "inactive_customers": sum(not c["is_active"] for c in customers),
        "kyc_verified_customers": sum(
            c["kyc_verified"] for c in customers
        ),
        "average_credit_score": round(
            sum(c["credit_score"] for c in customers) / total, 2
        ) if total else 0,
        "total_bank_balance": sum(c["balance"] for c in customers),
        "low_credit_score_customers": sum(
            c["credit_score"] < 400 for c in customers
        )
    })


if __name__ == "__main__":
    app.run(debug=True)
