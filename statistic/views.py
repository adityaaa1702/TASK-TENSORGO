
import pandas as pd
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import UploadFileForm
from .analysis import perform_statistical_analysis
import base64
import os

def index(request):
    context = {}

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file_instance = form.save()
            request.session['uploaded_file_path'] = file_instance.csv_file.path

            
            csv_data = pd.read_csv(file_instance.csv_file)

            
            user_question = request.POST.get('user_question', '')
            plot_type = request.POST.get('plot_type', 'histogram')

           
            analysis_result, plot_data, generated_text = perform_statistical_analysis(csv_data, user_question, plot_type)

           
            plot_filename = os.path.join('static', 'generatedplot.png')
            with open(plot_filename, 'wb') as plot_file:
                plot_file.write(plot_data.getvalue())

            
            encoded_plot = base64.b64encode(plot_data.getvalue()).decode('utf-8')

            context.update({
                'form': form,
                'analysis_result': analysis_result,
                'generated_text': generated_text,
                'encoded_plot': encoded_plot,
                'plot_filename': plot_filename, 
            })

            
            return redirect('result')

    else:
        form = UploadFileForm()
        context.update({'form': form})

    return render(request, 'index.html', context)


def result(request):
    
    uploaded_file_path = request.session.get('uploaded_file_path')

    if uploaded_file_path:
       
        data = pd.read_csv(uploaded_file_path)

        
        analysis_result, plot_data, generated_text= perform_statistical_analysis(data, question="Your question", plot_type="scatter")
        
        mean_value = analysis_result.mean().iloc[0]
        mode_value = analysis_result.mode().iloc[0, 0] if not analysis_result.mode().empty else None
        median_value = analysis_result.median().iloc[0]
        
        
        context = {
            'mean_value': mean_value,
            'mode_value': mode_value,
            'median_value': median_value,  # If you want to use the generated text in the template
        }

        return render(request, 'result.html', context)

    else:
        return redirect('index_page')
