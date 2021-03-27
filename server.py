# from typing import Optional
# from fastapi import FastAPI
from get_stream import main as start_stream
import os
# app = FastAPI()

# # check env vars

# @app.get("/health-check")
# def read_root():
#     return {"Hello": "World"}

# @app.get("/health-check")
# def health_check():
#     return {"code": 200}

# add endpoint to restart stream

# # start_stream()
from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
  return render_template("index.html")

@app.route("/health-check")
def read_root():
    return {"Hello": "World"}


MANDATORY_ENV_VARS = ["DISCORD_WEBHOOK", "FAUNA_KEY", "BEARER_TOKEN"]

for var in MANDATORY_ENV_VARS:
    if var not in os.environ:
        raise EnvironmentError("Failed because {} is not set.".format(var))

start_stream()
app.run(host='0.0.0.0', port=8080)