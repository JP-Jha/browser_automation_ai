import asyncio
from fastapi import FastAPI
from app.automation import automate_web_search, search_flights, gmail_login
from fastapi.responses import JSONResponse

app = FastAPI()

@app.post("/automate")
async def automate(input_data: dict):
    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(None, automate_web_search, input_data)
    return JSONResponse(content=result)

@app.post("/search-flights")
async def automate_flights(input_data: dict):
    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(None, search_flights, input_data)
    return JSONResponse(content=result)

@app.post("/gmail-login")
async def automate_gmail(input_data: dict):
    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(None, gmail_login, input_data)
    return JSONResponse(content=result)
