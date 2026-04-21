from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from starlette import status
from ..database import get_db
from ..models.incident import Incident
from ..schemas.incident import IncidentCreate, IncidentUpdate, IncidentResponse, DashboardResponse
from ..services.ai_service import get_ai_response
from .auth import get_current_user

router = APIRouter(prefix='/incidents', tags=['incidents'])

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=IncidentResponse)
async def create_incident(user: user_dependency, db: db_dependency,
                          incident_request: IncidentCreate):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    ai_result = get_ai_response(incident_request.issue_description)

    incident = Incident(
        title=incident_request.title,
        issue_description=incident_request.issue_description,
        ai_response=ai_result["ai_response"],
        severity=ai_result["severity"],
        status="OPEN",
        owner_id=user.get('id')
    )
    db.add(incident)
    db.commit()
    db.refresh(incident)
    return incident


@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_incidents(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return db.query(Incident).filter(Incident.owner_id == user.get('id')).all()


@router.get("/dashboard", status_code=status.HTTP_200_OK)
async def get_dashboard(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    user_id = user.get('id')
    total = db.query(Incident).filter(Incident.owner_id == user_id).count()
    open_inc = db.query(Incident).filter(Incident.owner_id == user_id,
                                         Incident.status == 'OPEN').count()
    resolved = db.query(Incident).filter(Incident.owner_id == user_id,
                                         Incident.status == 'RESOLVED').count()
    high = db.query(Incident).filter(Incident.owner_id == user_id,
                                     Incident.severity == 'HIGH').count()
    medium = db.query(Incident).filter(Incident.owner_id == user_id,
                                       Incident.severity == 'MEDIUM').count()
    low = db.query(Incident).filter(Incident.owner_id == user_id,
                                    Incident.severity == 'LOW').count()
    return {
        "total_incidents": total,
        "open_incidents": open_inc,
        "resolved_incidents": resolved,
        "high_severity": high,
        "medium_severity": medium,
        "low_severity": low
    }


@router.get("/{incident_id}", status_code=status.HTTP_200_OK)
async def get_incident(user: user_dependency, db: db_dependency,
                       incident_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    incident = db.query(Incident).filter(
        Incident.id == incident_id,
        Incident.owner_id == user.get('id')).first()
    if incident is None:
        raise HTTPException(status_code=404, detail='Incident not found')
    return incident


@router.patch("/{incident_id}/status", status_code=status.HTTP_200_OK)
async def update_incident_status(user: user_dependency, db: db_dependency,
                                 incident_update: IncidentUpdate,
                                 incident_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    incident = db.query(Incident).filter(
        Incident.id == incident_id,
        Incident.owner_id == user.get('id')).first()
    if incident is None:
        raise HTTPException(status_code=404, detail='Incident not found')
    incident.status = incident_update.status
    db.add(incident)
    db.commit()
    return {"message": "Incident status updated successfully"}


@router.delete("/{incident_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_incident(user: user_dependency, db: db_dependency,
                          incident_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    incident = db.query(Incident).filter(
        Incident.id == incident_id,
        Incident.owner_id == user.get('id')).first()
    if incident is None:
        raise HTTPException(status_code=404, detail='Incident not found')
    db.delete(incident)
    db.commit()