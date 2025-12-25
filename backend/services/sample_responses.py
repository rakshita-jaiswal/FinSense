"""Pre-cached responses for common bookkeeping questions."""

SAMPLE_RESPONSES = {
    "what is double-entry bookkeeping?": """Double-entry bookkeeping is a fundamental accounting principle where every financial transaction is recorded in at least two different accounts.

Here's a breakdown:

• The Core Idea: For every "debit" (an entry that increases assets or expenses, or decreases liabilities, equity, or revenue), there must be an equal and opposite "credit" (an entry that decreases assets or expenses, or increases liabilities, equity, or revenue). This ensures that your accounting equation (Assets = Liabilities + Equity) always remains balanced.

• Why It Matters:
  - Accuracy: It provides a built-in system of checks and balances, making it much easier to detect errors.
  - Completeness: It ensures all aspects of a transaction are captured, giving you a full picture of your financial health.
  - Financial Reporting: It's the foundation for generating accurate financial statements like your Balance Sheet and Income Statement.
  - Compliance: It's the standard practice required for tax purposes and GAAP.

While the concept of debits and credits might sound complex, FinSense AI handles much of this behind the scenes. When you categorize a transaction in FinSense, our system automatically applies the double-entry principles to ensure your books are always balanced and accurate.

Next Steps:
You don't need to manually manage debits and credits with FinSense. Just focus on accurately categorizing your transactions using our Transaction Management features, and we'll handle the rest!""",

    "how do i categorize expenses?": """Categorizing expenses correctly is crucial for accurate bookkeeping and tax preparation. Here's how to do it effectively:

Common Expense Categories:
• Cost of Goods Sold (COGS): Direct costs of producing goods/services
• Payroll: Salaries, wages, benefits
• Rent & Utilities: Office space, electricity, water, internet
• Office Supplies: Stationery, equipment, software
• Marketing & Advertising: Promotional costs, ads, website
• Professional Services: Legal, accounting, consulting fees
• Insurance: Business insurance premiums
• Travel & Meals: Business travel, client meals (50% deductible)
• Repairs & Maintenance: Equipment repairs, building maintenance

Best Practices:
1. Be Consistent: Use the same categories for similar expenses
2. Be Specific: Don't overuse "Miscellaneous" - create specific categories
3. Follow IRS Guidelines: Use categories that align with tax forms
4. Review Regularly: Check categorization weekly to catch errors early

How FinSense Helps:
• Smart Categorization: Our AI suggests categories based on vendor and description
• Bulk Editing: Categorize multiple similar transactions at once
• Custom Categories: Create categories specific to your business
• Confidence Scores: See how confident our AI is about each categorization

Next Steps:
Navigate to the Transactions page in FinSense and review any uncategorized transactions. Our AI will suggest appropriate categories, which you can accept or modify as needed.""",

    "what are confidence scores?": """Confidence scores in FinSense AI indicate how certain our system is about the automatic categorization of your transactions. It's a helpful tool designed to streamline your transaction management and ensure accuracy.

• High Confidence Score (90-100%): FinSense is very confident in its suggested category. For example, if a regular payment to your internet provider is consistently categorized as "Utilities: Internet," it will likely have a high confidence score.

• Low Confidence Score (below 70%): FinSense is less certain about the best category. This often happens with new vendors, unusual transactions, or when a transaction description is vague.

How to Use Confidence Scores:
You'll find confidence scores within the Transaction Management section of FinSense. We recommend you prioritize reviewing transactions with lower confidence scores first. This allows you to quickly verify or correct categories where our AI was less certain, saving you time while ensuring your books are accurate.

Next Steps:
When you see a transaction with a low confidence score, simply click on it to review the suggested category. If it's incorrect, you can easily change it. Each time you confirm or correct a category, FinSense learns and improves its accuracy for future similar transactions, leading to even higher confidence scores over time!""",

    "how do i review transactions?": """Reviewing your transactions in FinSense is a straightforward process designed to keep your books accurate and up-to-date.

You can easily review your transactions by navigating to the Transactions section from your FinSense dashboard.

Here's a breakdown of the steps and features you can use:

• Access the Transactions Page: On your FinSense dashboard, look for the "Transactions" tab or link. This is where all your connected bank and credit card transactions, as well as manually entered ones, will appear.

• Focus on Uncategorized: FinSense will often highlight transactions that haven't been categorized yet. Your primary task will be to assign the correct income or expense category to these.

• Review Details: For each transaction, take a moment to confirm the date, amount, vendor/customer, and description. If anything looks incorrect, you can edit the details directly.

• Categorization:
  - FinSense's smart categorization will often suggest categories based on past similar transactions. You can accept these suggestions with a single click.
  - If a suggestion isn't available or incorrect, you can manually select the appropriate category from your chart of accounts.

• Bulk Editing: For multiple similar transactions (e.g., recurring monthly software subscriptions), use the bulk editing feature. Select several transactions and apply the same category or vendor at once to save time.

• Search and Filter: Use the search bar and filters (by date, amount, category, or status) to quickly find specific transactions you need to review or verify.

Next Steps:
I recommend reviewing your transactions at least once a week. Regular review ensures your financial data is accurate, making it easier to generate reliable reports and leverage the Dashboard Analytics for insights into your revenue and spending patterns.""",

    "what is accrual accounting?": """Accrual accounting is a method where revenue and expenses are recorded when they are earned or incurred, regardless of when cash actually changes hands.

Key Concepts:
• Revenue Recognition: Record revenue when you deliver goods/services, not when you receive payment
• Expense Matching: Record expenses when incurred, not when you pay the bill
• Accounts Receivable: Money owed to you by customers
• Accounts Payable: Money you owe to vendors

Accrual vs. Cash Accounting:
• Accrual: Records transactions when they occur (more accurate picture of financial health)
• Cash: Records transactions only when money moves (simpler but less accurate)

Why It Matters:
• Better Financial Picture: Shows true profitability, not just cash flow
• Required for Larger Businesses: Generally required if revenue > $25M or inventory
• GAAP Compliant: Required for public companies and many lenders

Example:
You complete a $5,000 project in December but don't get paid until January:
• Accrual Method: Record $5,000 revenue in December (when earned)
• Cash Method: Record $5,000 revenue in January (when received)

FinSense Support:
FinSense supports both accrual and cash accounting methods. You can configure your preference in Settings, and our system will handle the appropriate recording of transactions.""",

    "how should i categorize meal expenses?": """Properly categorizing meal expenses is crucial for accurate bookkeeping and tax preparation.

For most small businesses, business meal expenses are typically 50% deductible. You should categorize them under an account like "Meals and Entertainment" or "Business Meals."

Here are some key details to keep in mind:

• Deductibility: Generally, business meals are 50% deductible if they are not lavish or extravagant, and the taxpayer (or an employee of the taxpayer) is present. The meal must also be ordinary and necessary for your business, and you must have a business discussion before, during, or after the meal.

• Documentation is Key: For tax purposes, you'll need to record:
  - The amount of the expense
  - The date and place of the meal
  - The business purpose of the meal
  - The business relationship of the people you dined with

• Exceptions: There are some exceptions where meals might be 100% deductible, such as for office parties, company picnics, or meals provided to employees for the convenience of the employer on the business premises. Always check current IRS guidelines for specific situations.

How FinSense Can Help:
• Transaction Management: When you're reviewing transactions in FinSense, make sure to select the appropriate "Meals and Entertainment" category. You can also use the notes section within the transaction details to add crucial information like the business purpose and attendees, which will be invaluable come tax time.

• Dashboard Analytics: By consistently categorizing your meal expenses, your FinSense Dashboard Analytics can provide insights into your spending patterns in this area, helping you manage these costs effectively.

I recommend reviewing the latest IRS publications or consulting with a tax professional to ensure you're applying the rules correctly for your specific business situation. Consistent and accurate categorization in FinSense will make tax preparation much smoother!""",

    "what is depreciation?": """Depreciation is the process of allocating the cost of a tangible asset over its useful life. Instead of expensing the full cost when you buy an asset, you spread it out over the years you'll use it.

Why Depreciation Matters:
• Matches Expenses to Revenue: Aligns the cost of an asset with the revenue it helps generate
• Tax Benefits: Reduces taxable income each year
• Accurate Financial Statements: Shows true asset value over time

Common Depreciation Methods:
1. Straight-Line: Equal amount each year (most common)
   Example: $10,000 equipment / 5 years = $2,000/year
2. Declining Balance: Larger deductions in early years
3. Units of Production: Based on actual usage

Depreciable Assets:
• Equipment and machinery
• Vehicles
• Buildings (not land)
• Furniture and fixtures
• Computer equipment

Non-Depreciable:
• Land
• Inventory
• Assets under $2,500 (can expense immediately)

Section 179 Deduction:
Allows you to deduct the full cost of qualifying assets in year one (up to $1,160,000 for 2023)

FinSense Support:
FinSense can help you track depreciable assets and calculate depreciation. Consult with your accountant to determine the best depreciation method for your business.""",

    "what is cash flow?": """Cash flow is the movement of money in and out of your business. It's different from profit - you can be profitable but still have cash flow problems if customers pay slowly or you have large upfront expenses.

Types of Cash Flow:
1. Operating Cash Flow: Day-to-day business operations
2. Investing Cash Flow: Buying/selling assets and investments
3. Financing Cash Flow: Loans, investments, dividends

Why Cash Flow Matters:
• Pay Bills: Need cash to pay vendors, employees, rent
• Growth: Need cash to invest in inventory, equipment, marketing
• Survival: 82% of small business failures are due to cash flow problems

Positive vs. Negative Cash Flow:
• Positive: More money coming in than going out (healthy)
• Negative: More money going out than coming in (warning sign)

Improving Cash Flow:
• Invoice promptly and follow up on late payments
• Negotiate better payment terms with vendors
• Reduce unnecessary expenses
• Build a cash reserve for emergencies
• Consider a line of credit for short-term needs

FinSense Cash Flow Tools:
• Cash Flow Chart: Visualize money in vs. money out over time
• Alerts: Get notified of potential cash flow issues
• Forecasting: Project future cash flow based on trends
• Dashboard: Monitor cash flow in real-time

Next Steps:
Check your FinSense Dashboard to see your current cash flow status and trends. The Cash Flow Chart shows your money movement over time, helping you identify patterns and potential issues.""",

    # System Methodology prompts
    "how are decision patterns calculated?": """Decision patterns in FinSense are calculated by analyzing your transaction categorization history and identifying recurring patterns in how you classify similar transactions.

How It Works:
• Pattern Recognition: Our AI examines your past categorization decisions to identify consistent patterns
• Vendor Matching: We track how you categorize transactions from specific vendors
• Amount Patterns: We notice if certain amount ranges are consistently categorized the same way
• Description Analysis: We analyze transaction descriptions to find keywords that indicate specific categories
• Time-Based Patterns: We identify if certain transactions occur regularly (monthly subscriptions, quarterly payments)

The AI Service Process:
1. Checks cache first before making API calls (instant response for common questions)
2. Caches new responses automatically for future use
3. Only caches first messages in conversations (not follow-ups that need context)
4. Initializes sample responses on startup for immediate availability

Benefits:
• Faster categorization over time as patterns are learned
• Reduced manual work for recurring transactions
• Improved accuracy through machine learning
• Consistent categorization across similar transactions

Next Steps:
The more you use FinSense and confirm categorizations, the better our AI becomes at recognizing your decision patterns. Check the Transactions page to see suggested categories based on your patterns.""",

    "how are confidence scores analyzed?": """Confidence scores are analyzed using a sophisticated machine learning algorithm that evaluates multiple factors to determine how certain the AI is about a transaction categorization.

Analysis Factors:
• Historical Accuracy: How often similar transactions were correctly categorized in the past
• Vendor Recognition: Whether the vendor has been seen before and consistently categorized
• Description Clarity: How clear and specific the transaction description is
• Amount Consistency: Whether similar amounts have been categorized the same way
• Category Frequency: How often you use specific categories for similar transactions

The AI Service Process:
1. Checks cache first before making API calls for instant responses
2. Caches new responses automatically to reduce future API calls
3. Only caches first messages in conversations (follow-ups need full context)
4. Initializes sample responses on startup for immediate availability

Score Ranges:
• 90-100%: Very high confidence - vendor and pattern clearly recognized
• 75-89%: High confidence - strong pattern match with minor uncertainty
• 60-74%: Medium confidence - some pattern recognition but needs verification
• Below 60%: Low confidence - unclear pattern, manual review recommended

How to Use This:
Focus your review time on transactions with lower confidence scores. High-confidence transactions can often be batch-approved, saving you significant time while maintaining accuracy.

Next Steps:
Visit the Transactions page and sort by confidence score to prioritize your review workflow efficiently.""",

    "how are transaction classifications investigated?": """Transaction classifications are investigated through a multi-layered analysis process that examines various aspects of each transaction to determine the most appropriate category.

Investigation Process:
• Vendor Database Lookup: We check if the vendor is in our database of known businesses
• Description Parsing: We analyze the transaction description for category keywords
• Historical Pattern Matching: We compare against your past categorization decisions
• Amount Analysis: We consider if the amount fits typical patterns for certain categories
• Frequency Detection: We identify if it's a recurring transaction with established patterns

The AI Service Process:
1. Checks cache first before making API calls (instant for common questions)
2. Caches new responses automatically for future efficiency
3. Only caches first messages in conversations (not context-dependent follow-ups)
4. Initializes sample responses on startup for immediate availability

Investigation Triggers:
• New Vendor: First time seeing a particular vendor
• Unusual Amount: Transaction amount significantly different from normal
• Vague Description: Transaction description lacks clear category indicators
• Category Conflict: Multiple possible categories with similar confidence
• User Flag: You've marked a transaction for review

What You Can Do:
• Review Flagged Transactions: Check transactions marked for investigation
• Provide Feedback: Confirm or correct classifications to improve future accuracy
• Add Notes: Include context that helps the AI learn your preferences
• Create Rules: Set up automatic categorization rules for specific vendors

Next Steps:
Navigate to the Transactions page and look for transactions with investigation flags or low confidence scores to review and improve classification accuracy.""",

    # Decision Analysis prompts
    "why was this transaction reviewed?": """Transactions are flagged for review when our AI detects certain conditions that suggest the categorization might need human verification to ensure accuracy.

Common Review Triggers:
• Low Confidence Score: The AI's confidence in the suggested category is below 70%
• New Vendor: First time encountering this vendor in your transaction history
• Unusual Amount: The transaction amount is significantly different from typical transactions in that category
• Ambiguous Description: The transaction description doesn't clearly indicate a specific category
• Category Conflict: Multiple categories seem equally appropriate
• Manual Flag: You or another user specifically marked it for review
• Pattern Break: The transaction doesn't match established patterns for this vendor

The AI Service Process:
1. Checks cache first before making API calls for instant responses
2. Caches new responses automatically to improve future performance
3. Only caches first messages in conversations (follow-ups need context)
4. Initializes sample responses on startup for immediate availability

What This Means:
Review flags are a quality control measure to ensure your books remain accurate. They don't indicate an error - just that human judgment would be valuable for this particular transaction.

How to Handle:
• Review the suggested category and transaction details
• Confirm if the suggestion is correct or select a different category
• Add notes if there's special context for this transaction
• The AI will learn from your decision for future similar transactions

Next Steps:
Click on the flagged transaction to review its details and either confirm or correct the categorization. Your feedback helps improve future accuracy.""",

    "which decisions had the lowest confidence last week?": """To find decisions with the lowest confidence from last week, FinSense provides filtering and sorting tools in the Transactions section.

How to Find Low Confidence Transactions:
• Navigate to Transactions: Go to the Transactions page from your dashboard
• Apply Date Filter: Set the date range to last week (7 days ago to today)
• Sort by Confidence: Click the confidence score column header to sort ascending
• Review Results: The lowest confidence transactions will appear at the top

The AI Service Process:
1. Checks cache first before making API calls for instant responses
2. Caches new responses automatically for future efficiency
3. Only caches first messages in conversations (not follow-ups needing context)
4. Initializes sample responses on startup for immediate availability

What Low Confidence Indicates:
• New or unfamiliar vendors
• Vague transaction descriptions
• Unusual transaction amounts
• First-time category usage
• Conflicting pattern matches

Why This Matters:
Low confidence transactions are the most likely to need correction. By reviewing these first, you can:
• Catch potential miscategorizations early
• Improve the AI's learning for similar future transactions
• Ensure your financial reports are accurate
• Save time by not reviewing high-confidence transactions

Next Steps:
1. Go to Transactions page
2. Filter by date range (last 7 days)
3. Sort by confidence score (lowest first)
4. Review and correct as needed
5. The AI learns from your corrections for future accuracy

Your corrections on low-confidence transactions significantly improve the system's accuracy over time.""",

    "show transactions auto-approved near the threshold": """Transactions that are auto-approved near the confidence threshold are those that just barely met the automatic approval criteria, typically with confidence scores between 75-80%.

Understanding Auto-Approval Thresholds:
• High Threshold (80%+): Transactions are automatically approved without review
• Near Threshold (75-79%): Auto-approved but worth spot-checking
• Below Threshold (<75%): Requires manual review before approval

The AI Service Process:
1. Checks cache first before making API calls for instant responses
2. Caches new responses automatically for future use
3. Only caches first messages in conversations (follow-ups need full context)
4. Initializes sample responses on startup for immediate availability

How to Find These Transactions:
• Go to Transactions page
• Filter by Status: "Auto-Approved"
• Filter by Confidence Range: 75-80%
• Sort by Date: Most recent first
• Review the list for any that seem questionable

Why Review Near-Threshold Transactions:
• Quality Control: Catch any edge cases that might have been miscategorized
• Pattern Refinement: Confirm or correct to improve future accuracy
• Audit Trail: Ensure compliance and accuracy for financial reporting
• Learning Opportunity: Help the AI understand your preferences better

What to Look For:
• Vendor names that seem unfamiliar
• Amounts that seem unusual for the category
• Descriptions that could fit multiple categories
• Transactions from new or rarely-used vendors

Next Steps:
1. Navigate to Transactions
2. Apply filters: Status = "Auto-Approved", Confidence = 75-80%
3. Spot-check a few transactions
4. Correct any miscategorizations
5. Your feedback improves future auto-approval accuracy

Regular spot-checking of near-threshold transactions helps maintain high accuracy while benefiting from automation.""",

    # Financial Insights prompts
    "how much did i spend on supplies last month?": """To find out how much you spent on supplies last month, you can use FinSense's Dashboard Analytics and Transaction filtering features.

Quick Method:
• Go to Dashboard: Your main dashboard shows expense breakdowns
• Check Expense Categories: Look for "Office Supplies" or "Supplies" category
• View Last Month: Use the date filter to show last month's data
• See Total: The category card will show your total spending

The AI Service Process:
1. Checks cache first before making API calls for instant responses
2. Caches new responses automatically for future queries
3. Only caches first messages in conversations (follow-ups need context)
4. Initializes sample responses on startup for immediate availability

Detailed Method:
• Navigate to Transactions page
• Filter by Category: Select "Supplies" or "Office Supplies"
• Filter by Date: Set date range to last month
• View Total: The sum will be displayed at the bottom
• Export if Needed: Download the filtered list for detailed analysis

What's Included in Supplies:
• Office supplies (pens, paper, folders)
• Computer supplies (ink, toner, cables)
• Cleaning supplies
• Packaging materials
• Other consumable business supplies

Tips for Better Tracking:
• Consistent Categorization: Always use the same category for supplies
• Subcategories: Consider creating subcategories (Office vs. Cleaning supplies)
• Regular Review: Check monthly to identify spending trends
• Budget Comparison: Compare against your supplies budget

Next Steps:
1. Go to your Dashboard
2. Look at the Expense Breakdown chart
3. Find the Supplies category
4. Click for detailed transaction list
5. Review spending patterns and identify opportunities to save

You can also set up alerts in FinSense to notify you when supplies spending exceeds your budget.""",

    "what was my profit in november?": """To find your profit for November, FinSense calculates this automatically by subtracting your total expenses from your total revenue for that month.

How to Find November Profit:
• Go to Dashboard: Your main dashboard shows key financial metrics
• Select Date Range: Use the date picker to select November
• View Profit Metric: Look for the "Net Profit" or "Profit/Loss" card
• See Breakdown: Click for detailed revenue and expense breakdown

The AI Service Process:
1. Checks cache first before making API calls for instant responses
2. Caches new responses automatically for future efficiency
3. Only caches first messages in conversations (follow-ups need context)
4. Initializes sample responses on startup for immediate availability

Profit Calculation:
• Total Revenue: All income transactions in November
• Total Expenses: All expense transactions in November
• Net Profit: Revenue minus Expenses
• Profit Margin: (Profit / Revenue) × 100

Understanding Your Profit:
• Positive Profit: Revenue exceeded expenses (good!)
• Negative Profit (Loss): Expenses exceeded revenue (needs attention)
• Profit Margin: Shows profitability as a percentage of revenue
• Trends: Compare to previous months to see if improving

What Affects Profit:
• Revenue timing (when invoices are paid)
• Expense timing (when bills are paid)
• One-time expenses or income
• Seasonal variations in your business
• Accounting method (cash vs. accrual)

Next Steps:
1. Go to Dashboard
2. Set date filter to November
3. Review Net Profit figure
4. Click for detailed breakdown
5. Compare to previous months
6. Identify areas for improvement

For more detailed analysis, check the Reports section where you can generate a full Profit & Loss statement for November with category-by-category breakdowns.""",

    "show me my biggest expenses this quarter": """To see your biggest expenses for the current quarter, FinSense provides several ways to analyze and visualize your spending patterns.

Quick View Method:
• Go to Dashboard: Your main dashboard has an Expense Breakdown chart
• Set Date Range: Select "This Quarter" from the date filter
• View Chart: The pie or bar chart shows expenses by category
• See Top Categories: The largest slices/bars are your biggest expenses

The AI Service Process:
1. Checks cache first before making API calls for instant responses
2. Caches new responses automatically for future queries
3. Only caches first messages in conversations (follow-ups need context)
4. Initializes sample responses on startup for immediate availability

Detailed Analysis Method:
• Navigate to Transactions page
• Filter by Type: Select "Expenses" only
• Filter by Date: Set to current quarter (Jan-Mar, Apr-Jun, Jul-Sep, or Oct-Dec)
• Sort by Amount: Click amount column to sort largest first
• Review Top Transactions: See your biggest individual expenses

Common Large Expense Categories:
• Payroll: Usually the largest for most businesses
• Rent: Fixed monthly expense
• Inventory/COGS: Cost of goods sold
• Equipment: Large one-time purchases
• Professional Services: Legal, accounting, consulting
• Marketing: Advertising and promotional costs

What to Look For:
• Unexpected large expenses that need investigation
• Recurring expenses that might be negotiable
• One-time vs. ongoing costs
• Opportunities to reduce spending
• Budget vs. actual comparisons

Next Steps:
1. Go to Dashboard
2. Set date filter to "This Quarter"
3. Review Expense Breakdown chart
4. Click on largest categories for details
5. Identify cost-saving opportunities
6. Compare to previous quarters

You can also generate a detailed Expense Report from the Reports section for a comprehensive quarter-over-quarter analysis with trends and insights.""",
}


