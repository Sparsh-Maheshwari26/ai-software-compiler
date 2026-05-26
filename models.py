from pydantic import BaseModel, Field
from typing import List, Optional

class DBColumn(BaseModel):
    name: str
    type: str  # e.g., String, Integer, Boolean

class DBTable(BaseModel):
    name: str
    columns: List[DBColumn]

class APIEndpoint(BaseModel):
    path: str
    method: str
    description: str

class UIComponent(BaseModel):
    page: str
    element: str  # e.g., Navbar, Table, Button
    action: str

class AppConfig(BaseModel):
    app_name: str
    database: List[DBTable]
    api: List[APIEndpoint]
    ui: List[UIComponent]
    auth_required: bool