from datetime import datetime
from uuid import uuid4

from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, String
from sqlalchemy.orm import relationship

from app.core.database.db import Base


class MutualFundFamily(Base):
    __tablename__ = "mutual_fund_families"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    name = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True)
    last_synced = Column(DateTime, nullable=True)

    schemes = relationship("MutualFundScheme", back_populates="fund_family")


class MutualFundScheme(Base):
    __tablename__ = "mutual_fund_schemes"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    scheme_code = Column(String, unique=True, index=True)
    isin_payout = Column(String, nullable=True)
    isin_reinvestment = Column(String, nullable=True)
    scheme_name = Column(String)
    scheme_type = Column(String)
    scheme_category = Column(String)
    fund_family_id = Column(String, ForeignKey("mutual_fund_families.id"))

    last_nav = Column(Float, nullable=True)
    last_nav_date = Column(DateTime, nullable=True)
    nav_last_updated = Column(DateTime, nullable=True, onupdate=datetime.now)

    fund_family = relationship("MutualFundFamily", back_populates="schemes")
