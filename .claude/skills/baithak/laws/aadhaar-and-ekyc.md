---
title: Aadhaar Act, 2016 (as amended 2019); Aadhaar (Authentication and Offline Verification) Regulations, 2021; Aadhaar Authentication rules (2025 amendment)
regulator: UIDAI
status: in force (with the Supreme Court's 2018 ruling striking down Section 57, which had allowed private use)
zone_trigger: BLACK
last_verified: 2026-11-05
sources:
  - https://www.uidai.gov.in/images/AUA-KUA_Agreements_Versions_60.pdf
  - https://thc.nic.in/Central%20Governmental%20Regulations/Aadhaar%20(Authentication%20and%20Offline%20Verification)%20Regulation,2021.pdf
  - https://didit.me/blog/aadhaar-ekyc/
  - https://www.gktoday.in/aadhaar-and-e-kyc-various-issues/
---

## What it says
Only entities licensed by UIDAI can run Aadhaar authentication or eKYC. These are called AUAs (authentication user agencies) and KUAs (KYC user agencies). Sub-KUAs use a KUA's eKYC service. The Supreme Court struck down Section 57 in 2018, which had let private companies use Aadhaar freely. Private use now runs through an approved route. Offline verification (Section 8A) lets an entity verify without storing the Aadhaar number. Section 8A(4) bars an entity seeking offline verification from requiring a holder to accept authentication or from storing the Aadhaar number. A 2025 change to the authentication rules lets the central government approve some private uses through a portal. Sources on storage and retention were not confirmed from primary text.

## What it means for a founder
- BLACK if: the startup stores raw Aadhaar numbers, or runs its own Aadhaar authentication or eKYC without a UIDAI licence or an approved route; or screen-scrapes an Aadhaar or bank login.
- GRAY if: the product uses offline verification (paper or XML) or a digital ID wallet such as DigiLocker, and does not keep the Aadhaar number. Get a lawyer's view on retention.
- Compliant route: use a licensed KUA or AUA as a sub-KUA, or DigiLocker, or offline verification. Do not store the Aadhaar number unless the route allows it.

## Watch for
- The exact storage and retention rules after the 2025 authentication amendment. This check found no primary text.
- Much of the source material is vendor marketing (Didit). Verify against the Act, the 2021 Regulations and UIDAI circulars before any build decision.
- Overlap with DPDP obligations in `dpdp-act-2023-and-rules-2025.md`.
