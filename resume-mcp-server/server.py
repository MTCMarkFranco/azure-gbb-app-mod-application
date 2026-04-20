"""
Mark Franco - Resume MCP Server
================================
An interactive MCP server that lets hiring managers explore Mark Franco's
qualifications for the Azure GBB Modernization Solution Engineer role
using any MCP-compatible client (GitHub Copilot, Claude Desktop, etc.).

Run:  python server.py
      mcp run server.py
"""

from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    "Mark Franco - Resume",
    instructions=(
        "Interactive resume server for Mark Franco. "
        "Query experience, skills, certifications, publications, "
        "and see how 19 years at Microsoft maps to the Azure GBB "
        "Modernization Solution Engineer role."
    ),
)

# ---------------------------------------------------------------------------
# Resume data
# ---------------------------------------------------------------------------

SUMMARY = (
    "Enterprise cloud architect with 19 years at Microsoft and 32+ years in "
    "the technology industry. Principal Solution Engineer at Microsoft "
    "Innovation Hub. Led application modernization and AI transformation "
    "engagements across financial services, insurance, energy, manufacturing, "
    "government, and transportation. 127+ GitHub repositories including "
    "containerized microservices, cloud-native applications, and MCP server "
    "implementations. Azure Solutions Architect Expert certified."
)

EXPERIENCE = {
    "company": "Microsoft Corporation, Toronto",
    "title": "Principal Solution Engineer, Innovation Hub",
    "tenure": "2007-Present (19 years)",
    "highlights": [
        "Led enterprise application modernization journeys across multiple industries",
        "Architected microservices on AKS, Container Apps, and Azure Red Hat OpenShift",
        "Designed serverless solutions with Azure Functions and App Service",
        "Led legacy .NET and Java refactoring to cloud-native architectures",
        "Competitive Cloud Displacement from AWS/GCP to Azure-native architectures",
        "DevOps & CI/CD transformation with GitHub Actions and Azure DevOps",
        "AI-enriched modernization with Azure AI Foundry and Azure OpenAI",
        "Data Platform Modernization to Microsoft Fabric-based analytics",
        "Public Sector & Regulated Industry modernization solutions",
        "Featured Speaker at AI Tour Toronto",
        "Created reference architectures and solution accelerators adopted Americas-wide",
    ],
}

SKILLS = {
    "Container & Orchestration": [
        "AKS",
        "Azure Red Hat OpenShift (ARO)",
        "Azure Container Apps (ACA)",
        "Docker",
        "Helm",
    ],
    "App Platforms": [
        "Azure App Service",
        "Azure Functions",
        "Azure Static Web Apps",
    ],
    "AI/ML": [
        "Azure AI Foundry",
        "Azure OpenAI (GPT-4o)",
        "Azure AI Search",
        "Azure ML",
    ],
    "Agentic AI": [
        "Multi-agent orchestration",
        "MCP Protocol",
        "Semantic Kernel",
        "AutoGen",
        "LangChain",
        "LangGraph",
    ],
    "Cloud Architecture": [
        "Azure (AKS, Container Apps, Cosmos DB, Functions, App Service, Fabric)",
        "Bicep IaC",
        "ARM",
    ],
    "DevOps & CI/CD": [
        "GitHub Actions",
        "Azure DevOps",
        "CI/CD pipelines",
        "Infrastructure as Code",
        "GitOps",
    ],
    "Security": [
        "Entra ID",
        "MSAL",
        "Managed Identity",
        "Passkeys/WebAuthn",
        "Zero-Trust",
    ],
    "Languages": [
        "C#/.NET",
        "Python",
        "TypeScript/JavaScript",
        "PowerShell",
        "Java",
    ],
    "Frontend": [
        "React 18",
        "Blazor Server",
        "Streamlit",
        "Tailwind CSS",
    ],
}

CERTIFICATIONS = [
    "Azure Solutions Architect Expert",
    "AZ-300: Azure Architect Technologies",
    "AZ-301: Azure Architect Design",
    "MCSA Cloud Platform",
    "Exam 532: Developing Microsoft Azure Solutions",
    "Exam 534: Architecting Microsoft Azure Solutions",
    "Insight Selling",
]

EDUCATION = {
    "institution": "Sheridan College",
    "program": "Computer Systems Technician, Software Engineering",
    "years": "1994-1998",
}

PUBLICATIONS = {
    "platform": "Medium (@codecentre76)",
    "articles": [
        "Supercharge GitHub Copilot with Context7",
        "Build Production Grade AI Solutions",
        "Leave the AI; Take the Engineering",
        "Why Chat Completion Isn't Dead",
        "Why Your Python Stream Breaks Behind Microsoft's APIM",
        "Can a Machine Think the Same Way Twice?",
    ],
}

