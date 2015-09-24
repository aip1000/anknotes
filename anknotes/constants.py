# -*- coding: utf-8 -*-
import os

PATH = os.path.dirname(os.path.abspath(__file__))


class ANKNOTES:
    FOLDER_ADDONS_ROOT = os.path.dirname(PATH)
    FOLDER_EXTRA = os.path.join(PATH, 'extra')
    FOLDER_ANCILLARY = os.path.join(FOLDER_EXTRA, 'ancillary')
    FOLDER_GRAPHICS = os.path.join(FOLDER_EXTRA, 'graphics')
    FOLDER_LOGS = os.path.join(FOLDER_EXTRA, 'logs')
    FOLDER_DEVELOPER = os.path.join(FOLDER_EXTRA, 'dev')
    FOLDER_USER = os.path.join(FOLDER_EXTRA, 'user')
    LOG_BASE_NAME = ''
    LOG_DEFAULT_NAME = 'anknotes'
    LOG_MAIN = LOG_DEFAULT_NAME
    LOG_ACTIVE = LOG_DEFAULT_NAME
    LOG_USE_CALLER_NAME = False
    TEMPLATE_FRONT = os.path.join(FOLDER_ANCILLARY, 'FrontTemplate.htm')
    CSS = u'_AviAnkiCSS.css'
    QT_CSS_QMESSAGEBOX = os.path.join(FOLDER_ANCILLARY, 'QMessageBox.css')
    ENML_DTD = os.path.join(FOLDER_ANCILLARY, 'enml2.dtd')
    TABLE_OF_CONTENTS_ENEX = os.path.join(FOLDER_USER, "Table of Contents.enex")
    VALIDATION_SCRIPT = os.path.join(FOLDER_ADDONS_ROOT, 'anknotes_start_note_validation.py')  # anknotes-standAlone.py')
    FIND_DELETED_NOTES_SCRIPT = os.path.join(FOLDER_ADDONS_ROOT, 'anknotes_start_find_deleted_notes.py')  # anknotes-standAlone.py')
    LOG_FDN_ANKI_ORPHANS = 'Find Deleted Notes\\'
    LOG_FDN_UNIMPORTED_EVERNOTE_NOTES = LOG_FDN_ANKI_ORPHANS + 'UnimportedEvernoteNotes'
    LOG_FDN_ANKI_TITLE_MISMATCHES = LOG_FDN_ANKI_ORPHANS + 'AnkiTitleMismatches'
    LOG_FDN_ANKNOTES_TITLE_MISMATCHES = LOG_FDN_ANKI_ORPHANS + 'AnknotesTitleMismatches'
    LOG_FDN_ANKNOTES_ORPHANS = LOG_FDN_ANKI_ORPHANS + 'AnknotesOrphans'
    LOG_FDN_ANKI_ORPHANS += 'AnkiOrphans'
    LAST_PROFILE_LOCATION = os.path.join(FOLDER_USER, 'anki.profile')
    ICON_EVERNOTE_WEB = os.path.join(FOLDER_GRAPHICS, u'evernote_web.ico')
    IMAGE_EVERNOTE_WEB = ICON_EVERNOTE_WEB.replace('.ico', '.png')
    ICON_EVERNOTE_ARTCORE = os.path.join(FOLDER_GRAPHICS, u'evernote_artcore.ico')
    ICON_TOMATO = os.path.join(FOLDER_GRAPHICS, u'Tomato-icon.ico')
    IMAGE_EVERNOTE_ARTCORE = ICON_EVERNOTE_ARTCORE.replace('.ico', '.png')
    EVERNOTE_CONSUMER_KEY = "holycrepe"
    EVERNOTE_IS_SANDBOXED = False
    DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
    DEVELOPER_MODE = (os.path.isfile(os.path.join(FOLDER_DEVELOPER, 'anknotes.developer')))
    DEVELOPER_MODE_AUTOMATE = (os.path.isfile(os.path.join(FOLDER_DEVELOPER, 'anknotes.developer.automate')))
    UPLOAD_AUTO_TOC_NOTES = True  # Set False if debugging note creation
    AUTO_TOC_NOTES_MAX = -1  # Set to -1 for unlimited
    ENABLE_VALIDATION = True
    AUTOMATE_VALIDATION = True
    ROOT_TITLES_BASE_QUERY = "notebookGuid != 'fdccbccf-ee70-4069-a587-82772a96d9d3'"
    NOTE_LIGHT_PROCESSING_INCLUDE_CSS_FORMATTING = False
    IMPORT_MODEL_STYLES_AS_URL = True

