# Complete Website Summarizer using OpenAI GPT-4o-mini

import requests
from bs4 import BeautifulSoup
from openai import OpenAI
from IPython.display import Markdown, display
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(override=True)

# Configuration
MODEL = "gpt-4o-mini"  # OpenAI's efficient and cost-effective model

# Get OpenAI API key with error checking
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise ValueError(
        "OPENAI_API_KEY not found! Please check your .env file.\n"
        "Make sure you have a .env file in the same directory with:\n"
        "OPENAI_API_KEY=your_api_key_here"
    )

# Initialize OpenAI client
openai = OpenAI(api_key=api_key)

def scrape_website(url):
    """
    Scrape a website and extract the main text content
    """
    try:
        # Send a request to the website
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get text content
        text = soup.get_text()
        
        # Clean up the text
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        return text
        
    except Exception as e:
        print(f"Error scraping website: {e}")
        return None

def summarize_with_openai(text, max_length=2000):
    """
    Summarize text using OpenAI GPT-4o-mini
    """
    try:
        # Truncate text if it's too long
        if len(text) > max_length:
            text = text[:max_length] + "..."
        
        # Create the prompt for summarization
        prompt = f"""Please provide a concise summary of the following text. Focus on the main points and key information:

{text}

Summary:"""
        
        # Use OpenAI to generate the summary
        response = openai.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=0.3
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        print(f"Error generating summary: {e}")
        return None

def summarize_website(url):
    """
    Complete function to scrape and summarize a website
    """
    print(f"Scraping website: {url}")
    
    # Scrape the website
    text_content = scrape_website(url)
    
    if text_content is None:
        return "Failed to scrape the website"
    
    print(f"Scraped {len(text_content)} characters of text")
    
    # Generate summary
    print("Generating summary with GPT-4o-mini...")
    summary = summarize_with_openai(text_content)
    
    if summary is None:
        return "Failed to generate summary"
    
    return summary

# Test the website summarizer
test_url = "https://www.monstercat.com/"
print("Testing website summarizer...")
print("=" * 50)

summary = summarize_website(test_url)
print("\nSUMMARY:")
print("=" * 50)
print(summary)