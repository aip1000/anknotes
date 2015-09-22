# -*- coding: utf-8 -*-
### Python Imports
try:
    from pysqlite2 import dbapi2 as sqlite
except ImportError:
    from sqlite3 import dbapi2 as sqlite

### Check if in Anki 
try:
    from aqt import mw    
    inAnki = True     
except: inAnki = False     
    
### Anknotes Imports
from anknotes.constants import *
from anknotes.logging import *
from anknotes.html import *
from anknotes.structs import *
from anknotes.db import *

### Anki and Evernote Imports
try:
    from aqt.qt import QIcon, QPixmap, QPushButton, QMessageBox
    from aqt.utils import tooltip
    from anknotes.evernote.edam.error.ttypes import EDAMSystemException, EDAMErrorCode, EDAMUserException, \
        EDAMNotFoundException
except:
    pass
    
# log('Checking for log at %s:\n%s' % (__name__,  dir(log)), 'import')
def get_friendly_interval_string(lastImport):
    if not lastImport: return ""
    td = (datetime.now() - datetime.strptime(lastImport, ANKNOTES.DATE_FORMAT))
    days = td.days
    hours, remainder = divmod(td.total_seconds(), 3600)
    minutes, seconds = divmod(remainder, 60)
    if days > 1:
        lastImportStr = "%d days" % td.days
    else:
        hours = round(hours)
        hours_str = '' if hours == 0 else ('1:%2d hr' % minutes) if hours == 1 else '%d Hours' % hours
        if days == 1:
            lastImportStr = "One Day%s" % ('' if hours == 0 else ', ' + hours_str)
        elif hours > 0:
            lastImportStr = hours_str
        else:
            lastImportStr = "%d:%02d min" % (minutes, seconds)
    return lastImportStr


class UpdateExistingNotes:
    IgnoreExistingNotes, UpdateNotesInPlace, DeleteAndReAddNotes = range(3)


class EvernoteQueryLocationType:
    RelativeDay, RelativeWeek, RelativeMonth, RelativeYear, AbsoluteDate, AbsoluteDateTime = range(6)


def get_tag_names_to_import(tagNames, evernoteTags=None, evernoteTagsToDelete=None, keepEvernoteQueryTags=True):
    if keepEvernoteQueryTags is None: keepEvernoteQueryTags =  mw.col.conf.get(SETTINGS.DELETE_EVERNOTE_TAGS_TO_IMPORT, True)    
    if not keepEvernoteQueryTags: return {} if isinstance(tagNames, dict) else []
    if evernoteTags is None: evernoteTags = mw.col.conf.get(SETTINGS.EVERNOTE_QUERY_TAGS, SETTINGS.EVERNOTE_QUERY_TAGS_DEFAULT_VALUE).split(",") 
    if evernoteTagsToDelete is None: evernoteTagsToDelete = mw.col.conf.get(SETTINGS.EVERNOTE_TAGS_TO_DELETE, "").split(",")
    tags_to_delete = evernoteTags + evernoteTagsToDelete
    if isinstance(tagNames, dict):        
        return {k: v for k, v in tagNames.items() if v not in tags_to_delete and (not hasattr(v, 'Name') or getattr(v, 'Name') not in tags_to_delete)}
    return sorted([v for v in tagNames if v not in tags_to_delete and (not hasattr(v, 'Name') or getattr(v, 'Name') not in tags_to_delete)],
                  key=lambda s: s.lower())

def find_evernote_guids(content):
    return [x.group('guid') for x in re.finditer(r'\b(?P<guid>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})\b', content)]

def find_evernote_links_as_guids(content):
    return [x.Guid for x in find_evernote_links(content)]

def replace_evernote_web_links(content):
    return re.sub(r'https://www.evernote.com/shard/(s\d+)/[\w\d]+/(\d+)/([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})',
                 r'evernote:///view/\2/\1/\3/\3/', content)

def find_evernote_links(content):
    """

    :param content:
    :return:
    :rtype : list[EvernoteLink]
    """
    # .NET regex saved to regex.txt as 'Finding Evernote Links'
    content = replace_evernote_web_links(content)
    regex_str = r'<a href="(?P<URL>evernote:///?view/(?P<uid>[\d]+?)/(?P<shard>s\d+)/(?P<guid>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/(?P=guid)/?)"(?:[^>]+)?>(?P<title>.+?)</a>'
    ids = get_evernote_account_ids()
    if not ids.valid:
        match = re.search(regex_str, content)
        if match:
            ids.update(match.group('uid'), match.group('shard'))
    return [EvernoteLink(m) for m in re.finditer(regex_str, content)]

def get_dict_from_list(lst, keys_to_ignore=list()):
    dic = {}
    for key, value in lst:
        if not key in keys_to_ignore: dic[key] = value
    return dic

_regex_see_also = None

def update_regex():
    global _regex_see_also
    regex_str = file(os.path.join(ANKNOTES.FOLDER_ANCILLARY, 'regex-see_also.txt'), 'r').read()
    regex_str = regex_str.replace('(?<', '(?P<')
    _regex_see_also = re.compile(regex_str, re.UNICODE | re.VERBOSE | re.DOTALL)


def regex_see_also():
    global _regex_see_also
    if not _regex_see_also: update_regex()
    return _regex_see_also