class MODELS:
    EVERNOTE_DEFAULT = 'evernote_note'
    EVERNOTE_REVERSIBLE = 'evernote_note_reversible'
    EVERNOTE_REVERSE_ONLY = 'evernote_note_reverse_only'
    EVERNOTE_CLOZE = 'evernote_note_cloze'
    TYPE_CLOZE = 1


class TEMPLATES:
    EVERNOTE_DEFAULT = 'EvernoteReview'
    EVERNOTE_REVERSED = 'EvernoteReviewReversed'
    EVERNOTE_CLOZE = 'EvernoteReviewCloze'


class FIELDS:    
    TITLE = 'Title'
    CONTENT = 'Content'
    SEE_ALSO = 'See_Also'
    TOC = 'TOC'
    OUTLINE = 'Outline'
    EXTRA = 'Extra'
    EVERNOTE_GUID = 'Evernote GUID'
    UPDATE_SEQUENCE_NUM = 'updateSequenceNum'
    EVERNOTE_GUID_PREFIX = 'evernote_guid='
    LIST = [TITLE, CONTENT, SEE_ALSO, EXTRA, TOC, OUTLINE,
               UPDATE_SEQUENCE_NUM]
    SEE_ALSO_FIELDS_ORD = LIST.index(SEE_ALSO) + 1

class DECKS:
    DEFAULT = "Evernote"
    TOC_SUFFIX = "::See Also::TOC"
    OUTLINE_SUFFIX = "::See Also::Outline"


class EVERNOTE:
    class TAG:
        TOC = '#TOC'
        AUTO_TOC = '#TOC.Auto'
        OUTLINE = '#Outline'
        OUTLINE_TESTABLE = '#Outline.Testable'
        REVERSIBLE = '#Reversible'
        REVERSE_ONLY = '#Reversible_Only'

    # Note that Evernote's API documentation says not to run API calls to findNoteMetadata with any less than a 15 minute interval
    PAGING_RESTART_INTERVAL = 60 * 15
    # Auto Paging is probably only useful in the first 24 hours, when API usage is unlimited, or when executing a search that is likely to have most of the notes up-to-date locally
    # To keep from overloading Evernote's servers, and flagging our API key, I recommend pausing 5-15 minutes in between searches, the higher the better.
    PAGING_TIMER_INTERVAL = 60 * 15
    PAGING_RESTART_DELAY_MINIMUM_API_CALLS = 10
    PAGING_RESTART_WHEN_COMPLETE = False
    IMPORT_TIMER_INTERVAL = PAGING_RESTART_INTERVAL * 2 * 1000
    METADATA_QUERY_LIMIT = 10000
    GET_NOTE_LIMIT = 10000


class TABLES:
    SEE_ALSO = "anknotes_see_also"
    MAKE_NOTE_QUEUE = "anknotes_make_note_queue"

    class EVERNOTE:
        NOTEBOOKS = "anknotes_evernote_notebooks"
        TAGS = "anknotes_evernote_tags"
        NOTES = u'anknotes_evernote_notes'
        NOTES_HISTORY = u'anknotes_evernote_notes_history'
        AUTO_TOC = u'anknotes_evernote_auto_toc'


