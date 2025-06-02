# YouTube Transcript LangChain Agent

Using an API key from Claude (Anthropic AI) and a YouTube video URL, you can talk to the AI about the transcript of the YouTube video!

## Requirements

- An API key from Anthropic, can make one [here](https://console.anthropic.com/settings/keys).
- A valid Python 3 installation.
- A link to a YouTube video.

## Setup

```
git clone https://github.com/nchatterjee143/YouTube-Transcript-LangChain-Agent.git
cd YouTube-Transcript-LangChain-Agent
pip install -r requirements.txt
cp -r .env.example .env
```
Once this is complete, open the new .env file. Place your API key in the first line of the .env file. In the second line of the .env file place the YouTube video URL. Finally, run `python main.py` to interact with the AI in your terminal window.