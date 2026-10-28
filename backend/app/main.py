from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from .database import Base, engine
from .routes import router
from .seed import seed

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Hotel Reservas API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")

@app.on_event("startup")
def startup():
    seed()


@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")
