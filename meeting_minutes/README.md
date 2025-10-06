# Meeting Minutes Generator

An AI-powered application that automatically generates meeting minutes from MP3 recordings using OpenAI's Whisper and GPT models.

## 🚀 Features

- **🎙️ Audio Transcription**: Convert MP3 recordings to text using OpenAI Whisper
- **📝 Smart Summarization**: AI-powered meeting summary generation
- **✅ Action Item Extraction**: Automatically identify tasks and next steps
- **👥 Participant Recognition**: Identify and track meeting participants
- **📋 Professional Formatting**: Generate properly formatted meeting minutes
- **🌐 Web Interface**: Easy-to-use Gradio web interface

## 📁 Project Structure

```
meeting_minutes/
├── app.py                 # Main Gradio application
├── audio_processor.py     # Audio file processing and transcription
├── meeting_analyzer.py    # AI-powered meeting analysis
├── config.py             # Configuration and settings
├── requirements.txt       # Python dependencies
├── .env                  # Environment variables (API keys)
└── README.md             # This file
```

## 🛠️ Installation

1. **Clone or download the project**
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   Create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## 🚀 Usage

1. **Run the application:**
   ```bash
   python app.py
   ```

2. **Open your browser** to `http://127.0.0.1:7860`

3. **Upload an MP3 file** of your meeting recording

4. **Optionally provide:**
   - Meeting title
   - List of participants

5. **Click "Generate Meeting Minutes"** and wait for processing

6. **Review the generated:**
   - Meeting summary
   - Action items and next steps

## 📋 Supported Formats

- **Audio Files**: MP3 only
- **File Size**: Maximum 50MB
- **Meeting Length**: Any length (processing time varies)

## 🔧 Configuration

Key settings in `config.py`:
- `MAX_FILE_SIZE_MB`: Maximum file size (default: 50MB)
- `DEFAULT_MODEL`: OpenAI model for analysis (default: gpt-4o-mini)
- `WHISPER_MODEL`: Whisper model for transcription (default: whisper-1)

## 🌐 Web Deployment

The application is configured for web access:

- **Local Network**: Access from other devices on your network
- **Public Access**: Gradio generates a temporary public URL
- **Custom Deployment**: Deploy to cloud platforms like Hugging Face Spaces

## 💡 Tips for Best Results

- **Clear Audio**: Use recordings with minimal background noise
- **Speaker Clarity**: Ensure speakers are clearly audible
- **Context**: Provide meeting title and participants for better analysis
- **File Size**: Keep files under 50MB for optimal processing

## 🔒 Security

- API keys are stored securely in environment variables
- No sensitive data is logged or stored permanently
- Audio files are processed temporarily and not saved

## 🛠️ Troubleshooting

**Common Issues:**

1. **"API key not found"**
   - Ensure `.env` file exists with `OPENAI_API_KEY=your_key`

2. **"File too large"**
   - Compress your MP3 file or use a shorter recording

3. **"Transcription failed"**
   - Check that the file is a valid MP3 format
   - Ensure the audio is clear and audible

4. **"Analysis failed"**
   - Check your OpenAI API key and account limits
   - Try with a shorter audio file

## 📊 API Usage

The application uses OpenAI APIs:
- **Whisper API**: For audio transcription
- **Chat Completions API**: For meeting analysis and summarization

Monitor your OpenAI usage dashboard to track API consumption.

## 🎯 Future Enhancements

Potential improvements:
- Support for additional audio formats (WAV, M4A)
- Speaker identification and diarization
- Meeting template customization
- Export to various formats (PDF, Word)
- Integration with calendar systems
- Real-time meeting transcription

## 📞 Support

For issues or questions:
1. Check the console output for error messages
2. Verify your OpenAI API key is valid
3. Ensure all dependencies are installed correctly
4. Check your internet connection

---

**Built with ❤️ using Gradio & OpenAI**
