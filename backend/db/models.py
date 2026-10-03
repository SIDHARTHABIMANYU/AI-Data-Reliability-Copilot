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