---
title: RBI e-mandate framework for recurring payments (2026 consolidated framework; earlier AFA limits from 2022)
regulator: RBI (with NPCI for UPI and RuPay)
status: in force (consolidated framework reported in April 2026)
zone_trigger: WHITE
last_verified: 2026-11-05
sources:
  - https://www.businesstoday.in/personal-finance/news/story/rbi-caps-recurring-payments-at-rs15000-without-otp-under-new-e-mandate-framework-526759-2026-04-21
  - https://www.outlookbusiness.com/ampstories/news/rbi-e-mandate-framework-2026-new-rules-for-auto-pay-upi-cards-wallets
  - https://www.khaitanco.com/thought-leaderships/RBI-enhances-transaction-limits-for-processing-of-e-mandates-for-recurring-transactions:-from-INR-5000-to-INR-15000
  - https://www.npci.org.in/PDF/npci/rupay/2022/Circular-RuPay-AutoPay-AFA-Limit-enhancement-and-compliance.pdf
---

## What it says
A recurring payment (an e-mandate) needs one full authentication when first set up. After that, recurring debits up to Rs 15,000 per transaction can run without a separate OTP. Above that, additional authentication is needed. Reports of the 2026 framework say certain categories (insurance premiums, mutual fund investments, credit card bill payments) may go up to Rs 1 lakh without extra authentication, if registered as e-mandates. Banks must send a pre-debit alert at least 24 hours before each debit, so the user can cancel. FASTag and NCMC top-ups are exempt from that alert. The UPI app or bank limit can be lower than Rs 15,000. The lowest applicable limit applies.

## What it means for a founder
- Subscriptions within the Rs 15,000 limit are feasible on UPI AutoPay. Expect cancellations: users can see the 24-hour alert and cancel in their UPI app.
- Above Rs 15,000 per debit, each payment needs the user's OTP or authentication. Plan billing around that.
- No legal problem is flagged by this file. This zone is WHITE for normal subscriptions. Pricing risk is covered by the India checks (filter 4, mandate friction), not by law.

## Watch for
- Sources in this check describe a 2026 framework, not a 2025 one. Verify the limit and exemptions against the RBI circular before relying on them.
- The Rs 1 lakh category rules and the list of e-mandate categories.
- Whether the limit applies per transaction or per day for your payment rail.
