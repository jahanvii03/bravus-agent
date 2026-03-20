from fastapi import FastAPI,HTTPException,Request
import uvicorn 
import os
import mimetypes
from starlette.middleware.sessions import SessionMiddleware
from config import DefaultConfig
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from routers.auth_routes import router as auth_router
app = FastAPI()
CONFIG=DefaultConfig()
app.include_router(auth_router,prefix='/api')
print(CONFIG.SECRET_KEY)
app.add_middleware(SessionMiddleware, secret_key=CONFIG.SECRET_KEY, max_age=1209600)

app.mount("/static", StaticFiles(directory="static"), name="static")
# Handle client-side routing
@app.get("/{full_path:path}")
async def serve_react(full_path: str, request: Request):
     if full_path.startswith("api/"):
         raise HTTPException(status_code=404, detail="API endpoint not found")
 
     # Ensure we are serving files from the static directory
     file_path = os.path.join("static", full_path)
 
     if os.path.isfile(file_path):
         mime_type, _ = mimetypes.guess_type(file_path)
         return FileResponse(file_path, media_type=mime_type)
 
     # Serve index.html for React routes
     return FileResponse("static/index.html")

if __name__ ==  "__main__":
    uvicorn.run(app, host="localhost", port=5000)