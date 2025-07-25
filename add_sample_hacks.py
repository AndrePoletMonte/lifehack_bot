import asyncio
from database.db import add_lifehacks_bulk
SAMPLES = [
    # English, Serbian
    ("Drink a glass of water right after waking up.", "Popij čašu vode odmah nakon buđenja."),
    ("Use Pomodoro technique: work 25 min, rest 5 min.", "Koristi Pomodoro tehniku: radi 25 min, odmori 5 min."),
    ("Write down 3 things you're grateful for each morning.", "Svako jutro zapiši 3 stvari na kojima si zahvalan."),
    ("Keep your workspace clean to boost productivity.", "Održavaj radni sto urednim za bolju produktivnost."),
    ("Plan your day the night before.", "Isplaniraj dan večer pre."),
]

async def main():
    
    from database.lifehacks import add_lifehack
    for text_en, text_sr in SAMPLES:
        await add_lifehack(text_en, text_sr)
        print(f"Added: {text_en} / {text_sr}")

if __name__ == "__main__":
    asyncio.run(main())