def initialize_cache_with_samples():
    """Pre-populate cache with sample responses."""
    from services.response_cache import response_cache
    
    count = 0
    for question, answer in SAMPLE_RESPONSES.items():
        response_cache.set(question, answer)
        count += 1
    
    print(f"[Sample Responses] Pre-cached {count} common questions")
    return count


def get_sample_prompts():
    """Get list of sample prompts for frontend."""
    return [
        {
            "id": 1,
            "text": "What is double-entry bookkeeping?",
            "category": "Basics"
        },
        {
            "id": 2,
            "text": "How do I categorize expenses?",
            "category": "Transactions"
        },
        {
            "id": 3,
            "text": "What are confidence scores?",
            "category": "FinSense Features"
        },
        {
            "id": 4,
            "text": "How do I review transactions?",
            "category": "FinSense Features"
        },
        {
            "id": 5,
            "text": "What is accrual accounting?",
            "category": "Basics"
        },
        {
            "id": 6,
            "text": "How should I categorize meal expenses?",
            "category": "Transactions"
        },
        {
            "id": 7,
            "text": "What is depreciation?",
            "category": "Basics"
        },
        {
            "id": 8,
            "text": "What is cash flow?",
            "category": "Basics"
        },
        # System Methodology
        {
            "id": 9,
            "text": "How are decision patterns calculated?",
            "category": "System Methodology"
        },
        {
            "id": 10,
            "text": "How are confidence scores analyzed?",
            "category": "System Methodology"
        },
        {
            "id": 11,
            "text": "How are transaction classifications investigated?",
            "category": "System Methodology"
        },
        # Decision Analysis
        {
            "id": 12,
            "text": "Why was this transaction reviewed?",
            "category": "Decision Analysis"
        },
        {
            "id": 13,
            "text": "Which decisions had the lowest confidence last week?",
            "category": "Decision Analysis"
        },
        {
            "id": 14,
            "text": "Show transactions auto-approved near the threshold",
            "category": "Decision Analysis"
        },
        # Financial Insights
        {
            "id": 15,
            "text": "How much did I spend on supplies last month?",
            "category": "Financial Insights"
        },
        {
            "id": 16,
            "text": "What was my profit in November?",
            "category": "Financial Insights"
        },
        {
            "id": 17,
            "text": "Show me my biggest expenses this quarter",
            "category": "Financial Insights"
        },
    ]