import requests
import json
import gradio as gr

# Set the API URL for Ollama (Make sure Ollama is running)
url = "http://localhost:11434/api/generate"

# Headers for the API request
headers = {
    'Content-Type': 'application/json'
}

# Store chat history
history = []

def generate_response(prompt):
    """Send prompt to CodeLlama via Ollama API and return response."""
    
    history.append(prompt)  # Append new prompt to history
    final_prompt = "\n".join(history)  # Combine all history into a single prompt

    # Data payload for Ollama API
    data = {
        "model": "codellama",
        "prompt": final_prompt,
        "stream": False
    }

    try:
        # Send request to Ollama API
        response = requests.post(url, headers=headers, data=json.dumps(data))
        print("Raw API Response:", response.text)  # Debugging

        if response.status_code == 200:
            data = response.json()
            actual_response = data.get('response', "No response received.")
            print("Processed Response:", actual_response)  # Debugging
            return actual_response
        else:
            return f"Error: {response.status_code} - {response.text}"
    
    except Exception as e:
        return f"Request failed: {str(e)}"

# Define Gradio UI with a Submit Button
with gr.Blocks() as interface:
    gr.Markdown("# 🤖 CodeLlama AI Chatbot")
    
    with gr.Row():
        prompt_input = gr.Textbox(lines=4, placeholder="Enter your Prompt here...", label="User Input")

    submit_button = gr.Button("Submit")  # Add Submit Button
    output_text = gr.Textbox(lines=10, label="AI Response")  # Output Box

    # Submit button triggers the response
    submit_button.click(fn=generate_response, inputs=prompt_input, outputs=output_text)

# Launch Gradio interface
interface.launch(share=True)  # Add share=True for external access
