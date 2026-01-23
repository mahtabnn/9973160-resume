from pydantic import BaseModel

class ProjectRequest(BaseModel):
    name: str
    email: str
    project_type: str
    budget: str
    description: str
