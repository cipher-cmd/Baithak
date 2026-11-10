# Law files: status and confidence (2026-11-05)

Every file lives in `.claude/skills/baithak/laws/`. The Chair may cite only these. Check each file's frontmatter for the authoritative `last_verified` date. Run `python .claude/skills/baithak/scripts/check_laws.py --lint` after every edit.

| File | Zone trigger | Confidence | What is still unverified |
|---|---|---|---|
| `online-gaming-act-2025.md` | BLACK | High (several sources agree) | Final rules; court challenges |
| `dpdp-act-2023-and-rules-2025.md` | GRAY | Medium | Exact phase dates differ by a day between sources |
| `payment-aggregators.md` | BLACK | Medium | 2025 Directions may not replace every earlier rule; official RBI text not opened |
| `digital-lending.md` | BLACK | Medium | The 5% DLG cap is from secondary sources; RBI index confirms a "Cap on DLG" heading but the clause text was not read |
| `deposits-and-pooled-investment.md` | BLACK | Medium-low | Deposits Act exemption list; current text of SEBI Act s.11AA; NBFC-P2P borrower and lender caps (Rs 50 lakh figure is from 2024) |
| `sebi-advice-and-finfluencers.md` | BLACK | Medium | Regulation 4 exemptions; no 2025 amendment to the 2013 Regulations found |
| `crypto-vda.md` | GRAY | Medium-low | Section number under the Income-tax Act, 2025 |
| `aadhaar-and-ekyc.md` | BLACK | Low | Storage and retention rules after the 2025 amendment; sources are vendor blogs |
| `telemedicine-and-e-pharmacy.md` | BLACK | Medium | E-pharmacy draft (2018) status; guideline issuer name |
| `it-act-and-intermediary-rules.md` | GRAY | Medium | Continuous-label requirement (April 2026 change) not confirmed |
| `upi-autopay-and-e-mandates.md` | WHITE | Medium | Sources describe a 2026 framework; the Rs 15,000 limit and exemptions need the RBI circular |
| `consumer-protection-e-commerce.md` | GRAY | Medium | Whether the 2023 Guidelines are binding in every case |
| `gst-basics-for-startups.md` | WHITE | Medium | Rs 20 lakh threshold and SAC 9983 treatment not confirmed on the GST portal |

## Rules for updating

- Verify by opening the official source (rbi.org.in, sebi.gov.in, indiacode.nic.in, CBIC, UIDAI, MeitY, CDSCO) if possible. Law-firm summaries are acceptable when the official page is not reachable. Say which one you used in the file.
- Never write a number, section, or date from memory.
- Turn any "unverified" point into a clear "Watch for" line in the law file.
- When a file is updated, change its `last_verified` date and this table.

## Known gaps to close before public launch

1. Open and read the official RBI, SEBI and CBIC texts for every BLACK file.
2. Check the Aadhaar file against the Act and the 2021 Regulations.
3. Ask an Indian lawyer to review the BLACK-zone files (also in the pre-launch checklist in `WORKPLAN.md` E3).
