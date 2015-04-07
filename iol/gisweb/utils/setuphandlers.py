from plone.app.controlpanel.security import ISecuritySchema
from plone import api
from Products.Five.utilities.marker import mark
from .interfaces import IIolDocument
import logging

PROFILE_ID = 'iol.utils.replication:default'
logger = logging.getLogger('iol.gisweb.utils')

def initPackage(context):
    try:
        catalog = api.portal.get_tool('portal_catalog')
        brains = catalog(portal_type='PlominoDatabase')
        for brain in brains:
            db = brain.getObject()
            for doc in db.getAllDocuments():
                if not IIolDocument.providedBy(doc):
                    mark(doc,IIolDocument)
    except:
        pass

