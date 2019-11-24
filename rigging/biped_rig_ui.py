from __future__ import print_function
import maya.cmds as cmds
import functools
import mcake.rigging.joint_tools as jt
import mcake.generic_utils.ui_utils as uu
import mcake.rigging.controls as rct
import mcake.generic_utils.base as gu

reload(gu)
reload(uu)
reload(jt)
reload(rct)

def createRiggingToolsUI():
    
    windowID = 'BipedRigWindow'
    
    if cmds.window( windowID, exists=True ):
        cmds.deleteUI( windowID )
        
    cmds.window( windowID, title='MCAKE: Biped Rigging Tools', sizeable=False, resizeToFitChildren=True )
    #cmds.rowColumnLayout( numberOfColumns=2, columnWidth=[ (1,120), (2,120) ], columnOffset=[ (1,'right',3) ] )
    cmds.gridLayout( numberOfColumns=2, cellWidthHeight=(250, 30) )
    
    cmds.separator( h=10, style='none' )
    cmds.separator( h=10, style='none' )
    cmds.text( label='HIK Character Name:' )
    
    cnFld = cmds.textField( text='BipedX1' )
    cmds.text( label='Root Joint: COG' )
    
    cmds.button( label='Freeze Trans + Fix : Joint Orients [to X]', width=100, height=30, command=functools.partial( clean_up_joint_orient, cnFld) )
    cmds.button( label='Check Joints Integrity', command=functools.partial( check_joints_integrity, cnFld) )
    cmds.button( label='Create Biped Control Rig', backgroundColor=(0.9,0.6,0.3), command=functools.partial( build_complete_rig, cnFld) )
    
    cmds.separator( h=10, style='none' )
    cmds.separator( h=10, style='none' )

    # Cancel button
    cmds.button( label='Cancel', command=functools.partial( uu.cancelCallback, windowID))

    cmds.showWindow()

def clean_up_joint_orient(cnFld, *pArgs):
    cn = uu.text_val(cnFld)
    # Assumes root is Hips, also select entire hierarchy - cool!
    cmds.select(cn + '_COG', hi=True)
    # Do a freeze trans on all selected bones
    gu.freeze_all_selected()
    # This is to point the end joints to the world, instead of random
    jt.orient_joints_to_world_all_selected()
    jt.orient_joints_to_x_all_selected()
    print('All joint oriented to X for', cn)
    check_joints_integrity(cnFld)

def set_joint_attributes_for_rigging(cnFld, *pArgs):
    cn = uu.text_val(cnFld)
    # IMPORTANT: This is determined by the joint orient (world vs x along joint)
    
    # Important: Do not lock X for leg joints to enable IK and Pole Vec solvers
    #cmds.setAttr(cn + '_RightUpLeg.jointTypeX', 0)
    #cmds.setAttr(cn + '_LeftUpLeg.jointTypeX', 0)
    #cmds.setAttr(cn + '_RightLeg.jointTypeX', 0)
    #cmds.setAttr(cn + '_LeftLeg.jointTypeX', 0)
    # --
    
    cmds.setAttr(cn + '_RightLeg.preferredAngleZ', 90)
    cmds.setAttr(cn + '_LeftLeg.preferredAngleZ', 90)

    print('Joint params set for', cn)

