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

def orient_joints_to_world():
    objs = cmds.ls(sl=True)
    for obj in objs:
        cmds.joint(obj, e=True, oj="none", ch=True, zso=True)
        print("Done for " + obj)

def is_zero(v):
    return abs(v - 0.0) < 1.0e-5

def check_joint_integrity():
    rmap = {}
    objs = cmds.ls(sl=True)
    for obj in objs:
        v = cmds.getAttr("{0}.rotateX".format(obj))
        rmap[obj] = (is_zero(v), v)
        v = cmds.getAttr("{0}.rotateY".format(obj))
        rmap[obj] = (is_zero(v), v)
        v3 = cmds.getAttr("{0}.rotateZ".format(obj))
        rmap[obj] = (is_zero(v), v)
        v = cmds.getAttr("{0}.jointOrientX".format(obj))
        rmap[obj] = (is_zero(v), v)
        v = cmds.getAttr("{0}.jointOrientY".format(obj))
        rmap[obj] = (is_zero(v), v)
    integ = True
    for k in rmap:
        if not rmap[k][0]:
            integ = False
            print("{0}: {1}".format(k,rmap[k][1]))
    return integ

#check_joint_integrtity()
