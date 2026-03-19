import os
from groq import Groq
from dotenv import load_dotenv
import pathlib

load_dotenv(pathlib.Path(__file__).parent.parent / '.env')


def get_ai_summary(df):
    try:
        summary = f"""
        Total Properties: {df.shape[0]}
        Columns: {list(df.columns)}
        Locations: {df['Location'].unique().tolist() if 'Location' in df.columns else 'N/A'}
        Average Price: {round(df['Price_Lakhs'].mean(), 2) if 'Price_Lakhs' in df.columns else 'N/A'} Lakhs
        Highest Price: {df['Price_Lakhs'].max() if 'Price_Lakhs' in df.columns else 'N/A'} Lakhs
        Lowest Price: {df['Price_Lakhs'].min() if 'Price_Lakhs' in df.columns else 'N/A'} Lakhs
        BHK Types: {df['BHK'].unique().tolist() if 'BHK' in df.columns else 'N/A'}
        Status: {df['Status'].value_counts().to_dict() if 'Status' in df.columns else 'N/A'}
        Sample Data: {df.head(5).to_string()}
        """

        client = Groq(api_key=os.getenv('GROQ_API_KEY'))
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            max_tokens=500,
            messages=[
                {
                    "role": "user",
                    "content": f"""You are a real estate data analyst in India.
                    Analyze this property dataset and give a clear professional summary
                    in 4-5 sentences. Focus on key insights, best areas, price trends,
                    and one investment recommendation.
                    Use Indian property terms like Lakhs, Crore, BHK.
                    Data: {summary}"""
                }
            ]
        )
        return response.choices[0].message.content

    except Exception as e:
        return f"AI analysis unavailable: {str(e)}"


def ask_ai(question, df):
    try:
        data_str = df.to_string()
        client = Groq(api_key=os.getenv('GROQ_API_KEY'))
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            max_tokens=400,
            messages=[
                {
                    "role": "user",
                    "content": f"""You are a real estate analyst in India.
                    Answer this question based on the property data below.
                    Be specific, use numbers from the data, keep answer under 5 sentences.
                    Use Indian terms like Lakhs, Crore, BHK.
                    Question: {question}
                    Property Data: {data_str}"""
                }
            ]
        )
        return response.choices[0].message.content

    except Exception as e:
        return f"AI unavailable: {str(e)}"


def get_ai_insights(df):
    try:
        summary = df.describe().to_string()
        data_str = df.to_string()
        client = Groq(api_key=os.getenv('GROQ_API_KEY'))
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            max_tokens=600,
            messages=[
                {
                    "role": "user",
                    "content": f"""You are a senior real estate analyst in India.
                    Find exactly 3 interesting hidden insights from this property data.
                    Format your response EXACTLY like this:

                    INSIGHT 1: [title]
                    [2 sentence explanation with specific numbers]

                    INSIGHT 2: [title]
                    [2 sentence explanation with specific numbers]

                    INSIGHT 3: [title]
                    [2 sentence explanation with specific numbers]

                    Data Statistics: {summary}
                    Full Data: {data_str}"""
                }
            ]
        )

        raw = response.choices[0].message.content
        insights = []
        for i in range(1, 4):
            start = raw.find(f'INSIGHT {i}:')
            end = raw.find(f'INSIGHT {i+1}:') if i < 3 else len(raw)
            if start != -1:
                insights.append(raw[start:end].strip())

        return insights if insights else [raw]

    except Exception as e:
        return [f"AI insights unavailable: {str(e)}"]