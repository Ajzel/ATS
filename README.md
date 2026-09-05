# 🚀 ATS Resume Analyzer

**See your resume the way an ATS and an HR recruiter do — before you hit submit.**

An AI-powered Applicant Tracking System (ATS) simulator that evaluates your resume against any job description, surfaces strengths and gaps, and returns a hard match percentage with missing keywords — powered by **Google Gemini**.

---

## 🏆 Highlights

- **End-to-end multimodal AI product** — resume PDFs are analyzed visually (not just text-parsed), using Gemini's native multimodal understanding to read layout, formatting, and content the way a human reviewer would
- **Solves a real, high-stakes problem** — automated resume screening is the #1 invisible barrier between job seekers and interviews; this project reverse-engineers that gatekeeping step
- **Production-oriented, not just a notebook demo** — fully Dockerized, with a dedicated `Dockerfile`, `.dockerignore`, and environment-based secrets management, ready for cloud deployment
- **Two distinct AI reasoning modes** — a qualitative HR-style evaluation and a quantitative ATS match-percentage scorer, each with independently engineered prompts
- **Clean separation of concerns** — PDF handling, prompt engineering, and UI are modular and easy to extend
- **Built and shipped solo**, from prompt design to containerized deployment

---

## 📌 Overview

Job seekers rarely get to see *why* a resume gets filtered out before a human ever reads it. **ATS Resume Analyzer** closes that gap — it reproduces how a real ATS + recruiter pipeline evaluates a candidate, so you can fix issues **before** you apply, not after a silent rejection.

Upload a resume PDF, paste a job description, and get back either:
- A **professional HR-style evaluation** of your fit for the role, or
- A **percentage match score** with the exact keywords missing from your resume.

Under the hood, the resume PDF is rendered to an image and analyzed directly by **Gemini's multimodal model** — no fragile text-extraction or OCR pipeline required.

---

## ✨ Key Features

✔ Upload any resume in **PDF** format
✔ Paste any **job description** — no formatting required
✔ Get a professional **HR-style evaluation** (strengths & weaknesses vs. the role)
✔ Get a hard **ATS match percentage**
✔ See exactly which **keywords are missing** to improve ranking
✔ Multimodal analysis — resume is read visually, layout and formatting included
✔ Custom-styled, branded Streamlit UI with background theming
✔ **Dockerized** for one-command, portable deployment

---

## 🧠 How It Works

```
┌────────────────┐     ┌──────────────────────┐     ┌───────────────────────┐
│  Resume Upload  │ --> │  PDF → Image           │ --> │  Base64-encoded JPEG   │
│    (PDF file)   │     │  (pdf2image, page 1)   │     │  image payload          │
└────────────────┘     └──────────────────────┘     └───────────┬───────────┘
                                                                  │
        Job Description ─────────────────────────────────────────┤
                                                                  ▼
                                                  ┌────────────────────────────┐
                                                  │   Google Gemini              │
                                                  │   (gemini-2.5-flash)         │
                                                  │   Multimodal Prompt Chain    │
                                                  └───────────────┬────────────┘
                                                                  │
                                       ┌──────────────────────────┴───────────────────────┐
                                       ▼                                                    ▼
                       ┌───────────────────────────┐                     ┌───────────────────────────┐
                       │  "Tell me about my Resume"  │                     │ "Percentage Match with JD"  │
                       │  → HR-style evaluation       │                     │  → % match + missing        │
                       │  → Strengths / weaknesses    │                     │    keywords                 │
                       └───────────────────────────┘                     └───────────────────────────┘
```

**Pipeline in short:** `Resume PDF → First page as Image → Gemini multimodal prompt → HR evaluation or ATS match score`

---

## 🛠 Tech Stack