GITHUB = {
    "total_repos": "127+",
    "key_repos": [
        {
            "name": "rules-iq",
            "description": "Agentic rules engine - containerized microservice",
        },
        {
            "name": "schematic-iq",
            "description": "AI schematic extraction - cloud-native pipeline, 95-99% accuracy",
        },
        {
            "name": "architecture-review-board",
            "description": "AI-powered architecture validation - microservices architecture",
        },
        {
            "name": "agentic.search.demo",
            "description": "Agentic search on Azure Container Apps",
            "stars": 1,
        },
        {
            "name": "voice-agent",
            "description": "Multimodal AI voice agent - serverless event-driven",
        },
        {
            "name": "python-sql-Interpreter",
            "description": "Natural-language SQL interpreter",
            "stars": 2,
        },
        {
            "name": "msal-passkey-force",
            "description": "Enterprise MSAL + passkey auth - App Service hosted",
        },
    ],
}

ROLE_REQUIREMENTS = {
    "Master's/Bachelor's + 4-6 years or 7+ years technical pre-sales/consulting": {
        "years": 19,
        "evidence": (
            "19 years at Microsoft in pre-sales / technical consulting as "
            "a Principal Solution Engineer. Led customer-facing modernization "
            "engagements across financial services, insurance, energy, "
            "manufacturing, government, and transportation."
        ),
    },
    "8+ years technical pre-sales, consulting, or technology delivery": {
        "years": 19,
        "evidence": (
            "19 years of continuous technical pre-sales and consulting "
            "experience at Microsoft, delivering enterprise modernization "
            "and AI solutions across 8+ industry verticals."
        ),
    },
    "6+ years with cloud/hybrid architectures, migrations, and technology management": {
        "years": 19,
        "evidence": (
            "19 years driving Azure adoption, cloud migrations, and "
            "application modernization. Certified Azure Solutions Architect "
            "Expert. Led AKS, Container Apps, Functions, and Fabric engagements."
        ),
    },
    "Hands-on Azure platforms (AKS, ARO, ACA, App Service, Functions)": {
        "years": 19,
        "evidence": (
            "Deep hands-on expertise with AKS, Azure Container Apps, "
            "App Service, and Azure Functions. 127+ GitHub repositories "
            "demonstrate continuous hands-on technical fluency including "
            "containerized microservices and serverless architectures."
        ),
    },
    "Java and .NET development, modernization, large-scale cloud migration": {
        "years": 19,
        "evidence": (
            "C#/.NET (40%) and Java expertise. Led legacy .NET Framework "
            "and Java application refactoring to cloud-native architectures. "
            "Delivered large-scale modernization initiatives for enterprise customers."
        ),
    },
    "CI/CD pipelines (GitHub Actions, Azure DevOps)": {
        "years": 19,
        "evidence": (
            "Extensive experience with GitHub Actions and Azure DevOps. "
            "This very application repo uses GitHub Actions CI/CD. "
            "Promoted DevOps culture and CI/CD best practices for enterprise customers."
        ),
    },
    "Executive presence selling to senior technical decision-makers": {
        "years": 19,
        "evidence": (
            "19 years engaging CXO-level decision-makers at Canada's largest "
            "enterprises. Drive modernization decisions by aligning Azure "
            "platform value with business outcomes, cost savings, and "
            "strategic IT transformation goals."
        ),
    },
    "Competitive cloud displacement (Azure vs AWS/GCP)": {
        "years": 19,
        "evidence": (
            "Led strategic migrations from AWS and GCP to Azure-native "
            "architectures, creating net-new consumption revenue. Deep "
            "understanding of hyperscaler competitive landscape."
        ),
    },
}

# ---------------------------------------------------------------------------
# Helper - build a searchable corpus
# ---------------------------------------------------------------------------


def _build_corpus() -> list[dict]:
    """Return a list of {section, text} dicts for full-text search."""
    entries: list[dict] = []
    entries.append({"section": "summary", "text": SUMMARY})

    exp_text = (
        f"{EXPERIENCE['company']} - {EXPERIENCE['title']} "
        f"({EXPERIENCE['tenure']}). "
        + ". ".join(EXPERIENCE["highlights"])
    )
    entries.append({"section": "experience", "text": exp_text})

    for category, items in SKILLS.items():
        entries.append(
            {"section": f"skills/{category}", "text": f"{category}: {', '.join(items)}"}
        )

    entries.append(
        {"section": "certifications", "text": ", ".join(CERTIFICATIONS)}
    )

    entries.append(
        {
            "section": "education",
            "text": (
                f"{EDUCATION['institution']} - {EDUCATION['program']} "
                f"({EDUCATION['years']})"
            ),
        }
    )

    pub_text = (
        f"{PUBLICATIONS['platform']}: "
        + "; ".join(PUBLICATIONS["articles"])
    )
    entries.append({"section": "publications", "text": pub_text})

    for repo in GITHUB["key_repos"]:
        entries.append(
            {
                "section": f"github/{repo['name']}",
                "text": f"{repo['name']}: {repo['description']}",
            }
        )

    return entries


