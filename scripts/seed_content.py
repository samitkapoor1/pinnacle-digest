"""
Seed / reference content for Pinnacle Digest.

This writes the structured JSON for each daily edition into content/.
It also serves as the living documentation of the content schema that
Claude fills in each day from the Daily Accountancy Briefing.

SCHEMA (content/YYYY-MM-DD.json)
--------------------------------
{
  "date": "2026-09-02",              # ISO date, drives ordering + URLs
  "masthead": "Daily Accountancy Briefing",
  "kicker": "the",                   # small script word above the masthead
  "region": "UK & Ireland",
  "summary": "One-line editorial summary (archive card + meta description).",
  "categories": [
    {
      "name": "HMRC",
      "badge": "CRYPTO DATA LIVE",   # optional pill shown in the section header
      "stories": [
        {
          "headline": "...",
          "tags": ["£1.38bn declared gains", "..."],   # coloured pills
          "body": ["paragraph one", "paragraph two"],   # 1+ paragraphs
          "meaning": "What this means for firms ...",    # optional callout
          "source": "Accountancy Age",
          "charts": [ <chart-spec>, ... ]                # optional
        }
      ]
    }
  ]
}

CHART SPECS
-----------
stat_row     {"type":"stat_row","items":[{"value":"£1.38bn","label":"..."}, ...]}
compare_bars {"type":"compare_bars","title":"...","unit":"...",
              "bars":[{"label":"H1 2025","value":4.2,"display":"£4.2b","caption":"..."}, ...],
              "note":"..."}
bars         {"type":"bars","title":"...","unit":"deals",
              "bars":[{"label":"Q1 2025","value":111,"display":"111"}, ...]}
gauge        {"type":"gauge","title":"...","value":57,"label":"..."}   # single %
"""

import json
import os

CONTENT_DIR = os.path.join(os.path.dirname(__file__), "..", "content")


