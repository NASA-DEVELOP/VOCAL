from sqlalchemy import Integer, String, Column
from sqlalchemy.ext.declarative import declarative_base

dbBase = declarative_base()

class dbPolygon(dbBase):
    __tablename__ = 'objects'
    
    id = Column(Integer, primary_key=True)
    vertices = Column(String)
    color = Column(String)
    
    def __repr__(self):
        return "<Polygon(vertices='%s', color='%s')>" % (self.vertices, self.color)