'''
def create_IK_Handles(cnFld, *pArgs):
    cn = uu.text_val(cnFld)
    n = cn + '_RightFoot_ikHandle'
    cmds.ikHandle(n=n, sj=cn+'_RightUpLeg', ee=cn+'_RightFoot', sol='ikRPsolver')
    cmds.setAttr(n + '.stickiness', 1)
    gu.freeze_transformations_by_name(n)
    n = cn + '_LeftFoot_ikHandle'
    cmds.ikHandle(n=n, sj=cn+'_LeftUpLeg', ee=cn+'_LeftFoot', sol='ikRPsolver')
    cmds.setAttr(n + '.stickiness', 1)
    gu.freeze_transformations_by_name(n)
'''

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

    control_builder_proc = cb.build_torus_control
    
    # Create IK Handles
    cb.create_IK_Handles()
    n = 'COG'
    cl_cog = control_builder_proc(prefix=n, radius=25, hr=0.05, scale=(1,0.3,1))
    cb.add_parent_constraint_control(target=n, parent=cl_global)
    rct.lock_scale(cl_cog)
    n = 'Hips'
    cl_hips = control_builder_proc(prefix=n, radius=15, hr=0.02, scale=(1,0.7,1))
    cb.add_orient_constraint_control(target=n, parent=cl_cog)
    rct.lock_trans_and_scale(cl_hips)
    n = 'SpineRoot'
    cl_spineRoot = control_builder_proc(prefix=n, radius=20, hr=0.02, scale=(1,0.7,1))
    cb.add_orient_constraint_control(target=n, parent=cl_cog)
    rct.lock_trans_and_scale(cl_spineRoot)
    n = 'Spine'
    cl_Spine = control_builder_proc(prefix=n, radius=15, hr=0.02, scale=(1,0.7,1))
    cb.add_orient_constraint_control(target=n, parent=cl_spineRoot)
    rct.lock_trans_and_scale(cl_Spine)
    n = 'Spine1'
    cl_Spine1 = control_builder_proc(prefix=n, radius=15, hr=0.02, scale=(1,0.7,1))
    cb.add_orient_constraint_control(target=n, parent=cl_Spine)
    rct.lock_trans_and_scale(cl_Spine1)
    n = 'Spine2'
    cl_Spine2 = control_builder_proc(prefix=n, radius=20, hr=0.02, scale=(1,0.7,1))
    cb.add_orient_constraint_control(target=n, parent=cl_Spine1)
    rct.lock_trans_and_scale(cl_Spine2)
    n = 'Neck'
    cl_neck = control_builder_proc(prefix=n, radius=10, hr=0.02, scale=(1,0.7,1))
    cb.add_orient_constraint_control(target=n, parent=cl_Spine2)
    rct.lock_trans_and_scale(cl_neck)
    n = 'Head'
    cl_Head = control_builder_proc(prefix=n, radius=15, hr=0.02, scale=(1,0.7,1))
    cb.add_orient_constraint_control(target=n, parent=cl_neck)
    rct.lock_trans_and_scale(cl_Head)
    n = 'RightShoulder'
    cl_RightShoulder = control_builder_proc(prefix=n, radius=8, axis=(1,0,0), hr=0.02, scale=(2,1,1))
    cb.add_orient_constraint_control(target=n, parent=cl_Spine2)
    rct.lock_trans_and_scale(cl_RightShoulder)
    n = 'LeftShoulder'
    cl_LeftShoulder = control_builder_proc(prefix=n, radius=8, axis=(1,0,0), hr=0.02, scale=(2,1,1))
    cb.add_orient_constraint_control(target=n, parent=cl_Spine2)
    rct.lock_trans_and_scale(cl_LeftShoulder)
    n = 'RightArm'
    cl_RightArm = control_builder_proc(prefix=n, radius=7, axis=(1,0,0), hr=0.02, scale=(2,1,1))
    cb.add_orient_constraint_control(target=n, parent=cl_RightShoulder)
    rct.lock_trans_and_scale(cl_RightArm)
    n = 'LeftArm'
    cl_LeftArm = control_builder_proc(prefix=n, radius=7, axis=(1,0,0), hr=0.02, scale=(2,1,1))
    cb.add_orient_constraint_control(target=n, parent=cl_LeftShoulder)
    rct.lock_trans_and_scale(cl_LeftArm)
    n = 'RightForeArm'
    cl_RightForeArm = control_builder_proc(prefix=n, radius=4, axis=(1,0,0), hr=0.02, scale=(2,1,1))
    cb.add_orient_constraint_control(target=n, parent=cl_RightArm)
    rct.lock_trans_and_scale(cl_RightForeArm)
    n = 'LeftForeArm'
    cl_LeftForeArm = control_builder_proc(prefix=n, radius=4, axis=(1,0,0), hr=0.02, scale=(2,1,1))
    cb.add_orient_constraint_control(target=n, parent=cl_LeftArm)
    rct.lock_trans_and_scale(cl_LeftForeArm)
    n = 'RightHand'
    cl_RightHand = control_builder_proc(prefix=n, radius=3, axis=(1,0,0), hr=0.02, scale=(2,1,1))
    cb.add_orient_constraint_control(target=n, parent=cl_RightForeArm)
    rct.lock_trans_and_scale(cl_RightHand)
    n = 'LeftHand'
    cl_LeftHand = control_builder_proc(prefix=n, radius=3, axis=(1,0,0), hr=0.02, scale=(2,1,1))
    cb.add_orient_constraint_control(target=n, parent=cl_LeftForeArm)
    rct.lock_trans_and_scale(cl_LeftHand)
    n = 'RightUpLeg'
    cl_RightUpLeg = control_builder_proc(prefix=n, radius=8, hr=0.1, scale=(1,0.7,1))
    cb.add_orient_constraint_control(target=n, parent=cl_hips)
    rct.lock_trans_and_scale(cl_RightUpLeg)
    n = 'LeftUpLeg'
    cl_LeftUpLeg = control_builder_proc(prefix=n, radius=8, hr=0.1, scale=(1,0.7,1))
    cb.add_orient_constraint_control(target=n, parent=cl_hips)
    rct.lock_trans_and_scale(cl_LeftUpLeg)

    # IK Pole Vector
    n = 'RightFoot_ikHandle_poleVec'
    cl_RightLeg_PoleVec = control_builder_proc(prefix=n, radius=2, axis=(0,0,1), hr=0.1, scale=(1,0.5,1))
    cb.add_poleVector_constraint_control(control=n, ik_handle='RightFoot_ikHandle', align_joint='RightLeg', parent=cl_global)

    n = 'LeftFoot_ikHandle_poleVec'
    cl_LeftLeg_PoleVec = control_builder_proc(prefix=n, radius=2, axis=(0,0,1), hr=0.1, scale=(1,0.5,1))
    cb.add_poleVector_constraint_control(control=n, ik_handle='LeftFoot_ikHandle', align_joint='LeftLeg', parent=cl_global)
    
    # Foot Roll Controls
    cb.create_footRoll_controls()

    # IK Handles Foot Roll controls - note: rotate for IK is useless
    n = 'RightFoot_FRoll_LocA'
    cl_RightUpLeg = control_builder_proc(prefix=n, radius=8, hr=0.1, scale=(1,0.5,2))
    cb.add_parent_constraint_control(target=n, parent=cl_global)
    rct.lock_scale(cl_RightUpLeg)

    n = 'LeftFoot_FRoll_LocA'
    cl_LeftUpLeg = control_builder_proc(prefix=n, radius=8, hr=0.1, scale=(1,0.5,2))
    cb.add_parent_constraint_control(target=n, parent=cl_global)
    rct.lock_scale(cl_LeftUpLeg)

    cb.create_footRoll_driven_keys()

    cb.add_finger_bend_and_curl_attributes()

def build_complete_rig(cnFld, *pArgs):
    #clean_up_joint_orient(cnFld)
    #check_joints_integrity(cnFld)
    set_joint_attributes_for_rigging(cnFld)
    build_controls(cnFld)