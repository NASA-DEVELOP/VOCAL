'''
Created on Jun 16, 2015

@author: Grant Mercer

'''
# import antigravity
import json

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer, String

# Create a declarative_base for dbPolygon to inherit from
dbBase = declarative_base()

class dbPolygon(dbBase):
    __tablename__ = 'objects'
    
    id = Column(Integer, primary_key=True)  # primary key
    vertices = Column(String)               # array of vertices, passed as string
    color = Column(String)                  # color of polygon
    time_ = Column(String)                  # time object was exported
    hdf = Column(String)                    # filename
    plot = Column(Integer)                  # type of plot drawn on
    
    #represent the data in JSON
    def __repr__(self):
        return json.JSONEncoder().encode({"plot":self.plot,
                                          "time":self.time_,
                                          "file":self.hdf, 
                                          "vetices":self.vertices, 
                                          "color":self.color})

# Internally manages the data base and offers abstractions to talk with it
class DatabaseManager(object):

    def __init__(self):
        # Create engine, session and generate table
        self.__dbEngine = create_engine('sqlite:///../db/CALIPSOdb.db', echo=True)
        self.__Session = sessionmaker(bind=self.__dbEngine)
        dbBase.metadata.create_all(self.__dbEngine)
                
    """
    def notifyDeletion(self, polygon):
        session = self.__Session()
        session.delete(
            dbPolygon(vertices=str(polygon.getVertices()), color=(polygon.getColor())))
        session.commit()
        session.close()
    """
    
    # Return an instance of a session, USERS job to ensure session is
    # committed/closed
    def getSession(self):
        return self.__Session()
        
    # Takes a list of polygons and commits them into the database, used
    # in polygonList to commit all visible polygons
    def commitToDB(self, polyList, time, f):
        session = self.__Session()
        for polygon in polyList[:-1]:
            if polygon.getVertices != None:
                session.add(
                    dbPolygon(time_=time,
                              hdf=f.rpartition('/')[2],
                              plot=polygon.getPlot(),
                              vertices=str(polygon.getVertices()), 
                              color=polygon.getColor()))
        session.commit()
        session.close()
    
    # Encode and write out a JSON object, currently still supported
    # but expect DEPRECATED
    def encode(self, filename, data):
        with open(filename, 'w') as outfile:
            json.dump(data, outfile)
                

db = DatabaseManager()