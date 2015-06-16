'''
Created on Jun 11, 2015

@author: nqian
@author: Grant Mercer

'''
# import antigravity
import json
from Tkinter import Message, Toplevel, Button
#from CALIPSO_Visualization_Tool import dbBase

import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from dbPolygon import dbBase, dbPolygon

class PolygonWriter(object):
    '''
    classdocs
    '''

    __dbEngine = create_engine('sqlite:///../db/CALIPSOdb.db', echo=True)

    def __init__(self, fileName="objs/polygons.json"):
        '''
        Constructor
        '''
        self.__fileName = fileName
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
        
    def getJsonFile(self):
        return self.__fileName
    
    def getPlotType(self):
        return self.__plotType
    
    def getHDFFile(self):
        return self.__hdf
        
    def getDictionary(self):
        return self.__dict
    
    def encode(self, data):
        with open(self.__fileName, 'w') as outfile:
            json.dump(data, outfile)
        
    def reset(self):
        for key in self.__dict:
            if key is not "HDFFile" or key is not "plotype":
                del key