'''
Created on Jun 16, 2015

@author: Grant Mercer

'''
# import antigravity
import json

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer, String
from gui import Constants

# Create a declarative_base for dbPolygon to inherit from
dbBase = declarative_base()

class dbPolygon(dbBase):
    '''
    Sqlalchemy class object, contains all data that is stored inside the database
    '''
    __tablename__ = 'objects'
    
    id = Column(Integer, primary_key=True)  # primary key
    tag = Column(String)                    # shape tag
    color = Column(String)                  # color of polygon
    vertices = Column(String)               # array of vertices, passed as string
    time_ = Column(String)                  # time object was exported
    hdf = Column(String)                    # filename
    plot = Column(String)                   # type of plot drawn on
    attributes = Column(String)             # list of object attributes
    coordinates = Column(String)            # plot coordinates for displaying to user
    notes = Column(String)                   # shape notes
    
    @staticmethod
    def plotString(i):
        return Constants.PLOTS[i]
    
    def __repr__(self):
        '''
        Represent the database class as a JSON object. Useful as our program
        already supporst JSON reading, so simply parse out the database as 
        seperate JSON 'files'
        '''
        data = {}
        for i in range(0,len(Constants.PLOTS)):
            data[self.plotString(i)] = {}
        data[self.plot] = {self.tag : 
            {"vertices":self.vertices, 
             "color":self.color, 
             "attributes":self.attributes, 
             "id": self.id,
             "coordinates":self.coordinates,
             "notes":self.notes}}
        data["time"] = self.time_
        data["hdfFile"] = self.hdf
        return json.dumps(data)


class DatabaseManager(object):
    '''
    Internally manages the database engine and any sql related objects.
    Hands out sessions with getSession() but only offers abstractions for
    other functionality. The database is INDEPENDENT from the application
    '''
    def __init__(self):
        '''
        Create the database engine using db/CALIPSO.db database.
        Echo all commands, create Session and table
        '''
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
    
    def getSession(self):
        '''
        Returns an instance of a session, USERS job to ensure session
        is committed/closed
        '''
        return self.__Session()
        
    def commitToDB(self, polyList, time, f):
        '''
        Takes a list of polygons and commits them into the database,
        used in polygonList to commit all visible polygons
        '''
        session = self.__Session()
        for polygon in polyList[:-1]:
            if polygon.getID() is None:
                session.add(
                    dbPolygon(tag=polygon.getTag(),
                              time_=time,
                              hdf=f.rpartition('/')[2],
                              plot=polygon.getPlot(),
                              vertices=str(polygon.getVertices()), 
                              color=polygon.getColor(),
                              attributes=str(polygon.getAttributes()),
                              coordinates=str(polygon.getCoordinates()),
                              notes=polygon.getNotes()))
            else:
                poly = session.query(dbPolygon).get(polygon.getID())
                print poly
                poly.time_ = time
                poly.plot = polygon.getPlot()
                poly.hdf = f.rpartition('/')[2]
                poly.plot = polygon.getPlot()
                poly.vertices = str(polygon.getVertices())
                poly.color = unicode(polygon.getColor())
                poly.attributes = str(polygon.getAttributes())
                poly.coordinates = str(polygon.getCoordinates())
                poly.notes = polygon.getNotes()
        session.commit()
        session.close()
    
    def encode(self, filename, data):
        '''
        Encode and write out a JSON object
        '''
        with open(filename, 'w') as outfile:
            json.dump(data, outfile)
                

# define the global database manager object
db = DatabaseManager()