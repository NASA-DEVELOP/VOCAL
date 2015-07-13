###################################
#   Created on Jun 16, 2015
#
#   @author: Grant Mercer
###################################

# import antigravity
import json
import os
import re
import constants

from sqlalchemy import create_engine, Column, Integer, String, desc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from tools.tools import byteify
from log import logger

# Create a declarative_base for dbPolygon to inherit from
dbBase = declarative_base()


class DatabasePolygon(dbBase):
    """
    Sqlalchemy class object, contains all data that is stored inside the database.
    Objects are represented as JSON

    .. py:data:: id
    .. py:data:: tag
    .. py:data:: color
    .. py:data:: time_
    .. py:data:: hdf
    .. py:data:: plot
    .. py:data:: attributes
    .. py:data:: coordinates
    .. py:data:: notes
    """
    __tablename__ = 'objects'

    id = Column(Integer, primary_key=True)  # primary key
    tag = Column(String)  # shape tag
    color = Column(String)  # color of polygon
    time_ = Column(String)  # time object was exported
    hdf = Column(String)  # filename
    plot = Column(String)  # type of plot drawn on
    attributes = Column(String)  # list of object attributes
    coordinates = Column(String)  # plot coordinates for displaying to user
    notes = Column(String)  # shape notes

    @staticmethod
    def plot_string(i):
        return constants.PLOTS[i]

    def __repr__(self):
        """
        Represent the database class as a JSON object. Useful as our program
        already supports JSON reading, so simply parse out the database as
        separate JSON 'files'
        """
        data = {}
        for key in constants.plot_type_enum:
            data[key] = {}
        data[self.plot] = {self.tag: {
            'color': self.color,
            'attributes': self.attributes,
            'id': self.id,
            'coordinates': self.coordinates,
            'notes': self.notes}}
        data['time'] = self.time_
        data['hdfFile'] = self.hdf
        logger.info('Converting from unicode to ASCII')
        return byteify(json.dumps(data))


class DatabaseManager(object):
    """
    Internally manages the database engine and any sql related objects.
    Hands out sessions with getSession() but only offers abstractions for
    other functionality. The database is INDEPENDENT from the application
    """

    def __init__(self):
        """
        Create the database engine using db/CALIPSO.db database.
        Echo all commands, create Session and table
        """
        logger.info('Instantiating DatabaseManager')
        path = os.path.dirname(os.path.realpath(__file__)) + r'./../db/CALIPSOdb.db'
        self.__dbEngine = create_engine('sqlite:///' + path, echo=False)
        self.__Session = sessionmaker(bind=self.__dbEngine)
        dbBase.metadata.create_all(self.__dbEngine)

    def query_unique_tag(self):
        """
        Grabs a session and queries the database to find the starting tag for the application.
        this tag is used so it does not overlap existing shape tags previously generated
        and stored into the database
        """
        session = self.__Session()
        # Grab db objects sorted by tag
        db_objects = session.query(DatabasePolygon).order_by(desc(DatabasePolygon.tag))
        # If database is empty, set tag to 0
        if db_objects.count() == 0:
            logger.info('No tags found, setting base case')
            tag = 0
        else:
            logger.info('Tag found')
            tag = int(re.search('(\d+)$', db_objects.first().tag).group(0)) + 1
        session.close()
        logger.info('Found unique tag %s' % tag)
        return tag

    def exists_tag(self, tag):
        """
        Check the database if a tag currently exists, if so return True, else
        return False

        :rtype: :py:class:`bool`
        """
        session = self.__Session()
        query = session.query(DatabasePolygon).filter_by(tag=tag)
        if query is None:
            session.close()
            return False
        session.close()
        return True

    def get_session(self):
        """
        Returns an instance of a session, USERS job to ensure session
        is committed/closed
        """
        logger.info('Getting session')
        return self.__Session()

    def commit_to_db(self, poly_list, time, f):
        """
        Takes a list of polygons and commits them into the database,
        used in polygonList to commit all visible polygons

        :param poly_list: the current polygonList corresponding to the active plot
        :param time: time of the JSON's creation
        :param f: file name
        """
        logger.info('Committing to database')
        session = self.__Session()
        # For every polygon object in the list except the end
        for polygon in poly_list[:-1]:
            if polygon.get_id() is None:
                obx = \
                    DatabasePolygon(tag=polygon.get_tag(),
                                    time_=time,
                                    hdf=f.rpartition('/')[2],
                                    plot=polygon.get_plot().name,
                                    color=polygon.get_color(),
                                    attributes=str(polygon.get_attributes()),
                                    coordinates=str(polygon.get_coordinates()),
                                    notes=polygon.get_notes())
                polygon.set_id(1)
                session.add(obx)

            else:
                poly = session.query(DatabasePolygon).get(polygon.get_id())
                if poly is None:
                    continue
                poly.time_ = time
                poly.plot = polygon.get_plot()
                poly.hdf = f.rpartition('/')[2]
                poly.plot = polygon.get_plot().name
                poly.color = unicode(polygon.get_color())
                poly.attributes = str(polygon.get_attributes())
                poly.coordinates = str(polygon.get_coordinates())
                poly.notes = polygon.get_notes()
        session.commit()
        session.close()

    def delete_item(self, idx):
        """
        Get a session and delete the object from the database.

        :param idx: the primary key for the object passed
        """
        logger.info('Deleting database entry')
        session = self.__Session()
        item = session.query(DatabasePolygon).get(idx)
        if item is not None:
            logger.error('Entry %d can not be deleted, query returned None' % idx)
            session.delete(item)
        logger.info('Committing database')
        session.commit()
        session.close()

    @staticmethod
    def encode(filename, data):
        """
        Encode and write out a JSON object

        :param filename: name of the file
        :param data: Python dictionary representation of a JSON
        """
        with open(filename, 'w') as outfile:
            json.dump(data, outfile)
        logger.info('Successfully encoded')

# define the global database manager object
db = DatabaseManager()
