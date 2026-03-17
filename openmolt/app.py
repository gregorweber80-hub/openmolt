from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from openmolt.core.config import Settings, load_app_config
from openmolt.core.security import SecurityPolicy
from openmolt.services.gateway import Gateway
from openmolt.services.gmail_service import GmailService
from openmolt.services.ollama_client import OllamaClient
from openmolt.services.skills import SkillRegistry
from openmolt.services.web_agent import WebAgent

settings = Settings()
config = load_app_config(settings.config_path)

policy = SecurityPolicy(
    mode=config.security.mode,
    require_explicit_send_approval=config.security.require_explicit_send_approval,
    allowed_domains=set(config.security.allowed_domains),
)

ollama = OllamaClient(host=config.ollama.host, model=config.ollama.model)
web_agent = WebAgent(policy=policy)
gmail = GmailService(policy=policy)
gateway = Gateway()
skills = SkillRegistry()
skills.load()

app = FastAPI(title="OpenMolt Dashboard")
app.mount("/static", StaticFiles(directory="openmolt/static"), name="static")
templates = Jinja2Templates(directory="openmolt/templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request,
        "dashboard.html",
        {
            "name": config.name,
            "security_mode": policy.mode,
            "skills": sorted(skills.skills.keys()),
            "ollama_model": config.ollama.model,
        },
    )


@app.post("/chat", response_class=HTMLResponse)
async def chat(request: Request, prompt: str = Form(...)) -> HTMLResponse:
    response = await ollama.chat(prompt=prompt, system="You are an autonomous but safe personal assistant.")
    return templates.TemplateResponse(request, "partials/chat_result.html", {"response": response})


@app.post("/search", response_class=HTMLResponse)
async def search(request: Request, query: str = Form(...)) -> HTMLResponse:
    result = await web_agent.search_web(query)
    return templates.TemplateResponse(request, "partials/search_result.html", {"result": result})


@app.post("/mail", response_class=HTMLResponse)
async def mail(
    request: Request,
    sender: str = Form(...),
    to: str = Form(...),
    subject: str = Form(...),
    body: str = Form(...),
    approved: bool = Form(False),
) -> HTMLResponse:
    msg = gmail.create_message(sender=sender, to=to, subject=subject, body=body)
    result = gmail.send_message(msg, approved=approved)
    return templates.TemplateResponse(request, "partials/mail_result.html", {"result": result})


@app.post("/gateway/register", response_class=HTMLResponse)
async def register_account(request: Request, service: str = Form(...), username: str = Form(...), password: str = Form(...)) -> HTMLResponse:
    gateway.register(service=service, username=username, password=password)
    return templates.TemplateResponse(request, "partials/gateway_result.html", {"result": f"Stored credentials for {service}."})


@app.post("/gateway/login", response_class=HTMLResponse)
async def login_account(request: Request, service: str = Form(...)) -> HTMLResponse:
    result = gateway.login(service)
    return templates.TemplateResponse(request, "partials/gateway_result.html", {"result": result})


@app.post("/skill", response_class=HTMLResponse)
async def run_skill(request: Request, skill_name: str = Form(...), text: str = Form(...)) -> HTMLResponse:
    result = skills.execute(skill_name, text)
    return templates.TemplateResponse(request, "partials/skill_result.html", {"result": result})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("openmolt.app:app", host="0.0.0.0", port=8000, reload=False)
