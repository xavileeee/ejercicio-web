"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Club de Ajedrez": {
        "description": "Aprende estrategias y compite en torneos de ajedrez",
        "schedule": "Viernes, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["carlos@mergington.edu", "lucia@mergington.edu"]
    },
    "Clase de Programación": {
        "description": "Aprende fundamentos de programación y desarrolla proyectos",
        "schedule": "Martes y Jueves, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["ana@mergington.edu", "isabel@mergington.edu"]
    },
    "Educación Física": {
        "description": "Actividades deportivas y educación física",
        "schedule": "Lunes, Miércoles y Viernes, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["diego@mergington.edu", "paula@mergington.edu"]
    },
    "Club de Robótica": {
        "description": "Diseña y construye robots innovadores",
        "schedule": "Miércoles, 4:00 PM - 5:30 PM",
        "max_participants": 15,
        "participants": ["jorge@mergington.edu"]
    },
    "Taller de Artes": {
        "description": "Expresión artística a través de pintura y escultura",
        "schedule": "Jueves, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["maria@mergington.edu", "alejandra@mergington.edu"]
    },
    "Club de Debate": {
        "description": "Desarrolla habilidades de oratoria y argumentación",
        "schedule": "Martes, 4:00 PM - 5:30 PM",
        "max_participants": 20,
        "participants": ["pedro@mergington.edu"]
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    # Normalize email (strip spaces, lowercase) and simple validation
    email = email.strip().lower()
    # Validar email format (simple check)
    if "@" not in email or "." not in email:
        raise HTTPException(status_code=400, detail="Invalid email format")     
    
    # Validar que no se haya inscrito ya
    if email in activities[activity_name]["participants"]:
        raise HTTPException(status_code=400, detail="Student already signed up for this activity")  

    # Get the specific activity
    activity = activities[activity_name]

    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}
