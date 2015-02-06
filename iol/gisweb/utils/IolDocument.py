from zope.interface import Interface, implements, Attribute
from zope.component import adapts
from plone import api
from AccessControl import ClassSecurityInfo
from App.class_init import InitializeClass
from Products.CMFPlomino.interfaces import IPlominoDocument, IPlominoForm
from zope.component import getGlobalSiteManager
import config
from zope.component import getUtility
from gisweb.iol.permissions import IOL_READ_PERMISSION,IOL_EDIT_PERMISSION
from .interfaces import IIolDocument


class IolDocument(object):
    implements(IIolDocument)
    adapts(IPlominoForm,IPlominoDocument)
    tipo_app = u""
    security = ClassSecurityInfo()
    security.declareObjectPublic()
    def __init__(self,obj):
        self.document = obj

    security.declareProtected(IOL_READ_PERMISSION,'getIolRoles')
    def getIolRoles(self):
        obj = self.document
        result = dict(
            iol_owner=[],
            iol_viewer=[],
            iol_reviewer = [],
            iol_manager = [],
        )
        for usr,roles in obj.get_local_roles():
            if 'Owner' in roles:
                result['iol_owner'].append(usr)
            if 'iol-viewer' in roles:
                result['iol_viewer'].append(usr)
            if 'iol-reviewer' in roles:
                result['iol_reviewer'].append(usr)
            if 'iol-manager' in roles:
                result['iol_manager'].append(usr)
        return result

    security.declareProtected(IOL_READ_PERMISSION,'updateStatus')
    def updateStatus(self):
        obj = self.document
        obj.setItem(STATUS_FIELD,api.content.get_state(obj=obj) )
        db = obj.getParentDatabase()
        # update index
        db.getIndex().indexDocument(obj)
        # update portal_catalog
        if db.getIndexInPortal():
            db.portal_catalog.catalog_object(obj, "/".join(db.getPhysicalPath() + (obj.getId(),)))

    security.declarePublic('isActionSupported')
    def isActionSupported(self,tr=''):
        if not tr:
            return False
        wftool = api.portal.get_tool(name='portal_workflow')
        for wfname in wftool.getChainFor(self):
            wf = wftool.getWorkflowById(wfname)
            if wf.isActionSupported(self,tr):
                return True
        return False

    security.declareProtected(IOL_READ_PERMISSION,'getInfoFor')
    def getInfoFor(self,obj,info,wf_id=''):
        wftool = api.portal.get_tool(name='portal_workflow')
        return wftool.getInfoFor(obj,info,default='')

InitializeClass(IolDocument)
