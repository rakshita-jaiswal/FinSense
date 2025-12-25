"""Mock transaction data generator for account sync simulation."""
import random
from datetime import datetime, timedelta
from typing import List, Dict


# Vendor data by source type
SQUARE_VENDORS = [
    "Daily Coffee Sales", "Lunch Service", "Dinner Service", "Catering Event",
    "Weekend Brunch", "Happy Hour", "Private Party", "Takeout Orders"
]

STRIPE_VENDORS = [
    "Online Order #", "Website Payment", "Mobile App Purchase", "Subscription Payment",
    "Gift Card Sale", "Delivery Fee", "Service Charge"
]

BANK_VENDORS = [
    "Sysco Boston", "US Foods", "Restaurant Depot", "Shamrock Foods",
    "Gordon Food Service", "Performance Food Group", "Ben E. Keith",
    "Cheney Brothers", "Reinhart Foodservice", "Vistar"
]

EXPENSE_VENDORS = [
    ("Con Edison", "Utilities", 250, 450),
    ("National Grid", "Utilities", 180, 350),
    ("Verizon Business", "Utilities", 120, 200),
    ("Waste Management", "Utilities", 80, 150),
    ("ADT Security", "Utilities", 60, 120),
    ("Staples", "Office Supplies", 50, 200),
    ("Office Depot", "Office Supplies", 40, 180),
    ("Amazon Business", "Office Supplies", 30, 250),
    ("Cintas", "Professional Fees", 100, 300),
    ("ADP Payroll", "Payroll", 2000, 5000),
    ("Paychex", "Payroll", 1800, 4500),
    ("Square Payroll", "Payroll", 1500, 4000),
    ("State Farm Insurance", "Professional Fees", 200, 500),
    ("Liberty Mutual", "Professional Fees", 180, 450),
    ("Sysco Boston", "Inventory - Food & Supplies", 200, 800),
    ("US Foods", "Inventory - Food & Supplies", 180, 750),
    ("Restaurant Depot", "Inventory - Food & Supplies", 150, 600),
    ("Shamrock Foods", "Inventory - Food & Supplies", 200, 700),
    ("Uber Eats", "Marketing", 50, 200),
    ("DoorDash", "Marketing", 40, 180),
    ("Grubhub", "Marketing", 45, 190),
    ("Facebook Ads", "Marketing", 100, 500),
    ("Google Ads", "Marketing", 150, 600),
    ("Instagram Ads", "Marketing", 80, 400),
]


def generate_square_transactions(count: int = 25) -> List[Dict]:
    """Generate mock Square POS transactions (mostly revenue)."""
    transactions = []
    now = datetime.utcnow()
    
    for i in range(count):
        # 80% revenue, 20% expenses
        is_revenue = random.random() < 0.8
        
        if is_revenue:
            vendor = random.choice(SQUARE_VENDORS)
            if "#" in vendor:
                vendor = f"{vendor}{random.randint(1000, 9999)}"
            
            amount = -round(random.uniform(25, 500), 2)  # Negative for revenue
            category = "Revenue"
            confidence = random.uniform(0.92, 0.99)
            status = "auto-approved"
            explanation = f"Categorized as Revenue because this is a Square POS transaction for {vendor.lower()}, indicating a customer payment."
            payment_method = "Square POS"
        else:
            vendor, category, min_amt, max_amt = random.choice(EXPENSE_VENDORS)
            amount = round(random.uniform(min_amt, max_amt), 2)
            confidence = random.uniform(0.85, 0.95)
            status = "auto-approved" if confidence > 0.90 else "needs-review"
            explanation = f"Categorized as {category} because {vendor} is a known vendor for this expense type."
            payment_method = "Business Debit"
        
        # Random date within last 30 days
        days_ago = random.randint(0, 30)
        transaction_date = now - timedelta(days=days_ago, hours=random.randint(0, 23))
        
        transactions.append({
            "date": transaction_date,
            "vendor": vendor,
            "amount": amount,
            "category": category,
            "confidence": confidence,
            "status": status,
            "explanation": explanation,
            "payment_method": payment_method,
            "original_description": vendor.upper()
        })
    
    return transactions


