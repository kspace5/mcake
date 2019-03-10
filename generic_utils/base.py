from __future__ import print_function
import maya.cmds as cmds

# Mass rename with string replace
def rename_selected_by_replace(old_str, new_str):
    objs = cmds.ls(sl=True)
    for obj in objs:
        str = obj.replace(old_str, new_str)
        print(str)
        cmds.rename(obj, str)
        print("Done for " + obj)

# Does center pivot and freeze transforma on all rename_selected_by_replace
# Super useful method
def freeze_and_center():
    objs = cmds.ls(sl=True)
    for obj in objs:
        cmds.makeIdentity(obj, apply=True, t=1, r=1, s=1, n=0, pn=1)
        cmds.CenterPivot(obj)
        print("Freeze and Center done for {0}".format(obj))

def freeze_and_center_by_name(obj):
    cmds.makeIdentity(obj, apply=True, t=1, r=1, s=1, n=0, pn=1)
    cmds.CenterPivot(obj)
    print("Freeze and Center done for {0}".format(obj))

def freeze_transformations_by_name(obj):
    cmds.makeIdentity(obj, apply=True, t=1, r=1, s=1, n=0, pn=1)
    print("Freeze Trans done for {0}".format(obj))

def zero_x_pivot():
    objs = cmds.ls(sl=True)
    for obj in objs:
        cmds.move(0, 0, 0, obj + ".scalePivot",obj + ".rotatePivot", absolute=True)
        print("zero_x_pivot done for {0}".format(obj))

def duplicate_and_mirror():
    objs = cmds.ls(sl=True)
    for obj in objs:
        ret = cmds.duplicate(obj, returnRootsOnly=True)
        cmds.scale(-1, 1, 1, obj)
        print("duplicate_and_mirror done for {0}".format(ret))

# Do all above (3 methods)
def duplicate_and_mirror_x():
    freeze_and_center()
    zero_x_pivot()
    duplicate_and_mirror()

# return an array as in [0.0, 94.11794271192076, -5.187759884926814]
def get_world_pos(obj):
    loc = cmds.xform(obj, q=True, ws=True, rp=True)
    return loc

def move_to_pos_of(src_obj, trg_obj):
    loc = get_world_pos(src_obj)
    cmds.move(loc[0],loc[1], loc[2], trg_obj, absolute=True)