| Layer                | Technology                                      |
|-----------------------|---------------------------------------------------|
| **Frontend / UI**      | [Streamlit](https://streamlit.io/) with custom CSS theming |
| **AI Model**           | Google Gemini — `gemini-2.5-flash` (multimodal)     |
| **PDF → Image**        | `pdf2image` (backed by `poppler-utils`)             |
| **Image Handling**     | Pillow (PIL)                                       |
| **Config Management**  | `python-dotenv`                                     |
| **Containerization**   | Docker (`python:3.10-slim` base image)             |
| **Language**           | Python                                              |

---

## 📁 File Structure

```
ats-resume-analyzer/
├── .venv/                 # Local Python virtual environment (git-ignored)
├── venv/                  # Secondary/alternate local virtual environment (git-ignored)
├── .dockerignore          # Excludes .git, .env, __pycache__ from the Docker build context
├── .env                   # Local environment variables (GOOGLE_API_KEY) — git-ignored, not committed
├── .gitignore             # Excludes venv/, .env, .streamlit/, caches, uploads, and raw resume files
├── app.py                 # Main Streamlit application — UI, PDF→image pipeline, Gemini prompts
├── ats bg photo 1.png      # Background asset
├── ATS logo 1.png          # Branding asset (alternate)
├── ATS logo 2.png          # App background image (loaded via set_bg())
├── ATS logo.png            # Branding asset
├── ATS pj 2.png             # Reference/design asset
├── ATS pj 3.png             # Reference/design asset
├── ATS_resume_check.png     # Reference/design asset
├── background.png           # Background asset
├── Dockerfile              # Container build (installs poppler-utils for pdf2image, runs on port 10000)
├── requirements.txt        # Python dependencies
└── README.md                # You are here
```

> **Note:** `.venv/` and `venv/` are local environments and `.env` holds your `GOOGLE_API_KEY` — none of these should be committed; they're excluded via `.gitignore` and `.dockerignore`.

---

## 🚀 Getting Started

### Option A — Run locally

**1. Clone the repository**
```bash
git clone https://github.com/<your-username>/ats-resume-analyzer.git
cd ats-resume-analyzer
```

**2. Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

**3. Install system dependency (required for `pdf2image`)**
- **Windows:** install [poppler](http://blog.alivate.com.au/poppler-windows/) and add it to PATH
- **macOS:** `brew install poppler`
- **Linux:** `sudo apt-get install poppler-utils`

**4. Install Python dependencies**
```bash
pip install -r requirements.txt
```

**5. Configure environment variables**
Create a `.env` file in the project root:
```env
GOOGLE_API_KEY=your_google_gemini_api_key_here
```

**6. Run the app**
```bash
streamlit run app.py
```
The app opens at `http://localhost:8501`.

### Option B — Run with Docker

```bash
docker build -t ats-resume-analyzer .
docker run -p 10000:10000 --env-file .env ats-resume-analyzer
```
The app will be available at `http://localhost:10000`.

---

## 🧑‍💻 Usage

1. **Paste the job description** into the text box.
2. **Upload your resume** as a PDF.
3. Click one of:
   - **"Tell me about my Resume"** → a detailed HR-style evaluation of your fit for the role
   - **"Percentage Match with Job Description"** → a match score plus the exact keywords your resume is missing
4. Read the response and update your resume accordingly — then re-run to track improvement.

---

## 🎯 Use Cases

- 🎓 **Students & recent grads** preparing for placements and internships
- 💼 **Job seekers** optimizing resumes for specific roles before applying
- 🧑‍🏫 **Career coaches** reviewing and benchmarking candidate resumes
- 🏢 **Recruiters** getting a quick, consistent first-pass read on incoming resumes
- 📊 **Understanding ATS keyword filtering** — learning exactly what automated screeners look for

---

## 🛣️ Roadmap / Future Improvements

- [ ] Re-enable the "How can I improve my skills" evaluation mode (prompt already scaffolded in code)
- [ ] Support multi-page resumes (currently only the first page is analyzed)
- [ ] Add resume format/layout scoring (fonts, sections, ATS-parseability)
- [ ] Export evaluation results as a downloadable PDF/report
- [ ] Add support for `.docx` resumes

---

## 📄 License

This project is provided as-is for educational and personal use. Add a `LICENSE` file to formalize terms before public distribution.

---

## 🙋 Author

**Mohammed Ajzel (AJ)** — AI/ML Engineer, focused on agentic AI, RAG, and LLM-powered applications.
🌐 Portfolio: [mohammed-ajzel.lovable.app](https://mohammed-ajzel.lovable.app)

Open to internship and entry-level AI/ML, agentic AI, and data science roles — feel free to reach out via the portfolio site.