CORPUS = _build_corpus()

# ---------------------------------------------------------------------------
# Resources
# ---------------------------------------------------------------------------


@mcp.resource("resume://summary")
def get_summary() -> str:
    """Professional summary for Mark Franco."""
    return SUMMARY


@mcp.resource("resume://experience")
def get_experience() -> str:
    """Work experience at Microsoft."""
    lines = [
        f"## {EXPERIENCE['title']}",
        f"**{EXPERIENCE['company']}** | {EXPERIENCE['tenure']}",
        "",
    ]
    for h in EXPERIENCE["highlights"]:
        lines.append(f"- {h}")
    return "\n".join(lines)


@mcp.resource("resume://skills")
def get_skills() -> str:
    """Technical skills matrix."""
    lines = ["## Technical Skills", ""]
    for category, items in SKILLS.items():
        lines.append(f"**{category}:** {', '.join(items)}")
    return "\n".join(lines)


@mcp.resource("resume://certifications")
def get_certifications() -> str:
    """Professional certifications."""
    return "\n".join(f"- {c}" for c in CERTIFICATIONS)


@mcp.resource("resume://education")
def get_education() -> str:
    """Education background."""
    return (
        f"**{EDUCATION['institution']}**\n"
        f"{EDUCATION['program']}\n"
        f"{EDUCATION['years']}"
    )


@mcp.resource("resume://publications")
def get_publications() -> str:
    """Published articles on Medium."""
    lines = [f"## Publications - {PUBLICATIONS['platform']}", ""]
    for article in PUBLICATIONS["articles"]:
        lines.append(f'- "{article}"')
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------


@mcp.tool()
def search_qualifications(query: str) -> str:
    """Search across all resume sections for keywords.

    Args:
        query: One or more keywords to search for (case-insensitive).
    """
    query_lower = query.lower()
    matches: list[str] = []
    for entry in CORPUS:
        if query_lower in entry["text"].lower():
            matches.append(f"[{entry['section']}] {entry['text']}")
    if not matches:
        return f"No matches found for '{query}'. Try broader terms."
    return f"Found {len(matches)} match(es) for '{query}':\n\n" + "\n\n".join(matches)


@mcp.tool()
def match_job_requirements(requirement: str) -> str:
    """Match a job requirement against Mark Franco's resume evidence.

    Args:
        requirement: A specific job requirement or qualification to match.
    """
    req_lower = requirement.lower()
    results: list[str] = []

    for req, data in ROLE_REQUIREMENTS.items():
        if any(word in req.lower() for word in req_lower.split() if len(word) > 3):
            results.append(
                f"**Requirement:** {req}\n"
                f"  ✅ {data['years']} years of relevant experience\n"
                f"  Evidence: {data['evidence']}"
            )

    if not results:
        for entry in CORPUS:
            if any(
                word in entry["text"].lower()
                for word in req_lower.split()
                if len(word) > 3
            ):
                results.append(f"[{entry['section']}] {entry['text']}")

    if not results:
        return (
            f"No direct match for '{requirement}'. "
            "Try rephrasing or use search_qualifications() for broader search."
        )
    return f"## Evidence for: {requirement}\n\n" + "\n\n".join(results)


@mcp.tool()
def get_highlights() -> str:
    """Return the top 5 most impressive facts from Mark Franco's resume."""
    highlights = [
        "🏢 **19 years at Microsoft** - one of the longest-tenured "
        "Solution Engineers in the Innovation Hub, with deep enterprise "
        "relationships and CXO engagement across the Americas.",
        "🏗️ **Hands-on modernization expertise** - architected solutions "
        "on AKS, Container Apps, App Service, and Azure Functions. "
        "Led legacy .NET and Java refactoring to cloud-native architectures.",
        "⚔️ **Competitive displacement wins** - led strategic migrations "
        "from AWS and GCP to Azure-native architectures, creating "
        "net-new consumption revenue.",
        "🤖 **127+ GitHub repositories** - not just a strategist, but a "
        "hands-on builder. Key projects include containerized microservices, "
        "agentic AI systems, and cloud-native applications.",
        "🎤 **Featured Speaker at AI Tour Toronto** - recognized by "
        "Microsoft as a subject-matter expert on enterprise "
        "transformation and cloud-native architecture.",
    ]
    return "## Top 5 Highlights\n\n" + "\n\n".join(
        f"{i}. {h}" for i, h in enumerate(highlights, 1)
    )


