# Personal AI Projects

This directory contains various AI-powered tools and applications.

## 🤖 Available Projects

### 1. Cover Letter Generator
**Location:** `cover_letter_generator/`
**Description:** AI-powered tool that generates personalized cover letters by analyzing resumes and job descriptions.

**Quick Start:**
```bash
cd cover_letter_generator
python app.py
```

**Features:**
- Upload resume (PDF, DOCX, TXT)
- Paste job description
- AI-generated personalized cover letters
- Real-time progress tracking

---

### 2. AI Tutor
**Location:** `ai_tutor.py`
**Description:** Compare responses from GPT-4o-mini and Llama 3.2 for educational purposes.

**Usage:**
```bash
python ai_tutor.py
```

---

### 3. Website Summarizer
**Location:** `website_summarizer.py`
**Description:** Scrape and summarize website content using AI.

**Usage:**
```bash
python website_summarizer.py
```

---

## 🛠️ Setup

1. **Install dependencies:**
   ```bash
   pip install gradio openai python-dotenv pypdf2 python-docx requests beautifulsoup4 ollama ipython
   ```

2. **Set up environment variables:**
   Create a `.env` file in the project directory:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## 🧹 Cache Management

The projects create various cache files during operation:

### **Cache Types:**
- **`__pycache__/`**: Python bytecode cache for faster imports
- **Gradio cache**: Temporary files for file uploads and UI components
- **Log files**: Application logs and error reports

### **Cleanup Options:**

1. **Automatic cleanup script:**
   ```bash
   python cleanup.py
   ```

2. **Manual cleanup:**
   ```bash
   # Remove Python cache
   find . -name "__pycache__" -type d -exec rm -rf {} +
   find . -name "*.pyc" -type f -delete
   
   # Remove Gradio cache
   rm -rf ~/.gradio/ ~/.cache/gradio/
   ```

3. **Prevent cache in git:**
   - Added `.gitignore` to exclude cache files from version control

## 📝 Notes

- Each project has its own documentation and setup instructions
- The Cover Letter Generator is the most comprehensive project with modular architecture
- All projects use OpenAI's GPT-4o-mini for AI capabilities
- Cache files are automatically ignored by git but can be cleaned up using the cleanup script
