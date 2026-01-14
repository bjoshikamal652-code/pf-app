from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key = "jkjoshi")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
users = {}

@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "page": "register"})

@app.api_route("/register", methods=["GET", "POST"])
def register(request: Request, email: str = Form(None), password: str = Form(None)):
    if request.method == "POST":
        if email in users:
            return templates.TemplateResponse("index.html", {"request": request, "page": "register", "msg": "User already registered"})
        users[email] = password
        request.session["email"] = email
        return RedirectResponse(url="/login", status_code=303)
    return templates.TemplateResponse("index.html", {"request": request, "page": "register"})

@app.api_route("/login", methods=["GET", "POST"])
def login(request: Request, email: str = Form(None), password: str = Form(None)):
    if request.method == "POST":
        if email not in users:
            return templates.TemplateResponse("index.html", {"request": request, "page": "login", "msg": "User not registered"})
        if users[email] != password:
            return templates.TemplateResponse("index.html", {"request": request, "page": "login", "msg": "Invalid credentials"})
        request.session["email"] = email
        return RedirectResponse(url="/home", status_code=303)
    return templates.TemplateResponse("index.html", {"request": request, "page": "login"})

@app.get("/home", response_class=HTMLResponse)
def home(request: Request):
    session_email = request.session.get("email")
    if not session_email:
        return RedirectResponse(url="/login", status_code=303)
    msg = ("Welcome to FastAPI Authentication System!\n\n"
           "This is a full-stack web application built using Python's FastAPI framework, implementing secure session-based user authentication.\n\n"
           "The project demonstrates core web development concepts including user registration, login functionality, protected routes, and session management.\n\n"
           "Features:\n"
           "User Registration & Login System\n"
           "Session-based Authentication\n"
           "Password Protection\n"
           "Secure Route Handling\n"
           "Clean & Responsive UI\n\n"
           "Technologies Used: Python (FastAPI), HTML5, CSS3, Jinja2 Templating\n\n"
           "This project showcases practical implementation of backend logic with FastAPI, frontend design with HTML/CSS, and smooth integration between user interface and server.")
    return templates.TemplateResponse("index.html", {"request": request, "page": "home", "msg": msg})

@app.get("/logout")
def logout(request: Request):
    session_email = request.session.get("email")
    if not session_email:
        return RedirectResponse(url="/login", status_code=303)
    request.session.clear()
    return RedirectResponse(url="/login", status_code=303)
