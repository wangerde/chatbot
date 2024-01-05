from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    print("Xin")
    return {"message": "Hello World"}