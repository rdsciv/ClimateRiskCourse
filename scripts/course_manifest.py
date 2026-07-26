"""Single source of truth for exercise IDs, titles, and variants."""

from __future__ import annotations

SECTIONS: list[dict] = [
    {
        "id": "00-orientation",
        "title": "Orientation",
        "week": 0,
        "question": "How do I take this course and which client am I serving?",
        "deliverable": "Environment ready; client track chosen",
        "exercises": [
            {
                "id": "00.01-how-this-course-works",
                "title": "How this course works",
                "variants": ["explainer"],
            },
            {
                "id": "00.02-install-grok-build",
                "title": "Install Grok Build",
                "variants": ["explainer", "problem"],
            },
            {
                "id": "00.03-choose-your-client-track",
                "title": "Choose your client track",
                "variants": ["explainer", "problem"],
            },
            {
                "id": "00.04-course-repo-tour",
                "title": "Course repo tour",
                "variants": ["explainer"],
            },
        ],
    },
    {
        "id": "01-the-client",
        "title": "The Client",
        "week": 1,
        "question": "What does this client need, and how will you deliver it?",
        "deliverable": "Initial Framing & Delivery Plan",
        "exercises": [
            {
                "id": "01.01-grok-build-in-a-client-workspace",
                "title": "Grok Build in a client workspace",
                "variants": ["explainer"],
            },
            {
                "id": "01.02-write-the-engagement-agents-md",
                "title": "Write the engagement AGENTS.md",
                "variants": ["problem", "solution"],
            },
            {
                "id": "01.03-connect-and-query-the-book",
                "title": "Connect and query the book",
                "variants": ["problem", "solution"],
            },
            {
                "id": "01.04-read-the-file-at-machine-speed",
                "title": "Read the file at machine speed",
                "variants": ["problem", "solution"],
            },
            {
                "id": "01.05-scope-materiality-and-guardrails",
                "title": "Scope: materiality and guardrails",
                "variants": ["explainer", "problem"],
            },
            {
                "id": "01.06-delivery-plan-the-client-would-sign",
                "title": "Delivery plan the client would sign",
                "variants": ["problem", "solution"],
            },
        ],
    },
    {
        "id": "02-portfolio-mapping",
        "title": "Portfolio Mapping",
        "week": 2,
        "question": "Given what this portfolio actually does, where does risk concentrate?",
        "deliverable": "Mapped Portfolio & Risk Hypothesis Register",
        "exercises": [
            {
                "id": "02.01-whole-book-screen",
                "title": "Whole-book screen",
                "variants": ["explainer"],
            },
            {
                "id": "02.02-batch-geocode-the-portfolio",
                "title": "Batch geocode the portfolio",
                "variants": ["problem", "solution"],
            },
            {
                "id": "02.03-classify-by-activity",
                "title": "Classify by activity",
                "variants": ["problem", "solution"],
            },
            {
                "id": "02.04-choose-resolution",
                "title": "Choose resolution",
                "variants": ["explainer", "problem"],
            },
            {
                "id": "02.05-risk-hypothesis-register",
                "title": "Risk hypothesis register",
                "variants": ["problem", "solution"],
            },
        ],
    },
    {
        "id": "03-hazard-data",
        "title": "Hazard Data",
        "week": 3,
        "question": "Which hazard data and scenarios matter for these assets?",
        "deliverable": "Organized Hazard Dataset",
        "exercises": [
            {
                "id": "03.01-climate-data-strategy",
                "title": "Climate data strategy",
                "variants": ["explainer"],
            },
            {
                "id": "03.02-pull-hazard-data",
                "title": "Pull hazard data",
                "variants": ["problem", "solution"],
            },
            {
                "id": "03.03-asset-level-exposure-scoring",
                "title": "Asset-level exposure scoring",
                "variants": ["problem", "solution"],
            },
            {
                "id": "03.04-structure-backward-from-deliverables",
                "title": "Structure backward from deliverables",
                "variants": ["explainer"],
            },
            {
                "id": "03.05-audit-log-every-pull",
                "title": "Audit log every pull",
                "variants": ["problem", "solution"],
            },
        ],
    },
    {
        "id": "04-scenario-analysis",
        "title": "Scenario Analysis",
        "week": 4,
        "question": "Which scenarios does the regulator require, and which does this portfolio need?",
        "deliverable": "Scenario Results, Standard & Bespoke",
        "exercises": [
            {
                "id": "04.01-standard-regulatory-scenarios",
                "title": "Standard regulatory scenarios",
                "variants": ["explainer", "problem"],
            },
            {
                "id": "04.02-bespoke-stress-from-hypotheses",
                "title": "Bespoke stress from hypotheses",
                "variants": ["problem", "solution"],
            },
            {
                "id": "04.03-institutional-transmission",
                "title": "Institutional transmission",
                "variants": ["explainer"],
            },
            {
                "id": "04.04-break-point-testing",
                "title": "Break-point testing",
                "variants": ["problem", "solution"],
            },
            {
                "id": "04.05-multi-agent-scenario-runs",
                "title": "Multi-agent scenario runs",
                "variants": ["problem", "solution"],
            },
            {
                "id": "04.06-read-output-for-signal",
                "title": "Read output for signal",
                "variants": ["explainer"],
            },
        ],
    },
    {
        "id": "05-portfolio-synthesis",
        "title": "Portfolio Synthesis",
        "week": 5,
        "question": "What does this mean for the portfolio as a whole, and what should change?",
        "deliverable": "Portfolio Synthesis with Pricing Implications",
        "exercises": [
            {
                "id": "05.01-aggregate-and-concentration",
                "title": "Aggregate and concentration",
                "variants": ["problem", "solution"],
            },
            {
                "id": "05.02-priority-names",
                "title": "Priority names and assets",
                "variants": ["problem", "solution"],
            },
            {
                "id": "05.03-pricing-and-capital-language",
                "title": "Pricing and capital language",
                "variants": ["problem", "solution"],
            },
            {
                "id": "05.04-document-data-gaps",
                "title": "Document data gaps",
                "variants": ["explainer", "problem"],
            },
            {
                "id": "05.05-visualize-the-book",
                "title": "Visualize the book",
                "variants": ["problem", "solution"],
            },
            {
                "id": "05.06-actionable-recommendations",
                "title": "Actionable recommendations",
                "variants": ["problem", "solution"],
            },
        ],
    },
    {
        "id": "06-delivery",
        "title": "Delivery",
        "week": 6,
        "question": "Can this stand up in front of the board and the regulator?",
        "deliverable": "Board Presentation + Regulatory Submission",
        "exercises": [
            {
                "id": "06.01-two-audiences",
                "title": "Two audiences",
                "variants": ["explainer"],
            },
            {
                "id": "06.02-templates-and-qa-agents",
                "title": "Templates and QA agents",
                "variants": ["problem", "solution"],
            },
            {
                "id": "06.03-trace-every-figure-to-source",
                "title": "Trace every figure to source",
                "variants": ["problem", "solution"],
            },
            {
                "id": "06.04-board-presentation",
                "title": "Board presentation",
                "variants": ["problem", "solution"],
            },
            {
                "id": "06.05-export-html-pdf",
                "title": "Export HTML and PDF",
                "variants": ["problem", "solution"],
            },
            {
                "id": "06.06-capstone-checklist",
                "title": "Capstone checklist",
                "variants": ["explainer"],
            },
        ],
    },
]


def all_exercise_paths() -> list[tuple[str, str, str, list[str]]]:
    """Yield (section_id, exercise_id, title, variants)."""
    out = []
    for section in SECTIONS:
        for ex in section["exercises"]:
            out.append((section["id"], ex["id"], ex["title"], ex["variants"]))
    return out
