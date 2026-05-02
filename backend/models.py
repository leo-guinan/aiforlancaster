"""
SQLAlchemy models for Bottega Bodega membership database.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, Text, JSON, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

class Member(Base):
    __tablename__ = 'members'
    
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False, index=True)
    name = Column(String, nullable=True)
    tier = Column(String, nullable=False)  # 'mallrat' | 'dining_club'
    stripe_customer_id = Column(String, unique=True, nullable=True)
    stripe_payment_id = Column(String, unique=True, nullable=False)
    joined_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    content_deliveries = relationship('MallratContentDelivery', back_populates='member')
    wall_entries = relationship('WallEntry', back_populates='member')
    ballads = relationship('MarvinBallad', back_populates='member')
    rsvps = relationship('EventRSVP', back_populates='member')

class MallratContent(Base):
    __tablename__ = 'mallrat_content'
    
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    file_path = Column(String, nullable=False)  # path to content file on disk
    note_text = Column(Text, nullable=False)    # handwritten-style note
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    active = Column(Boolean, default=True)
    
    deliveries = relationship('MallratContentDelivery', back_populates='content')

class MallratContentDelivery(Base):
    __tablename__ = 'mallrat_deliveries'
    
    id = Column(Integer, primary_key=True)
    member_id = Column(Integer, ForeignKey('members.id'), nullable=False)
    content_id = Column(Integer, ForeignKey('mallrat_content.id'), nullable=False)
    delivered_at = Column(DateTime, default=datetime.utcnow)
    access_token = Column(String, unique=True, nullable=False)  # for secure download
    viewed = Column(Boolean, default=False)
    
    member = relationship('Member', back_populates='content_deliveries')
    content = relationship('MallratContent', back_populates='deliveries')

class DiningEvent(Base):
    __tablename__ = 'dining_events'
    
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    date = Column(DateTime, nullable=False)
    location = Column(String, nullable=True)
    capacity = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    rsvps = relationship('EventRSVP', back_populates='event')

class EventRSVP(Base):
    __tablename__ = 'event_rsvps'
    
    id = Column(Integer, primary_key=True)
    member_id = Column(Integer, ForeignKey('members.id'), nullable=False)
    event_id = Column(Integer, ForeignKey('dining_events.id'), nullable=False)
    rsvp_at = Column(DateTime, default=datetime.utcnow)
    attended = Column(Boolean, default=False)
    notes = Column(Text, nullable=True)
    
    member = relationship('Member', back_populates='rsvps')
    event = relationship('DiningEvent', back_populates='rsvps')

class WallEntry(Base):
    __tablename__ = 'wall_entries'
    
    id = Column(Integer, primary_key=True)
    member_id = Column(Integer, ForeignKey('members.id'), nullable=False)
    image_url = Column(String, nullable=False)  # path on server or URL
    caption = Column(String, nullable=True)
    installed_at = Column(DateTime, nullable=True)  # when put on wall
    created_at = Column(DateTime, default=datetime.utcnow)
    is_visible = Column(Boolean, default=True)
    
    member = relationship('Member', back_populates='wall_entries')

class MarvinBallad(Base):
    __tablename__ = 'marvin_ballads'
    
    id = Column(Integer, primary_key=True)
    member_id = Column(Integer, ForeignKey('members.id'), nullable=False)
    prompt = Column(Text, nullable=False)
    audio_url = Column(String, nullable=True)
    status = Column(String, default='queued')  # queued | processing | complete | error
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    error_message = Column(Text, nullable=True)
    
    member = relationship('Member', back_populates='ballads')

def init_db(engine=None):
    """Create all tables."""
    if engine is None:
        from config import Config
        engine = create_engine(Config.DATABASE)
    Base.metadata.create_all(engine)
    return engine
