import os
import openai

#gets openai key
openai.api_key = os.getenv("OPENAI_API_KEY")

#performs sentiment analysis on a piece of text
def sentimentAnalysis(text):
    sentiment_analyzer = openai.Completion.create(engine="text-davinci-002", 
                                                  prompt=f"perform sentiment analysis of the following text: {text}", 
                                                  temperature=0.75,
                                                max_tokens=50,
                                                frequency_penalty=0,
                                                presence_penalty=0,
                                                )
    
    result = sentiment_analyzer.choices[0].text.strip()
    return result