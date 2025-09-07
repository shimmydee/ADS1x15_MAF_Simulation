# ADS1x15_MAF_Simulation

## What is this?
Moving-Average Filter microservice for ADC/DSP exploration.
Send a list of numbers (`signal`) and a window size; get the smoothed signal and a peak-preservation metric.

## Run locally
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python app.py
# In another terminal:
curl -X POST http://localhost:8000/process \
  -H "Content-Type: application/json" \
  -d '{"signal":[0,0,1,5,1,0,0],"window":3}'

## Run with Docker
docker build -t maf-api:latest .
docker run -p 8000:8000 maf-api:latest
<img width="598" height="444" alt="image" src="https://github.com/user-attachments/assets/f5b32cdb-2b82-4bab-af54-d642b654103f" />
