from sqlalchemy import Column, Integer, String, Date, DateTime
from backend.db.database import Base


class PipelineRun(Base):
    __tablename__ = "pipeline_runs"

    run_id = Column(Integer, primary_key=True, index=True)
    dataset = Column(String(50), nullable=False)
    file_name = Column(String(255), nullable=False)
    run_date = Column(Date, nullable=False)
    row_count = Column(Integer)
    status = Column(String(20), nullable=False)
    started_at = Column(DateTime)
    completed_at = Column(DateTime)

class Incident(Base):
    __tablename__ = "incidents"

    incident_id = Column(Integer, primary_key=True, index=True)
    dataset = Column(String(50), nullable=False)
    file_name = Column(String(255), nullable=False)
    incident_type = Column(String(50), nullable=False)
    severity = Column(String(20), nullable=False)
    description = Column(String(1000), nullable=False)
    status = Column(String(20), nullable=False)
    detected_at = Column(DateTime, nullable=False)
    resolved_at = Column(DateTime, nullable=True)