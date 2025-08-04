from dotenv import load_dotenv
import os

load_dotenv()

PASSWORD=os.getenv("PASSWORD")
HOST=os.getenv("HOST")
PORT=os.getenv("PORT")
DB=os.getenv("DB")
USER=os.getenv("USER")
OPENROUTER_API_KEY=os.getenv("OPENROUTER_API_KEY")
DEEPSEEK_API_BASE=os.getenv("DEEPSEEK_API_BASE")

URL = f"postgresql+asyncpg://postgres:{PASSWORD}@{HOST}:{PORT}/{DB}"
DATABASE_URL = os.getenv("DATABASE_URL", URL)