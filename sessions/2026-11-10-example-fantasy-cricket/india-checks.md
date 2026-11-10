# India checks (Chair)

Type: 2. Consumer app and content (+ 8. Regulated sector, money staked in option A), per idea-types.md.

## Legal zone
- **Option A: BLACK.** Users pay money to enter a contest for a money prize. That is an online money game, banned nationwide, including fantasy sports, with payments and advertising also barred [laws/online-gaming-act-2025.md]. Verify with a lawyer before you build.
- **Option B: GRAY.** Free-to-play with no money stake is the compliant route named in [laws/online-gaming-act-2025.md]. Two edges keep it GRAY, not WHITE: (1) any reward that can be converted to cash pushes it back toward a money game, so the paid ad-free pass must win nothing; (2) college students include minors and the app collects personal data, and DPDP duties on children's data and targeted ads at children apply from about May 2027 [laws/dpdp-act-2023-and-rules-2025.md]. Compliance switch: age gate at signup, no ad targeting for under-18s, no cash-equivalent prizes. Verify with a lawyer before you build.
- Ads and sponsored leagues should follow [laws/advertising-and-endorsements.md] (GRAY: endorsement disclosure).

## Type checks (consumer app)
| Check | Grade | Why |
|---|---|---|
| Delta 4 against today's habit | AT RISK | Free fantasy and prediction games already exist; B must beat them for Tier-2 students, not just copy them |
| Retention after the first month | AT RISK | Cricket is seasonal; usage spikes on match days and drops between tournaments (rule of thumb) |
| Revenue per user vs acquisition outside India 1 | AT RISK | Ad revenue per Tier-2 student is low (rule of thumb); campus ambassadors keep acquisition cheap |
| Content cost per user | PASS | Match data and scoring, no content production |

## Friction filters
1. Rs 12k employee test: n/a for this type.
2. Hard-money anchor: n/a for this type.
3. Gatekeeper: n/a for this type.
4. Collection and payment friction: A: FAIL (payments for money games are barred). B: AT RISK (ad and sponsor money; sponsors pay late).
5. Public rails and incumbent bundling: AT RISK. Large apps already offer free fantasy and prediction features with bigger audiences.

## Scalability
CAPPED. Bottleneck: revenue per user in Tier-2 (USD ad-tech and server costs against low INR ad yield) and the seasonal cricket calendar.

## Evidence level
0 (founder intuition).

## Note
No seat specialises in gaming; seat views on game design are outside their recorded experience.
