from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from api.routes import router
# from minimal import router as test
# print("Imported router object:", id(router), router)
# print("Number of routes in imported router:", len(router.routes))
app = FastAPI()

app.include_router(router, prefix="/api")

app.mount("/", StaticFiles(directory="static", html=True), name="static")

@app.get("/test")
def test():
    return {"message": "Direct route works hbjkas[asasnaisak"}

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Server is runnisdsdn"}

# @app.post("/send_location")
# async def post_test():
#     return {"status": "post received"}
