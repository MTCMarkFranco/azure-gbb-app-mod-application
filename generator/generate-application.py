"""
Job Application Repo Generator
===============================
Creates a complete GitHub job-application repository from a job description.

Usage:
    python generate-application.py

The script will prompt for:
  - Job title
  - Company name
  - Hiring manager name (optional)
  - Job description text

It then:
  1. Creates a local repo with Resume.md, index.html, README.md, workflows, and Resume.pdf
  2. Creates a GitHub repo and pushes
  3. Enables GitHub Pages on /docs

Prerequisites:
  - Python 3.10+ with fpdf2 installed  (pip install fpdf2)
  - GitHub CLI (gh) authenticated       (gh auth status)
"""

import json
import os
import re
import shutil
import subprocess
import sys
import textwrap
from pathlib import Path
from string import Template

SCRIPT_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = SCRIPT_DIR / "templates"
PROFILE_PATH = SCRIPT_DIR / "profile.json"
FONTS_DIR = Path(r"C:\Windows\Fonts")


# ──────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────
def slugify(text: str) -> str:
    """Convert text to a URL/repo-friendly slug."""
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"[\s-]+", "-", text)
    return text.strip("-")


def run(cmd: str, cwd: str | None = None, check: bool = True) -> subprocess.CompletedProcess:
    """Run a shell command and return result."""
    print(f"  > {cmd}")
    return subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True, check=check)


