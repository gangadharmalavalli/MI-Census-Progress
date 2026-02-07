from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import StreamingResponse
from app.auth import authenticate
from app.logic import generate_reports

app = FastAPI(title="MI Census Secure System")

@app.post("/login")
def login(user: str = Form(...), password: str = Form(...)):
    taluk = authenticate(user, password)
    if not taluk:
        raise HTTPException(status_code=401, detail="Invalid login")
    return {"status": "success", "taluk": taluk}

@app.post("/generate")
def generate(
    user: str = Form(...),
    password: str = Form(...),
    master: UploadFile = File(...),
    monitor: UploadFile = File(...)
):
    taluk = authenticate(user, password)
    if not taluk:
        raise HTTPException(status_code=403, detail="Unauthorized")

    excel, graph, card = generate_reports(
        master.file,
        monitor.file,
        taluk
    )

    return {
        "excel": StreamingResponse(
            excel,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": "attachment; filename=Progress_Report.xlsx"}
        ),
        "graph": StreamingResponse(
            graph,
            media_type="image/png",
            headers={"Content-Disposition": "attachment; filename=Progress_Graph.png"}
        ),
        "card": StreamingResponse(
            card,
            media_type="image/png",
            headers={"Content-Disposition": "attachment; filename=Taluk_Summary.png"}
        )
    }
