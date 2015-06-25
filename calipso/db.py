###################################
#    Created on Jun 16, 2015
#
#    @author: Grant Mercer
###################################

# import antigravity
import json
import re
import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer, String, desc
import constants
from tools.tools import byteify

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
        return constants.PLOTS[i]
    
    def __repr__(self):
        '''
        Represent the database class as a JSON object. Useful as our program
        already supporst JSON reading, so simply parse out the database as 
        seperate JSON 'files'
        '''
        data = {}
        for i in range(0,len(constants.PLOTS)):
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
        return byteify(json.dumps(data))


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
        path = os.path.dirname(os.path.realpath(__file__)) + "\\..\\db\\CALIPSOdb.db"
        self.__dbEngine = create_engine('sqlite:///' + path, echo=False)
        self.__Session = sessionmaker(bind=self.__dbEngine)
        dbBase.metadata.create_all(self.__dbEngine)
    
    def queryUniqueTag(self):
        '''
        Grabs a session and queries the database to find the starting tag for the application.
        this tag is used so it does not overlap existing shape tags previously generated
        and stored into the database
        '''
        session = self.__Session()
        objs = session.query(dbPolygon).order_by(desc(dbPolygon.tag))
        if objs.count() == 0:
            tag = 0
        else:
            tag = int(re.search('(\d+)$', objs.first().tag).group(0)) + 1
        session.close()
        return tag
        #print tag
        #return tag
    
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
        :param polyList: the current polygonList corresponding to the active plot
        :param time: time of the JSON's creation
        :param f: file name
        '''
        session = self.__Session()
        for polygon in polyList[:-1]:
            if polygon.getID() is None:
                obx = \
                    dbPolygon(tag=polygon.getTag(),
                              time_=time,
                              hdf=f.rpartition('/')[2],
                              plot=polygon.getPlot(),
                              vertices=str(polygon.getVertices()), 
                              color=polygon.getColor(),
                              attributes=str(polygon.getAttributes()),
                              coordinates=str(polygon.getCoordinates()),
                              notes=polygon.getNotes())
                polygon.setID(1)
                session.add(obx)
                
            else:
                poly = session.query(dbPolygon).get(polygon.getID())
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
    
    def deleteItem(self, idx):
        '''
        Get a session and delete the object from the database.
        :param indx: the primary key for the object passed
        '''
        session = self.__Session()
        item = session.query(dbPolygon).get(idx)
        session.delete(item)
        session.commit()
        session.close()
    
    def encode(self, filename, data):
        '''
        Encode and write out a JSON object
        :param filename: name of the file
        :param data: Python dictionary representation of a JSON
        '''
        with open(filename, 'w') as outfile:
            json.dump(data, outfile)
                

# define the global database manager object
db = DatabaseManager()