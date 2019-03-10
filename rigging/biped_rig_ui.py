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
    
    windowID = 'riggerWindow'
    
    if cmds.window( windowID, exists=True ):
        cmds.deleteUI( windowID )
        
    cmds.window( windowID, title='MCAKE: Biped Rigging Tools', sizeable=False, resizeToFitChildren=True )
    #cmds.rowColumnLayout( numberOfColumns=2, columnWidth=[ (1,120), (2,120) ], columnOffset=[ (1,'right',3) ] )
    cmds.gridLayout( numberOfColumns=2, cellWidthHeight=(150, 50) )
    
    cmds.separator( h=10, style='none' )
    cmds.separator( h=10, style='none' )
    cmds.text( label='HIK Character Name:' )
    
    cnFld = cmds.textField( text='UrvaX2' )
    cmds.text( label='Root Joint: COG' )
    
    cmds.button( label='Fix All Joint Orient', width=100, height=30, command=functools.partial( clean_up_joint_orient, cnFld) )
    cmds.button( label='Check Joints Integrity', command=functools.partial( check_joints_integrity, cnFld) )
    cmds.button( label='Set Joint Params For Rigging', command=functools.partial( set_joint_attributes_for_rigging, cnFld) )
    cmds.button( label='Create IK Handles', command=functools.partial( create_IK_Handles, cnFld) )
    cmds.button( label='Build Biped Control Rig', backgroundColor=(0.8,0.3,0.3), command=functools.partial( build_controls, cnFld) )
    
    cmds.separator( h=10, style='none' )
    cmds.separator( h=10, style='none' )

    # Cancel button
    cmds.button( label='Cancel', command=functools.partial( uu.cancelCallback, windowID))

    cmds.showWindow()

def clean_up_joint_orient(cnFld, *pArgs):
    cn = uu.text_val(cnFld)
    # Assumes root is Hips, also select entire hierarchy - cool!
    cmds.select(cn + '_COG', hi=True)
    # This is to point the end joints to the world, instead of random
    jt.orient_joints_to_world_all_selected()
    jt.orient_joints_to_x_all_selected()
    print('All joint oriented to X for', cn)
    check_joints_integrity(cnFld)

def set_joint_attributes_for_rigging(cnFld, *pArgs):
    cn = uu.text_val(cnFld)
    # IMPORTANT: This is determined by the joint orient (world vs x along joint)
    cmds.setAttr(cn + "_RightUpLeg.jointTypeX", 0)
    cmds.setAttr(cn + "_LeftUpLeg.jointTypeX", 0)
    cmds.setAttr(cn + "_RightLeg.jointTypeX", 0)
    cmds.setAttr(cn + "_LeftLeg.jointTypeX", 0)
    cmds.setAttr(cn + "_RightLeg.preferredAngleZ", 90)
    cmds.setAttr(cn + "_LeftLeg.preferredAngleZ", 90)

    print('Joint params set for', cn)

def create_IK_Handles(cnFld, *pArgs):
    cn = uu.text_val(cnFld)
    cmds.ikHandle(n=cn+'_RightFoot_ikHandle', sj=cn+'_RightUpLeg', ee=cn+'_RightFoot', sol='ikRPsolver')
    cmds.setAttr(cn + "_RightFoot_ikHandle.stickiness", 1)
    cmds.ikHandle(n=cn+'_LeftFoot_ikHandle', sj=cn+'_LeftUpLeg', ee=cn+'_LeftFoot', sol='ikRPsolver')
    cmds.setAttr(cn + "_LeftFoot_ikHandle.stickiness", 1)

def check_joints_integrity(cnFld, *pArgs):
    cn = uu.text_val(cnFld)
    # Assumes root is Hips, also select entire hierarchy - cool!
    cmds.select(cn + '_COG', hi=True)
    integ = jt.check_joint_integrity_all_selected()
    msg = 'All joints verified clean - Congrats!\n(i.e. All joint rotate X,Y,Z and jointOrient X,Y,Z are zeroed out)' if integ else 'Dirty joints found!'
    print(msg)

