
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
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            
            uploaded_file = form.save()

            
            df = pd.read_csv(uploaded_file.csv_file)

            
            height_column = df.iloc[:, 1]

            
            mean_value = height_column.mean()
            mode_value = height_column.mode()[0] if not height_column.mode().empty else None
            median_value = height_column.median()

        
            context = {
                'mean_value': mean_value,
                'mode_value': mode_value,
                'median_value': median_value,
            }

            
            return render(request, 'result.html', context)

    return render(request, 'result.html')