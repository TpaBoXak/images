import uvicorn
from app import main_app
from config import settings

import time
if __name__ == "__main__":
    print("waiting for 10 seconds")
    time.sleep(10)
    uvicorn.run(app="main:main_app", reload=True,
            host=settings.run.host,
            port=settings.run.port)