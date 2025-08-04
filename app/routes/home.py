from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

import os

# تحديد مكان القوالب
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def read_home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request, "title": "الرئيسية"})

@router.get("/about", response_class=HTMLResponse)
async def read_about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request, "title": "من نحن"})

@router.get("/contact", response_class=HTMLResponse)
async def get_contact(request: Request):
    return templates.TemplateResponse("contact.html", {"request": request, "title": "تواصل معنا"})

@router.post("/contact", response_class=HTMLResponse)
async def post_contact(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    message: str = Form(...)
):
    print("📩 رسالة جديدة:", name, email, message)
    return templates.TemplateResponse("contact.html", {
        "request": request,
        "title": "تواصل معنا",
        "success": True,
        "name": name
    })
