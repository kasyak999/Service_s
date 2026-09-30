from fastapi import FastAPI
from sqladmin import Admin

from app.core.config import settings
from app.core.db import engine
from app.core.admin import UserAdmin, PartsRequestAdmin, ServiceCenterAdmin


app = FastAPI()
admin = Admin(
    app,
    engine,
    # authentication_backend=AdminAuth(secret_key=settings.secret),
    # templates_dir=templates_dir,
    title=settings.app_title,
)
admin.add_view(UserAdmin)
admin.add_view(PartsRequestAdmin)
admin.add_view(ServiceCenterAdmin)

@app.get('/')
def read_root():
    return {'Hello': 'FastAPI1111111111'}
