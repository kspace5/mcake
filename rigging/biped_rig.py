from __future__ import print_function
import maya.cmds as cmds
import functools
import mcake.rigging.joint_tools as jt
import mcake.generic_utils.ui_utils as uu
import mcake.rigging.controls as rct
reload(uu)
reload(jt)
reload(rct)

def createRiggingToolsUI():
    
    windowID = 'myWindowID'
    
    if cmds.window( windowID, exists=True ):
        cmds.deleteUI( windowID )
        
    cmds.window( windowID, title='MCAKE: Biped Rigging Tools', sizeable=False, resizeToFitChildren=True )
    
    cmds.rowColumnLayout( numberOfColumns=2, columnWidth=[ (1,120), (2,120) ], columnOffset=[ (1,'right',3) ] )
    
    def applyCallback( pStartTimeField, pEndTimeField, pTargetAttributeField, *pArgs ):
        print('Apply button pressed.')
    
    cmds.separator( h=10, style='none' )
    cmds.separator( h=10, style='none' )
    cmds.text( label='HIK Character Name:' )
    
    cnFld = cmds.textField( text='UrvaX2' )
    
    
    cmds.button( label='Init Joints', command=functools.partial( clean_up_joint_orient, cnFld) )
    cmds.button( label='Check Joints Integrity', command=functools.partial( check_joints_integrity, cnFld) )
    
    cmds.button( label='Build Control', command=functools.partial( build_controls, cnFld) )
    
    cmds.separator( h=10, style='none' )
    cmds.separator( h=10, style='none' )

    # Cancel button
    cmds.button( label='Cancel', command=functools.partial( uu.cancelCallback, windowID))

    cmds.showWindow()

def clean_up_joint_orient(cnFld, *pArgs):
    charName = uu.text_val(cnFld)
    # Assumes root is Hips, also select entire hierarchy - cool!
    cmds.select(charName + '_Hips', hi=True)
    jt.orient_joints_to_world()
    print('All joint oriented to World for', charName)
    check_joints_integrity(cnFld)

def check_joints_integrity(cnFld, *pArgs):
    integ = jt.check_joint_integrity()
    msg = 'All joints verified clean - Congrats!\n(i.e. All joint rotate X,Y,Z and jointOrient X,Y,Z are zeroed out)' if integ else 'Dirty joints found!'
    print(msg)

# build and bind controls
def build_controls(cnFld, *pArgs):
    cn = uu.text_val(cnFld)
    top_cl_grp = rct.c_top_grp(cn)

    rct.build_global_control(cn)
    rct.bind_global_control(cn)
    
    #cog_ctrl = rct.build_cog_control(cn)
    #rct.bind_cog_control_to_hips(cn, cog_ctrl)

    cl_cog = rct.build_circle_control(cn + '_ctrl_COG', 25)
    rct.add_orient_constraint_control(cn + '_Root', cl_cog, cn + '_ctrl_global')
    #rct.lock_scale(cl_cog)

    cl_name = rct.build_circle_control(cn + '_ctrl_SpineRoot', 20)
    rct.add_orient_constraint_control(cn + '_SpineRoot', cl_name, cl_cog)
    #rct.lock_trans_and_scale(cl_name)

    cl_name = rct.build_circle_control(cn + '_ctrl_Hips', 15)
    rct.add_orient_constraint_control(cn + '_Hips', cl_name, cl_cog)
    #rct.lock_trans_and_scale(cl_name)