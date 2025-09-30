# AI Tutor - GPT-4o-mini and Llama 3.2 Comparison Tool

from dotenv import load_dotenv
from IPython.display import Markdown, display, update_display
from openai import OpenAI
import ollama

# Load environment variables
load_dotenv()

# Constants
MODEL_GPT = 'gpt-4o-mini'
MODEL_LLAMA = 'llama3.2'

# Set up environment
openai = OpenAI()

def ask_question_gpt(question, system_prompt=None, user_prompt=None):
    """
    Ask a question using GPT-4o-mini with streaming response
    """
    if system_prompt is None:
        system_prompt = "You are a helpful technical tutor who answers questions about python code, software engineering, data science and LLMs"
    
    if user_prompt is None:
        user_prompt = "Please give a detailed explanation to the following question: " + question
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    
    print("GPT-4o-mini Response:")
    print("=" * 50)
    
    stream = openai.chat.completions.create(
        model=MODEL_GPT, 
        messages=messages, 
        stream=True
    )
    
    response = ""
    for chunk in stream:
        content = chunk.choices[0].delta.content or ''
        response += content
        print(content, end='', flush=True)
    
    print("\n" + "=" * 50)
    return response

def ask_question_llama(question, system_prompt=None, user_prompt=None):
    """
    Ask a question using Llama 3.2
    """
    if system_prompt is None:
        system_prompt = "You are a helpful technical tutor who answers questions about python code, software engineering, data science and LLMs"
    
    if user_prompt is None:
        user_prompt = "Please give a detailed explanation to the following question: " + question
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    
    print("Llama 3.2 Response:")
    print("=" * 50)
    
    response = ollama.chat(model=MODEL_LLAMA, messages=messages)
    reply = response['message']['content']
    
    print(reply)
    print("=" * 50)
    return reply

def compare_ai_models(question):
    """
    Compare responses from both GPT-4o-mini and Llama 3.2
    """
    print(f"Question: {question}")
    print("\n" + "=" * 80)
    
    # Get GPT response
    gpt_response = ask_question_gpt(question)
    
    print("\n" + "=" * 80)
    
    # Get Llama response
    llama_response = ask_question_llama(question)
    
    return gpt_response, llama_response

# Example usage
if __name__ == "__main__":
    # Example question from the notebook
    question = """
Please explain what this code does and why:
yield from {book.get("author") for book in books if book.get("author")}
"""
    
    # Compare both models
    gpt_response, llama_response = compare_ai_models(question)
    
    print("\n" + "=" * 80)
    print("Comparison complete!")
