
import pandas as pd
import matplotlib.pyplot as plt
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import io
import base64

def perform_statistical_analysis(data, question=None, plot_type='histogram'):
   
    analysis_result = data.describe()

    
    plt.figure(figsize=(10, 6))

    if plot_type == 'histogram':
        plt.hist(data.iloc[:, 0], bins=30, color='blue', alpha=0.7)
        plt.title('Histogram of Data')
        plt.xlabel('Values')
        plt.ylabel('Frequency')
        plt.grid(True)
    elif plot_type == 'scatter':
        plt.scatter(data.iloc[:, 0], data.iloc[:, 1], color='red', alpha=0.7)
        plt.title('Scatter Plot')
        plt.xlabel('X Values')
        plt.ylabel('Y Values')
        plt.grid(True)
    elif plot_type == 'line':
        plt.plot(data.iloc[:, 0], data.iloc[:, 1], color='green', marker='o', linestyle='-', linewidth=2, markersize=8)
        plt.title('Line Plot')
        plt.xlabel('X Values')
        plt.ylabel('Y Values')
        plt.grid(True)
    

    
    plot_data = io.BytesIO()
    plt.savefig(plot_data, format='png')
    plot_data.seek(0)

    
    mean_values = data.mean()
    median_values = data.median()
    mode_values = data.mode().iloc[0]  
    std_dev_values = data.std()
    correlation_matrix = data.corr()

    prompt = f"Data analysis results:\n\n{analysis_result}\n\nAdditional Statistics:\n\nMean:\n{mean_values}\n\nMedian:\n{median_values}\n\nMode:\n{mode_values}\n\nStandard Deviation:\n{std_dev_values}\n\nCorrelation Coefficients:\n{correlation_matrix}\n\nUser question: {question}\nAnswer:"
    
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    model = GPT2LMHeadModel.from_pretrained("gpt2")

    
    inputs = tokenizer.encode(prompt, return_tensors="pt", max_length=512, truncation=True)

 
    outputs = model.generate(
        inputs,
        max_length=len(inputs[0]) + 50,
        num_beams=5,
        no_repeat_ngram_size=2,
        top_k=50,
        top_p=0.95,
        temperature=0.7,
        do_sample=True,  
        pad_token_id=tokenizer.eos_token_id  
    )

   
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return analysis_result, plot_data, generated_text
