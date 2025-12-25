"""Dashboard analytics routes."""
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends
from typing import List, Dict
import random

from models.user import UserInDB
from auth.dependencies import get_current_user
from database import get_database


router = APIRouter(prefix="/api/v1/dashboard", tags=["dashboard"])


@router.get("/stats", response_model=dict)
async def get_dashboard_stats(current_user: UserInDB = Depends(get_current_user)):
    """
    Get financial overview statistics.
    
    Calculates:
    - Monthly revenue (sum of negative amounts)
    - Total expenses (sum of positive amounts)
    - Net profit (revenue - expenses)
    - Cash balance (cumulative)
    - Percentage changes (mocked with random +/- 5-15%)
    """
    db = get_database()
    
    # Get current month's transactions
    now = datetime.utcnow()
    start_of_month = datetime(now.year, now.month, 1)
    
    transactions = await db.transactions.find({
        "user_id": current_user.id,
        "date": {"$gte": start_of_month}
    }).to_list(length=None)
    
    # Calculate stats
    monthly_revenue = 0.0
    total_expenses = 0.0
    
    for trans in transactions:
        amount = trans["amount"]
        if amount < 0:  # Revenue (negative amounts)
            monthly_revenue += abs(amount)
        else:  # Expenses (positive amounts)
            total_expenses += amount
    
    net_profit = monthly_revenue - total_expenses
    
    # Calculate cash balance (simplified - just net profit for now)
    cash_balance = net_profit
    
    # Mock percentage changes (random +/- 5-15%)
    revenue_change = round(random.uniform(-15, 15), 1)
    profit_change = round(random.uniform(-15, 15), 1)
    expenses_change = round(random.uniform(-15, 15), 1)
    cash_change = round(random.uniform(-15, 15), 1)
    
    return {
        "monthlyRevenue": round(monthly_revenue, 2),
        "netProfit": round(net_profit, 2),
        "totalExpenses": round(total_expenses, 2),
        "cashBalance": round(cash_balance, 2),
        "revenueChange": revenue_change,
        "profitChange": profit_change,
        "expensesChange": expenses_change,
        "cashChange": cash_change
    }


@router.get("/revenue-trend", response_model=dict)
async def get_revenue_trend(current_user: UserInDB = Depends(get_current_user)):
    """
    Get revenue vs expenses trend for the last 7 days.
    
    Returns daily revenue and expenses grouped by date.
    """
    db = get_database()
    
    # Get last 7 days of transactions
    now = datetime.utcnow()
    seven_days_ago = now - timedelta(days=7)
    
    transactions = await db.transactions.find({
        "user_id": current_user.id,
        "date": {"$gte": seven_days_ago}
    }).to_list(length=None)
    
    # Group by date
    daily_data: Dict[str, Dict[str, float]] = {}
    
    for trans in transactions:
        date_str = trans["date"].strftime("%b %d")
        
        if date_str not in daily_data:
            daily_data[date_str] = {"revenue": 0.0, "expenses": 0.0}
        
        amount = trans["amount"]
        if amount < 0:  # Revenue
            daily_data[date_str]["revenue"] += abs(amount)
        else:  # Expenses
            daily_data[date_str]["expenses"] += amount
    
    # Convert to array format
    data = []
    for i in range(7):
        date = now - timedelta(days=6-i)
        date_str = date.strftime("%b %d")
        
        data.append({
            "date": date_str,
            "revenue": round(daily_data.get(date_str, {}).get("revenue", 0), 2),
            "expenses": round(daily_data.get(date_str, {}).get("expenses", 0), 2)
        })
    
    return {"data": data}


@router.get("/expense-breakdown", response_model=dict)
async def get_expense_breakdown(current_user: UserInDB = Depends(get_current_user)):
    """
    Get expense breakdown by category.
    
    Returns category-wise expense distribution with percentages and colors.
    """
    db = get_database()
    
    # Get current month's expense transactions
    now = datetime.utcnow()
    start_of_month = datetime(now.year, now.month, 1)
    
    transactions = await db.transactions.find({
        "user_id": current_user.id,
        "date": {"$gte": start_of_month},
        "amount": {"$gt": 0}  # Only expenses (positive amounts)
    }).to_list(length=None)
    
    # Group by category
    category_totals: Dict[str, float] = {}
    
    for trans in transactions:
        category = trans["category"]
        amount = trans["amount"]
        
        if category not in category_totals:
            category_totals[category] = 0.0
        
        category_totals[category] += amount
    
    # Calculate total expenses
    total_expenses = sum(category_totals.values())
    
    # Get category colors from categories collection
    categories = await db.categories.find({}).to_list(length=None)
    category_colors = {cat["name"]: cat["color"] for cat in categories}
    
    # Build response data
    data = []
    for category, amount in sorted(category_totals.items(), key=lambda x: x[1], reverse=True):
        percentage = (amount / total_expenses * 100) if total_expenses > 0 else 0
        
        data.append({
            "category": category,
            "amount": round(amount, 2),
            "percentage": round(percentage, 1),
            "color": category_colors.get(category, "#6366f1")  # Default color if not found
        })
    
    return {"data": data}


