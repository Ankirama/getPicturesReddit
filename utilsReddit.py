import re
import os
import logging

def extractAnimeName(title):
    '''
    @brief: Try to extract anime name in []
    example: 'Double docking [Kantai Collection][x-post from /r/kanmusu]' will return Kantai Collection
    'x-post from /r/kanmusu' is ignored
    @param title: title where we will extract anime
    @return False if any error or if anime not found, else anime name
    '''
    m = re.findall(r'(?<=\[)([- \w\/\'!]+)\]', title)
    if m != None:
        for s in m:
            if re.search('^x-post from', s) == None:
                logging.info("Anime extracted: %s", s)
                return s
    logging.warning("Unable to find an anime in %s", title)
    return False

def createFolder(name):
    '''
    @brief: check if path already exists, if not create folder
    @param name: path to create (folder)
    @return: True if already exists or created, False if any error
    '''
    if not os.path.exists(name):
        try:
            os.makedirs(name)
            logging.info("[%s]: Directory created", name)
            return True
        except OSError as e:
            logging.warning("Unable to create %s: %s", e)
            return False
    else:
        return True
