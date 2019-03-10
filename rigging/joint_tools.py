from __future__ import print_function
import maya.cmds as cmds
import numpy as np

def align_joints():
    objs = cmds.ls(sl=True)
    for obj in objs:
        cmds.setAttr("{0}.translateZ".format(obj), 0)
        cmds.setAttr("{0}.jointOrientX".format(obj), 0)
        cmds.setAttr("{0}.jointOrientY".format(obj), 0)
        print("Done for " + obj)

def orient_joints_to_world_all_selected():
    objs = cmds.ls(sl=True)
    for obj in objs:
        cmds.joint(obj, e=True, oj="none", ch=True, zso=True)
        print("Done for " + obj)

def orient_joints_to_x_all_selected():
    objs = cmds.ls(sl=True)
    for obj in objs:
        cmds.joint(obj, e=True, oj="xzy", secondaryAxisOrient="xup", ch=True, zso=True)
        print("Done for " + obj)

def is_zero(v):
    return abs(v - 0.0) < 1.0e-5

# IMPORTANT: This is determined based on joint orient
def check_joint_integrity_all_selected():
    rmap = {}
    objs = cmds.ls(sl=True)
    for obj in objs:
        k = "{0}.rotateX".format(obj)
        v = cmds.getAttr(k)
        rmap[k] = (is_zero(v), v)
        k = "{0}.rotateX".format(obj)
        v = cmds.getAttr(k)
        rmap[k] = (is_zero(v), v)
        k = "{0}.rotateX".format(obj)
        v = cmds.getAttr(k)
        rmap[k] = (is_zero(v), v)
        k = "{0}.rotateX".format(obj)
        v = cmds.getAttr(k)
        rmap[k] = (is_zero(v), v)
        k = "{0}.rotateX".format(obj)
        v = cmds.getAttr(k)
        rmap[k] = (is_zero(v), v)
    integ = True
    for k, v in rmap.items():
        if not v[0]:
            integ = False
            print("{0}: {1}".format(k,v[1]))
    return integ