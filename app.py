import os
import gradio as gr
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize the LLM - using OpenAI model
def initialize_llm():
    try:
        # Using GPT-3.5-turbo by default (change to "gpt-4" if you have access)
        model_name = "gpt-3.5-turbo"
        llm = ChatOpenAI(
            model_name=model_name,
            temperature=0.7,
            max_tokens=1024
        )
        return llm
    except Exception as e:
        print(f"Error initializing model: {e}")
        return None

# Prompt templates
question_template = """You are an expert interviewer for technical roles. Based on the job role provided, 
generate one challenging but realistic interview question that would be asked in a real interview.
The question should test both technical knowledge and practical application.

Job Role: {job_role}

Generate a single, focused technical interview question for this role.
"""

feedback_template = """You are an expert technical interviewer evaluating a candidate's response to a technical interview question.

Job Role: {job_role}
Interview Question: {question}
Candidate's Answer: {answer}

Evaluate the answer and provide detailed feedback with the following structure:

RATING:
First, rate the answer on a scale of 1-5 stars (where 1 is poor and 5 is excellent). 
Provide your numerical rating first (just the number 1-5), followed by a brief explanation of the rating.

FEEDBACK:
Then provide 3-4 bullet points of specific feedback, mentioning both strengths and areas for improvement.
Consider:
1. Technical accuracy (is the information correct?)
2. Completeness (did they cover all necessary aspects?)
3. Clarity (was the explanation clear and well-structured?)
4. Practical relevance (did they show practical understanding, not just theory?)

EXPERT ANSWER:
Finally, provide a model answer that would impress an interviewer for this role. This answer should be concise 
but comprehensive, demonstrating deep expertise, practical experience, and strategic thinking. 
Show what a top-tier candidate would say to this question.
"""

# Create chains
def create_chains(llm):
    question_chain = LLMChain(
        llm=llm,
        prompt=PromptTemplate.from_template(question_template),
        verbose=True
    )
    
    feedback_chain = LLMChain(
        llm=llm,
        prompt=PromptTemplate.from_template(feedback_template),
        verbose=True
    )
    
    return question_chain, feedback_chain

# Initialize the model and chains
llm = initialize_llm()
if llm:
    question_chain, feedback_chain = create_chains(llm)
else:
    question_chain, feedback_chain = None, None

# Function to generate questions
def generate_question(job_role):
    if not job_role.strip():
        return "Please enter a job role to get an interview question."
    
    if not question_chain:
        return "Error: Model not initialized. Please check your API token."
    
    try:
        question = question_chain.run(job_role=job_role)
        return question
    except Exception as e:
        return f"Error generating question: {str(e)}"

# Function to generate feedback
def generate_feedback(job_role, question, answer):
    if not job_role.strip() or not question.strip() or not answer.strip():
        return "Please make sure all fields are filled in.", "Please make sure all fields are filled in.", "Please make sure all fields are filled in."
    
    if not feedback_chain:
        return "Error: Model not initialized.", "Error: Model not initialized.", "Error: Model not initialized."
    
    try:
        full_feedback = feedback_chain.run(job_role=job_role, question=question, answer=answer)
        
        # Split the feedback into the three sections
        sections = full_feedback.split("RATING:")
        if len(sections) > 1:
            parts = sections[1].split("FEEDBACK:")
            rating = parts[0].strip()
            
            if len(parts) > 1:
                remaining = parts[1].split("EXPERT ANSWER:")
                feedback = remaining[0].strip()
                expert_answer = remaining[1].strip() if len(remaining) > 1 else "No expert answer provided."
            else:
                feedback = "Processing error. Couldn't extract feedback."
                expert_answer = "Processing error. Couldn't extract expert answer."
        else:
            # Fallback if the expected format isn't found
            rating = "Unable to extract rating."
            feedback = "Processing error. Couldn't extract feedback."
            expert_answer = "Processing error. Couldn't extract expert answer."
            
        return rating, feedback, expert_answer
    except Exception as e:
        return f"Error: {str(e)}", f"Error: {str(e)}", f"Error: {str(e)}"

# Create the Gradio interface
def create_interface():
    with gr.Blocks(title="AI Interview Assistant", theme=gr.themes.Soft()) as app:
        gr.Markdown("# AI Interview Assistant")
        gr.Markdown("Practice interview questions and get feedback on your answers.")
        
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### Step 1: Enter a job role")
                job_role = gr.Textbox(label="Job Role", placeholder="e.g., AI Engineer, Data Scientist, Frontend Developer")
                question_btn = gr.Button("Get Interview Question", variant="primary")
            
        with gr.Row():
            with gr.Column():
                gr.Markdown("### Step 2: Answer the interview question")
                question_output = gr.Textbox(label="Interview Question", lines=4, interactive=False)
                answer_input = gr.Textbox(label="Your Answer", lines=8, placeholder="Type your interview answer here...")
                feedback_btn = gr.Button("Submit Answer & Get Feedback", variant="primary")
        
        with gr.Row():
            with gr.Column():
                gr.Markdown("### Step 3: Review your feedback")
                rating_output = gr.Textbox(label="Rating (1-5 Stars)", lines=2, interactive=False)
                feedback_output = gr.Textbox(label="Detailed Feedback", lines=8, interactive=False)
                expert_output = gr.Textbox(label="Expert Answer Example", lines=10, interactive=False)
        
        # Set up event handlers
        question_btn.click(
            fn=generate_question,
            inputs=[job_role],
            outputs=[question_output]
        )
        
        feedback_btn.click(
            fn=generate_feedback,
            inputs=[job_role, question_output, answer_input],
            outputs=[rating_output, feedback_output, expert_output]
        )
        
        # Examples
        gr.Examples(
            [
                ["Machine Learning Engineer", "", ""],
                ["Frontend Developer", "", ""],
                ["DevOps Engineer", "", ""],
                ["Data Scientist", "", ""],
            ],
            inputs=[job_role, question_output, answer_input]
        )
    
    return app

# Create and launch the app
demo = create_interface()

if __name__ == "__main__":
    demo.launch()