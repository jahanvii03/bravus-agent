import os
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse, JSONResponse
from config import DefaultConfig
from utils.hash_utils import hash_id
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config

CONFIG = DefaultConfig()

router = APIRouter()

COMMON_TENANT_ID = "common"

oauth = OAuth(
    Config(
        environ={
            "AZURE_CLIENT_ID": CONFIG.AZURE_CLIENT_ID,
            "AZURE_CLIENT_SECRET": CONFIG.AZURE_CLIENT_SECRET,
            "AZURE_TENANT_ID": COMMON_TENANT_ID,
        }
    )
)


oauth.register(
    name='azure',
    client_id=CONFIG.AZURE_CLIENT_ID,
    client_secret=CONFIG.AZURE_CLIENT_SECRET,
    authorize_url=f"https://login.microsoftonline.com/{COMMON_TENANT_ID}/oauth2/v2.0/authorize?prompt=login",
    access_token_url=f"https://login.microsoftonline.com/{COMMON_TENANT_ID}/oauth2/v2.0/token",
    client_kwargs={'scope': 'User.Read', 'code_challenge_method': 'S256'},
)


# Azure login route
@router.get("/login/azure")
async def login_with_azure(request: Request):
    request.session.clear()
    redirect_uri = request.url_for("authorize_azure")
    # if os.getenv("FLASK_ENV", "development") == "development":
    #     redirect_uri = str(redirect_uri).replace("https://", "http://")
    # else:
    redirect_uri = str(redirect_uri).replace("http://", "https://")
    return await oauth.azure.authorize_redirect(request, redirect_uri)

@router.get("/login/azure/authorize")
async def authorize_azure(request: Request):
    try:
        token = await oauth.azure.authorize_access_token(request)
        print("token : ", token)
 
        user_info_response = await oauth.azure.get(
            'https://graph.microsoft.com/v1.0/me?$select=displayName,mail,userPrincipalName,department,companyName',
            token=token
        )
        user_info = user_info_response.json()
        user_email = user_info.get("mail") or user_info.get("userPrincipalName")

        request.session['user'] = {
            "userId": hash_id(user_email),
            "name": user_info["displayName"],
            "email": user_email,
            "loginWith": "azure",
            "department": user_info.get("department"),
            "isAdmin": True,
            "oid": hash_id(user_email),
            "groups": [],
        }

        # return RedirectResponse(url="http://localhost:5173/home")
        return RedirectResponse(url="/")

    except ValueError as e:
        if "mismatching_state" in str(e):
            request.session.clear()
            return RedirectResponse(url="/login/azure")
        raise


@router.get("/logout")
async def logout(request: Request):
    request.session.pop('user', None)
    request.session.clear()
    return RedirectResponse(url='/')


@router.get("/user")
async def get_user(request: Request):
    user = request.session.get('user')
    if user:
        return JSONResponse({"user": user})
    else:
        return RedirectResponse(url="/")
 