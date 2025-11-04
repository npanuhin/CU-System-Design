from fastapi import FastAPI, File, UploadFile

app = FastAPI()


@app.get("/get")
def get_example():
    return {"message": "GET request received"}


@app.post("/post")
def post_example(data: dict):
    return {"message": "POST request received", "data": data}


@app.put("/put/{item_id}")
def put_example(item_id: int, data: dict):
    return {"message": f"PUT request received for item {item_id}", "data": data}


@app.delete("/delete/{item_id}")
def delete_example(item_id: int):
    return {"message": f"DELETE request received for item {item_id}"}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "content_size": len(contents),
    }
