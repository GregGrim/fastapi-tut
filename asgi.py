import uvicorn


if __name__ == "__main__":
    uvicorn.run(
        "app:create_app", host="localhost", port=8001, reload=True, factory=True
    )