class SETTINGS:
    ANKI_PROFILE_NAME = ''
    EVERNOTE_LAST_IMPORT = "ankNotesEvernoteLastAutoImport"
    ANKNOTES_CHECKABLE_MENU_ITEMS_PREFIX = "ankNotesCheckableMenuItems"
    KEEP_EVERNOTE_TAGS_DEFAULT_VALUE = True
    EVERNOTE_QUERY_TAGS_DEFAULT_VALUE = "#Anki_Import"
    DEFAULT_ANKI_DECK_DEFAULT_VALUE = DECKS.DEFAULT
    EVERNOTE_ACCOUNT_UID = 'ankNotesEvernoteAccountUID'
    EVERNOTE_ACCOUNT_SHARD = 'ankNotesEvernoteAccountSHARD'
    EVERNOTE_ACCOUNT_UID_DEFAULT_VALUE = '0'
    EVERNOTE_ACCOUNT_SHARD_DEFAULT_VALUE = 'x999'
    EVERNOTE_QUERY_TAGS = 'anknotesEvernoteQueryTags'
    EVERNOTE_QUERY_USE_TAGS = 'anknotesEvernoteQueryUseTags'
    EVERNOTE_QUERY_EXCLUDED_TAGS = 'anknotesEvernoteQueryExcludedTags'
    EVERNOTE_QUERY_USE_EXCLUDED_TAGS = 'anknotesEvernoteQueryUseExcludedTags'
    EVERNOTE_QUERY_LAST_UPDATED_VALUE_RELATIVE = 'anknotesEvernoteQueryLastUpdatedValueRelative'
    EVERNOTE_QUERY_LAST_UPDATED_VALUE_ABSOLUTE_DATE = 'anknotesEvernoteQueryLastUpdatedValueAbsoluteDate'
    EVERNOTE_QUERY_LAST_UPDATED_VALUE_ABSOLUTE_TIME = 'anknotesEvernoteQueryLastUpdatedValueAbsoluteDateTime'
    EVERNOTE_QUERY_LAST_UPDATED_TYPE = 'anknotesEvernoteQueryLastUpdatedType'
    EVERNOTE_QUERY_USE_LAST_UPDATED = 'anknotesEvernoteQueryUseLastUpdated'
    EVERNOTE_QUERY_NOTEBOOK = 'anknotesEvernoteQueryNotebook'
    EVERNOTE_QUERY_NOTEBOOK_DEFAULT_VALUE = 'My Anki Notebook'
    EVERNOTE_QUERY_USE_NOTEBOOK = 'anknotesEvernoteQueryUseNotebook'
    EVERNOTE_QUERY_NOTE_TITLE = 'anknotesEvernoteQueryNoteTitle'
    EVERNOTE_QUERY_USE_NOTE_TITLE = 'anknotesEvernoteQueryUseNoteTitle'
    EVERNOTE_QUERY_SEARCH_TERMS = 'anknotesEvernoteQuerySearchTerms'
    EVERNOTE_QUERY_USE_SEARCH_TERMS = 'anknotesEvernoteQueryUseSearchTerms'
    EVERNOTE_QUERY_ANY = 'anknotesEvernoteQueryAny'
    DELETE_EVERNOTE_TAGS_TO_IMPORT = 'anknotesDeleteEvernoteTagsToImport'
    UPDATE_EXISTING_NOTES = 'anknotesUpdateExistingNotes'
    EVERNOTE_PAGINATION_CURRENT_PAGE = 'anknotesEvernotePaginationCurrentPage'
    EVERNOTE_AUTO_PAGING = 'anknotesEvernoteAutoPaging'
    EVERNOTE_AUTH_TOKEN = 'anknotesEvernoteAuthToken_' + ANKNOTES.EVERNOTE_CONSUMER_KEY + (
        "_SANDBOX" if ANKNOTES.EVERNOTE_IS_SANDBOXED else "")
    KEEP_EVERNOTE_TAGS = 'anknotesKeepEvernoteTags'
    EVERNOTE_TAGS_TO_DELETE = 'anknotesEvernoteTagsToDelete'
    ANKI_DECK_EVERNOTE_NOTEBOOK_INTEGRATION = 'anknotesUseNotebookNameForAnkiDeckName'
    DEFAULT_ANKI_DECK = 'anknotesDefaultAnkiDeck'