EDITION_0902 = {
    "date": "2026-09-02",
    "masthead": "Daily Accountancy Briefing",
    "kicker": "the",
    "region": "UK & Ireland",
    "summary": "HMRC's first standalone crypto-gains dataset, MTD auto-enrolment from September, an eight-fold jump in UK financial-services M&A, and a fresh QuickBooks price rise.",
    "categories": [
        {
            "name": "HMRC",
            "badge": "CRYPTO DATA LIVE",
            "stories": [
                {
                    "headline": "First standalone crypto-gains data lands; every practitioner should be paying attention",
                    "tags": ["£1.38bn declared gains", "240 filers = 52% of £1m+ gains", "CARF auto-exchange 2027"],
                    "body": [
                        "HM Revenue & Customs has published its inaugural set of statistics on taxable cryptoasset capital gains, having isolated digital assets into a standalone section of the Self Assessment return for the first time. The dataset shows £1.38bn in declared gains across 17,600 filers for 2024/25, with just 240 individuals (1.4% of filers) accounting for 52% of gains above £1m. Total disposal proceeds reached £13.8bn and enforcement activity has already generated £168m in additional CGT receipts. With the Crypto-Asset Reporting Framework (CARF) switching voluntary disclosure to automatic exchange in 2027, firms are being urged to audit client portfolios for unreported disposals, token swaps and staking income, refresh onboarding questionnaires and consider directing exposed clients to HMRC's Digital Disclosure Service before the matching engine goes live."
                    ],
                    "meaning": "Run a crypto-exposure sweep across the personal tax book this September. Directing exposed clients through the Digital Disclosure Service now is cheaper than being matched by CARF in 2027.",
                    "source": "Accountancy Age",
                    "charts": [
                        {"type": "stat_row", "items": [
                            {"value": "£1.38bn", "label": "declared crypto gains, 2024/25"},
                            {"value": "17,600", "label": "filers reporting gains"},
                            {"value": "£168m", "label": "extra CGT from enforcement"}
                        ]},
                        {"type": "gauge", "value": 52, "title": "Concentration of large gains",
                         "label": "of gains above £1m came from just 240 filers (1.4% of all filers)"}
                    ]
                },
                {
                    "headline": "Direct-recovery consultation on lower-value tax debts closes",
                    "tags": ["4.8m taxpayers, ~£4bn in scope", "£5k / £10k thresholds"],
                    "body": [
                        "HMRC's consultation on tackling lower-value tax debts closed on Friday 28 August, setting the stage for a significant expansion of the Revenue's direct-recovery-of-debt powers. The proposals would allow HMRC to instruct banks and building societies to take monthly deductions from taxpayers' accounts to recover debts of up to £5,000 for individuals and £10,000 for businesses. HMRC estimates up to 4.8m taxpayers, owing around £4bn in aggregate, could fall in scope. Practitioners should expect a policy response later this autumn and prepare debt-management protocols for exposed clients, particularly those on payment plans with historic arrears."
                    ],
                    "source": "AOL, HMRC",
                    "charts": [
                        {"type": "stat_row", "items": [
                            {"value": "4.8m", "label": "taxpayers potentially in scope"},
                            {"value": "~£4bn", "label": "aggregate debt in scope"},
                            {"value": "£5k / £10k", "label": "individual / business thresholds"}
                        ]}
                    ]
                },
                {
                    "headline": "£16bn corporate tax gap and 81,000 'nudge' letters signal a widening net",
                    "tags": ["£16bn CT gap", "81,000 crypto nudge letters"],
                    "body": [
                        "Fresh HMRC data puts unpaid corporate tax at roughly £16bn and confirms that 81,000 'nudge' letters have been sent to cryptoasset holders, alongside a broader push on offshore and gig-economy income. The scale of activity indicates that compliance capacity is being reallocated toward higher-yield, data-driven interventions. Firms with SME and owner-managed business books should expect a heavier flow of one-to-many correspondence into Q4, and consider proactive risk reviews of cross-border services, marketplaces and crypto exposures."
                    ],
                    "meaning": "Assume one-to-many correspondence volumes rise into Q4. Sweep SME books for cross-border service, marketplace and crypto exposure before the first letters land.",
                    "source": "Accountancy Age"
                }
            ]
        },
        {
            "name": "Making Tax Digital",
            "stories": [
                {
                    "headline": "HMRC begins auto-enrolling taxpayers into MTD for Income Tax from this month",
                    "tags": ["Auto-enrol from September", "Letters bypass agents"],
                    "body": [
                        "From September, HMRC will start automatically signing up taxpayers it believes should be in scope of Making Tax Digital for Income Tax Self Assessment. The initial population comprises sole traders and landlords with combined gross income above £50,000 for 2024/25, with the threshold falling to £30,000 from April 2027. Crucially, HMRC has confirmed the sign-up letters go direct to the taxpayer. Agents will not receive a copy, making proactive client outreach and 64-8 audits an immediate priority for practices."
                    ],
                    "meaning": "Run a 64-8 audit across every in-scope client this week and get ahead of the letter. Once auto-enrolment activates, clients call you first and you are working without HMRC's paper trail.",
                    "source": "ATT, HMRC"
                },
                {
                    "headline": "First quarterly update deadline lands with 51% compliance",
                    "tags": ["436k of 864k", "Soft-landing penalty holiday"],
                    "body": [
                        "The first mandatory MTD quarterly update deadline on 7 August saw 436,000 of the 864,000 taxpayers HMRC identified as in scope file on time, a compliance rate of just over 50%. HMRC has confirmed it will not levy penalty points for late quarterly updates during the 2026/27 soft-landing year, but late-filing behaviour is being logged. Firms should treat the first cycle as a diagnostic on client readiness and bookkeeping quality rather than a compliance win."
                    ],
                    "source": "HMRC, trade press",
                    "charts": [
                        {"type": "compare_bars", "title": "First MTD quarterly update, 7 August 2026",
                         "unit": "taxpayers", "bars": [
                             {"label": "In scope", "value": 864000, "display": "864k", "caption": "Identified by HMRC"},
                             {"label": "Filed on time", "value": 436000, "display": "436k", "caption": "51% compliance"}
                         ], "note": "No penalty points during the 2026/27 soft-landing year, but late-filing behaviour is being logged."}
                    ]
                },
                {
                    "headline": "Mandatory e-invoicing regime targeted for 2029",
                    "tags": ["Peppol-style network", "B2B and B2G VAT"],
                    "body": [
                        "The Government has confirmed it is working toward a mandatory e-invoicing regime from 2029, primarily covering VAT invoices for B2B and B2G transactions. HMRC has confirmed the model will rely on invoices exchanged between businesses through software providers rather than through a central government portal, a decentralised design closer to the Peppol network than to Italy's SDI. Software vendors are already positioning product roadmaps around the announcement."
                    ],
                    "source": "HMRC policy update"
                }
            ]
        },
        {
            "name": "Accountancy in Practice",
            "stories": [
                {
                    "headline": "Tech-stack fatigue: firms want to halve the number of tools they run",
                    "tags": ["8+ tools average", "57% want to halve stack"],
                    "body": [
                        "Practice-management commentary this week returned to a familiar theme: the average UK accountancy firm now runs eight or more tools to deliver core services, and 57% want to reduce that stack by half over the next three years. The trend is driving renewed interest in consolidated ledger-plus-practice platforms and in AI-native workflow tools that replace three or four point solutions at once. Vendors selling into mid-market firms should expect harder procurement conversations this budgeting cycle."
                    ],
                    "meaning": "Map current tools against workflow this quarter. Consolidation candidates surface fast; a September rationalisation plan avoids paying for duplicate licences into 2027.",
                    "source": "AccountingWEB",
                    "charts": [
                        {"type": "gauge", "value": 57, "title": "Appetite for consolidation",
                         "label": "of firms want to halve their tool stack within three years"}
                    ]
                },
                {
                    "headline": "Talent squeeze intensifies for tech-fluent accountants",
                    "tags": ["80% hiring difficulty", "Strategic advisor as baseline"],
                    "body": [
                        "80% of firms report difficulty hiring skilled professionals, with the sharpest gap in candidates who combine technical accounting with data, automation and AI literacy. The profession is increasingly framing the 'strategic advisor', capable of navigating a digital-first, complex regulatory environment, as the new baseline rather than a specialism, with knock-on effects for training pipelines, apprenticeship design and lateral hiring strategies."
                    ],
                    "source": "Accountancy Age",
                    "charts": [
                        {"type": "gauge", "value": 80, "title": "Hiring difficulty",
                         "label": "of firms report difficulty hiring tech-fluent professionals"}
                    ]
                },
                {
                    "headline": "Private equity keeps buying: accountancy consolidation runs hot",
                    "tags": ["BDO UK&I", "Xeinadin", "FS multiples up"],
                    "body": [
                        "Deal trackers continue to show strong PE interest in UK and Irish accountancy platforms, with rollups and cross-border tie-ups dominating the pipeline. The BDO UK & Ireland combination remains the sector's most-watched integration, and mid-tier firms report regular inbound approaches from sponsor-backed consolidators. Partners weighing exit or recapitalisation should re-baseline valuation expectations against the recent uptick in financial-services multiples."
                    ],
                    "source": "Accountancy Today, Inside Public Accounting"
                }
            ]
        },
        {
            "name": "Corporate Finance & M&A",
            "stories": [
                {
                    "headline": "UK financial-services M&A value up eight-fold in H1 2026",
                    "tags": ["8x on H1 2025", "Insurance / AM heavy"],
                    "body": [
                        "EY's half-year read on UK financial-services M&A shows aggregate deal value up roughly eight-fold on H1 2025, driven by a small number of large insurance and asset-management transactions and by continued PE dry-powder deployment. Advisory teams should expect a busy Q4 run-rate as processes launched over the summer come to market."
                    ],
                    "source": "EY, Consultancy.uk",
                    "charts": [
                        {"type": "compare_bars", "title": "UK financial-services M&A: H1 2025 vs H1 2026",
                         "unit": "£ billion, disclosed deal value", "bars": [
                             {"label": "H1 2025", "value": 4.2, "display": "£4.2b", "caption": "Prior-year base"},
                             {"label": "H1 2026", "value": 33.7, "display": "£33.7b", "caption": "135 deals, 2 megadeals"}
                         ], "note": "Seven deals over £1bn, including two in the £8bn to £10bn range. The top 7 accounted for 93% of value; the 'flight to quality' thesis holds."}
                    ]
                },
                {
                    "headline": "Ireland: H1 volumes hold up, aggregate value softens",
                    "tags": ["Q1: 126 deals, €1.43bn", "Prof services / insurance / healthcare"],
                    "body": [
                        "Ireland's M&A market entered a more subdued phase in H1 2026, with aggregate deal value stepping back from the elevated 2025 comparators even as deal count held steady. Q1 recorded 126 deals worth roughly €1.43bn, ahead of both Q1 2025 (111) and Q4 2025 (117). Corporate finance houses continue to flag professional services, insurance and healthcare as the most active sectors, with strong cross-border interest from UK and US buyers."
                    ],
                    "meaning": "Ireland deal count is holding, value is softer. Advisers should coach vendors to run tight processes and prepare quality-of-earnings packs early to protect certainty of close.",
                    "source": "Philip Lee, Grant Thornton Ireland",
                    "charts": [
                        {"type": "bars", "title": "Irish M&A deal count by quarter", "unit": "disclosed deals",
                         "bars": [
                             {"label": "Q1 2025", "value": 111, "display": "111"},
                             {"label": "Q4 2025", "value": 117, "display": "117"},
                             {"label": "Q1 2026", "value": 126, "display": "126"}
                         ]}
                    ]
                }
            ]
        },
        {
            "name": "Independent Financial Advisory & FCA",
            "stories": [
                {
                    "headline": "PS26/15 finalises the revised UK transaction-reporting regime",
                    "tags": ["FCA", "PS26/15 · 3 August 2026"],
                    "body": [
                        "The FCA has published PS26/15, setting out the final rules for a modernised UK transaction-reporting regime. Advisers and wealth managers with in-house dealing or reporting infrastructure should map the changes against their MiFIR reporting pipelines now, particularly around instrument-reference data and reportable-field scope. Outsourced providers are expected to reissue client change-control notes over the autumn."
                    ],
                    "source": "FCA"
                },
                {
                    "headline": "PS26/16 rewires information flows for UK equity IPOs",
                    "tags": ["FCA", "PS26/16 · 5 August 2026"],
                    "body": [
                        "PS26/16 confirms the FCA's new framework for information flows around UK equity IPOs, part of the broader push to make London a more competitive listing venue. Corporate finance advisers, brokers and IFAs advising on placings should refresh research-and-connected-analyst protocols and pre-IPO communications templates ahead of Q4 launch windows."
                    ],
                    "source": "FCA"
                },
                {
                    "headline": "AIFM reform consultation (CP26/28) puts a size-graduated regime on the table",
                    "tags": ["CP26/28", "Small <£750m / Med / Large"],
                    "body": [
                        "The FCA's consultation on a modernised UK AIFM regime moves toward a graduated framework in which managers are categorised as Small (under £750m AUM), Medium (£750m to £5bn) or Large (over £5bn), with proportionate obligations at each tier. Boutique managers and multi-family offices operating just below the £750m boundary should model both the 'stay small' and 'grow through' scenarios during business planning."
                    ],
                    "meaning": "Model the £750m boundary as a live strategic threshold in the FY27 business plan, not a regulatory footnote.",
                    "source": "FCA"
                },
                {
                    "headline": "Financial-crime review flags weaknesses in asset management",
                    "tags": ["Sanctions screening gaps", "SoW evidence", "Governance MI"],
                    "body": [
                        "The FCA published findings from its review of financial-crime frameworks across asset management and alternative investment firms, highlighting good practice alongside areas needing improvement, particularly around sanctions screening, source-of-wealth evidence and governance MI. Advisory firms with discretionary or model-portfolio propositions should benchmark against the findings and refresh AML training accordingly."
                    ],
                    "source": "FCA"
                },
                {
                    "headline": "Cryptoasset authorisation window opens 30 September",
                    "tags": ["Window opens 30 Sep 2026", "Regime live 25 Oct 2027"],
                    "body": [
                        "The FCA has confirmed the cryptoasset authorisation window opens on 30 September 2026, with the substantive regime taking effect from 25 October 2027. Firms with permitted activities that touch cryptoassets, including wealth managers using tokenised funds, should confirm perimeter position before the window opens."
                    ],
                    "source": "FCA policy timetable"
                }
            ]
        },
        {
            "name": "Ireland: Technical Watch",
            "stories": [
                {
                    "headline": "R&D tax credit rises to 35% for periods ending on or after 31 December 2026",
                    "tags": ["30% to 35%", "First-year threshold €87,500"],
                    "body": [
                        "The R&D tax credit rate steps up from 30% to 35% for accounting periods ending on or after 31 December 2026, and the first-year payment threshold rises to €87,500 from €75,000. The combined effect improves cash flow for smaller innovation-active clients and re-opens the case for reviewing which activities and staff costs are being claimed. Firms should refresh client eligibility matrices and consider running a look-back exercise for FY25 claims filed on the old rate."
                    ],
                    "meaning": "Refresh the R&D eligibility matrix and book a look-back review across FY25 claims. Even a small uplift on prior filings compounds fast at the higher rate.",
                    "source": "Budget 2026 update",
                    "charts": [
                        {"type": "compare_bars", "title": "Irish R&D tax credit rate", "unit": "% credit",
                         "bars": [
                             {"label": "Current", "value": 30, "display": "30%", "caption": "Pre-2026 periods"},
                             {"label": "From 31 Dec 2026", "value": 35, "display": "35%", "caption": "Threshold €75k to €87.5k"}
                         ], "note": "First-year payment threshold rises to €87,500 from €75,000."}
                    ]
                },
                {
                    "headline": "New crypto reporting obligations bed in alongside broader compliance load",
                    "tags": ["Crypto reporting live", "CRO · CT1 · iXBRL · RBO"],
                    "body": [
                        "Budget 2026 introduced significant new reporting requirements for cryptocurrency transactions, adding to an already dense Irish compliance calendar that includes CRO annual returns, CT1, iXBRL, VAT, PAYE, RBO beneficial-ownership updates and bank-record obligations. Practices should treat crypto in the same way as offshore accounts a decade ago: identify exposed clients now, document positions and prepare disclosure options."
                    ],
                    "source": "Outbooks Ireland"
                }
            ]
        },
        {
            "name": "Software Updates",
            "stories": [
                {
                    "headline": "QuickBooks Online lifts prices again from 1 August",
                    "tags": ["Live from 1 Aug", "$38 to $275 US tier range"],
                    "body": [
                        "QuickBooks Online implemented another price increase effective 1 August 2026, with US entry-level pricing now spanning roughly $38 to $275 per month depending on plan. UK list-price movements typically follow. Practices should refresh client-billing assumptions and, where relevant, re-negotiate wholesale and partner discount tiers before the next renewal cycle."
                    ],
                    "meaning": "Renegotiate wholesale and partner discount tiers before UK list-price movements follow, and update client engagement letters to reflect the new pass-through economics.",
                    "source": "Intuit, Insightful Accountant"
                },
                {
                    "headline": "Xero pushes AI data-capture into UK product ahead of MTD",
                    "tags": ["Xero", "£26 Growing to £37 Grow"],
                    "body": [
                        "Xero has continued rolling out AI-powered data capture and extraction to UK customers in the run-up to MTD for Income Tax, and its Xerocon event drew 45+ exhibitors in Denver in August. UK pricing has moved every year for three consecutive years, the former £26 'Growing' plan is now the £37 'Grow' plan, and product roadmaps continue to prioritise MTD ITSA readiness."
                    ],
                    "source": "Xero"
                },
                {
                    "headline": "MTD-compatible software field stays crowded but stable",
                    "tags": ["Sage", "Xero", "QuickBooks"],
                    "body": [
                        "Sage, Xero and QuickBooks remain the anchor MTD-recognised platforms for UK VAT and are each publicly committed to MTD for Income Tax support. Firms consolidating tech stacks should weigh not only feature parity but bureau-workflow depth, API access and the quality of client-facing mobile experiences, the last increasingly the deciding factor in landlord-and-sole-trader segments."
                    ],
                    "source": "TechFinitive"
                }
            ]
        }
    ]
}


