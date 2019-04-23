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
    cmds.button( label='Mirror Named', command=functools.partial(eh_mirror_given, cnFld))
    cmds.separator( h=10, style='none' )
    cmds.button( label='Mirror rx', command=functools.partial(eh_mirror_vals, ['rx'] ))
    cmds.button( label='Mirror ry', command=functools.partial(eh_mirror_vals, ['ry'] ))
    cmds.button( label='Mirror rz', command=functools.partial(eh_mirror_vals, ['rz'] ))
    cmds.button( label='Mirror tx', command=functools.partial(eh_mirror_vals, ['tx'] ))
    cmds.button( label='Mirror ty', command=functools.partial(eh_mirror_vals, ['ty'] ))
    cmds.button( label='Mirror tz', command=functools.partial(eh_mirror_vals, ['tz'] ))


    cmds.button( label='Swap Rot Trans', command=functools.partial(eh_swap_vals, ['rx','ry','rz','tx','ty','tz'] ))
    cmds.button( label='Swap Named', command=functools.partial(eh_swap_given, cnFld))
    cmds.separator( h=10, style='none' )
    cmds.button( label='Swap rx', command=functools.partial(eh_swap_vals, ['rx'] ))
    cmds.button( label='Swap ry', command=functools.partial(eh_swap_vals, ['ry'] ))
    cmds.button( label='Swap rz', command=functools.partial(eh_swap_vals, ['rz'] ))
    cmds.button( label='Swap tx', command=functools.partial(eh_swap_vals, ['tx'] ))
    cmds.button( label='Swap ty', command=functools.partial(eh_swap_vals, ['ty'] ))
    cmds.button( label='Swap tz', command=functools.partial(eh_swap_vals, ['tz'] ))
    
    cmds.button( label='Trans Rot Trans', command=functools.partial(eh_trans_vals, ['rx','ry','rz','tx','ty','tz'] ))
    cmds.button( label='Trans Named', command=functools.partial(eh_trans_given, cnFld))
    cmds.separator( h=10, style='none' )
    cmds.button( label='Trans rx', command=functools.partial(eh_trans_vals, ['rx'] ))
    cmds.button( label='Trans ry', command=functools.partial(eh_trans_vals, ['ry'] ))
    cmds.button( label='Trans rz', command=functools.partial(eh_trans_vals, ['rz'] ))
    cmds.button( label='Trans tx', command=functools.partial(eh_trans_vals, ['tx'] ))
    cmds.button( label='Trans ty', command=functools.partial(eh_trans_vals, ['ty'] ))
    cmds.button( label='Trans tz', command=functools.partial(eh_trans_vals, ['tz'] ))

    # Cancel button
    cmds.button( label='Cancel', command=functools.partial( g_cancelCallback, windowID))

    cmds.showWindow()

# Event Handlers
def g_cancelCallback(windowID,  *pArgs ):
    if cmds.window( windowID, exists=True ):
        cmds.deleteUI( windowID )

def eh_swap_given(cnFld, *p):
    eh_swap_vals([uu.text_val(cnFld)])

def eh_mirror_given(cnFld, *p):
    eh_mirror_vals([uu.text_val(cnFld)])

def eh_trans_given(cnFld, *p):
    eh_trans_vals([uu.text_val(cnFld)])

# copy([rx,ry,rz])
def eh_swap_vals(attrs, *p):
    print(attrs)
    objs = cmds.ls(sl=True)
    if len(objs) == 0:
        return

    a = objs[0]
    b = objs[1]

    for attr in attrs:
        print('Swapping ', attr)
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

    for attr in attrs:
        ta = cmds.getAttr(a + '.' + attr)
        tb = cmds.getAttr(b + '.' + attr)
        cmds.setAttr(a + '.' + attr, -tb)
        cmds.setAttr(b + '.' + attr, -ta)

    print("Done key value mirror for", attrs)

def eh_trans_vals(attrs, *p):
    print(attrs)
    objs = cmds.ls(sl=True)
    if len(objs) == 0:
        return

    a = objs[0]
    b = objs[1]

    for attr in attrs:
        print('Swapping ', attr)
        ta = cmds.getAttr(a + '.' + attr)
        cmds.setAttr(b + '.' + attr, ta)

    print("Done key value tranfer for", attrs)