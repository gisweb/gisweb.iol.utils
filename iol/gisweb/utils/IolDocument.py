from zope.interface import Interface, implements, Attribute
from zope.component import adapts
from plone import api
from AccessControl import ClassSecurityInfo
from App.class_init import InitializeClass
from Products.CMFPlomino.interfaces import IPlominoDocument, IPlominoForm
from Products.CMFPlone.utils import getToolByName
from zope.component import getGlobalSiteManager
import config
from zope.component import getUtility
from gisweb.iol.permissions import IOL_READ_PERMISSION,IOL_EDIT_PERMISSION
from .interfaces import IIolDocument

from copy import deepcopy
import simplejson as json
import DateTime
import datetime


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
    def isActionSupported(self, tr=''):
        obj = self.document
        if not tr:
            return False
        wftool = api.portal.get_tool(name='portal_workflow')
        for wfname in wftool.getChainFor(obj):
            wf = wftool.getWorkflowById(wfname)
            if wf.isActionSupported(obj, tr):
                return True
        return False

    security.declareProtected(IOL_READ_PERMISSION,'wfInfo')
    def wfInfo(self,):
        obj = self.document
        result = dict(
            wf_chain=list(),
            wf_state='',
            wf_variables=dict(),
            wf_actions=list(),
        )
        wftool = getToolByName(obj, 'portal_workflow')

        result['wf_state'] = api.content.get_state(obj)

        for wf_id in wftool.getChainFor(obj):
            result['wf_chain'].append(wf_id)

        for wf_var in wftool.getCatalogVariablesFor(obj):
            result['wf_variables'][wf_var] = wftool.getInfoFor(obj, wf_var, default='')

        result['wf_actions'] = [dict(id=res['id'],title=res['name'],url=res['url']) for res in wftool.listActions(object=obj)]
        return result

    security.declareProtected(IOL_READ_PERMISSION,'getInfoFor')
    def getInfoFor(self,info,wf_id=''):
        obj = self.document
        wftool = api.portal.get_tool(name='portal_workflow')
        return wftool.getInfoFor(obj,info,default='')

    def _serialDatagridItem(doc, obj ):
        result = list()
        itemvalue = doc.getItem(obj['name'])
        for el in itemvalue:
            i = 0
            res = dict()
            for fld in obj['field_list']:
                res[fld]= el[i]
                i+=1
            result.append(res)
        return result



    security.declarePublic('serializeDoc')
    def serializeDoc(self):
        doc = self.document
        results = dict(deepcopy(doc.items))
        frm = doc.getForm()
        fieldnames = []
        for i in frm.getFormFields(includesubforms=True, doc=None, applyhidewhen=False):
            if i.getFieldType()=='DATAGRID':
                fieldnames.append(dict(field=i,name=i.getId(),form=i.getSettings().associated_form,field_list=i.getSettings().field_mapping.split(',')))
        try:
            for f in fieldnames:
                if f['name'] in results:
                    del results[f['name']]
                results[f['name']]=self._serialDatagridItem(doc,f)
        except:
            results[f['name']]= []
            api.portal.show_message(message='Errore nel campo %s' %f['name'], request=doc.REQUEST)
        return results


InitializeClass(IolDocument)
