from datetime import UTC, datetime, timedelta

from fastapi import Depends, FastAPI, Header, HTTPException
from jose import JWTError, jwt

app = FastAPI()

SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"


# Create Token
def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


@app.post("/login")
def login(username: str, password: str):
    if username != "admin" or password != "123456":
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token({"sub": username})
    return {"access_token": token, "token_type": "bearer"}


def token_verify(token: str = Header(None)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


@app.get("/dashboard")
def dashboard(user: dict = Depends(token_verify)):
    return {"message": f"Welcome {user['sub']} to the dashboard!"}
