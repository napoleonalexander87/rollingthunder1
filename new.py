from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routes import router
# from minimal import router as test
# print("Imported router object:", id(router), router)
# print("Number of routes in imported router:", len(router.routes))
app = FastAPI()

# Mount static folder at root → serves index.html automatically
app.mount("/", StaticFiles(directory="static", html=True), name="static")

# Include router with prefix (redirect_slashes already disabled on router itself)
app.include_router(router)

@app.on_event("startup")
async def startup_event():
    print("=== Startup Diagnostics ===")
    print("Raw router paths (without prefix):")
    print("server is running")
    for r in router.routes:
        print(f"  - {r.path} ({r.methods})")

    print("\nApp routes after include_router (should have /api prefix):")
    for r in app.routes:
        if hasattr(r, 'path') and r.path.startswith('/api'):
            print(f"  - {r.path} ({r.methods})")

    if not any(r.path.startswith('/api') for r in app.routes if hasattr(r, 'path')):
        print("WARNING: No /api routes found in app.routes → router was NOT included!")
@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Server is runnin"}