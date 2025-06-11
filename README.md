# CrewAI Hiking Determinator

Using API keys from OpenAI and OpenWeatherMap, you can ask AI if you should go on a hike in a specified ZIP code!

## Requirements

- An API key from OpenAI, can make one [here](https://platform.openai.com/settings/organization/api-keys).
- An API key from OpenWeatherMap, can make one [here](https://home.openweathermap.org/api_keys)
- A valid Python 3 installation, preferrably 3.12!

## Setup

```
git clone https://github.com/nchatterjee143/CrewAI-Hiking-Determinator.git
cd CrewAI-Hiking-Determinator
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp -r .env.example .env
```
Once this is complete, open the new .env file. Place your API keys in the line of the .env file. In the second line of the .env file place the YouTube video URL. Finally, run `python app.py` to interact with the AI in your web browser of choice.