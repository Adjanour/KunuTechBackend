from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.core import database

from app.routes.optimization import router as optimization_router
from app.routes import users,bin,devices,marketplace,notification,qr,chat,gamification,collectors,challenges


app = FastAPI(
    title="KunuTech WasteSense API",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"]
)

app.include_router(optimization_router, prefix="/api", tags=["Route Optimization"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(bin.router, prefix="/api/bins", tags=["Bins"])
app.include_router(devices.router, prefix="/api/devices", tags=["Devices"])
app.include_router(marketplace.router, prefix="/api/marketplace", tags=["Marketplace"])
app.include_router(notification.router, prefix="/api/notification", tags=["Notification"])
app.include_router(qr.router, prefix="/api/qr", tags=["QR"])
app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])
app.include_router(gamification.router, prefix="/api/gamification", tags=["Gamification"])
app.include_router(challenges.router, prefix="/api/challenges", tags=["Challenges"])
app.include_router(collectors.router, prefix="/api/collectors", tags=["Collectors"])