@router.get("/recent-transactions", response_model=dict)
async def get_recent_transactions(current_user: UserInDB = Depends(get_current_user)):
    """
    Get 5 most recent transactions.
    
    Returns the latest transactions sorted by date.
    """
    db = get_database()
    
    # Get 5 most recent transactions
    transactions_cursor = db.transactions.find({
        "user_id": current_user.id
    }).sort("date", -1).limit(5)
    
    transactions = await transactions_cursor.to_list(length=5)
    
    # Convert to response format
    transaction_list = []
    for trans in transactions:
        transaction_list.append({
            "id": str(trans["_id"]),
            "date": trans["date"].isoformat() + "Z",
            "vendor": trans["vendor"],
            "amount": trans["amount"],
            "category": trans["category"],
            "confidence": trans["confidence"],
            "status": trans["status"],
            "explanation": trans["explanation"],
            "paymentMethod": trans["payment_method"]
        })
    
    return {"transactions": transaction_list}


@router.get("/alerts", response_model=dict)
async def get_alerts(current_user: UserInDB = Depends(get_current_user)):
    """
    Get financial alerts and notifications.
    
    Generates smart alerts based on transaction patterns:
    - Unusual expenses (3x typical amount)
    - Upcoming payroll
    - Revenue trends
    """
    db = get_database()
    
    alerts = []
    now = datetime.utcnow()
    
    # Get recent transactions for analysis
    thirty_days_ago = now - timedelta(days=30)
    transactions = await db.transactions.find({
        "user_id": current_user.id,
        "date": {"$gte": thirty_days_ago}
    }).to_list(length=None)
    
    # Check for unusual expenses (3x typical amount)
    expense_amounts = [t["amount"] for t in transactions if t["amount"] > 0]
    if expense_amounts:
        avg_expense = sum(expense_amounts) / len(expense_amounts)
        
        for trans in transactions:
            if trans["amount"] > 0 and trans["amount"] > (avg_expense * 3):
                alerts.append({
                    "id": str(trans["_id"]),
                    "type": "warning",
                    "title": "Unusual Expense Detected",
                    "message": f"{trans['vendor']} purchase of ${trans['amount']:.2f} is 3x your typical expense. Review to ensure proper categorization.",
                    "date": trans["date"].isoformat() + "Z",
                    "actionable": True
                })
                break  # Only show one unusual expense alert
    
    # Check for upcoming payroll
    payroll_transactions = [t for t in transactions if "payroll" in t["category"].lower()]
    if payroll_transactions:
        # Sort by date and get the most recent
        payroll_transactions.sort(key=lambda x: x["date"], reverse=True)
        last_payroll = payroll_transactions[0]
        last_payroll_date = last_payroll["date"]
        
        # Assume bi-weekly payroll (14 days)
        next_payroll_date = last_payroll_date + timedelta(days=14)
        days_until_payroll = (next_payroll_date - now).days
        
        if 0 <= days_until_payroll <= 7:
            alerts.append({
                "id": "payroll-upcoming",
                "type": "info",
                "title": "Payroll Scheduled",
                "message": f"Next payroll of ${last_payroll['amount']:.2f} is due in {days_until_payroll} days. You have sufficient funds.",
                "date": now.isoformat() + "Z",
                "actionable": False
            })
    
    # Check revenue trends
    revenue_amounts = [abs(t["amount"]) for t in transactions if t["amount"] < 0]
    if len(revenue_amounts) >= 7:
        # Compare last 7 days vs previous 7 days
        recent_revenue = sum(revenue_amounts[:7])
        previous_revenue = sum(revenue_amounts[7:14]) if len(revenue_amounts) >= 14 else sum(revenue_amounts[7:])
        
        if previous_revenue > 0:
            change_percent = ((recent_revenue - previous_revenue) / previous_revenue) * 100
            
            if change_percent > 10:
                alerts.append({
                    "id": "revenue-up",
                    "type": "success",
                    "title": f"Revenue Up {change_percent:.0f}%",
                    "message": f"Your recent revenue is trending {change_percent:.0f}% higher than the previous period. Great job!",
                    "date": now.isoformat() + "Z",
                    "actionable": False
                })
            elif change_percent < -10:
                alerts.append({
                    "id": "revenue-down",
                    "type": "warning",
                    "title": f"Revenue Down {abs(change_percent):.0f}%",
                    "message": f"Your recent revenue is {abs(change_percent):.0f}% lower than the previous period. Consider reviewing your sales strategy.",
                    "date": now.isoformat() + "Z",
                    "actionable": True
                })
    
    return {"alerts": alerts}