from fastapi import FastAPI,File,UploadFile
# from fastapi_pagination import Page, Params, paginate
from typing import List
from classes import class_req,class_res
#python -m uvicorn main:app --reload
#sse
app=FastAPI()

@app.get("/")
async def root():
    return "fuck you"
#---------------------------------------------------
@app.post("/api/user/join")
async def join(join: class_req.join):
    return "fuck you"

@app.post("/api/user/login")
async def login(login: class_req.login):
    return "fuck you"
#-----------------------------------------------
@app.post("/api/file/upload")
async def create_file(file: class_req.File=File()):
    return {"file_size":len(file)}
#------------------------------------------------

@app.post("/api/case/create")
async def create_case(case: class_req.case_req):
    return {"case_name":case.case_name}

@app.get("/api/case/list",response_model=class_res.case_list)
async def get_list():
    return class_res.case_list(case_id=1)

@app.put("/api/case/list/{case_id}")
async def update_case():
    return "fuck you"

@app.delete("/api/case/list/{case_id}")
async def delete_case():
    return "fuck you"

#-----------------------------------------------