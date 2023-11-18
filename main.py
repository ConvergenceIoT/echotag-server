from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()

class TrainingData(BaseModel):
    raw: list[float]
    label: str

@app.post("/train")
async def train_model(data: TrainingData):
    # Access the raw data and label
    raw_data = data.raw
    label = data.label

    # Perform training logic here (you can replace this with your actual training code)
    # For demonstration purposes, we'll just print the data.
    print("Training Data:")
    print("Raw Data:", raw_data)
    print("Label:", label)

    # You can return a response if needed
    return {"message": "Model training complete", "status": "success"}

@app.get("/")
async def healthcheck():
    # You can return a response if needed
    return {"message": "health check!"}

if __name__ == "__main__":
    # TODO 로컬 배포
    # uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)
    # TODO 실서버 배포
    uvicorn.run("main:app", host="0.0.0.0", port=8080)