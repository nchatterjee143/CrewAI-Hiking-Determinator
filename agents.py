import requests
from crewai import Crew, Agent, Task
from langchain_openai import ChatOpenAI
import os
from datetime import datetime, timezone, timedelta
import logging
import html

# Silence terminal logs from langchain and crewai
logging.getLogger('langchain').setLevel(logging.WARNING)
logging.getLogger('crewai').setLevel(logging.WARNING)

api_key = os.getenv('OPENWEATHERMAP_API_KEY')

def get_weather(zip_code):
    weather_url = f"https://api.openweathermap.org/data/2.5/weather?zip={zip_code},us&appid={api_key}&units=imperial"
    response = requests.get(weather_url)
    data = response.json()

    if response.status_code != 200 or 'main' not in data:
        return None, None, None, None

    temp = data['main']['temp']
    description = data['weather'][0]['description']
    city = data.get('name', 'your area')
    offset_seconds = data['timezone']
    return temp, description, city, offset_seconds

def get_local_time(offset_seconds):
    current_utc = datetime.utcnow().replace(tzinfo=timezone.utc)
    local_time = current_utc + timedelta(seconds=offset_seconds)
    return local_time

def check_hiking_conditions(zip_code):
    temp, description, city, offset_seconds = get_weather(zip_code)

    if temp is None:
        return "<p class='error'>❌ Sorry, I couldn't get the weather information. Please check the ZIP code.</p>"

    local_time = get_local_time(offset_seconds)
    time_str = local_time.strftime("%I:%M %p")
    hour = local_time.hour

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.5
    )

    weather_agent = Agent(
        role='Weather & Time Safety Analyst',
        goal='Advise on hiking safety based on weather and time of day',
        backstory='Expert in outdoor conditions, local time, and safety best practices.',
        verbose=False,
        allow_delegation=False,
        llm=llm
    )

    task = Task(
        description=f"""
        Determine if it's safe to hike near ZIP code {zip_code} ({city}).
        Weather: {description}, {temp}ºF.
        Local time is currently {time_str}.

        - If temperature is over 80ºF, warn about heat risks and recommend hydration.
        - If time is between 8:00 PM and 5:00 AM (i.e., hour < 5 or hour >= 20), advise against hiking.
        - Otherwise, if safe, recommend some hiking gear, hydration tips, nearby trail advice, and trail recommendations within a 10 km radius.
        """,
        expected_output="Return an HTML-formatted hiking recommendation with clear justification and practical advice.",
        agent=weather_agent
    )

    crew = Crew(
        agents=[weather_agent],
        tasks=[task],
        verbose=False
    )

    raw_result = str(crew.kickoff()).strip()
    if raw_result.startswith("```html"):
        raw_result = raw_result.removeprefix("```html").strip()
    if raw_result.endswith("```"):
        raw_result = raw_result.removesuffix("```").strip()

    result = html.unescape(raw_result)

    if not result.lower().startswith("<p>") and not result.lower().startswith("<div>") and not result.lower().startswith("<h"):
        result = f"<p>{result}</p>"

    return f"""
    <div class='result'>
        <h2>Hiking Safety Recommendation</h2>
        <p><strong>Location:</strong> {city} ({zip_code})</p>
        <p><strong>Current Weather:</strong> {description}, {temp}ºF</p>
        <p><strong>Local Time:</strong> {time_str}</p>
        <div class='advice'>{result}</div>
    </div>
    """
