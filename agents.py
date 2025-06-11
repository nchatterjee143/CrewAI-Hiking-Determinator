import requests
from crewai import Crew, Agent, Task
from langchain_community.llms import OpenAI
import os

def get_weather(city):
    api_key = os.getenv('OPENWEATHER_API_KEY')
    endpoint = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=imperial"
    response = requests.get(endpoint)
    data = response.json()

    if response.status_code != 200 or 'main' not in data:
        return None, None
    return data['main']['temp'], data['weather'][0]['description']

def check_hiking_conditions(city):
    temperature, description = get_weather(city)

    if temperature is None:
        return "Sorry, I couldn't get the weather information. Please check the city name."

    llm = OpenAI(
        model="gpt-4o-mini",
        temperature=0.5
    )

    weather_agent = Agent(
        role='Weather Safety Analyst',
        goal='Advise on outdoor hiking safety based on temperature and weather',
        backstory='An expert in outdoor survival and weather-based health risks.',
        verbose=True,
        allow_delegation=False,
        llm=llm
    )

    task = Task(
        description=f"""Determine if it's safe to hike in {city}.
        The weather is described as: {description} with a temperature of {temperature}ºF.
        If it's above 80ºF, advise caution due to dehydration risk.""",
        expected_output='Clear advice on whether to hike or not, with reasoning.',
        agent=weather_agent
    )

    crew = Crew(agents=[weather_agent], tasks=[task], verbose=False)
    result = crew.kickoff()
    return result
