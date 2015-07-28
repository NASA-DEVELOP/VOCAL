###################################
#   Created on Jun 16, 2015
#
#   @author: Grant Mercer
###################################

# import antigravity
import json
import os
import re
import zipfile
import shutil
import ast

import constants
from tools.tools import zipdir
from constants import PATH
from sqlalchemy import create_engine, Column, Integer, String, func, NUMERIC
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from tools.tools import byteify
from log.log import logger


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
    lat = Column(String)

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
            'lat': self.lat,
            'notes': self.notes}}
        data['time'] = self.time_
        data['hdfFile'] = self.hdf
        logger.info('Converting unicode to ASCII')
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
        path = os.path.dirname(os.path.realpath(__file__)) + './../db/CALIPSOdb.db'
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
        # Grab db objects sorted by a tags NUMERIC portion, not the shape portion
        db_objects = session.query(DatabasePolygon).order_by(
            func.cast(func.replace(DatabasePolygon.tag, 'shape', ''),
                      NUMERIC).desc())

        # If database is empty, set tag to 0, otherwise get the number potion of
        # the shape with the highest numeric value and start there
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
        # for every polygon object in the list except the end
        for polygon in poly_list[:-1]:
            # if the ID does not exist we have a new object to commit
            if polygon.get_id() is None:
                logger.debug('committing new shape: %s' % polygon.get_tag())
                lat = polygon.generate_lat_range()
                obx = \
                    DatabasePolygon(tag=polygon.get_tag(),
                                    time_=time,
                                    hdf=f.rpartition('/')[2],
                                    plot=constants.PLOTS[polygon.get_plot()],
                                    color=polygon.get_color(),
                                    attributes=str(polygon.get_attributes()),
                                    coordinates=str(polygon.get_coordinates()),
                                    lat=lat,
                                    notes=polygon.get_notes())
                session.add(obx)
                session.commit()
                polygon.set_id(obx.id)
            # otherwise we simply update the entries of the existing database object
            else:
                logger.debug('updating existing entry: %s' % polygon.get_tag())
                poly = session.query(DatabasePolygon).get(polygon.get_id())
                if poly is None:
                    logger.critical('This should never happen, why did it happen?')
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
            if not polygon.get_saved():
                polygon.save()
        session.close()

    def delete_item(self, idx):
        """
        Get a session and delete the object from the database.

        :param idx: the primary key for the object passed
        """
        session = self.__Session()
        # search for item by unique db ID
        item = session.query(DatabasePolygon).get(idx)
        if item is not None:
            logger.info('Deleting %s' % item.tag)
            session.delete(item)
        else:
            logger.error('%s can not be deleted, query returned None' % item.tag)
            logger.error('You\'ve likely gotten this error because multiple shapes' +
                         'are sharing the same tag, this is BAD and means the code' +
                         'is bugged, fix it!')
        logger.info('Committing database')
        session.commit()
        session.close()

    def dump_to_json(self, zip_fname):
        """
        Dump the contents of the database into a JSON file with the specific format
        of DatabasePolygon. Creates a directory '{PROJECT}/tmp' and exports all db
        objects to it, then zips the directory and deletes tmp. Returns ``True`` on
        success, ``False`` otherwise

        :param str zip_fname: name of the zip file
        :rtype: bool
        """
        session = self.__Session()
        # tmp should not previously exist because we don't want files we didn't
        # add ourselves
        if os.path.exists(PATH + '/../tmp'):
            logger.error('Tmp directory should not exist, will not zip')
            return False
        logger.info('Creating /tmp and exporting shapes')
        os.makedirs(PATH + '/../tmp')
        for shape in session.query(DatabasePolygon).order_by(DatabasePolygon.tag):
            self.encode(PATH + '/../tmp/' + shape.tag + '.json', str(shape))
        logger.info('Packing /tmp into %s' % zip_fname)
        zipf = zipfile.ZipFile(zip_fname, 'w')
        zipdir(PATH + '/../tmp', zipf)
        zipf.close()
        shutil.rmtree(PATH + '/../tmp')
        session.close()
        return True

    def import_from_json(self, zip_fname):
        """
        Import a *.zip* file selected by the user, the zip file must be
        the same format as how ``dump_to_json`` creates a zip, otherwise
        an error will be raised. Uses functionality similar to ``ShapeReader``,
        but as db should **never** be dependent on another class we need to
        impl our own import method. The big difference here is that shapes
        are not added to the current shape list, instead are only loaded into
        the local database.

        :rtype: bool
        """
        session = self.__Session()

        zip_ref = zipfile.ZipFile(zip_fname, 'r')
        zip_ref.extractall(PATH + '/../tmp')
        zip_ref.close()

        logger.info('querying unique tag for new database objects')
        new = self.query_unique_tag()

        # walk through tmp, which is where we extracted the zip db to. for each file:
        # read the data into a literal_eval(string) -> dict, find the shape in the dict
        # and add to database, increment new tag
        for root, dirs, files in os.walk(PATH + '/../tmp'):
            for file_ in files:
                with open(os.path.join(root, file_), 'r') as ifile:
                    data = byteify(json.load(ifile))
                data = ast.literal_eval(data)
                keys = [x for x in data if x in constants.plot_type_enum.keys()]
                for key in keys:
                    for shape in data[key]:
                        fshape = data[key][shape]
                        tag = 'shape' + str(new)
                        time = data['time']
                        hdf = data['hdfFile']
                        color = fshape['color']
                        coordinates = fshape['coordinates']
                        attributes = fshape['attributes']
                        notes = fshape['notes']
                        lat = fshape['lat']

                        obx = \
                            DatabasePolygon(tag=tag,
                                            time_=time,
                                            hdf=hdf,
                                            plot=key,
                                            color=color,
                                            coordinates=coordinates,
                                            lat=lat,
                                            attributes=attributes,
                                            notes=notes)
                        session.add(obx)
                        new += 1
        session.commit()
        shutil.rmtree(PATH + '/../tmp')
        return True

    @staticmethod
    def encode(filename, data):
        """
        Encode and write out a JSON object

        :param filename: name of the file
        :param data: Python dictionary representation of a JSON
        """
        with open(filename, 'w') as outfile:
            json.dump(data, outfile)
        logger.info('Successfully encoded %s' % filename)

# define the global database manager object
db = DatabaseManager()

if __name__ == '__main__':
    pass