# build and bind controls
def build_controls(cnFld, *pArgs):
    cn = uu.text_val(cnFld)

    cb = rct.BipedControlBuilder(cn)

    cl_global = cb.build_global_control()
    cb.bind_global_control()
    
    cl_cog = cb.build_circle_control('COG', 25)
    cb.add_parent_constraint_control('COG', cl_global)
    rct.lock_scale(cl_cog)

    cl_hips = cb.build_circle_control('Hips', 15)
    cb.add_orient_constraint_control('Hips', cl_cog)
    rct.lock_trans_and_scale(cl_hips)

    cl_spineRoot = cb.build_circle_control('SpineRoot', 20)
    cb.add_orient_constraint_control('SpineRoot', cl_cog)
    rct.lock_trans_and_scale(cl_spineRoot)

    cl_Spine = cb.build_circle_control('Spine', 15)
    cb.add_orient_constraint_control('Spine', cl_spineRoot)
    rct.lock_trans_and_scale(cl_Spine)

    cl_Spine1 = cb.build_circle_control('Spine1', 15)
    cb.add_orient_constraint_control('Spine1', cl_Spine)
    rct.lock_trans_and_scale(cl_Spine1)

    cl_Spine2 = cb.build_circle_control('Spine2', 20)
    cb.add_orient_constraint_control('Spine2', cl_Spine1)
    rct.lock_trans_and_scale(cl_Spine2)

    cl_neck = cb.build_circle_control('Neck', 10)
    cb.add_orient_constraint_control('Neck', cl_Spine2)
    rct.lock_trans_and_scale(cl_neck)

    cl_Head = cb.build_circle_control('Head', 15)
    cb.add_orient_constraint_control('Head', cl_neck)
    rct.lock_trans_and_scale(cl_Head)

    cl_RightShoulder = cb.build_circle_control('RightShoulder', 8, (1,0,0))
    cb.add_orient_constraint_control('RightShoulder', cl_Spine2)
    rct.lock_trans_and_scale(cl_RightShoulder)

    cl_LeftShoulder = cb.build_circle_control('LeftShoulder', 8, (1,0,0))
    cb.add_orient_constraint_control('LeftShoulder', cl_Spine2)
    rct.lock_trans_and_scale(cl_LeftShoulder)

    cl_RightArm = cb.build_circle_control('RightArm', 7, (1,0,0))
    cb.add_orient_constraint_control('RightArm', cl_RightShoulder)
    rct.lock_trans_and_scale(cl_RightArm)

    cl_LeftArm = cb.build_circle_control('LeftArm', 7, (1,0,0))
    cb.add_orient_constraint_control('LeftArm', cl_LeftShoulder)
    rct.lock_trans_and_scale(cl_LeftArm)

    cl_RightForeArm = cb.build_circle_control('RightForeArm', 4, (1,0,0))
    cb.add_orient_constraint_control('RightForeArm', cl_RightArm)
    rct.lock_trans_and_scale(cl_RightForeArm)

    cl_LeftForeArm = cb.build_circle_control('LeftForeArm', 4, (1,0,0))
    cb.add_orient_constraint_control('LeftForeArm', cl_LeftArm)
    rct.lock_trans_and_scale(cl_LeftForeArm)

    cl_RightHand = cb.build_circle_control('RightHand', 3, (1,0,0))
    cb.add_orient_constraint_control('RightHand', cl_RightForeArm)
    rct.lock_trans_and_scale(cl_RightHand)

    cl_LeftHand = cb.build_circle_control('LeftHand', 3, (1,0,0))
    cb.add_orient_constraint_control('LeftHand', cl_LeftForeArm)
    rct.lock_trans_and_scale(cl_LeftHand)