EDITION_0901 = {
    "date": "2026-09-01",
    "masthead": "Daily Accountancy Briefing",
    "kicker": "the",
    "region": "UK & Ireland",
    "summary": "HMRC opens the MTD ITSA exemption window and readies September auto-enrolment, P800 errors resurface, Xeinadin extends its roll-up, and UK M&A value climbs almost eight-fold.",
    "categories": [
        {
            "name": "Making Tax Digital",
            "badge": "AUTO-ENROL FROM SEPTEMBER",
            "stories": [
                {
                    "headline": "HMRC opens MTD ITSA exemption window for £30,000 taxpayers",
                    "tags": ["April 2027 threshold", "Digitally excluded only"],
                    "body": [
                        "HMRC has opened the formal application route for exemption from Making Tax Digital for Income Tax Self Assessment for taxpayers in the £30,000 income band, with the exemption focused narrowly on the digitally excluded rather than offering broad relief. The move arrives three weeks after the first £50,000 quarterly filing deadline on 7 August 2026 and ahead of the £30,000 threshold entering mandation from 6 April 2027, giving practices a defined window to assess which clients meet the exemption tests before the next tranche is drawn in."
                    ],
                    "meaning": "Screen the £30k client cohort for exemption evidence this September. Digital exclusion, disability and remoteness are the qualifying tests, and the evidence takes time to gather.",
                    "source": "Business & Accountancy Daily"
                },
                {
                    "headline": "September auto-enrolment looms for non-signed-up MTD taxpayers",
                    "tags": ["Auto-enrol from September", "Penalty-point holiday continues"],
                    "body": [
                        "From September 2026 HMRC will begin signing up in-scope taxpayers who have not registered themselves for MTD for Income Tax, closing a loophole exposed in early filing data. Practitioners are being urged to reconcile client lists against HMRC's mandation records this week. While the 2026/27 transition year continues to waive late-submission penalty points for quarterly updates, the legal obligation to keep digital records remains in force and unaffected by the softer penalty regime."
                    ],
                    "source": "AccountingWEB, ICAEW Insights"
                },
                {
                    "headline": "Incorporation rush ahead of MTD ITSA raises quality concerns",
                    "tags": ["23% incorporated", "Remedial autumn work"],
                    "body": [
                        "Analysis published this week suggests 23% of sole traders inside the £50,000 band moved to incorporate in the run-up to the 7 August MTD ITSA deadline, choosing corporate structures over quarterly reporting. Advisers warn that the administrative saving is often illusory. Incorporations completed without a full commercial rationale are expected to generate a fresh wave of remedial work on directors' loans, dividend planning and payroll registrations through the autumn."
                    ],
                    "meaning": "Every rushed incorporation is a fresh CT, statutory accounts and payroll mandate on your desk this autumn. Price it in, staff it up, and offer offshore delivery to catch the wave.",
                    "source": "Accountancy Age",
                    "charts": [
                        {"type": "gauge", "value": 23, "title": "Incorporation rush",
                         "label": "of £50k-band sole traders incorporated ahead of the 7 August deadline"}
                    ]
                }
            ]
        },
        {
            "name": "HMRC",
            "stories": [
                {
                    "headline": "HMRC P800 calculation errors flagged again",
                    "tags": ["Multiple employments", "In-year benefit changes"],
                    "body": [
                        "AccountingWEB has re-raised long-standing concerns that HMRC's automated P800 tax calculation is producing incorrect reconciliations for a material share of PAYE taxpayers, particularly those with multiple employments or in-year benefit changes. Firms handling personal tax volumes are advised to spot-check any refund or underpayment notice received by clients in the current cycle rather than accept the HMRC figure at face value, and to keep supporting workings on file in case a formal correction is needed."
                    ],
                    "meaning": "Spot-check every P800 that lands on the personal tax desk this cycle. Multiple employments and mid-year benefit changes are the two error patterns to isolate.",
                    "source": "AccountingWEB"
                },
                {
                    "headline": "Consultation opens on 'timely payments' for income tax Self Assessment",
                    "tags": ["Timely Payments", "Autumn planning window"],
                    "body": [
                        "HMRC has launched a consultation on moving certain Self Assessment taxpayers away from the January payment cycle towards a more frequent 'timely payments' model. The paper sets out possible cohorts, cash-flow impacts and interaction with MTD quarterly updates. Practice response deadlines will land during the busy autumn planning window and firms are encouraged to prepare client-level cash-flow scenarios before submitting formal representations."
                    ],
                    "source": "AccountingWEB"
                },
                {
                    "headline": "Let-property nudge letters landing in August",
                    "tags": ["Let Property Campaign", "MTD trigger for landlords"],
                    "body": [
                        "HMRC has issued a fresh batch of letters urging recipients to disclose let-property income and reminding them that in-scope landlords now sit within MTD obligations. Advisers should treat receipt of a letter as a trigger to run a full property-income review, quantify any Let Property Campaign disclosure exposure and confirm whether the client falls into the £50,000 or the coming £30,000 MTD wave."
                    ],
                    "source": "HMRC Stakeholder communications"
                }
            ]
        },
        {
            "name": "Accountancy in Practice",
            "stories": [
                {
                    "headline": "Xeinadin extends UK roll-up with Cooper Dawn Jerrom",
                    "tags": ["Xeinadin", "Cooper Dawn Jerrom", "Alan W Simons · Campbell Crossley & Davis · PRB"],
                    "body": [
                        "Xeinadin has added Cooper Dawn Jerrom to its UK stable, continuing the group's acquisition-led expansion after recent deals for PRB Accountants, Bournemouth-based Alan W Simons & Co and Blackpool insolvency practice Campbell Crossley & Davis. The pace of consolidation reinforces the trend of private-equity-backed platforms buying up mid-tier and boutique firms across the UK and Ireland, and continues to reset benchmark multiples for partner exits and succession planning conversations."
                    ],
                    "source": "International Accounting Bulletin"
                },
                {
                    "headline": "AI restructuring lags AI ambition in accounting firms",
                    "tags": ["85% expect AI gains", "<20% have restructured pricing"],
                    "body": [
                        "New survey data shows 85% of accounting-firm leaders expect AI to improve their firm's business model, but fewer than two in ten have restructured pricing, service lines or team design to capture the value. The gap between belief and operating change is the headline risk for the next planning cycle. Without deliberate change to fee models and resourcing, productivity gains from AI-assisted work leak straight back to clients as compressed pricing."
                    ],
                    "meaning": "Redesign pricing, service lines and resourcing this quarter, not next year. AI productivity gains only stay inside the firm if the operating model catches up.",
                    "source": "AccountingWEB",
                    "charts": [
                        {"type": "compare_bars", "title": "AI ambition vs operating change", "unit": "% of firm leaders",
                         "bars": [
                             {"label": "Expect AI gains", "value": 85, "display": "85%", "caption": "Belief"},
                             {"label": "Restructured pricing", "value": 18, "display": "<20%", "caption": "Action"}
                         ], "note": "The belief-to-action gap is the headline risk for the next planning cycle."}
                    ]
                }
            ]
        },
        {
            "name": "Technical Updates",
            "stories": [
                {
                    "headline": "FRC's revised audit supervision model moves toward reliance on firm SoQM",
                    "tags": ["FRC", "Risk-based supervision", "Firm SoQM foundation"],
                    "body": [
                        "The Financial Reporting Council is progressing its updated supervisory approach for UK audit firms, placing greater weight on each firm's system of quality management (SoQM) and dialling back inspection intensity where the regulator has confidence in a firm's own controls. The July Annual Review of Audit Quality signalled persistent variation between the largest and smallest firms, especially in SoQM investment, and audit teams should treat documentation of quality management design and monitoring as a live regulatory exposure this cycle."
                    ],
                    "meaning": "SoQM documentation is now supervisory currency. Firms with credible design and monitoring evidence earn lighter inspections; those without get more.",
                    "source": "FRC, The Accountant"
                },
                {
                    "headline": "Revised UK auditing standards on fraud and going concern",
                    "tags": ["ISA (UK) 240", "ISA (UK) 570", "Corporate Governance Code"],
                    "body": [
                        "The FRC's final revisions to ISA (UK) 240 (fraud) and ISA (UK) 570 (going concern) are in the implementation window, aligning UK requirements with recent IAASB changes. Alongside these, a refresh to three reporting standards is intended to shorten auditor's reports and clarify responsibilities under the revised UK Corporate Governance Code. Firms should be updating audit methodology, working papers and reviewer checklists now, not at the year-end."
                    ],
                    "source": "FRC"
                }
            ]
        },
        {
            "name": "Software Updates",
            "stories": [
                {
                    "headline": "QuickBooks Online pricing repriced from 1 August",
                    "tags": ["Live from 1 Aug", "$38 to $275 US tier range"],
                    "body": [
                        "QuickBooks Online moved to a new pricing schedule from 1 August 2026, with entry tiers reported in the range of $38 to $275 per month. Firms with volume client bases on QBO should refresh their client-fee schedules and re-model the margin on subscriptions resold to clients, and revisit any pass-through arrangements before the next billing run."
                    ],
                    "source": "Intuit"
                },
                {
                    "headline": "Xero embeds AI data capture ahead of MTD ITSA",
                    "tags": ["Xero", "Landlord workflow validated"],
                    "body": [
                        "Xero's UK product release has bedded in AI-powered data capture and extraction, positioned explicitly around MTD for Income Tax readiness. Practices standardising on Xero for landlord and sole-trader books should validate the new capture flow end-to-end on a live quarterly update before rolling it out across client portfolios, particularly for clients where bank feeds or receipt volumes have historically been noisy."
                    ],
                    "source": "Xero"
                },
                {
                    "headline": "Sage UK & Ireland posts 10% revenue growth",
                    "tags": ["Sage", "+10% UK&I revenue"],
                    "body": [
                        "Sage's latest full-year results show 10% revenue growth in the UK and Ireland, with traction across Sage Intacct, Sage Accounting, Sage 50 and Sage 200. The message to practice is that the mid-market stack is shifting decisively toward cloud-first, AI-enabled and compliance-ready platforms. Firms still anchored in desktop deployments should build a clear migration roadmap into their FY27 plans."
                    ],
                    "source": "Sage"
                }
            ]
        },
        {
            "name": "Corporate Finance & M&A",
            "stories": [
                {
                    "headline": "UK M&A: value up eight-fold in H1, quality over quantity thesis holds",
                    "tags": ["£33.7bn FS H1", "135 deals", "Top 7 = 93% of value"],
                    "body": [
                        "Half-year data confirms a sharp rebound in UK M&A: deal volume rose roughly 25% year on year while disclosed value climbed almost eight-fold. UK financial services alone recorded 135 disclosed transactions worth £33.7bn against £4.2bn in H1 2025, with seven deals above £1bn (including two megadeals between £8bn and £10bn) accounting for around 93% of value. Commentary from the major houses characterises 2026 as a 'flight to quality' market: fewer, larger, higher-conviction deals, with financing cost and valuation gaps keeping the long tail quiet."
                    ],
                    "source": "Consultancy.uk, EY, Financier Worldwide",
                    "charts": [
                        {"type": "compare_bars", "title": "UK financial-services M&A: H1 2025 vs H1 2026",
                         "unit": "£ billion, disclosed deal value", "bars": [
                             {"label": "H1 2025", "value": 4.2, "display": "£4.2b", "caption": "Prior-year base"},
                             {"label": "H1 2026", "value": 33.7, "display": "£33.7b", "caption": "135 deals, 2 megadeals"}
                         ], "note": "Seven deals over £1bn accounted for around 93% of value. Volume up ~25% year on year."}
                    ]
                },
                {
                    "headline": "Ireland M&A outlook: professional services demand underpins deal flow",
                    "tags": ["Ireland", "PE seeking platforms"],
                    "body": [
                        "Irish market commentary continues to flag professional services, and accountancy in particular, as a standout sub-sector for M&A demand, driven by private equity seeking live platforms and bolt-ons. Xeinadin's continued Dublin-area activity is the clearest live example, and Irish partners approaching succession should be pressure-testing valuation ranges against fresh comparable deals before committing to any internal-buy-out timetable."
                    ],
                    "source": "Baker Tilly Ireland, PwC Ireland"
                }
            ]
        },
        {
            "name": "Independent Financial Advisory",
            "stories": [
                {
                    "headline": "IFA sector response to fiscal-drag squeeze on SMEs",
                    "tags": ["VAT threshold cliff-edge", "Remuneration mix review"],
                    "body": [
                        "IFA representative bodies have re-stated concerns that the freeze on income tax and NIC thresholds, alongside the unchanged VAT registration threshold, is eroding the real incomes of small business operators and their staff. For advisers with SME owner-manager books this reinforces the case for revisiting remuneration mix, pension contributions and salary-sacrifice arrangements ahead of the autumn planning window, particularly where clients are approaching the VAT registration cliff-edge."
                    ],
                    "meaning": "Book a remuneration and pension-contribution review with every SME owner-manager client this September, especially those inside the VAT threshold shadow.",
                    "source": "IFA, Adviser-Hub"
                },
                {
                    "headline": "Fee benchmarks stable: hourly £150 to £350, ongoing 0.5% to 1.0% AUA",
                    "tags": ["£150 to £350 per hour", "Consumer Duty fair value"],
                    "body": [
                        "Consumer-facing fee benchmarking for 2026 continues to cluster around £150 to £350 per hour for advice, £500 to £3,500 for one-off plans and 0.5% to 1.0% of assets under advice for ongoing service. The stability of the range against a backdrop of AI-driven productivity in back-office functions is likely to attract renewed regulator focus on fair value under Consumer Duty. Firms should ensure their price-and-value assessments are demonstrably refreshed for the current cycle."
                    ],
                    "source": "Sector fee surveys"
                }
            ]
        }
    ]
}


def main():
    os.makedirs(CONTENT_DIR, exist_ok=True)
    for edition in (EDITION_0901, EDITION_0902):
        path = os.path.join(CONTENT_DIR, edition["date"] + ".json")
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(edition, fh, ensure_ascii=False, indent=2)
        print("wrote", os.path.relpath(path))


if __name__ == "__main__":
    main()
