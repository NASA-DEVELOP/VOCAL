'''
Created on Jun 11, 2015

@author: nqian
@author: Grant Mercer

'''
# import antigravity
import json
#from CALIPSO_Visualization_Tool import dbBase
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

dbBase = declarative_base()

class dbPolygon(dbBase):
    __tablename__ = 'objects'
    
    id = Column(Integer, primary_key=True)
    vertices = Column(String)
    color = Column(String)
    
    def __repr__(self):
        return "<Polygon(vertices='%s', color='%s')>" % (self.vertices, self.color)

class DatabaseManager(object):
    '''
    classdocs
    '''

    __dbEngine = create_engine('sqlite:///../db/CALIPSOdb.db', echo=True)

    def __init__(self):
        '''
        Constructor
        '''
        
        self.__plotType = 0
        self.__hdf = ''
        self.__dict = {}
        
        dbBase.metadata.create_all(self.__dbEngine)  # @UndefinedVariable
        
        self.__Session = sessionmaker(bind=self.__dbEngine)
        
        #delete empty objects and display database
        session = self.__Session()
        #for db in session.query(dbPolygon).filter_by(color='').all():
        #    session.delete(db)
        #session.commit()
        
        lst = session.query(dbPolygon).all()
        print lst
        session.close()
        
    def createTable(self):
        dbBase.metadata.create_all(self.__dbEngine)
        
    def notifyDeletion(self, polygon):
        session = self.__Session()
        session.delete(
            dbPolygon(vertices=str(polygon.getVertices()), color=(polygon.getColor())))
        session.commit()
        session.close()
        
    def commitToDB(self, polyList):
        session = self.__Session()
        for polygon in polyList[:-1]:
            if polygon.getVertices != None:
                session.add(
                    dbPolygon(vertices=str(polygon.getVertices()), color=polygon.getColor()))
        session.commit()
        session.close()
        
    def setJsonFile(self, fileName):
        self.__fileName = fileName
        
    def setPlotType(self, plotType):
        self.__plotType = plotType
        
    def setHDFFile(self, hdf):
        self.__hdf = hdf
    
    def getPlotType(self):
        return self.__plotType
    
    def getHDFFile(self):
        return self.__hdf
        
    def getDictionary(self):
        return self.__dict
    
    def encode(self, filename, data):
        with open(filename, 'w') as outfile:
            json.dump(data, outfile)
        
    def reset(self):
        for key in self.__dict:
            if key is not "HDFFile" or key is not "plotype":
                del key
                
dbManager = DatabaseManager()