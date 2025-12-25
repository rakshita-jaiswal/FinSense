# Feature Restrictions Implementation Plan

## Overview
Implement feature restrictions so free plan users only have access to basic features, while premium features require an upgrade.

## Plan Structure

### Free Plan Features (Always Available)
1. ✅ Basic dashboard view
2. ✅ Manual transaction entry
3. ✅ Basic transaction list
4. ✅ Profile management
5. ✅ Settings access

### Premium Features (Require Upgrade)
1. 🔒 FinSense AI chat
2. 🔒 Auto-categorization
3. 🔒 Transaction confidence scores
4. 🔒 Smart transaction review
5. 🔒 Advanced charts (Revenue vs Expense trends, Expense breakdown)
6. 🔒 Financial reports with filters
7. 🔒 Receipt upload
8. 🔒 Export data
9. 🔒 Bank account connection
10. 🔒 Automatic transaction sync

## Implementation Strategy

### 1. Header Changes ✅
- Replace "Trial Active" with "Upgrade Plan" button for free users
- Show "Premium" badge for premium users
- Button navigates to /pricing page

### 2. Feature Lock Overlay Component
- Create reusable `<FeatureLockOverlay>` component
- Shows upgrade prompt when free users try to access premium features
- Includes "Upgrade to Premium" button

### 3. Page-Level Restrictions
- **FinSense AI Page**: Show feature lock overlay for free users
- **Connect Accounts Page**: Show feature lock overlay for free users
- **Transaction Review Page**: Show feature lock overlay for free users
- **Reports Page**: Show feature lock overlay for free users
- **Receipts Page**: Show feature lock overlay for free users

### 4. Component-Level Restrictions
- **Dashboard Charts**: Show locked state for advanced charts
- **Transaction List**: Disable export button for free users
- **Transaction Items**: Hide confidence scores for free users
- **AI Query Component**: Show locked state for free users

### 5. Backend Validation
- Add middleware to check subscription status for premium endpoints
- Return 403 Forbidden for free users accessing premium features
- Ensure data integrity and security

## Current Status

### Completed ✅
1. Header updated to show "Upgrade Plan" button
2. Subscription context updated (hasAccess: false for free plan)
3. Backend subscription endpoint updated

### Next Steps 🔄
1. Implement feature lock overlays on premium pages
2. Add restrictions to dashboard components
3. Update transaction list to hide premium features
4. Test complete flow

## Testing Checklist
- [ ] Free user sees "Upgrade Plan" button in header
- [ ] Free user cannot access FinSense AI
- [ ] Free user cannot connect bank accounts
- [ ] Free user cannot see advanced charts
- [ ] Free user cannot export data
- [ ] Premium user has full access to all features
- [ ] Upgrade button navigates to pricing page