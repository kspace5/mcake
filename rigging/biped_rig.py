from __future__ import print_function
import maya.cmds as cmds
import functools
import mcake.rigging.joint_tools as jt
import mcake.generic_utils.ui_utils as uu
reload(uu)
reload(jt)

def createRiggingToolsUI():
    
    windowID = 'myWindowID'
    
    if cmds.window( windowID, exists=True ):
        cmds.deleteUI( windowID )
        
    cmds.window( windowID, title="MCAKE: Biped Rigging Tools", sizeable=False, resizeToFitChildren=True )
    
    cmds.rowColumnLayout( numberOfColumns=3, columnWidth=[ (1,120), (2,120), (3,120) ], columnOffset=[ (1,'right',3) ] )
    
    def applyCallback( pStartTimeField, pEndTimeField, pTargetAttributeField, *pArgs ):
        print('Apply button pressed.')
    
    cmds.separator( h=10, style='none' )
    cmds.separator( h=10, style='none' )
    cmds.separator( h=10, style='none' )
    cmds.text( label='HIK Character Name:' )
    
    charNameFld = cmds.textField( text='UrvaX2' )
    
    
    cmds.button( label='Initialize', command=functools.partial( clean_up_joint_orient, charNameFld) )
    
    cmds.button( label='Check Joints Integrity', command=functools.partial( check_joints_integrity, charNameFld) )
    cmds.separator( h=10, style='none' )
    cmds.separator( h=10, style='none' )

    # Cancel button
    cmds.button( label='Cancel', command=functools.partial( uu.cancelCallback, windowID))

    cmds.showWindow()

def clean_up_joint_orient(charNameFld, *pArgs):
    charName = uu.text_val(charNameFld)
    # Assumes root is Hips, also select entire hierarchy - cool!
    cmds.select(charName + '_Hips', hi=True)
    jt.orient_joints_to_world()
    print('All joint oriented to World for', charName)
    check_joints_integrity(charNameFld)

def check_joints_integrity(charNameFld, *pArgs):
    integ = jt.check_joint_integrity()
    msg = "All joints verified clean - Congrats!\n(i.e. All joint rotate X,Y,Z and jointOrient X,Y,Z are zeroed out)" if integ else "Dirty joints found!"
    print(msg)