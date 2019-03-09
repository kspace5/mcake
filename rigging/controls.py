from __future__ import print_function
import maya.cmds as cmds
import mcake.generic_utils.base as gu
reload(gu)

# Control name/prefix mappings
CTRL_KEY = '_ctrl_'

JOINTS_MASTER_REF = '_Reference' # Already created by Maya HIK
CONTROLS_TOP_GROUP = CTRL_KEY + 'Reference' # Highest levele group created for all controls
# Controls
CTRL_GLOBAL = CTRL_KEY + 'global'
CTRL_COG = CTRL_KEY + 'cog'

def c_top_grp(cn):
    return cn + CONTROLS_TOP_GROUP

def build_global_control(cn):
    ctrl_name = cn + CTRL_GLOBAL
    cmds.curve( p=[(0 ,0 ,40),(-30 ,0 ,30),(-30, 0, 0),(30, 0, 0),(30 ,0 ,30),(0, 0, 40)],d=2, n=ctrl_name)
    gu.freeze_and_center_by_name(ctrl_name)
    cmds.group( ctrl_name, n=c_top_grp(cn) )
    gu.freeze_and_center_by_name(c_top_grp(cn))
    cmds.move(0, 0, -20, r=True, os=True, wd=True)
    
def bind_global_control(cn):
    cmds.parentConstraint( cn + CTRL_GLOBAL, cn + JOINTS_MASTER_REF, mo=True, n=cn + "_ctrl_global_parentConstraint")
    cmds.scaleConstraint( cn + CTRL_GLOBAL, cn + JOINTS_MASTER_REF, mo=True, n=cn + "_ctrl_global_scaleConstraint")

def build_cog_control(cn):
    name = cn + CTRL_COG
    cmds.circle( nr=(0, 1, 0), c=(0, 0, 0), r=25 ,n=name)
    cmds.parent( name, c_top_grp(cn))