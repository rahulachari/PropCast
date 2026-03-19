from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
import os
import json
from django.conf import settings
import plotly.express as px
import plotly.utils
from .ml_model import train_and_predict
from .ai_engine import get_ai_summary, ask_ai, get_ai_insights
from .pdf_generator import generate_pdf_report


def upload(request):
    context = {}

    if request.method == 'POST':
        csv_file = request.FILES.get('csv_file')
        question = request.POST.get('question', '')

        if csv_file and csv_file.name.endswith('.csv'):
            file_path = os.path.join(settings.MEDIA_ROOT, csv_file.name)
            with open(file_path, 'wb+') as f:
                for chunk in csv_file.chunks():
                    f.write(chunk)
            request.session['last_csv'] = csv_file.name

        last_csv = request.session.get('last_csv')
        if last_csv:
            file_path = os.path.join(settings.MEDIA_ROOT, last_csv)
            if os.path.exists(file_path):
                df = pd.read_csv(file_path)

                if 'Price_Lakhs' in df.columns:
                    avg = round(df['Price_Lakhs'].mean(), 1)
                    high = df['Price_Lakhs'].max()
                    low = df['Price_Lakhs'].min()
                    avg_display = f"₹{round(avg/100, 2)} Crore" if avg >= 100 else f"₹{int(avg)} Lakhs"
                    high_display = f"₹{round(high/100, 2)} Crore" if high >= 100 else f"₹{int(high)} Lakhs"
                    low_display = f"₹{round(low/100, 2)} Crore" if low >= 100 else f"₹{int(low)} Lakhs"
                else:
                    avg_display = high_display = low_display = 'N/A'

                context = {
                    'filename': last_csv,
                    'rows': df.shape[0],
                    'columns': df.shape[1],
                    'col_names': list(df.columns),
                    'missing': int(df.isnull().sum().sum()),
                    'avg_price': avg_display,
                    'high_price': high_display,
                    'low_price': low_display,
                    'preview': df.head(10).to_html(
                        classes='table table-striped table-bordered table-hover',
                        index=False
                    ),
                }

                if 'Location' in df.columns and 'Price_Lakhs' in df.columns:
                    fig1 = px.bar(
                        df,
                        x='Location',
                        y='Price_Lakhs',
                        title='Property Price by Location (Lakhs)',
                        color='Price_Lakhs',
                        color_continuous_scale='Blues',
                        text='Price_Lakhs'
                    )
                    fig1.update_layout(plot_bgcolor='white', paper_bgcolor='white', font=dict(size=13))
                    context['chart_price'] = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)

                if 'Status' in df.columns:
                    status_counts = df['Status'].value_counts().reset_index()
                    status_counts.columns = ['Status', 'Count']
                    fig2 = px.pie(
                        status_counts,
                        names='Status',
                        values='Count',
                        title='Sold vs Available Properties',
                        color_discrete_sequence=['#1a1a2e', '#4a90d9']
                    )
                    fig2.update_layout(paper_bgcolor='white', font=dict(size=13))
                    context['chart_status'] = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)

                if 'BHK' in df.columns:
                    bhk_counts = df['BHK'].value_counts().reset_index()
                    bhk_counts.columns = ['BHK', 'Count']
                    bhk_counts['BHK'] = bhk_counts['BHK'].astype(str) + ' BHK'
                    fig3 = px.bar(
                        bhk_counts,
                        x='BHK',
                        y='Count',
                        title='BHK Type Distribution',
                        color='Count',
                        color_continuous_scale='Greens',
                        text='Count'
                    )
                    fig3.update_layout(plot_bgcolor='white', paper_bgcolor='white', font=dict(size=13))
                    context['chart_bhk'] = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)

                context['ai_summary'] = get_ai_summary(df)
                context['ai_insights'] = get_ai_insights(df)

                if question:
                    context['question'] = question
                    context['ai_answer'] = ask_ai(question, df)

            else:
                context['error'] = 'Previous file not found. Please upload again.'

    return render(request, 'upload.html', context)


def predict(request):
    context = {}

    media_path = settings.MEDIA_ROOT
    csv_files = [f for f in os.listdir(media_path) if f.endswith('.csv')]

    if csv_files:
        latest_csv = max(
            csv_files,
            key=lambda f: os.path.getmtime(os.path.join(media_path, f))
        )
        df = pd.read_csv(os.path.join(media_path, latest_csv))
        if 'Location' in df.columns:
            context['locations'] = sorted(df['Location'].unique().tolist())

    if request.method == 'POST':
        location = request.POST.get('location')
        bhk = int(request.POST.get('bhk'))
        area_sqft = int(request.POST.get('area_sqft'))
        age_years = int(request.POST.get('age_years'))

        result, error = train_and_predict(location, bhk, area_sqft, age_years)

        if error:
            context['error'] = error
        else:
            context['result'] = result

    return render(request, 'predict.html', context)


def download_report(request):
    last_csv = request.session.get('last_csv')

    if not last_csv:
        return HttpResponse("No data found. Please upload a CSV first.", status=400)

    file_path = os.path.join(settings.MEDIA_ROOT, last_csv)

    if not os.path.exists(file_path):
        return HttpResponse("File not found. Please upload again.", status=400)

    df = pd.read_csv(file_path)
    ai_summary = get_ai_summary(df)
    ai_insights = get_ai_insights(df)

    pdf_buffer = generate_pdf_report(df, ai_summary, ai_insights, last_csv)

    response = HttpResponse(pdf_buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="PropCast_Report.pdf"'
    return response