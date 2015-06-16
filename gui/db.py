'''
Created on Jun 16, 2015

@author: Grant Mercer

'''
# import antigravity
import json

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer, String

dbBase = declarative_base()

class dbPolygon(dbBase):
    __tablename__ = 'objects'
    
    id = Column(Integer, primary_key=True)
    vertices = Column(String)
    color = Column(String)
    time_ = Column(String)
    hdf = Column(String)
    plot = Column(Integer)
    
    def __repr__(self):
        return json.JSONEncoder().encode({"plot":self.plot,
                                          "time":self.time_,
                                          "file":self.hdf, 
                                          "vetices":self.vertices, 
                                          "color":self.color})

class DatabaseManager(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.__plotType = 0
        self.__hdf = ''
        self.__dict = {}

        self.__dbEngine = create_engine('sqlite:///../db/CALIPSOdb.db', echo=True)
        self.__Session = sessionmaker(bind=self.__dbEngine)
        dbBase.metadata.create_all(self.__dbEngine)
                
    def notifyDeletion(self, polygon):
        session = self.__Session()
        session.delete(
            dbPolygon(vertices=str(polygon.getVertices()), color=(polygon.getColor())))
        session.commit()
        session.close()
    
    def getSession(self):
        return self.__Session()
        
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
    
    def encode(self, filename, data):
        with open(filename, 'w') as outfile:
            json.dump(data, outfile)
        
    def reset(self):
        for key in self.__dict:
            if key is not "HDFFile" or key is not "plotype":
                del key
                

db = DatabaseManager()