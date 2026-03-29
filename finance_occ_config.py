"""Shared finance occupation mappings used across the paper pipeline."""

from __future__ import annotations

FINANCE_OCCS = {
    "11-3031.00": "Financial Managers",
    "11-3031.01": "Treasurers and Controllers",
    "11-3031.02": "Financial Managers, Branch or Department",
    "13-2011.00": "Accountants and Auditors",
    "13-2051.00": "Financial and Investment Analysts",
    "13-2052.00": "Personal Financial Advisors",
    "13-2061.00": "Financial Examiners",
    "13-2031.00": "Budget Analysts",
    "13-2041.00": "Credit Analysts",
    "13-2082.00": "Tax Preparers",
    "13-2099.00": "Financial Specialists, All Other",
    "13-1111.00": "Management Analysts",
    "13-2054.00": "Financial Risk Specialists",
    "43-3031.00": "Bookkeeping, Accounting, and Auditing Clerks",
}


FINANCE_OCC_DETAILS = {
    "11-3031.00": {
        "occupation": "Financial Managers",
        "bls_soc": "11-3031",
        "aioe_soc": ["11-3031"],
        "title_aliases": ["financial managers", "financial manager"],
        "notes": "BLS/AIOE broad occupation match.",
    },
    "11-3031.01": {
        "occupation": "Treasurers and Controllers",
        "bls_soc": "11-3031",
        "aioe_soc": ["11-3031"],
        "title_aliases": [
            "treasurers and controllers",
            "treasurer and controller",
            "financial managers",
        ],
        "notes": "O*NET detailed occupation nested under Financial Managers in BLS/AIOE.",
    },
    "11-3031.02": {
        "occupation": "Financial Managers, Branch or Department",
        "bls_soc": "11-3031",
        "aioe_soc": ["11-3031"],
        "title_aliases": [
            "financial managers branch or department",
            "financial managers",
        ],
        "notes": "O*NET detailed occupation nested under Financial Managers in BLS/AIOE.",
    },
    "13-2011.00": {
        "occupation": "Accountants and Auditors",
        "bls_soc": "13-2011",
        "aioe_soc": ["13-2011"],
        "title_aliases": ["accountants and auditors", "accountant", "auditor"],
        "notes": "",
    },
    "13-2051.00": {
        "occupation": "Financial and Investment Analysts",
        "bls_soc": "13-2051",
        "aioe_soc": ["13-2051"],
        "title_aliases": [
            "financial and investment analysts",
            "financial analyst",
            "investment analyst",
        ],
        "notes": "",
    },
    "13-2052.00": {
        "occupation": "Personal Financial Advisors",
        "bls_soc": "13-2052",
        "aioe_soc": ["13-2052"],
        "title_aliases": ["personal financial advisors", "personal financial advisor"],
        "notes": "",
    },
    "13-2061.00": {
        "occupation": "Financial Examiners",
        "bls_soc": "13-2061",
        "aioe_soc": ["13-2061"],
        "title_aliases": ["financial examiners", "financial examiner"],
        "notes": "",
    },
    "13-2031.00": {
        "occupation": "Budget Analysts",
        "bls_soc": "13-2031",
        "aioe_soc": ["13-2031"],
        "title_aliases": ["budget analysts", "budget analyst"],
        "notes": "",
    },
    "13-2041.00": {
        "occupation": "Credit Analysts",
        "bls_soc": "13-2041",
        "aioe_soc": ["13-2041"],
        "title_aliases": ["credit analysts", "credit analyst"],
        "notes": "",
    },
    "13-2082.00": {
        "occupation": "Tax Preparers",
        "bls_soc": "13-2082",
        "aioe_soc": ["13-2082"],
        "title_aliases": ["tax preparers", "tax preparer"],
        "notes": "",
    },
    "13-2099.00": {
        "occupation": "Financial Specialists, All Other",
        "bls_soc": "13-2099",
        "aioe_soc": ["13-2099"],
        "title_aliases": ["financial specialists all other", "financial specialists"],
        "notes": "",
    },
    "13-1111.00": {
        "occupation": "Management Analysts",
        "bls_soc": "13-1111",
        "aioe_soc": ["13-1111"],
        "title_aliases": ["management analysts", "management analyst"],
        "notes": "",
    },
    "13-2054.00": {
        "occupation": "Financial Risk Specialists",
        "bls_soc": "13-2054",
        "aioe_soc": ["13-2054"],
        "title_aliases": ["financial risk specialists", "financial risk specialist"],
        "notes": "",
    },
    "43-3031.00": {
        "occupation": "Bookkeeping, Accounting, and Auditing Clerks",
        "bls_soc": "43-3031",
        "aioe_soc": ["43-3031"],
        "title_aliases": [
            "bookkeeping accounting and auditing clerks",
            "bookkeeping clerks",
            "accounting clerks",
            "auditing clerks",
        ],
        "notes": "",
    },
}
