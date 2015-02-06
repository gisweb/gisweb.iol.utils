from zope.i18nmessageid import MessageFactory
from AccessControl import allow_module
allow_module('gisweb.iol.utils.interfaces')
MessageFactory = MessageFactory('gisweb.iol.utils')