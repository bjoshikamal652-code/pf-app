from fastapi import FastAPI, Request, Form
from fastapi.responses import JSONResponse
from starlette.middleware.sessions import SessionMiddleware


app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key = "jkjoshi")
users = []

@app.post("/register")
def register(request: Request, email: str = Form(...)):
    users.append(email)
    request.session["registered_email"] = email
    return JSONResponse(content={"msg": f"{email} registered"}, status_code = 201) # 201 creating new resource


@app.post("/login")
def login(request: Request, email: str = Form(...)):
    if email not in users:
        return JSONResponse(content={"msg": f"not registered"}, status_code = 403) # forbidden

    request.session["email"] = email
    return JSONResponse(content={"msg": f"login successful"}, status_code = 200)

@app.get("/home")
def home(request: Request, email: str):
    session_email = request.session.get("email")
    if session_email != email:
        return JSONResponse(content={"msg": f"not authorized"}, status_code = 401)

    return JSONResponse(content={"msg": f"Welcome {email}"}, status_code = 200)

@app.put("/profile")
def profile(
    request: Request,
    full_name: str = Form(...),
    address: str = Form(...),
    gender: str = Form(...),
    email: str = Form(...)
):
    session_email = request.session.get("email")
    if session_email != email:
        return JSONResponse(content={"msg": "unauthorized"}, status_code=401)

    profile = {
        "full_name": full_name,
        "address": address,
        "gender": gender,
        "email": email
    }
    request.session["profile"] = profile
    return JSONResponse(content=profile, status_code=200)
    # content=profile
    # Ye actual data hai bhej raha hai.
    # profile ek dictionary hai, jisme user ka form-data hai

@app.get("/profile")
def get_profile(request: Request, email: str):
    session_email = request.session.get("email")
    if session_email != email:
        return JSONResponse(content={"msg": "unauthorized"}, status_code = 401) # 401 unauthorized

    profile = request.session.get("profile")
    if not profile:
        return JSONResponse(content={"msg": "no profile found"}, status_code = 400) #400 bad request
    return JSONResponse(content=profile, status_code = 200)

@app.get("/logout")
def logout(request: Request, email: str):
    session_email = request.session.get("email")
    if session_email != email:
        return JSONResponse(content={"msg": f"error"}, status_code = 401)

    request.session.clear()

    return JSONResponse(content={"msg": f"logged out{email}"}, status_code = 200)

# In register/login routes:
# You are setting the session key, so you use session["email"].
# This directly saves the value — no need to check if the key exists.
# In home/logout and other routes:
# You are checking the session key, so you use session.get("email").
# This safely checks if the key exists — if not, it returns None instead of error.
