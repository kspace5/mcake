from __future__ import print_function
import maya.cmds as cmds

# Mass rename with string replace
def rename_selected_by_replace(old_str, new_str):
    obj_names = cmds.ls(sl=True)
    for obj_name in obj_names:
        str = obj_name.replace(old_str, new_str)
        print(str)
        cmds.rename(obj_name, str)
        print("Done for " + obj_name)


# Does center pivot and freeze transforma on all rename_selected_by_replace
# Super useful method
def freeze_and_center():
    obj_names = cmds.ls(sl=True)
    for obj_name in obj_names:
        cmds.makeIdentity(obj_name, apply=True, t=1, r=1, s=1, n=0, pn=1)
        cmds.CenterPivot(obj_name)
        print("Done for {0}".format(obj_name))


def zero_x_pivot():
    obj_names = cmds.ls(sl=True)
    for obj_name in obj_names:
        cmds.move(0, 0, 0, obj_name + ".scalePivot",obj_name + ".rotatePivot", absolute=True)
        print("Done for {0}".format(obj_name))

def duplicate_and_mirror():
    obj_names = cmds.ls(sl=True)
    for obj_name in obj_names:
        ret = cmds.duplicate(obj_name, returnRootsOnly=True)
        cmds.scale(-1, 1, 1, obj_name)
        print("Done for {0}".format(ret))

# Do all above (3 methods)
def duplicate_and_mirror_x():
    freeze_and_center()
    zero_x_pivot()
    duplicate_and_mirror()