def generate_stripe_transactions(count: int = 20) -> List[Dict]:
    """Generate mock Stripe payment transactions (mostly revenue)."""
    transactions = []
    now = datetime.utcnow()
    
    for i in range(count):
        # 85% revenue, 15% expenses
        is_revenue = random.random() < 0.85
        
        if is_revenue:
            vendor = random.choice(STRIPE_VENDORS)
            if "#" in vendor:
                vendor = f"{vendor}{random.randint(10000, 99999)}"
            
            amount = -round(random.uniform(15, 350), 2)  # Negative for revenue
            category = "Revenue"
            confidence = random.uniform(0.93, 0.99)
            status = "auto-approved"
            explanation = f"Categorized as Revenue because this is a Stripe payment transaction, indicating online customer payment."
            payment_method = "Stripe"
        else:
            vendor, category, min_amt, max_amt = random.choice(EXPENSE_VENDORS)
            amount = round(random.uniform(min_amt, max_amt), 2)
            confidence = random.uniform(0.82, 0.93)
            status = "auto-approved" if confidence > 0.88 else "needs-review"
            explanation = f"Categorized as {category} based on vendor pattern matching for {vendor}."
            payment_method = "Business Credit"
        
        # Random date within last 30 days
        days_ago = random.randint(0, 30)
        transaction_date = now - timedelta(days=days_ago, hours=random.randint(0, 23))
        
        transactions.append({
            "date": transaction_date,
            "vendor": vendor,
            "amount": amount,
            "category": category,
            "confidence": confidence,
            "status": status,
            "explanation": explanation,
            "payment_method": payment_method,
            "original_description": vendor.upper()
        })
    
    return transactions


def generate_bank_transactions(count: int = 35) -> List[Dict]:
    """Generate mock bank account transactions (mixed revenue and expenses)."""
    transactions = []
    now = datetime.utcnow()
    
    for i in range(count):
        # 40% revenue, 60% expenses (more diverse)
        is_revenue = random.random() < 0.40
        
        if is_revenue:
            vendor = f"Deposit - {random.choice(['Square', 'Stripe', 'Cash', 'Check'])}"
            amount = -round(random.uniform(500, 3000), 2)  # Negative for revenue
            category = "Revenue"
            confidence = random.uniform(0.90, 0.98)
            status = "auto-approved"
            explanation = f"Categorized as Revenue because this is a bank deposit from payment processing."
            payment_method = "Bank Transfer"
        else:
            vendor, category, min_amt, max_amt = random.choice(EXPENSE_VENDORS)
            amount = round(random.uniform(min_amt, max_amt), 2)
            confidence = random.uniform(0.75, 0.92)
            status = "auto-approved" if confidence > 0.85 else "needs-review"
            explanation = f"Categorized as {category} based on historical spending patterns with {vendor}."
            payment_method = random.choice(["Business Debit", "Business Credit", "ACH Transfer", "Check"])
        
        # Random date within last 30 days
        days_ago = random.randint(0, 30)
        transaction_date = now - timedelta(days=days_ago, hours=random.randint(0, 23))
        
        transactions.append({
            "date": transaction_date,
            "vendor": vendor,
            "amount": amount,
            "category": category,
            "confidence": confidence,
            "status": status,
            "explanation": explanation,
            "payment_method": payment_method,
            "original_description": vendor.upper()
        })
    
    return transactions


def generate_transactions_for_source(source: str) -> List[Dict]:
    """Generate transactions based on account source."""
    source = source.lower()
    
    if source == "square":
        return generate_square_transactions()
    elif source == "stripe":
        return generate_stripe_transactions()
    elif source == "bank":
        return generate_bank_transactions()
    else:
        return []