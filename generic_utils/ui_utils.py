from __future__ import print_function
import maya.cmds as cmds

def cancelCallback(windowID,  *pArgs ):
    if cmds.window( windowID, exists=True ):
        cmds.deleteUI( windowID )

def text_val(field):
    return cmds.textField( field, query=True, text=True )
    