@mcp.tool()
def why_hire_mark() -> str:
    """Return a compelling argument for hiring Mark Franco."""
    return """
## Why Hire Mark Franco for Azure GBB Modernization?

### The Short Version
Mark doesn't just *advise* on modernization - he **builds** it. With 127+ GitHub repos,
19 years of Microsoft enterprise relationships, Azure Solutions Architect Expert
certification, and a track record of creating reference architectures adopted across
the Americas, he's the rare person who can whiteboard a modernization roadmap with a
CTO at 9 AM and push the containerized proof-of-concept by 5 PM.

### The Strategic Case
| What the GBB Role Needs             | What Mark Brings                                       |
|--------------------------------------|--------------------------------------------------------|
| Azure modernization depth            | AKS, ARO, ACA, App Service, Functions - hands-on daily |
| .NET and Java expertise              | C#/.NET (40%), Java, legacy refactoring experience      |
| Competitive displacement             | Led AWS/GCP to Azure migrations at enterprise scale     |
| CXO engagement & executive presence  | 19 yrs engaging CXO-level decision-makers               |
| CI/CD & DevOps best practices        | GitHub Actions, Azure DevOps, IaC at enterprise scale   |
| Reference architectures & IPs        | Created solution accelerators adopted Americas-wide     |
| Regulated industry expertise         | Financial services, insurance, government, energy        |
| Thought leadership                   | Featured speaker, 6+ published articles on Medium       |

### The Human Case
Mark built *this MCP server* to apply for the job. That tells you three things:
1. He understands modern engineering deeply enough to build interactive tools.
2. He's resourceful - he turned a resume into a technical demonstration.
3. He genuinely wants this role, and he'll bring that energy every day.

**Mark Franco is the builder the GBB team needs.**
"""


@mcp.tool()
def compare_to_role() -> str:
    """Compare Mark Franco's qualifications against the Azure GBB Modernization role."""
    lines = [
        "## Role Fit: Azure GBB Modernization Solution Engineer",
        "",
    ]
    for req, data in ROLE_REQUIREMENTS.items():
        lines.append(f"### {req}")
        lines.append(f"  **{data['years']} years** of relevant experience")
        lines.append(f"  {data['evidence']}")
        lines.append("")
    lines.append("---")
    lines.append(
        "**Overall:** Mark exceeds every listed requirement. "
        "His 19 years at Microsoft, hands-on Azure modernization expertise, "
        "competitive displacement track record, and Americas-wide impact "
        "make him an exceptionally strong fit for the GBB Modernization role."
    )
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Prompts
# ---------------------------------------------------------------------------


@mcp.prompt()
def interview_mark() -> str:
    """A prompt template for conducting a mock interview with Mark Franco."""
    return (
        "You are a senior hiring manager at Microsoft CSA conducting a final-round "
        "interview for the Azure GBB Modernization Solution Engineer role. The candidate "
        "is Mark Franco.\n\n"
        "Use the resume MCP server tools to look up Mark's background, then "
        "ask him probing questions about:\n"
        "1. His experience architecting modernization solutions on AKS, Container Apps, and Functions\n"
        "2. How he approaches legacy .NET and Java refactoring for enterprise customers\n"
        "3. A specific competitive displacement he's led (AWS/GCP to Azure)\n"
        "4. How he engages CXO-level decision-makers on modernization strategy\n"
        "5. His approach to building reference architectures and solution accelerators\n\n"
        "After each answer, evaluate the response against what you know from "
        "the resume data and ask follow-up questions. Be thorough but fair."
    )


@mcp.prompt()
def qualification_deep_dive(area: str) -> str:
    """A prompt for exploring a specific qualification area in depth.

    Args:
        area: The qualification area to explore (e.g., 'AKS', 'Modernization', 'Competitive').
    """
    return (
        f"You are researching Mark Franco's qualifications in **{area}**.\n\n"
        "Use the resume MCP server tools to:\n"
        f"1. Search for all references to '{area}' across the resume\n"
        f"2. Identify specific projects, certifications, and experience related to {area}\n"
        "3. Compare his expertise against typical requirements for a GBB Modernization role\n"
        "4. Provide a confidence rating (1-10) on his depth in this area\n\n"
        "Be specific - cite repos, certifications, and engagement examples."
    )


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    mcp.run()
