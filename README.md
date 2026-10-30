# SkillVault - 自建 Antigravity & Claude Code 技能雙生態知識庫

這是一個依據 **`generative_ui`** 企業級標準打造的純前端互動式 HTML 工具，專門用來**記錄、檢索、維護您在 Antigravity 與 Claude Code 中所打造的所有自製技能**，並完整關聯其**應用專案（Projects）**、**觸發時機**、**使用指引 (How to Use)** 與**底層架構 (Content & Architecture)**。

---

## 🌟 核心特色

1. **涵蓋雙生態 39 大自建與專案技能**：
   - ⚡ **Antigravity 技能 (26 項)**：
     - 全域技能 (15 項)：`audiobook-to-markdown`, `bilingual-site-sync`, `datasheet-fact-check`, `fde-ai-swe`, `garmin-connect-track`, `generative_ui`, `resume-match-analyzer`, `shared-project-memory`, `static-site-audit`, `svg-technical-figures`, `taiwanese-book-cover-studio`, `taiwanese-cultural-webapp`, `taiwanese-epub-publishing`, `taiwanese-moe-audio`, `web-speech-tts`
     - 專案技能 (11 項)：`digital-archive-ebook-ui`, `financial-report-multiformat-analyzer`, `google-translate-learning-workflow`, `lean-expert-workspace-manager`, `orid-decision-compass`, `priso-property-declarations`, `quarterly-earnings-batch-updater`, `rwd-compliance-checker`, `semiconductor-dashboard-perf`, `strait-watch-compass-dev`, `workplace-principles-workflow`
   - 🟣 **Claude Code 專案技能 (10 項)**：`emergency-card-editor`, `fintech-toolkit-dev`, `music-transcriber`, `radar-docs`, `run-dynamic-scheduler`, `run-fb-stt`, `run-taigi-tts`, `run-taigi-tug-of-war`, `ship`, `verify-stock-report`
   - 🌐 **跨平台通用技能 (3 項)**：`book-to-skill`, `column-book-publishing`, `portfolio-sync` (同時支援 Claude Code, Antigravity, Copilot CLI, Amp)
2. **完整應用專案追蹤 (50+ 個專案)**：
   - 每一項技能均標記關聯的實務專案（如 `project_claude_TG_game`, `project_claude_tggame_馬力歐`, `台中捷運四界行`, `Laigoakho_Tennjinsiu_OCR_MD`, `護國二校`, `BOOK To SKILL TRIAL`, `SW_ENGINNERING`, `PROJECT_CLAUDE_SW_FDE_AI`, `FINICIAL ANNUAL REPORT DOWNLOAD TO MD_dashboard`, `project_claude_memory_manufature_test`, `to train how you react under stress`, `Cqc-defect-map` 等 50+ 個專案）。
   - 支援依「專案名稱」一鍵篩選專案所使用的所有技能。
3. **未來一鍵更新與同步腳本 (`sync_skills.py`)**：
   - 只要在終端機執行 `python sync_skills.py`，全自動遍歷電腦中所有 `.gemini`、`.claude`、`.agents`、`.agent` 與 `skills` 技能目錄，並自動同步更新 `skills_data.json` 與 `skills_data.js` 前端介面。
4. **完整 CRUD 與持久化**：
   - 支援網頁即時新增與編輯，自動保存於 `localStorage` (v3)，並在 `sync_skills.py` 更新後自動感知最新時間戳無縫刷新。
   - 支援 JSON 匯出備份與跨電腦匯入。
5. **雙主題 (☀️/🌙) 與中英雙語系 (🌐 EN/中文)**：即時切換。

---

## 🚀 快速開啟與更新

- **直接在瀏覽器開啟工具 (本機完整私有版)**：
  👉 [**`index.html`**](file:///c:/Users/tu-hs/OneDrive/文件/2022_0308_MASA/2022-0708/Projects_antigravity/skill-record/index.html)
- **未來同步更新指令**：
  ```powershell
  python sync_skills.py
  ```

---

## 🌐 GitHub Pages 公開展示發布 (Zero-Leak Portfolio)

本專案內建**零外洩公開展示發布機制**，執行 `python sync_skills.py` 時會自動於 **`docs/`** 目錄生成公開脫敏版本：

- ✅ **徹底過濾敏感資訊**：徹底移除所有 `fullContent`（核心提示詞 Prompt）、移除所有本機路徑（`C:\Users\...`）、遮罩內部自動化腳本與機密指令。
- ✅ **保持專業技術履歷展示**：完整保留 39 項技能名稱、雙生態來源徽章、技術標籤（LangGraph、Whisper、EPUB 3 等）、分類、高層次用途描述與中英雙語/暗色主題介面。
- 🚀 **一鍵發布步驟**：
  1. 將專案 commit 並 push 到 GitHub 儲存庫。
  2. 進入 GitHub Repo 的 **Settings** ➔ **Pages**。
  3. **Build and deployment** 來源選擇 **Deploy from a branch**。
  4. 分支選擇 **`main`**，目錄選擇 **`/docs`** ➔ 點擊 **Save**。
  5. 即可擁有專屬的公開技能成果展現網站（如 `https://<your-username>.github.io/<repo>/`）！

