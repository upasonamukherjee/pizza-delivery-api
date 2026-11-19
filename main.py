from fastapi import FastAPI
from auth_routes import auth_router
from order_routes import order_router

app = FastAPI(
    title="Pizza Delivery API",
    description=(
        "A REST API for ordering pizza.\n\n"
        "**Features:** user signup and login with JWT access and refresh tokens, "
        "placing, viewing, updating and deleting orders, and staff-only order management.\n\n"
        "To try protected routes, log in at `/auth/login`, then click **Authorize** "
        "and paste the access token."
    ),
    version="1.0.0",
)

app.include_router(auth_router)
app.include_router(order_router)

