from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from datetime import datetime

import re
from datetime import timedelta


from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Set up CORS
origins = [
    "http://localhost",
    "http://localhost:8080",
    "https://example.com",
    "https://www.example.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the input data model


class InputData(BaseModel):
    js_expression: str

# Define the output data model


class OutputData(BaseModel):
    py_expression: str

# Define the conversion function


def convert_js2py(expression):
    # Replace && with and
    expression = re.sub(r'&&', 'and', expression)

    # Replace || with or
    expression = re.sub(r'\|\|', 'or', expression)

    # Replace === with ==
    expression = re.sub(r'===', '==', expression)

    # Replace !== with !=
    expression = re.sub(r'!==', '!=', expression)

    # Replace parseInt with int
    expression = re.sub(r'parseInt\((.*?)\)', r"int(\1)", expression)

    # Replace new Date() with datetime.now()
    expression = re.sub(r'new Date\(\)', 'datetime.now()', expression)

    # Replace new Date('YYYY-MM-DD') with datetime.strptime('YYYY-MM-DD', '%Y-%m-%d')
    expression = re.sub(r'new Date\((.*?)\)',
                        "datetime.strptime(\\1,'%Y-%m-%d')", expression)
    expression = re.sub(r"new Date\('([^']+?)T([^']+?)'\)",
                        r"datetime.strptime('\1T\2', '%Y-%m-%dT%H:%M:%S')", expression)
    expression = re.sub(
        r"new Date\('([^']+?)T([^']+?)\.(\d{3})Z'\)", r"datetime.strptime('\1T\2', '%Y-%m-%dT%H:%M:%S.%fZ')", expression)

    expression = re.sub(r'/1000/60/60/24/365\)',
                        r'.days/365.2425)', expression)

    # Replace (1000/60/60/24)
    expression = re.sub(
        r'/1000/60/60/24', r'/timedelta(hours=24, seconds=60, minutes=60, milliseconds=1000)', expression)

    # Replace (1000/60/60/24/365)
    expression = re.sub(r'/1000/60/60/24/365',
                        r'/timedelta(days=1)/365.2425', expression)

    return expression


# Mount the static files directory to serve HTML, CSS, and JS files
app.mount("/", StaticFiles(directory="static"), name="static")

# Define the API endpoint
@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/js2py")
def convert_expression(input_data: InputData) -> OutputData:
    py_expression = convert_js2py(input_data.js_expression)
    return OutputData(py_expression=py_expression)
