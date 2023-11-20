from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import echotag
from typing import Optional

app = FastAPI()


class LabeledData(BaseModel):
    raw: list[float]
    label: str


class UnlabeledData(BaseModel):
    raw: list[float]


@app.post("/overwrite-fingerprints")
async def overwriteFingerprints(labeledDataList: list[LabeledData]):
    return echotag.overwriteFingerprints(labeledDataList)


@app.post("/add-fingerprint")
async def addFingerprint(labeledData: LabeledData):
    return echotag.addFingerprint(labeledData)


@app.post("/label")
async def label(unlabeledDataList: list[UnlabeledData]):

    return echotag.label(unlabeledDataList)


@app.get("/health")
async def healthcheck():
    # You can return a response if needed
    return {"message": "health check!"}

if __name__ == "__main__":
    # TODO 로컬 배포
    # uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)
    # TODO 실서버 배포
    uvicorn.run("main:app", host="0.0.0.0", port=8080)
