# Idea types

The Chair classifies every idea into one primary type in Step 1, and at most one secondary type, before running the India checks. The type decides which extra facts the brief needs, which checks run in Step 2, which `laws/` files to read, and how much weight each seat gets. Numbers marked `(rule of thumb)` are heuristics, not sourced facts. Say so when you use them.

The 5 friction filters in `india-filters.md` were written for software and services sold to Indian businesses. For other types, run the type checks below and grade only the filters the type lists. Write `n/a for this type` for the rest. The 4 scalability bottlenecks apply to every type.

Each type's law list names files in `laws/`. If a file is listed as missing, or no file fits, the zone is `UNMAPPED` and the Chair names the regulator in the list. Never cite a law from memory.

## How to classify

| If the founder mainly... | Type |
|---|---|
| sells software, an app or an API to businesses | 1. Software and SaaS |
| sells an app, content or a community to consumers | 2. Consumer app and content |
| connects buyers and sellers and takes a cut | 3. Marketplace and platform |
| sells a physical product they brand (food, FMCG, cosmetics, apparel, D2C) | 4. Physical product and D2C |
| makes things: a factory, hardware, devices, EVs, components | 5. Manufacturing and hardware |
| sells people's time or expertise (agency, consulting, coaching, clinic, local services) | 6. Service business |
| runs a shop, restaurant, cloud kitchen or franchise | 7. Local and offline business |
| touches money, health, property, education or insurance | 8. Regulated sector (add it as a secondary type to any of the above) |

A hardware device with a subscription app is type 5, secondary type 1. A tuition app is type 2, secondary type 8 (education). A pharmacy delivery app is type 3, secondary type 8 (health).

## 1. Software and SaaS

- **Brief needs:** buyer and user (often different), price and billing cycle, sales motion (self-serve, inside sales, field, channel partner).
- **Checks:** all 5 friction filters. Plus: gross margin after cloud and AI costs; payback months on acquisition cost; will a buyer abroad pay many times the Indian price?
- **Laws:** `dpdp-act-2023-and-rules-2025.md`, `it-act-and-intermediary-rules.md`, `gst-basics-for-startups.md`.
- **Seats:** Girish 3, Vembu 2, Nithin 2 if it touches customer data or money.

## 2. Consumer app and content

