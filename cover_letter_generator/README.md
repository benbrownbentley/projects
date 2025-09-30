# AI Cover Letter Generator

A powerful AI-powered tool that generates personalized cover letters by analyzing your resume and job descriptions using OpenAI's GPT-4o-mini.

## 🚀 Features

- **Smart Resume Parsing**: Supports PDF, DOCX, and text files
- **Job Description Analysis**: Extracts key requirements and company culture
- **AI-Powered Generation**: Creates personalized cover letters using advanced AI agents
- **Progress Tracking**: Real-time status updates during generation
- **Professional Formatting**: Outputs in markdown with proper structure

## 📁 Project Structure

```
cover_letter_generator/
├── app.py                      # Main Gradio application (193 lines)
├── config.py                   # Configuration and constants (95 lines)
├── resume_parser.py            # Resume parsing logic (95 lines)
├── job_analyzer.py             # Job description analysis (55 lines)
├── cover_letter_generator.py   # Main AI agent (234 lines)
├── .env                        # Environment variables (API keys)
└── README.md                   # This file
```

## 🛠️ Installation

1. **Install dependencies:**
   ```bash
   pip install gradio openai python-dotenv pypdf2 python-docx
   ```

2. **Set up environment variables:**
   Create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## 🚀 Usage

1. **Navigate to the project directory:**
   ```bash
   cd cover_letter_generator
   ```

2. **Run the application:**
   ```bash
   python app.py
   ```

3. **Open your browser** to `http://127.0.0.1:7860`

4. **Upload your resume** (PDF, DOCX, or text file)

5. **Paste a job description** in the text area

6. **Click "Generate Cover Letter"** and watch the progress!

## 📋 Module Overview

### `config.py`
- Centralized configuration and constants
- Environment variable management
- AI prompts and templates
- Fallback data structures

### `resume_parser.py`
- PDF, DOCX, and text file parsing
- AI-powered resume analysis
- Structured data extraction
- Error handling and fallbacks

### `job_analyzer.py`
- Job description parsing
- Requirement extraction
- Company culture analysis
- JSON-structured output

### `cover_letter_generator.py`
- Main AI agent orchestration
- Tool integration for enhanced analysis
- Cover letter generation logic
- Metadata and formatting

### `app.py`
- Gradio UI interface
- Progress tracking
- Event handling
- Error management

## 🔧 Key Improvements

1. **Modular Design**: Each module has a single responsibility
2. **Better Error Handling**: Comprehensive error handling with fallbacks
3. **Progress Indicators**: Real-time status updates for users
4. **Cleaner Code**: Reduced from 615 lines to ~600 lines across 5 focused modules
5. **Maintainability**: Easy to modify individual components
6. **Reusability**: Modules can be used independently

## 🎯 Benefits of Refactoring

- **Readability**: Each file is focused and easy to understand
- **Maintainability**: Changes to one module don't affect others
- **Testing**: Individual modules can be tested separately
- **Scalability**: Easy to add new features or modify existing ones
- **Collaboration**: Multiple developers can work on different modules

## 🔍 Example Usage

The application includes example job descriptions for testing:
- Software Engineer position
- Marketing Manager role

Simply expand the "Example Job Descriptions" accordion and copy the text to test the system!