def load_profile() -> dict:
    with open(PROFILE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def load_template(name: str) -> str:
    path = TEMPLATES_DIR / name
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def render(template_str: str, variables: dict) -> str:
    """Safe template rendering using $$ for literal $ and ${var} for substitution."""
    t = Template(template_str)
    return t.safe_substitute(variables)


# ──────────────────────────────────────────────
# Input collection
# ──────────────────────────────────────────────
def collect_inputs() -> dict:
    print("\n╔══════════════════════════════════════════════╗")
    print("║   Job Application Repository Generator       ║")
    print("╚══════════════════════════════════════════════╝\n")

    job_title = input("Job Title (e.g. 'Azure GBB Modernization Solution Engineer'): ").strip()
    if not job_title:
        print("Error: Job title is required.")
        sys.exit(1)

    company = input("Company (e.g. 'Microsoft') [Microsoft]: ").strip() or "Microsoft"
    hiring_manager = input("Hiring Manager Name (optional, press Enter to skip): ").strip()
    
    # Derive repo name
    default_slug = slugify(job_title) + "-application"
    repo_name = input(f"Repo name [{default_slug}]: ").strip() or default_slug

    print("\nPaste the job description below (press Enter twice when done):")
    lines = []
    empty_count = 0
    while True:
        line = input()
        if line.strip() == "":
            empty_count += 1
            if empty_count >= 2:
                break
            lines.append("")
        else:
            empty_count = 0
            lines.append(line)
    job_description = "\n".join(lines).strip()

    if not job_description:
        print("Warning: No job description provided. Generating with placeholder content.")
        job_description = "<!-- TODO: Paste the full job description here -->"

    return {
        "job_title": job_title,
        "company": company,
        "hiring_manager": hiring_manager,
        "repo_name": repo_name,
        "job_description": job_description,
    }


# ──────────────────────────────────────────────
# Variable assembly
# ──────────────────────────────────────────────
def build_variables(inputs: dict, profile: dict) -> dict:
    """Build the full variable dict for template rendering."""
    github_user = profile["github_user"]
    repo_name = inputs["repo_name"]
    pages_url = f"https://{github_user.lower()}.github.io/{repo_name}/"
    repo_url = f"https://github.com/{github_user}/{repo_name}"

    addressee = inputs["hiring_manager"] or "Hiring Team"
    if inputs["hiring_manager"]:
        dear_line = f"Dear {inputs['hiring_manager']} and the Hiring Team,"
    else:
        dear_line = f"Dear {inputs['company']} Hiring Team,"

    # Build certifications markdown list
    certs_md = "\n".join(f"- {c}" for c in profile["certifications"])
    certs_html = "\n".join(f'          <li><span class="cert-icon">✅</span> {c}</li>' for c in profile["certifications"])

    # Build publications
    pubs_md = "\n".join(f"- [{p}]({profile['medium_url']})" for p in profile["publications"])
    pubs_html = "\n".join(
        f'          <li>\n            <span class="pub-icon">📝</span>\n'
        f'            <a href="{profile["medium_url"]}" target="_blank" rel="noopener">{p}</a>\n          </li>'
        for p in profile["publications"]
    )

    # Build verticals
    vertical_icons = {
        "Financial Services": "🏦", "Insurance": "🛡️", "Energy": "⚡",
        "Manufacturing": "🏭", "Government": "🏛️", "Transportation": "✈️",
        "Telecommunications": "📡", "Technology": "💻", "Non-Profit": "🤝",
    }
    verticals_html_parts = []
    for v in profile["industry_verticals"]:
        icon = "🏢"
        for key, emoji in vertical_icons.items():
            if key in v:
                icon = emoji
                break
        verticals_html_parts.append(
            f'          <span class="vertical-tag"><span class="vertical-icon">{icon}</span> {v}</span>'
        )
    verticals_html = "\n".join(verticals_html_parts)
    verticals_md = " · ".join(profile["industry_verticals"])

    return {
        # Identity
        "NAME": profile["name"],
        "NAME_UPPER": profile["name"].upper(),
        "LOCATION": profile["location"],
        "LINKEDIN_URL": profile["linkedin_url"],
        "LINKEDIN_HANDLE": profile["linkedin_handle"],
        "GITHUB_URL": profile["github_url"],
        "GITHUB_HANDLE": profile["github_handle"],
        "GITHUB_USER": github_user,
        "MEDIUM_URL": profile["medium_url"],
        "MEDIUM_HANDLE": profile["medium_handle"],
        "REPOS_COUNT": profile["github_repos_count"],
        "YEARS_MS": profile["years_at_microsoft"],
        "YEARS_INDUSTRY": profile["years_in_industry"],
        "CURRENT_ROLE": profile["current_role"],
        "CURRENT_ORG": profile["current_org"],
        "EDUCATION_SCHOOL": profile["education_school"],
        "EDUCATION_PROGRAM": profile["education_program"],
        "EDUCATION_YEARS": profile["education_years"],

        # Job-specific
        "JOB_TITLE": inputs["job_title"],
        "COMPANY": inputs["company"],
        "HIRING_MANAGER": inputs["hiring_manager"] or "Hiring Team",
        "DEAR_LINE": dear_line,
        "REPO_NAME": repo_name,
        "REPO_URL": repo_url,
        "PAGES_URL": pages_url,
        "JOB_DESCRIPTION": inputs["job_description"],
        "BADGE_URL": f"https://github.com/{github_user}/{repo_name}/actions/workflows/validate-qualifications.yml/badge.svg",
        "WORKFLOW_URL": f"https://github.com/{github_user}/{repo_name}/actions/workflows/validate-qualifications.yml",

        # Rendered blocks
        "CERTIFICATIONS_MD": certs_md,
        "CERTIFICATIONS_HTML": certs_html,
        "PUBLICATIONS_MD": pubs_md,
        "PUBLICATIONS_HTML": pubs_html,
        "VERTICALS_HTML": verticals_html,
        "VERTICALS_MD": verticals_md,
    }


# ──────────────────────────────────────────────
# PDF generation (adapted from existing script)
# ──────────────────────────────────────────────
def generate_pdf(md_path: Path, output_path: Path, variables: dict):
    """Generate a styled PDF from the Resume.md file."""
    try:
        from fpdf import FPDF
    except ImportError:
        print("  ⚠ fpdf2 not installed. Skipping PDF generation.")
        print("    Run: pip install fpdf2")
        return

    DARK_BLUE = (30, 58, 138)
    MED_BLUE = (37, 99, 235)
    LINK_BLUE = (59, 130, 246)
    HEADER_BG_START = (239, 246, 255)
    HEADER_BG_END = (219, 234, 254)
    DARK_TEXT = (17, 24, 39)
    MED_TEXT = (55, 65, 81)
    LIGHT_TEXT = (107, 114, 128)
    TABLE_HEADER_BG = (30, 58, 138)
    TABLE_HEADER_FG = (255, 255, 255)
    TABLE_ROW_BG = (248, 250, 252)
    TABLE_ALT_BG = (241, 245, 249)
    TABLE_BORDER = (203, 213, 225)
    SECTION_LINE = (59, 130, 246)
    BULLET_COLOR = (59, 130, 246)

    EMOJI_MAP = {
        "\U0001f4b0": "$", "\u2694\ufe0f": "*", "\u2694": "*",
        "\u26a1": ">", "\U0001f310": "@", "\u267b\ufe0f": "~",
        "\u267b": "~", "\ufe0f": "", "\U0001f517": "", "\U0001f4cd": "",
    }

    def strip_emojis(text):
        for e, r in EMOJI_MAP.items():
            text = text.replace(e, r)
        return re.sub(r"[\U00010000-\U0010ffff]", "", text)

    def strip_md(text):
        text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
        text = re.sub(r"\*(.+?)\*", r"\1", text)
        text = re.sub(r"\[(.+?)\]\(.+?\)", r"\1", text)
        return strip_emojis(text)

    class ResumePDF(FPDF):
        def __init__(self):
            super().__init__(format="letter")
            self.set_auto_page_break(auto=True, margin=20)
            self.add_font("SegoeUI", "", str(FONTS_DIR / "segoeui.ttf"))
            self.add_font("SegoeUI", "B", str(FONTS_DIR / "segoeuib.ttf"))
            self.add_font("SegoeUI", "I", str(FONTS_DIR / "segoeuii.ttf"))
            self.add_font("SegoeUI", "BI", str(FONTS_DIR / "segoeuiz.ttf"))
            self.add_font("SegoeUISB", "", str(FONTS_DIR / "seguisb.ttf"))
            self.add_font("SegoeUISB", "I", str(FONTS_DIR / "seguisbi.ttf"))
            self.add_font("Consolas", "", str(FONTS_DIR / "consola.ttf"))
            self.add_font("Consolas", "B", str(FONTS_DIR / "consolab.ttf"))

        def header(self): pass

        def footer(self):
            self.set_y(-15)
            self.set_font("SegoeUI", "", 8)
            self.set_text_color(*LIGHT_TEXT)
            self.cell(0, 10, f"{variables['NAME']} \u2014 Application for {variables['JOB_TITLE']}  |  Page {self.page_no()}", align="C")

        def draw_gradient(self, x, y, w, h, c1, c2, steps=50):
            sh = h / steps
            for i in range(steps):
                r = c1[0] + (c2[0] - c1[0]) * i / steps
                g = c1[1] + (c2[1] - c1[1]) * i / steps
                b = c1[2] + (c2[2] - c1[2]) * i / steps
                self.set_fill_color(int(r), int(g), int(b))
                self.rect(x, y + i * sh, w, sh + 0.5, "F")

        def section_line(self):
            self.set_draw_color(*SECTION_LINE)
            self.set_line_width(0.5)
            self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
            self.ln(4)

        def ensure_space(self, mm):
            if self.get_y() + mm > self.h - self.b_margin:
                self.add_page()

    # Parse markdown into sections
    with open(md_path, "r", encoding="utf-8") as f:
        md = f.read()

    lines = md.split("\n")
    sections = []
    i = 0
    while i < len(lines):
        s = lines[i].strip()
        if s.startswith("# ") and not s.startswith("## "):
            sections.append({"type": "h1", "text": s[2:].strip()})
        elif s.startswith("## "):
            sections.append({"type": "h2", "text": s[3:].strip()})
        elif s.startswith("### "):
            sections.append({"type": "h3", "text": s[4:].strip()})
        elif s.startswith("#### "):
            sections.append({"type": "h4", "text": s[5:].strip()})
        elif s.startswith("---"):
            sections.append({"type": "hr"})
        elif s.startswith("| ") and i + 1 < len(lines):
            tlines = [s]
            i += 1
            while i < len(lines) and lines[i].strip().startswith("|"):
                tlines.append(lines[i].strip())
                i += 1
            rows = []
            for tl in tlines:
                if re.match(r"^\|[\s\-:|]+\|$", tl):
                    continue
                rows.append([c.strip() for c in tl.split("|")[1:-1]])
            sections.append({"type": "table", "rows": rows})
            continue
        elif s.startswith("- "):
            items = [s[2:].strip()]
            i += 1
            while i < len(lines) and lines[i].strip().startswith("- "):
                items.append(lines[i].strip()[2:].strip())
                i += 1
            sections.append({"type": "bullet_list", "items": items})
            continue
        elif s.startswith("1. "):
            items = [re.sub(r"^\d+\.\s+", "", s)]
            i += 1
            while i < len(lines) and re.match(r"^\d+\.\s+", lines[i].strip()):
                items.append(re.sub(r"^\d+\.\s+", "", lines[i].strip()))
                i += 1
            sections.append({"type": "numbered_list", "items": items})
            continue
        elif s and not s.startswith("["):
            plines = [s]
            i += 1
            while i < len(lines) and lines[i].strip() and not lines[i].strip().startswith("#") and not lines[i].strip().startswith("|") and not lines[i].strip().startswith("-") and not lines[i].strip().startswith("---") and not re.match(r"^\d+\.\s+", lines[i].strip()):
                plines.append(lines[i].strip())
                i += 1
            sections.append({"type": "paragraph", "text": re.sub(r"\s{2,}", "\n", " ".join(plines))})
            continue
        i += 1

    # Build PDF
    pdf = ResumePDF()
    pdf.add_page()
    pdf.draw_gradient(0, 0, pdf.w, 100, HEADER_BG_START, HEADER_BG_END)
    pdf.set_y(18)
    pdf.set_font("SegoeUISB", "", 22)
    pdf.set_text_color(*DARK_BLUE)
    pdf.cell(0, 12, variables["NAME"], align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("SegoeUI", "", 11)
    pdf.set_text_color(*MED_BLUE)
    pdf.cell(0, 7, f"Application for {variables['JOB_TITLE']}", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)
    pdf.set_font("SegoeUI", "", 9)
    pdf.set_text_color(*MED_TEXT)
    pdf.cell(0, 5, variables["LOCATION"], align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(*LINK_BLUE)
    pdf.set_font("SegoeUI", "", 9)
    tw = pdf.get_string_width("LinkedIn  \u00b7  GitHub  \u00b7  Medium")
    pdf.set_x((pdf.w - tw) / 2)
    pdf.write(5, "LinkedIn", variables["LINKEDIN_URL"])
    pdf.write(5, "  \u00b7  ")
    pdf.write(5, "GitHub", variables["GITHUB_URL"])
    pdf.write(5, "  \u00b7  ")
    pdf.write(5, "Medium", variables["MEDIUM_URL"])
    pdf.ln(12)

    skip_h1 = True
    for sec in sections:
        st = sec["type"]
        if st == "h1" and skip_h1:
            skip_h1 = False
            continue
        if st == "h2":
            clean = re.sub(r"[^\x00-\x7F]+\s*", "", sec["text"]).strip()
            if clean == "Resume":
                pdf.add_page()
                pdf.draw_gradient(0, 0, pdf.w, 55, HEADER_BG_START, HEADER_BG_END)
                pdf.set_y(15)
                pdf.set_font("SegoeUISB", "", 24)
                pdf.set_text_color(*DARK_BLUE)
                pdf.cell(0, 12, variables["NAME_UPPER"], align="C", new_x="LMARGIN", new_y="NEXT")
                pdf.set_font("SegoeUI", "", 10)
                pdf.set_text_color(*MED_TEXT)
                pdf.cell(0, 6, variables["LOCATION"], align="C", new_x="LMARGIN", new_y="NEXT")
                pdf.set_text_color(*LINK_BLUE)
                pdf.set_font("SegoeUI", "", 9)
                pdf.write(5, variables["LINKEDIN_HANDLE"], variables["LINKEDIN_URL"])
                pdf.write(5, "  \u00b7  ")
                pdf.write(5, variables["GITHUB_HANDLE"], variables["GITHUB_URL"])
                pdf.set_text_color(*MED_TEXT)
                pdf.write(5, f"  \u00b7  {variables['REPOS_COUNT']} GitHub Repositories")
                pdf.ln(12)
                continue
            pdf.ensure_space(20)
            pdf.set_font("SegoeUISB", "", 14)
            pdf.set_text_color(*DARK_BLUE)
            pdf.cell(0, 9, clean, new_x="LMARGIN", new_y="NEXT")
            pdf.section_line()
            continue
        if st == "h1":
            clean = strip_md(sec["text"])
            if variables["NAME"].upper() in clean.upper():
                continue
            pdf.ensure_space(15)
            pdf.set_font("SegoeUISB", "", 20)
            pdf.set_text_color(*DARK_BLUE)
            pdf.cell(0, 12, clean, new_x="LMARGIN", new_y="NEXT")
            pdf.ln(2)
            continue
        if st == "h3":
            pdf.ensure_space(15)
            pdf.ln(3)
            pdf.set_font("SegoeUISB", "", 12)
            pdf.set_text_color(*DARK_BLUE)
            pdf.cell(0, 8, strip_md(sec["text"]), new_x="LMARGIN", new_y="NEXT")
            pdf.set_draw_color(*SECTION_LINE)
            pdf.set_line_width(0.3)
            pdf.line(pdf.l_margin, pdf.get_y(), pdf.l_margin + 50, pdf.get_y())
            pdf.ln(3)
            continue
        if st == "h4":
            pdf.ensure_space(12)
            pdf.ln(2)
            pdf.set_font("SegoeUISB", "", 11)
            pdf.set_text_color(*MED_TEXT)
            pdf.cell(0, 7, strip_md(sec["text"]), new_x="LMARGIN", new_y="NEXT")
            pdf.ln(1)
            continue
        if st == "hr":
            pdf.ln(2)
            pdf.section_line()
            continue
        if st == "paragraph":
            text = sec["text"]
            if not text.strip():
                continue
            pdf.ensure_space(10)
            if text.startswith(f"**{variables['NAME']}**"):
                pdf.ln(3)
                pdf.set_font("SegoeUISB", "", 11)
                pdf.set_text_color(*DARK_BLUE)
                pdf.cell(0, 6, variables["NAME"], new_x="LMARGIN", new_y="NEXT")
                continue
            clean = strip_md(text)
            clean = re.sub(r"[^\x00-\x7F]+\s*", "", clean).strip()
            pdf.set_font("SegoeUI", "", 10)
            pdf.set_text_color(*MED_TEXT)
            pdf.multi_cell(0, 5, clean)
            pdf.ln(2)
            continue
        if st == "table":
            rows = sec["rows"]
            if not rows:
                continue
            pdf.ensure_space(20)
            n = len(rows[0])
            tw = pdf.w - pdf.l_margin - pdf.r_margin
            if n == 2:
                pdf.set_font("SegoeUISB", "", 9)
                mw = max(pdf.get_string_width(strip_md(r[0])) for r in rows) + 10
                cw = [min(mw, tw * 0.35), tw - min(mw, tw * 0.35)]
            elif n == 3:
                cw = [tw * 0.22, tw * 0.48, tw * 0.30]
            else:
                cw = [tw / n] * n
            # Header
            pdf.set_fill_color(*TABLE_HEADER_BG)
            pdf.set_text_color(*TABLE_HEADER_FG)
            pdf.set_font("SegoeUISB", "", 9)
            x = pdf.l_margin
            for j, cell in enumerate(rows[0]):
                w = cw[j] if j < len(cw) else cw[-1]
                pdf.set_xy(x, pdf.get_y())
                pdf.cell(w, 8, f" {strip_md(cell)}", fill=True)
                x += w
            pdf.ln(8)
            # Rows
            for ri, row in enumerate(rows[1:], 1):
                if pdf.get_y() + 8 > pdf.h - pdf.b_margin:
                    pdf.add_page()
                bg = TABLE_ROW_BG if ri % 2 == 0 else TABLE_ALT_BG
                pdf.set_fill_color(*bg)
                pdf.set_text_color(*DARK_TEXT)
                x = pdf.l_margin
                for j, cell in enumerate(row):
                    w = cw[j] if j < len(cw) else cw[-1]
                    pdf.set_font("SegoeUISB" if "**" in cell else "SegoeUI", "", 9)
                    pdf.set_xy(x, pdf.get_y())
                    pdf.multi_cell(w, 8, f" {strip_md(cell)}", fill=True)
                    if j < len(row) - 1:
                        pdf.set_y(pdf.get_y() - 8)
                    x += w
                pdf.set_draw_color(*TABLE_BORDER)
                pdf.set_line_width(0.2)
                pdf.line(pdf.l_margin, pdf.get_y(), pdf.l_margin + tw, pdf.get_y())
            pdf.ln(4)
            continue
        if st == "bullet_list":
            for item in sec["items"]:
                pdf.ensure_space(8)
                pdf.set_x(pdf.l_margin + 4)
                pdf.set_font("SegoeUI", "", 10)
                pdf.set_text_color(*BULLET_COLOR)
                pdf.cell(6, 5, "\u2022", align="C")
                pdf.set_text_color(*MED_TEXT)
                pdf.set_font("SegoeUI", "", 9.5)
                tx = pdf.l_margin + 10
                pdf.set_x(tx)
                pdf.multi_cell(pdf.w - pdf.r_margin - tx, 5, strip_md(item))
                pdf.ln(1)
            pdf.ln(2)
            continue
        if st == "numbered_list":
            for num, item in enumerate(sec["items"], 1):
                pdf.ensure_space(8)
                pdf.set_x(pdf.l_margin + 4)
                pdf.set_font("SegoeUISB", "", 10)
                pdf.set_text_color(*DARK_BLUE)
                pdf.cell(10, 5, f"{num}.", align="R")
                tx = pdf.l_margin + 16
                pdf.set_x(tx)
                pdf.set_font("SegoeUI", "", 9.5)
                pdf.set_text_color(*MED_TEXT)
                pdf.multi_cell(pdf.w - pdf.r_margin - tx, 5, strip_md(item))
                pdf.ln(1)
            pdf.ln(2)
            continue

    pdf.ln(5)
    pdf.set_font("SegoeUI", "I", 8)
    pdf.set_text_color(*LIGHT_TEXT)
    pdf.cell(0, 5, f"Generated from {variables['REPO_URL']}", align="C")

    pdf.output(str(output_path))
    print(f"  ✅ PDF generated: {output_path.name}")


# ──────────────────────────────────────────────
# Repo generation
# ──────────────────────────────────────────────
def generate_repo(variables: dict, target_dir: Path):
    """Generate all repo files from templates."""
    print("\n📁 Generating repository files...")

    docs_dir = target_dir / "docs"
    wf_dir = target_dir / ".github" / "workflows"
    docs_dir.mkdir(parents=True, exist_ok=True)
    wf_dir.mkdir(parents=True, exist_ok=True)

    # Render templates
    templates = {
        "Resume.template.md": docs_dir / "Resume.md",
        "index.template.html": docs_dir / "index.html",
        "README.template.md": target_dir / "README.md",
        "validate-qualifications.template.yml": wf_dir / "validate-qualifications.yml",
        "deploy-pages.template.yml": wf_dir / "deploy-pages.yml",
        "gitignore.template": target_dir / ".gitignore",
    }

    for tmpl_name, output_path in templates.items():
        tmpl_path = TEMPLATES_DIR / tmpl_name
        if not tmpl_path.exists():
            print(f"  ⚠ Template missing: {tmpl_name}")
            continue
        content = load_template(tmpl_name)
        rendered = render(content, variables)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(rendered)
        print(f"  ✅ {output_path.relative_to(target_dir)}")

    # Generate PDF
    md_path = docs_dir / "Resume.md"
    pdf_path = docs_dir / "Resume.pdf"
    if md_path.exists():
        print("  📄 Generating PDF...")
        generate_pdf(md_path, pdf_path, variables)


# ──────────────────────────────────────────────
# Git & GitHub operations
# ──────────────────────────────────────────────
def setup_github(variables: dict, target_dir: Path):
    """Create GitHub repo, push, enable Pages."""
    repo_name = variables["REPO_NAME"]
    github_user = variables["GITHUB_USER"]

    print("\n🔗 Setting up GitHub repository...")

    # Check gh auth
    result = run("gh auth status", check=False)
    if result.returncode != 0:
        print("  ❌ GitHub CLI not authenticated. Run: gh auth login")
        return False

    # Detect default branch
    branch_result = run("git config --global init.defaultBranch", check=False)
    default_branch = branch_result.stdout.strip() or "master"
    print(f"  Using branch: {default_branch}")

    # Git init and commit
    run(f"git init -b {default_branch}", cwd=str(target_dir))
    run("git add -A", cwd=str(target_dir))
    run('git commit -m "Initial application repo generated by job-application-generator"', cwd=str(target_dir))

    # Create repo and push
    result = run(
        f"gh repo create {github_user}/{repo_name} --public --source . --remote origin --push",
        cwd=str(target_dir),
        check=False,
    )
    if result.returncode != 0:
        print(f"  ❌ Failed to create repo: {result.stderr}")
        print("  You can manually create and push:")
        print(f"    gh repo create {github_user}/{repo_name} --public")
        print(f"    git remote add origin https://github.com/{github_user}/{repo_name}.git")
        print(f"    git push -u origin {default_branch}")
        return False

    print(f"  ✅ Repo created: https://github.com/{github_user}/{repo_name}")

    # Enable GitHub Pages on /docs from default branch
    print("  🌐 Enabling GitHub Pages...")
    pages_payload = f'{{"source":{{"branch":"{default_branch}","path":"/docs"}}}}'
    pages_result = run(
        f'gh api repos/{github_user}/{repo_name}/pages --method POST --input - < (echo {pages_payload})',
        check=False,
    )
    # Fallback: try with gh api --field
    if pages_result.returncode != 0:
        run(
            f'gh api repos/{github_user}/{repo_name}/pages --method POST '
            f'-f "source[branch]={default_branch}" -f "source[path]=/docs"',
            check=False,
        )

    pages_url = f"https://{github_user.lower()}.github.io/{repo_name}/"
    print(f"  ✅ Pages will be live at: {pages_url}")
    print(f"     (May take 1-2 minutes to deploy)")

    return True


# ──────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────
def main():
    profile = load_profile()
    inputs = collect_inputs()
    variables = build_variables(inputs, profile)

    # Target directory (sibling to generator)
    target_dir = SCRIPT_DIR.parent.parent / variables["REPO_NAME"]
    if target_dir.exists():
        print(f"\n⚠ Directory already exists: {target_dir}")
        overwrite = input("Overwrite? (y/N): ").strip().lower()
        if overwrite != "y":
            print("Aborted.")
            sys.exit(0)
        shutil.rmtree(target_dir)

    target_dir.mkdir(parents=True, exist_ok=True)
    print(f"📂 Target: {target_dir}")

    generate_repo(variables, target_dir)

    push = input("\n🚀 Create GitHub repo and push? (Y/n): ").strip().lower()
    if push != "n":
        setup_github(variables, target_dir)

    print("\n╔══════════════════════════════════════════════╗")
    print("║   ✅ Application repo generated!              ║")
    print("╠══════════════════════════════════════════════╣")
    print(f"║  📂 {target_dir}")
    print(f"║  🔗 {variables['REPO_URL']}")
    print(f"║  🌐 {variables['PAGES_URL']}")
    print("╠══════════════════════════════════════════════╣")
    print("║  Next steps:                                 ║")
    print("║  1. Review & customize the cover letter       ║")
    print("║  2. Update validate-qualifications.yml        ║")
    print("║  3. Regenerate PDF if you edit Resume.md      ║")
    print("╚══════════════════════════════════════════════╝")


if __name__ == "__main__":
    main()