- **Brief needs:** how often one user comes back each week, how it earns (ads, subscription, micro-payments, commerce), the acquisition channel.
- **Checks:** filters 4 and 5. Plus: Delta 4 against today's habit; the retention curve after the first month; whether revenue per user covers acquisition outside India 1; creator or content cost per user.
- **Laws:** `dpdp-act-2023-and-rules-2025.md` (children's data matters here), `it-act-and-intermediary-rules.md`, `consumer-protection-e-commerce.md`, `online-gaming-act-2025.md` if any money is staked, `advertising-and-endorsements.md` (missing until added; regulator CCPA and ASCI).
- **Seats:** Kunal 3, Deepinder 2.

## 3. Marketplace and platform

- **Brief needs:** both sides, who pays the take rate, how supply is onboarded, order frequency.
- **Checks:** filters 3, 4 and 5. Plus: liquidity (does a buyer find a match within a few tries in one city?); leakage (do both sides meet once and then deal off-platform?); take rate against what the supply side can afford; quality control and refunds; one city working before the next.
- **Laws:** `consumer-protection-e-commerce.md`, `it-act-and-intermediary-rules.md`, `payment-aggregators.md` if the platform holds money, `dpdp-act-2023-and-rules-2025.md`. Foreign investment rules for inventory-led e-commerce: missing; regulator DPIIT.
- **Seats:** Deepinder 3, Kunal 2, Nithin 2 if money is held.

## 4. Physical product and D2C (food, FMCG, cosmetics, apparel, gadgets you brand)

- **Brief needs:** cost of goods per unit, selling price, channel (own website, Amazon or Flipkart, quick commerce, general trade through distributors, modern trade), who manufactures, minimum order quantity.
- **Checks:** filters 4 and 5 only. Plus these six:
  1. **Gross margin after cost of goods.** A brand that must pay for ads, platform fees and returns usually needs a high gross margin to survive (rule of thumb). Ask the founder for the number.
  2. **Channel margin stack.** General trade passes margin to the distributor and the retailer; marketplaces and quick commerce charge commission, ads and fees. Walk one unit from factory price to the shelf price.
  3. **Working capital.** Inventory days plus receivable days minus payable days. Modern trade and marketplaces can pay late, and slow stock locks up cash.
  4. **Returns and COD.** Cash-on-delivery orders that are refused and shipped back cost two-way shipping (rule of thumb: high in Tier-2 and Tier-3 towns). What share of orders are COD, and what happens to a refused parcel?
  5. **Repeat purchase.** A product bought once a year cannot carry a high acquisition cost.
  6. **Certification and labelling before the first sale:** food licence, label rules, quality marks.
- **Laws:** `food-safety-fssai.md`, `legal-metrology-packaged-commodities.md`, `bis-quality-control-orders.md`, `drugs-cosmetics-and-medical-devices.md` for cosmetics, supplements that make claims, and devices, `advertising-and-endorsements.md`, `environment-consents-and-epr.md` for plastic packaging, `consumer-protection-e-commerce.md`, `gst-basics-for-startups.md`. Any of these not yet in `laws/` is UNMAPPED.
- **Seats:** Kunal 3 (brand, status, repeat), Deepinder 2 (operations, discounts), Nithin 2 (cash and working capital). No seat has deep D2C experience: say so in the verdict.

## 5. Manufacturing and hardware

- **Brief needs:** capex, monthly capacity, the bill of materials and how much of it is imported, who buys (consumer, B2B, government), certification needed.
- **Checks:** filters 2 and 4. Plus:
  1. **Capex and break-even utilisation.** At what share of capacity does the plant cover fixed cost?
  2. **Import dependence.** Which parts come from one foreign supplier? What happens if a duty or a ban changes?
  3. **Certification lead time.** Quality marks and testing can take months; cash burns while you wait.
  4. **Working capital and buyer payment terms.** Large buyers and government can pay late.
  5. **Service network.** Who repairs it in Tier-2 towns?
  6. **Government levers:** production-linked incentives, state subsidies, public procurement. Treat them as upside, never as the business case.
- **Laws:** `bis-quality-control-orders.md`, `environment-consents-and-epr.md` (pollution consents, e-waste and battery rules), `labour-codes.md`, `legal-metrology-packaged-commodities.md` for packaged goods, `gst-basics-for-startups.md`, `export-import-and-fema.md` if it exports or imports. Any of these not yet in `laws/` is UNMAPPED.
- **Seats:** Vembu 3 (making, R&D, rural plants), Nithin 2 (capital discipline), Deepinder 2 (operations at scale). No seat has deep factory experience: say so in the verdict.

## 6. Service business (agency, consulting, coaching, clinic, local services)

- **Brief needs:** who delivers the service (the founder or a team), price per client or per hour, client acquisition channel, repeat or one-off.
- **Checks:** filters 1, 3 and 4. Plus:
  1. **Founder dependence.** If the founder stops working for a month, does revenue stop?
  2. **Utilisation.** What share of paid team hours is billed? Below a healthy level the business loses money on every hire (rule of thumb; ask for the number).
  3. **Productisation path.** Can a repeated service become a fixed-price package, a tool, or software?
  4. **Client concentration.** Does one client bring a large share of revenue?
  5. **Collection.** Advance payment, milestone billing, or 60 to 180 days (rule of thumb) after the invoice?
  6. **India-to-global option:** is the same service worth far more to buyers abroad?
- **Laws:** `gst-basics-for-startups.md`, `dpdp-act-2023-and-rules-2025.md` for client data, `labour-codes.md`, `advertising-and-endorsements.md` for coaching and courses that promise results. Clinics: `telemedicine-and-e-pharmacy.md` plus state clinical establishment rules (missing; regulator: state health department). Coaching centres: `coaching-and-education.md`. Any of these not yet in `laws/` is UNMAPPED.
- **Seats:** Vembu 2 (products over hours), Girish 2 (India-to-global services), Nithin 2. No seat built a service firm: say so in the verdict.

## 7. Local and offline business (shop, restaurant, cloud kitchen, franchise)

- **Brief needs:** location, rent, staff, average bill, daily footfall or orders, delivery share.
- **Checks:** filters 3 and 4. Plus: rent as a share of revenue; break-even orders per day; aggregator commission on delivery orders; staff churn; licences needed before opening; unit economics of the second outlet before the tenth.
- **Laws:** `food-safety-fssai.md` for food, `legal-metrology-packaged-commodities.md` for packaged goods, `gst-basics-for-startups.md`, `labour-codes.md`. Shop and trade licences are state and municipal rules: UNMAPPED, check the state labour department and the municipal corporation.
- **Seats:** Deepinder 3, Kunal 2, Nithin 2.

## 8. Regulated sector (add as a secondary type)

Run the primary type's checks, then add the sector's lines below. A regulated sector raises the bar for the legal zone: if no law file covers the exact activity, the zone is UNMAPPED, never WHITE.

- **Money (payments, lending, deposits, investing, crypto):** the fintech law files already in `laws/`. Nithin 3.
- **Health (telemedicine, pharmacy, clinics, devices, health data):** `telemedicine-and-e-pharmacy.md`, `drugs-cosmetics-and-medical-devices.md`, `dpdp-act-2023-and-rules-2025.md`. Check: who is the licensed professional, where prescriptions come from, and what a wrong answer costs a patient. Nithin 2 (trust).
- **Education (coaching, schools, courses, degrees, edtech):** `coaching-and-education.md`, `consumer-protection-e-commerce.md`, `advertising-and-endorsements.md`. Check: refund policy, claims about results or jobs, minors' data.
- **Real estate (brokerage, proptech, co-living, construction):** `rera-real-estate.md`. Check: is a project or agent registration needed, and does the business hold buyer money?
- **Insurance (selling, comparing, embedding):** `insurance-irdai.md`. Check: is the founder selling or advising (an intermediary licence), or only showing information?

## Write it down

In `india-checks.md`, open with `Type: <primary> (+ <secondary>)`, then the type checks, then the graded filters (with `n/a for this type` where they do not apply), then scalability. If a type has no specialist seat, write one line: "No seat specialises in <type>; seat views here are outside their recorded experience."
