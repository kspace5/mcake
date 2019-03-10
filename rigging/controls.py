import maya.cmds as cmds
import mcake.generic_utils.base as gu
reload(gu)

# Control name/prefix mappings
CL_KEY = '_ctrl_'

JOINTS_MASTER_REF = '_Reference' # Already created by Maya HIK
CONTROLS_TOP_GROUP = CL_KEY + 'Reference' # Highest level group created for all controls
# Controls
CL_GLOBAL = CL_KEY + 'global'

def cl_top_grp(cn):
    return cn + CONTROLS_TOP_GROUP

def build_global_control(cn):
    ctrl_name = cn + CL_GLOBAL
    cmds.curve( p=[(0 ,0 ,40),(-30 ,0 ,30),(-30, 0, 0),(30, 0, 0),(30 ,0 ,30),(0, 0, 40)],d=2, n=ctrl_name)
    gu.freeze_and_center_by_name(ctrl_name)
    cmds.group( ctrl_name, n=cl_top_grp(cn) )
    gu.freeze_and_center_by_name(cl_top_grp(cn))
    cmds.move(0, 0, -20, r=True, os=True, wd=True)
    
def bind_global_control(cn):
    cmds.parentConstraint( cn + CL_GLOBAL, cn + JOINTS_MASTER_REF, mo=True, n=cn + '_ctrl_global_parentConstraint')
    cmds.scaleConstraint( cn + CL_GLOBAL, cn + JOINTS_MASTER_REF, mo=True, n=cn + '_ctrl_global_scaleConstraint')

def build_circle_control(name, radius=25, axis=(0, 1, 0)):
    cmds.circle( nr=axis, c=(0, 0, 0), r=radius ,n=name)
    #cmds.scale( 3, 3, 3, 'curve1', pivot=(1, 0, 0), absolute=True )
    return name

def pvt_align_control(trg_obj, ctrl_obj, parent):
    cmds.parent(ctrl_obj, parent)
    gu.move_to_pos_of(trg_obj, ctrl_obj)
    gu.freeze_transformations_by_name(ctrl_obj)

def add_orient_constraint_control(trg_obj, ctrl_obj, parent):
    pvt_align_control(trg_obj, ctrl_obj, parent)
    cmds.orientConstraint( ctrl_obj, trg_obj, mo=True, n=ctrl_obj + '_orientConstraint')

def add_parent_constraint_control(trg_obj, ctrl_obj, parent):
    pvt_align_control(trg_obj, ctrl_obj, parent)
    cmds.parentConstraint( ctrl_obj, trg_obj, mo=True, n=ctrl_obj + '_parentConstraint')

def add_scale_constraint_control(trg_obj, ctrl_obj, parent):
    pvt_align_control(trg_obj, ctrl_obj, parent)
    cmds.scaleConstraint( ctrl_obj, trg_obj, mo=True, n=ctrl_obj + '_scaleConstraint')

def lock_trans(obj):
    cmds.setAttr(obj + '.tx', lock=True)
    cmds.setAttr(obj + '.ty', lock=True)
    cmds.setAttr(obj + '.tz', lock=True)

def lock_scale(obj):
    cmds.setAttr(obj + '.sx', lock=True)
    cmds.setAttr(obj + '.sy', lock=True)
    cmds.setAttr(obj + '.sz', lock=True)

def lock_trans_and_scale(obj):
    lock_trans(obj)
    lock_scale(obj) 