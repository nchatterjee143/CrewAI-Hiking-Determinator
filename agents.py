import requests
from crewai import Crew, Agent, Task
from langchain_openai import ChatOpenAI
import os
from datetime import datetime, timezone, timedelta

api_key = os.getenv('OPENWEATHERMAP_API_KEY')

def get_weather(zip_code):
    weather_url = f"https://api.openweathermap.org/data/2.5/weather?zip={zip_code},us&appid={api_key}&units=imperial"
    response = requests.get(weather_url)
    data = response.json()

    if response.status_code != 200 or 'main' not in data:
        return None, None, None, None, None

    temp = data['main']['temp']
    description = data['weather'][0]['description']
    city = data.get('name', 'your area')
    lat = data['coord']['lat']
    lon = data['coord']['lon']
    return temp, description, city, lat, lon

def get_local_time(lat, lon):
    timezone_url = f"http://api.openweathermap.org/data/2.5/timezone?lat={lat}&lon={lon}&appid={api_key}"
    response = requests.get(timezone_url)

    if response.status_code != 200:
        return None

    data = response.json()
    current_utc = datetime.utcnow().replace(tzinfo=timezone.utc)
    offset_seconds = data['timezone']['offset_seconds']
    local_time = current_utc + timedelta(seconds=offset_seconds)
    return local_time

def check_hiking_conditions(zip_code):
    temp, description, city, lat, lon = get_weather(zip_code)

    if temp is None:
        return "❌ Sorry, I couldn't get the weather information. Please check the ZIP code."

    local_time = get_local_time(lat, lon)
    if local_time is None:
        return "❌ Could not determine the local time at that location."

    local_hour = local_time.hour
    time_str = local_time.strftime("%I:%M %p")

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.5
    )

    weather_agent = Agent(
        role='Weather & Time Safety Analyst',
        goal='Advise on hiking safety based on weather and time of day',
        backstory='Expert in outdoor conditions, local time, and safety best practices.',
        verbose=True,
        allow_delegation=False,
        llm=llm
    )

    task = Task(
        description=f"""
        Determine if it's safe to hike near ZIP code {zip_code} ({city}).
        Weather: {description}, {temp}ºF.
        Local time is currently {time_str}.

        - If temperature is over 80ºF, warn about heat risks and recommend hydration.
        - If time is between 8:00 PM and 5:00 AM, advise against hiking for safety reasons (e.g. visibility, animal risks).
        - Otherwise, if safe, recommend some tips, gear, and trail best practices.
        """,
        expected_output="Hiking recommendation (yes or no) with clear justification and practical advice.",
        agent=weather_agent
    )

    crew = Crew(agents=[weather_agent], tasks=[task], verbose=False)
    result = crew.kickoff()
    return result
