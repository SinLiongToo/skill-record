# -*- coding: utf-8 -*-
"""
SkillVault - Auto Sync Script (Enhanced Universal Scanner)
自動掃描並同步 Antigravity、Claude Code、.agents、.gemini 的所有自建與專案技能。

使用方式:
    python sync_skills.py
"""

import os
import sys
import re
import json

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECTS_DIR = os.path.abspath(os.path.join(ROOT_DIR, ".."))
WORKSPACE_BASE = os.path.abspath(os.path.join(PROJECTS_DIR, ".."))
ANTIGRAVITY_GLOBAL_DIR = os.path.expanduser(r"~\.gemini\config\skills")

print("=" * 65)
print("🚀 SkillVault 全域與專案技能自動同步更新工具 (Universal Scanner)")
print(f"📁 根目錄: {ROOT_DIR}")
print(f"📁 專案根目錄: {WORKSPACE_BASE}")
print(f"📁 全域 Antigravity 技能: {ANTIGRAVITY_GLOBAL_DIR}")
print("=" * 65)

def parse_skill_markdown(filepath):
    """解析 SKILL.md 檔案的 YAML frontmatter、標題、觸發時機、使用指引與架構"""
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
    except Exception as e:
        print(f"  ❌ 讀取失敗 {filepath}: {e}")
        return None

    name = ""
    description = ""
    title = ""

    # Parse YAML frontmatter
    yaml_match = re.search(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    if yaml_match:
        yaml_text = yaml_match.group(1)
        name_m = re.search(r"^name:\s*([^\n\r]+)", yaml_text, re.MULTILINE)
        if name_m:
            name = name_m.group(1).strip().strip('"').strip("'")
        
        desc_m = re.search(r"^description:\s*(?:>-\s*|\"|')?(.*?)(?:\"|'|\n[a-zA-Z0-9_-]+:|$)", yaml_text, re.DOTALL | re.MULTILINE)
        if desc_m:
            description = desc_m.group(1).strip()
            description = re.sub(r"\s+", " ", description)

    if not name:
        name = os.path.basename(os.path.dirname(filepath))
        if name in [".agents", ".claude", ".gemini", "skills"]:
            name = os.path.basename(filepath).replace(".md", "").replace(".MD", "")

    # Clean name
    name = name.strip()

    # Parse Title (first # heading)
    title_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
    if title_match:
        title = title_match.group(1).strip()
    else:
        title = name.replace("-", " ").replace("_", " ").title()

    # Intro text before the first ## heading (handling CRLF safely)
    intro_match = re.search(r"^#[^\r\n]*\r?\n\s*(.*?)(?=\r?\n##|\Z)", content, re.DOTALL)
    intro_text = intro_match.group(1).strip() if intro_match else ""

    # Extract When to Use / Overview
    when_match = re.search(r"##\s*(?:[0-9]+\.\s*)?(?:When to Use|When to write|Overview|觸發時機|Philosophy|Core Architecture)[^\r\n]*\r?\n(.*?)(?=\r?\n##|\Z)", content, re.DOTALL | re.IGNORECASE)
    if when_match:
        when_to_use = when_match.group(1).strip()
    elif intro_text:
        when_to_use = intro_text
    else:
        when_to_use = description

    # Extract How to Use / Commands / Workflows
    how_match = re.search(r"##\s*(?:[0-9]+\.\s*)?(?:How to Use|Workflow|Steps|At the start of a task|How to write|Verify|Automation|Web Canvas|Typography|Core code|Sequential queue|Automated test|Quick Start|Running|Serve|Modes of Operation|使用說明|Every change|Authentication|Incremental Synchronization|Visualization & Dual-Target Deployment Pipeline)[^\r\n]*\r?\n(.*?)(?=\r?\n##\s*[0-9]*\s*(?:Principles|Rules|Files|Patterns|Why speech|Common root|Frequent traps|Architecture|Content|Checklist|Notes|Supported Projects|3\.|4\.|5\.)|\Z)", content, re.DOTALL | re.IGNORECASE)
    how_to_use = how_match.group(1).strip() if how_match else "請參照原始 SKILL.md 檔案操作。"

    # Extract Architecture / Content
    arch_match = re.search(r"##\s*(?:[0-9]+\.\s*)?(?:Principles|Rules|Files|Patterns|Why speech|Common root causes|Frequent traps|Specification Matrix|Upstream Architecture|Resilient Audio|Architecture|Core Architecture|Typography|Blueprints|Philosophy|Content|核心內容|核心優勢|Figures|Physiological|Design notes)[^\r\n]*\r?\n(.*?)(?=\r?\n##\s*[0-9]*\s*(?:Workflow|Steps|How to Use|Quick Start|Verify|At the start|Core code|使用說明|Testing|Every change|Checklist|Notes|4\.|5\.)|\Z)", content, re.DOTALL | re.IGNORECASE)
    architecture = arch_match.group(1).strip() if arch_match else "詳細內部架構請參照本技能原始碼與相關模組。"

    return {
        "name": name,
        "title": title,
        "description": description or title,
        "whenToUse": when_to_use[:1500] if len(when_to_use) > 1500 else when_to_use,
        "howToUse": how_to_use[:4000] if len(how_to_use) > 4000 else how_to_use,
        "architecture": architecture[:4000] if len(architecture) > 4000 else architecture,
        "fullContent": content
    }

def get_category(name):
    cat_map = {
        "audiobook-to-markdown": "Audio & AI",
        "fde-ai-swe": "Software & AI Systems",
        "garmin-connect-track": "Health & Endurance Analytics",
        "radar-docs": "RF & Radar Engineering",
        "generative_ui": "UI & Interactive Tools",
        "resume-match-analyzer": "Career & Analytics",
        "taiwanese-cultural-webapp": "Culture & Web Development",
        "taiwanese-epub-publishing": "Publishing & Typography",
        "run-taigi-tug-of-war": "Culture & Game",
        "run-taigi-tts": "Audio & Speech",
        "emergency-card-editor": "Safety & Reference",
        "run-dynamic-scheduler": "Productivity & Schedule",
        "fintech-toolkit-dev": "Finance & Toolkits",
        "music-transcriber": "Audio & Music AI",
        "ship": "DevOps & Release",
        "verify-stock-report": "Finance & Analytics",
        "run-fb-stt": "Audio & STT",
        "book-to-skill": "Knowledge & Agent Tools",
        "financial-report-multiformat-analyzer": "Finance & Analytics",
        "quarterly-earnings-batch-updater": "Finance & Automation",
        "semiconductor-dashboard-perf": "Semiconductor & Engineering",
        "lean-expert-workspace-manager": "Engineering & Quality",
        "orid-decision-compass": "Decision & Management",
        "strait-watch-compass-dev": "Geo & Analysis",
        "rwd-compliance-checker": "UI & Frontend Testing",
        "portfolio-sync": "Career & Analytics",
        "google-translate-learning-workflow": "Language & Learning",
        "priso-property-declarations": "Governance & Data",
        "workplace-principles-workflow": "Workplace & Principles",
        "column-book-publishing": "Publishing & Typography",
        "digital-archive-ebook-ui": "Publishing & Typography",
        "bilingual-site-sync": "Localization & Web Sync",
        "datasheet-fact-check": "Engineering & Quality",
        "shared-project-memory": "Knowledge & Agent Tools",
        "static-site-audit": "UI & Frontend Testing",
        "svg-technical-figures": "UI & Interactive Tools",
        "taiwanese-book-cover-studio": "Publishing & Typography",
        "taiwanese-moe-audio": "Audio & Speech",
        "web-speech-tts": "Audio & Speech"
    }
    return cat_map.get(name, "Specialized Skill")

def get_icon(name):
    icon_map = {
        "audiobook-to-markdown": "🎙️",
        "fde-ai-swe": "🏛️",
        "garmin-connect-track": "🏃‍♂️",
        "radar-docs": "📡",
        "generative_ui": "🎨",
        "resume-match-analyzer": "📊",
        "taiwanese-cultural-webapp": "🇹🇼",
        "taiwanese-epub-publishing": "📖",
        "run-taigi-tug-of-war": "⚔️",
        "run-taigi-tts": "🗣️",
        "emergency-card-editor": "🆘",
        "run-dynamic-scheduler": "⏱️",
        "fintech-toolkit-dev": "📈",
        "music-transcriber": "🎵",
        "ship": "🚀",
        "verify-stock-report": "📊",
        "run-fb-stt": "🎬",
        "book-to-skill": "📚",
        "financial-report-multiformat-analyzer": "💼",
        "quarterly-earnings-batch-updater": "📑",
        "semiconductor-dashboard-perf": "🔬",
        "lean-expert-workspace-manager": "📏",
        "orid-decision-compass": "🧭",
        "strait-watch-compass-dev": "🗺️",
        "rwd-compliance-checker": "📱",
        "portfolio-sync": "👤",
        "google-translate-learning-workflow": "🌐",
        "priso-property-declarations": "🏛️",
        "workplace-principles-workflow": "💼",
        "column-book-publishing": "📰",
        "digital-archive-ebook-ui": "📜",
        "bilingual-site-sync": "🌐",
        "datasheet-fact-check": "📋",
        "shared-project-memory": "🧠",
        "static-site-audit": "🧪",
        "svg-technical-figures": "📐",
        "taiwanese-book-cover-studio": "🎨",
        "taiwanese-moe-audio": "🔊",
        "web-speech-tts": "📱"
    }
    return icon_map.get(name, "⚡")

def get_tags(name):
    tags_map = {
        "audiobook-to-markdown": ["Whisper", "Streaming", "PyAV", "Markdown", "Colab GPU"],
        "fde-ai-swe": ["FDE", "LangGraph", "pgvector", "Pydantic v2", "Hybrid RAG", "Production"],
        "garmin-connect-track": ["Garmin Connect", "Endurance Analytics", "HRV", "Sleep Stages", "Chart.js", "GitHub Pages", "Sport English"],
        "radar-docs": ["77 GHz Radar", "RF Circuit", "GitHub Pages", "Knowledge Graph", "Bilingual", "Automotive Radar"],
        "generative_ui": ["Generative UI", "Tailwind CSS", "Dark/Light Mode", "Bilingual i18n", "Standalone HTML"],
        "resume-match-analyzer": ["Resume", "ATS Keywords", "Salary Benchmark", "Scoring Gauge", "STAR Method"],
        "taiwanese-cultural-webapp": ["Taiwanese Hokkien", "Tâi-lô", "Tone Sandhi", "Leaflet", "NLSC Maps"],
        "taiwanese-epub-publishing": ["EPUB 3", "Readmoo", "Kobo", "Iansui Font", "Typography"],
        "run-taigi-tug-of-war": ["Buzzer Game", "ChhoeTaigi", "Questions Bank", "Playwright", "Vocabulary"],
        "run-taigi-tts": ["Text-to-Speech", "moedict", "Audio Proxy", "Playwright", "Taiwanese"],
        "emergency-card-editor": ["98 Topics", "Offline HTML", "Wikimedia CC", "ZH/EN Bilingual", "Emergency"],
        "run-dynamic-scheduler": ["Dynamic Scheduler", "Drag & Drop", "CSV Export", "Single-file HTML"],
        "fintech-toolkit-dev": ["FinTech", "Portfolio Rebalance", "yfinance", "GitHub Pages", "Retirement"],
        "music-transcriber": ["Demucs", "Basic Pitch", "Tabs", "MusicXML", "MIDI", "Flask"],
        "ship": ["CQC Defect Map", "GitHub Pages", "Playwright", "Deploy", "Verification"],
        "verify-stock-report": ["Stock Report", "Playwright", "Server", "Finance"],
        "run-fb-stt": ["Facebook Video", "Reel", "Speech-to-Text", "Whisper"],
        "book-to-skill": ["Book to Skill", "Framework Extraction", "Claude Code", "Antigravity"],
        "financial-report-multiformat-analyzer": ["Financial Report", "SEC EDGAR", "PDF", "Dashboard", "Metrics"],
        "quarterly-earnings-batch-updater": ["Quarterly Earnings", "Batch Updater", "JSON Metrics", "Automation"],
        "semiconductor-dashboard-perf": ["Semiconductor", "Wafer Test", "STDF", "Performance", "Dashboard"],
        "lean-expert-workspace-manager": ["CPK", "Six Sigma", "Lean", "Distribution", "Simulator"],
        "orid-decision-compass": ["ORID", "Facilitation", "Decision Making", "Mindful"],
        "strait-watch-compass-dev": ["Defense", "Tracking", "Taiwan Strait", "Data Pipeline"],
        "rwd-compliance-checker": ["Responsive Web", "RWD", "Mobile", "Testing", "CSS"],
        "portfolio-sync": ["Resume", "CV", "Portfolio", "Markdown"],
        "google-translate-learning-workflow": ["Translate", "Learning", "Vocabulary", "Language"],
        "priso-property-declarations": ["Property Declarations", "Data Parsing", "Open Data"],
        "workplace-principles-workflow": ["Principles", "Workplace", "Management", "Book Publishing"],
        "column-book-publishing": ["Newspaper Column", "Book Publishing", "EPUB", "Liberty Times"],
        "digital-archive-ebook-ui": ["Docsify", "Digital Archive", "POJ Typography", "Medical Dictionary", "Dark Mode"],
        "bilingual-site-sync": ["Bilingual", "i18n", "Static Site", "Localization", "Sync", "Traditional Chinese"],
        "datasheet-fact-check": ["Datasheet", "Fact-Check", "Semiconductor", "Electronics", "Standards", "Automotive"],
        "shared-project-memory": ["Project Memory", "PROJECT_MEMORY.md", "AGENTS.md", "Claude Code", "Antigravity", "Multi-Agent"],
        "static-site-audit": ["Browser Audit", "Headless Edge", "Playwright", "Console Errors", "Overflow", "Dark/Light Mode", "GitHub Pages"],
        "svg-technical-figures": ["SVG", "Schematics", "Block Diagram", "Signal Chain", "Dark Mode", "Responsive", "Technical Figures"],
        "taiwanese-book-cover-studio": ["Book Cover", "Typography", "300 DPI", "A5 Bleed", "E-Book", "Cinnabar Seal", "Woodblock Print", "Hokkien"],
        "taiwanese-moe-audio": ["MOE Dictionary", "Taiwanese Audio", "ChhoeTaigi", "Tone Sandhi", "Audio Queue", "CDN Versioning"],
        "web-speech-tts": ["Web Speech API", "Text-to-Speech", "Mobile Audio", "LINE in-app browser", "iPhone Safari", "Android Chrome"]
    }
    return tags_map.get(name, [name])

KNOWN_PROJECT_MAP = {
    "audiobook-to-markdown": ["audiobook_md_learn", "BOOK To SKILL TRIAL", "台語audio download"],
    "fde-ai-swe": ["SW_ENGINNERING", "PROJECT_CLAUDE_SW_FDE_AI", "REQTRACKER", "PRB project review board", "decision managerment", "FMEA", "stdf v4 parser", "rf_circuit_放大器"],
    "garmin-connect-track": ["GARMIN_CONNET_TRACK", "GPX reader"],
    "radar-docs": ["project_claude_circuit", "rf_circuit_放大器"],
    "generative_ui": ["skill-record", "FINICIAL ANNUAL REPORT DOWNLOAD TO MD_dashboard", "CPK distribution simulator", "to train how you react under stress", "magic cube Rubik's Cube", "REVERSE_eng_translate_offline", "九九乘法app", "退休計算 retire", "全方面_緊急應變小卡", "Mandala grid"],
    "resume-match-analyzer": ["SW_ENGINNERING", "LIFE review indicator", "Priority score card", "PERSONAL CV"],
    "taiwanese-cultural-webapp": ["台中捷運四界行", "台北捷運四界走", "高雄捷運四界走", "台灣鐵路四界行", "景點博物館四界行", "台文教學互動app", "project_claude_tggame_馬力歐", "Taiwanese Lô-má-jī Tone Sandhi Tool", "七字仔字典", "數字文白音", "taigi_ rap"],
    "taiwanese-epub-publishing": ["工作的管見-書", "Laigoakho_Tennjinsiu_OCR_MD", "BOOK To SKILL TRIAL", "護國二校", "電子冊", "護國_HTML_EBOOK"],
    "run-taigi-tug-of-war": ["project_claude_TG_game", "project_claude_tggame_馬力歐", "台文教學互動app"],
    "run-taigi-tts": ["project_claude_TTS_SST", "CRAWL TTS", "台語audio download"],
    "emergency-card-editor": ["Project_claude_enmergency", "全方面_緊急應變小卡"],
    "run-dynamic-scheduler": ["project_claude_dynamic_schedule"],
    "fintech-toolkit-dev": ["project_claude_FINTECH", "rebalance_FINTECH"],
    "music-transcriber": ["Project_claude_musiccontent", "PROJECT_CLAUDE_SUNO_VEDIO"],
    "ship": ["PROJECT_CLAUDE_CQC_TRACKER", "Cqc-defect-map"],
    "book-to-skill": ["BOOK To SKILL TRIAL", "audiobook_md_learn"],
    "financial-report-multiformat-analyzer": ["FINICIAL ANNUAL REPORT DOWNLOAD TO MD_dashboard", "finicial anuual report"],
    "quarterly-earnings-batch-updater": ["FINICIAL ANNUAL REPORT DOWNLOAD TO MD_dashboard", "finicial anuual report"],
    "semiconductor-dashboard-perf": ["SANITY_CSV_PARSER", "project_CLAude_CSVparser", "stdf v4 parser", "project_claude_memory_manufature_test", "project_claudes_sanitycheck", "sanity check", "rf_circuit_放大器"],
    "lean-expert-workspace-manager": ["CPK distribution simulator", "LEAN TOOL", "lean_compass"],
    "orid-decision-compass": ["ORID_discuss", "decision managerment", "compass _ mindful_ decision", "to train how you react under stress"],
    "strait-watch-compass-dev": ["PRC共軍動態干擾"],
    "rwd-compliance-checker": ["lean_compass", "skill-record"],
    "portfolio-sync": ["PERSONAL CV"],
    "google-translate-learning-workflow": ["G_Translate_learning", "g_translate_organation", "REVERSE_eng_translate_offline", "englishfromgemnina"],
    "priso-property-declarations": ["官員財產申報_"],
    "workplace-principles-workflow": ["工作的管見-書"],
    "column-book-publishing": ["憂國 - 評論集", "自由時報", "2026 寫作"],
    "digital-archive-ebook-ui": ["Laigoakho_Tennjinsiu_OCR_MD", "護國二校", "護國_HTML_EBOOK"],
    "bilingual-site-sync": ["project_claude_circuit", "GARMIN_CONNET_TRACK", "自由時報"],
    "datasheet-fact-check": ["project_claude_circuit", "SANITY_CSV_PARSER", "MCU_PMIC_EV", "rf_circuit_放大器"],
    "shared-project-memory": ["SW_ENGINNERING", "project_claude_circuit", "skill-record", "GARMIN_CONNET_TRACK"],
    "static-site-audit": ["project_claude_circuit", "GARMIN_CONNET_TRACK", "PROJECT_CLAUDE_CQC_TRACKER", "skill-record"],
    "svg-technical-figures": ["project_claude_circuit", "rf_circuit_放大器", "MCU_PMIC_EV"],
    "taiwanese-book-cover-studio": ["工作的管見-書", "電子冊", "憂國 - 評論集", "護國_HTML_EBOOK", "自由時報"],
    "taiwanese-moe-audio": ["台中捷運四界行", "台北捷運四界走", "高雄捷運四界走", "台灣鐵路四界行", "景點博物館四界行", "project_claude_tggame_馬力歐"],
    "web-speech-tts": ["project_claude_circuit", "GARMIN_CONNET_TRACK", "台文教學互動app", "REVERSE_eng_translate_offline"]
}

def scan_all_skills():
    skills_by_name = {}

    # 1. 掃描 Antigravity 全域技能目錄 (~/.gemini/config/skills)
    if os.path.exists(ANTIGRAVITY_GLOBAL_DIR):
        print("\n🔍 [1/3] 正在掃描 Antigravity 全域技能目錄...")
        for item in sorted(os.listdir(ANTIGRAVITY_GLOBAL_DIR)):
            item_path = os.path.join(ANTIGRAVITY_GLOBAL_DIR, item)
            skill_md = os.path.join(item_path, "SKILL.md")
            if os.path.isdir(item_path) and os.path.exists(skill_md):
                data = parse_skill_markdown(skill_md)
                if data:
                    name = data["name"]
                    print(f"  ⚡ 發現 Antigravity 全域技能: {name}")
                    skills_by_name[name] = {
                        "id": name,
                        "name": name,
                        "title": data["title"],
                        "category": get_category(name),
                        "agent": "Antigravity",
                        "icon": get_icon(name),
                        "tags": get_tags(name),
                        "path": skill_md,
                        "description": data["description"],
                        "whenToUse": data["whenToUse"],
                        "howToUse": data["howToUse"],
                        "architecture": data["architecture"],
                        "projects": list(KNOWN_PROJECT_MAP.get(name, []))
                    }

    # 2. 掃描所有專案內的 .claude/skills, .agents/skills, .agent/skills, .gemini/skills, skills
    print("\n🔍 [2/3] 正在全域遞迴掃描各專案技能目錄 (.claude/skills, .agents/skills, .agent/skills, .gemini/skills, skills)...")
    for root, dirs, files in os.walk(WORKSPACE_BASE):
        # Skip node_modules and .git
        if "node_modules" in root or ".git" in root or "venv" in root:
            continue

        candidate_targets = []
        for folder_type in [".claude", ".agents", ".agent", ".gemini"]:
            if folder_type in dirs:
                t_dir = os.path.join(root, folder_type, "skills")
                if os.path.exists(t_dir):
                    candidate_targets.append((folder_type, t_dir))
        if "skills" in dirs and os.path.basename(root) not in [".claude", ".agents", ".agent", ".gemini", "tools", "lib"]:
            t_dir = os.path.join(root, "skills")
            if os.path.exists(t_dir):
                candidate_targets.append(("skills", t_dir))

        for folder_type, target_skills_dir in candidate_targets:
            project_name = os.path.basename(root)
            
            # Deduce agent source
            if folder_type == ".claude":
                agent_source = "Claude Code"
            elif folder_type == ".gemini":
                agent_source = "Antigravity"
            else: # .agents, .agent, skills
                agent_source = "Antigravity" if "Projects_antigravity" in root else "Cross-Agent"

            for entry in sorted(os.listdir(target_skills_dir)):
                entry_path = os.path.join(target_skills_dir, entry)
                skill_file = None
                if os.path.isfile(entry_path) and (entry_path.endswith(".md") or entry_path.endswith(".MD")):
                    skill_file = entry_path
                elif os.path.isdir(entry_path):
                    cand = os.path.join(entry_path, "SKILL.md")
                    if os.path.exists(cand):
                        skill_file = cand
                    else:
                        for sub in os.listdir(entry_path):
                            if sub.lower().endswith(".md"):
                                skill_file = os.path.join(entry_path, sub)
                                break

                if skill_file and "node_modules" not in skill_file:
                    data = parse_skill_markdown(skill_file)
                    if data:
                        name = data["name"]
                        print(f"  📦 發現專案技能: {name} (來源: {agent_source}, 專案: {project_name})")
                        
                        if name not in skills_by_name:
                            proj_list = [project_name]
                            for p in KNOWN_PROJECT_MAP.get(name, []):
                                if p not in proj_list:
                                    proj_list.append(p)

                            skills_by_name[name] = {
                                "id": f"{agent_source.lower().replace(' ', '-')}-{name}",
                                "name": name,
                                "title": data["title"],
                                "category": get_category(name),
                                "agent": agent_source,
                                "icon": get_icon(name),
                                "tags": get_tags(name),
                                "path": skill_file,
                                "description": data["description"],
                                "whenToUse": data["whenToUse"],
                                "howToUse": data["howToUse"],
                                "architecture": data["architecture"],
                                "projects": proj_list
                            }
                        else:
                            # Merge project if not present
                            if project_name not in skills_by_name[name]["projects"]:
                                skills_by_name[name]["projects"].append(project_name)
                            # If existing path is generic, prefer specific
                            skills_by_name[name]["path"] = skill_file

    # 3. 掃描通用獨立專案 (如 BOOK To SKILL TRIAL)
    cross_path = os.path.join(PROJECTS_DIR, "BOOK To SKILL TRIAL", "SKILL.md")
    if os.path.exists(cross_path) and "book-to-skill" not in skills_by_name:
        data = parse_skill_markdown(cross_path)
        if data:
            print(f"  🌐 發現 Cross-Agent 技能: {data['name']}")
            skills_by_name["book-to-skill"] = {
                "id": "book-to-skill",
                "name": "book-to-skill",
                "title": data["title"],
                "category": "Knowledge & Agent Tools",
                "agent": "Cross-Agent",
                "icon": "📚",
                "tags": ["Book-to-Skill", "Claude Code", "Antigravity", "Copilot CLI", "Framework Extraction"],
                "path": cross_path,
                "description": data["description"],
                "whenToUse": data["whenToUse"],
                "howToUse": data["howToUse"],
                "architecture": data["architecture"],
                "projects": ["BOOK To SKILL TRIAL", "audiobook_md_learn"]
            }

    # Convert to list and sort
    skill_list = list(skills_by_name.values())
    skill_list.sort(key=lambda s: (0 if s["agent"] == "Antigravity" else (1 if s["agent"] == "Claude Code" else 2), s["name"]))
    return skill_list

def generate_public_showcase(skills):
    """
    自動生成適合發布至 GitHub Pages 的隱私遮罩展示包 (docs/ 目錄)
    - 徹底移除 fullContent (零提示詞洩漏)
    - 徹底移除 本機路徑 (如 C:\\Users\\...，零本機路徑洩漏)
    - 遮罩內部指令與架構細節，僅保留公開規格與簡介
    - 生成 docs/index.html, docs/skills_data.js, docs/.nojekyll
    """
    import shutil
    from datetime import datetime

    docs_dir = os.path.join(ROOT_DIR, "docs")
    os.makedirs(docs_dir, exist_ok=True)

    # 1. 建立 .nojekyll 防止 GitHub Pages 忽略特定檔案
    nojekyll_path = os.path.join(docs_dir, ".nojekyll")
    if not os.path.exists(nojekyll_path):
        with open(nojekyll_path, "w", encoding="utf-8") as f:
            f.write("")

    # 2. 產出完全脫敏的公開資料庫 (Zero PII, Zero Secret Prompts)
    public_skills = []
    for s in skills:
        pub_item = {
            "id": s["id"],
            "name": s["name"],
            "title": s["title"],
            "category": s["category"],
            "agent": s["agent"],
            "icon": s["icon"],
            "tags": s.get("tags", []),
            "description": s.get("description", ""),
            "whenToUse": s.get("whenToUse", ""),
            "projects": s.get("projects", []),
            # 敏感資訊全面遮罩
            "path": "🔒 Protected Enterprise Repository",
            "howToUse": "🛡️【公開技術展示】：本技能之完整提示詞工程 (System Prompts)、自動化腳本與底層設定檔依法規與專利資訊安全規範保護。如需進一步技術交流或企業諮詢，歡迎聯繫合作。",
            "architecture": "🛡️【架構規範】：採用 Antigravity 與 Claude Code 雙生態 Spec-Driven 架構標準封裝，支援動態上下文管理與可重複調度之 AI 代理人工作流。"
        }
        public_skills.append(pub_item)

    # 3. 輸出 docs/skills_data.js (加上 window.PUBLIC_MODE = true)
    docs_js_path = os.path.join(docs_dir, "skills_data.js")
    pub_json_str = json.dumps(public_skills, ensure_ascii=False, indent=2).replace("</", "<\\/")
    with open(docs_js_path, "w", encoding="utf-8") as f:
        f.write("// Auto-generated Sanitized Public Showcase for GitHub Pages\n")
        f.write("// ZERO PII, ZERO internal prompts, ZERO local file paths\n")
        f.write("window.PUBLIC_MODE = true;\n")
        f.write(f"window.SKILLS_DATA = {pub_json_str};\n")
        f.write(f'window.SKILLS_SYNCED_AT = "{datetime.now().strftime("%Y-%m-%d %H:%M")}";\n')
    print(f"🌐 已生成 GitHub Pages 公開脫敏資料檔: {docs_js_path}")

    # 4. 複製 index.html 至 docs/index.html
    src_html = os.path.join(ROOT_DIR, "index.html")
    dest_html = os.path.join(docs_dir, "index.html")
    shutil.copy2(src_html, dest_html)
    print(f"📄 已同步 GitHub Pages 前端頁面: {dest_html}")

def main():
    skills = scan_all_skills()
    print("\n" + "=" * 65)
    print(f"✨ 全量掃描完成！共發現 {len(skills)} 項跨平台技能！")
    
    # Save to JSON
    json_path = os.path.join(ROOT_DIR, "skills_data.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(skills, f, ensure_ascii=False, indent=2)
    print(f"💾 已輸出資料庫: {json_path}")

    # Write external JS data file (works with file:// — no fetch / no HTML injection needed)
    js_path = os.path.join(ROOT_DIR, "skills_data.js")
    json_str = json.dumps(skills, ensure_ascii=False, indent=2).replace("</", "<\\/")
    with open(js_path, "w", encoding="utf-8") as f:
        f.write("// Auto-generated by sync_skills.py — do not edit by hand\n")
        f.write(f"window.SKILLS_DATA = {json_str};\n")
        from datetime import datetime
        f.write(f'window.SKILLS_SYNCED_AT = "{datetime.now().strftime("%Y-%m-%d %H:%M")}";\n')
    print(f"🔄 已同步更新前端資料檔: {js_path}")

    # Generate sanitized GitHub Pages bundle in docs/
    generate_public_showcase(skills)

    print("=" * 65)
    print("🎉 同步作業圓滿成功！")
    print("   👉 本機完整版：請在瀏覽器重新整理 index.html")
    print("   👉 GitHub Pages 公開脫敏版：已備妥於 docs/ 目錄（零提示詞、零本機路徑洩漏）")
    print("=" * 65)

if __name__ == "__main__":
    main()
