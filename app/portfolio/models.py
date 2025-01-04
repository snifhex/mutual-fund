from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, DateTime, Float, ForeignKey, String
from sqlalchemy.orm import relationship

from app.core.database.db import Base


class Portfolio(Base):
    __tablename__ = "portfolios"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(String, ForeignKey("users.id"))
    total_value = Column(Float, default=0.0)
    last_updated = Column(DateTime, default=datetime.now())

    investments = relationship("Investment", back_populates="portfolio")


class Investment(Base):
    __tablename__ = "investments"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    portfolio_id = Column(String, ForeignKey("portfolios.id"))
    scheme_id = Column(String, ForeignKey("mutual_fund_schemes.id"))
    units = Column(Float)
    purchase_price = Column(Float)
    current_price = Column(Float)
    purchase_date = Column(DateTime, default=datetime.now())
    last_updated = Column(DateTime, default=datetime.now())

    portfolio = relationship("Portfolio", back_populates="investments")
