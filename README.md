# AI Interview Assistant

An interactive AI-powered web application to help users practice technical interview questions and receive detailed feedback on their answers. Built with **Gradio**, **LangChain**, and **OpenAI's GPT-4** model.

---

## Features

- Generate challenging, realistic technical interview questions based on a given job role.
- Submit your answers and receive detailed evaluation including:
  - A star rating (1-5)
  - Strengths and areas for improvement in your response
  - A model expert answer for comparison
- User-friendly interface powered by Gradio for easy interaction.

---

## Demo

Launch the app locally and open the provided URL in your browser to practice your interview skills interactively.

---

## Installation

# Clone the repository
git clone https://github.com/dreamer522/ai_interview.git

# Change directory into the project folder
cd ai_interview

# Create a virtual environment (recommended)
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
# source venv/bin/activate

# Install required dependencies
pip install -r requirements.txt

Set up environment variables

Create a .env file in the project root containing your OpenAI API key:

init
OPENAI_API_KEY=your_openai_api_key_here

Run the app locally:

#bash
python app.py
This will start a local Gradio server, and the terminal will display a link (e.g., http://127.0.0.1:7860) to access the interface in your browser.

How it works
Generate Interview Question: Enter a job role (e.g., "Data Scientist") and click Get Interview Question. The app uses LangChain with OpenAI’s GPT to generate a focused technical interview question relevant to the role.

Answer and Get Feedback: Submit your answer to the generated question and click Submit Answer & Get Feedback. The app evaluates your response and provides:

A star rating (1-5)

Detailed bullet-point feedback highlighting technical accuracy, completeness, clarity, and practical relevance

An expert-level model answer to guide your learning

Technologies Used
Python — core programming language

Gradio — UI framework for rapid web app deployment

LangChain — LLM orchestration and prompt chaining

OpenAI GPT-3.5-turbo — language model powering question generation and evaluation

python-dotenv — environment variable management
Project Structure
app.py — main application code with model initialization, prompt chains, and Gradio interface

.env — environment variables (not included in repo for security)

requirements.txt — Python package dependencies

Future Improvements
Support multi-question interviews with session tracking

Add support for different interview formats (e.g., behavioral, system design)

Integrate voice input/output for a more interactive experience

Allow user account management and progress tracking"# ai_interview" 
