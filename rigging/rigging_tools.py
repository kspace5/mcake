import maya.cmds as cmds
import functools
import mcake.generic_utils.ui_utils as uu

def createRiggingToolsUI():
    
    windowID = 'myWindowID'
    
    if cmds.window( windowID, exists=True ):
        cmds.deleteUI( windowID )
        
    cmds.window( windowID, title="MCAKE: Animation & Rigging Tools", sizeable=False, resizeToFitChildren=True )
    
    cmds.rowColumnLayout( numberOfColumns=3, columnWidth=[ (1,120), (2,120), (3,120) ], columnOffset=[ ] )
    
    cmds.text( label='Attribute Name:' )
    cnFld = cmds.textField( text='baseRoll' )
    cmds.separator( h=10, style='none' )

    cmds.button( label='Mirror Rot Trans', command=functools.partial(eh_mirror_vals, ['rx','ry','rz','tx','ty','tz'] ))
    cmds.button( label='Mirror Given', command=functools.partial(eh_mirror_given, cnFld))
    cmds.separator( h=10, style='none' )
    cmds.button( label='Mirror rx', command=functools.partial(eh_mirror_vals, ['rx'] ))
    cmds.button( label='Mirror ry', command=functools.partial(eh_mirror_vals, ['ry'] ))
    cmds.button( label='Mirror rz', command=functools.partial(eh_mirror_vals, ['rz'] ))
    cmds.button( label='Mirror tx', command=functools.partial(eh_mirror_vals, ['tx'] ))
    cmds.button( label='Mirror ty', command=functools.partial(eh_mirror_vals, ['ty'] ))
    cmds.button( label='Mirror tz', command=functools.partial(eh_mirror_vals, ['tz'] ))


    cmds.button( label='Copy Rot Trans', command=functools.partial(eh_copy_vals, ['rx','ry','rz','tx','ty','tz'] ))
    cmds.button( label='Copy Given', command=functools.partial(eh_copy_given, cnFld))
    cmds.separator( h=10, style='none' )
    cmds.button( label='Copy rx', command=functools.partial(eh_copy_vals, ['rx'] ))
    cmds.button( label='Copy ry', command=functools.partial(eh_copy_vals, ['ry'] ))
    cmds.button( label='Copy rz', command=functools.partial(eh_copy_vals, ['rz'] ))
    cmds.button( label='Copy tx', command=functools.partial(eh_copy_vals, ['tx'] ))
    cmds.button( label='Copy ty', command=functools.partial(eh_copy_vals, ['ty'] ))
    cmds.button( label='Copy tz', command=functools.partial(eh_copy_vals, ['tz'] ))
    
    # Cancel button
    cmds.button( label='Cancel', command=functools.partial( g_cancelCallback, windowID))

    cmds.showWindow()

# Event Handlers
def g_cancelCallback(windowID,  *pArgs ):
    if cmds.window( windowID, exists=True ):
        cmds.deleteUI( windowID )

def eh_copy_given(cnFld, *p):
    eh_copy_vals([uu.text_val(cnFld)])

def eh_mirror_given(cnFld, *p):
    eh_mirror_vals([uu.text_val(cnFld)])

# copy([rx,ry,rz])
def eh_copy_vals(attrs, *p):
    print(attrs)
    objs = cmds.ls(sl=True)
    if len(objs) == 0:
        return

    a = objs[0]
    b = objs[1]
    avals = []
    bvals = []

    for attr in attrs:
        print('Copying ', attr)
        ta = cmds.getAttr(a + '.' + attr)
        tb = cmds.getAttr(b + '.' + attr)
        cmds.setAttr(a + '.' + attr, tb)
        cmds.setAttr(b + '.' + attr, ta)

    print("Done key value swap for", attrs)

def eh_mirror_vals(attrs, *p):
    objs = cmds.ls(sl=True)
    if len(objs) == 0:
        return

    a = objs[0]
    b = objs[1]
    avals = []
    bvals = []

    for attr in attrs:
        ta = cmds.getAttr(a + '.' + attr)
        tb = cmds.getAttr(b + '.' + attr)
        cmds.setAttr(a + '.' + attr, -tb)
        cmds.setAttr(b + '.' + attr, -ta)

    print("Done key value mirror for", attrs)
