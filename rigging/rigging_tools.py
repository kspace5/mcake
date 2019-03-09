import maya.cmds as cmds
import functools
import mcake.generic_utils.ui_utils as uu

def createRiggingToolsUI():
    
    windowID = 'myWindowID'
    
    if cmds.window( windowID, exists=True ):
        cmds.deleteUI( windowID )
        
    cmds.window( windowID, title="MCAKE: Rigging Tools", sizeable=False, resizeToFitChildren=True )
    
    cmds.rowColumnLayout( numberOfColumns=3, columnWidth=[ (1,120), (2,120), (3,120) ], columnOffset=[ (1,'right',3) ] )
    
    def applyCallback( pStartTimeField, pEndTimeField, pTargetAttributeField, *pArgs ):
        print('Apply button pressed.')
    
    cmds.button( label='Mirror Rot Trans [y,z]', command=eh_mirror_rot_trans )
    cmds.button( label='Mirror Rot', command=eh_mirror_rot )
    
    # Cancel button
    cmds.button( label='Cancel', command=functools.partial( g_cancelCallback, windowID))

    cmds.showWindow()


def g_cancelCallback(windowID,  *pArgs ):
    if cmds.window( windowID, exists=True ):
        cmds.deleteUI( windowID )

# Event Handler
def eh_mirror_rot_trans(*pArgs):
    print("Mirror Keyable")
    objs = cmds.ls(sl=True)
    c = 0
    src = []
    target = []
    for obj in objs:
        if c == 0:
            src.append(cmds.getAttr("{0}.translateX".format(obj)))
            src.append(cmds.getAttr("{0}.translateY".format(obj)))
            src.append(cmds.getAttr("{0}.translateZ".format(obj)))
            src.append(cmds.getAttr("{0}.rotateX".format(obj)))
            src.append(cmds.getAttr("{0}.rotateY".format(obj)))
            src.append(cmds.getAttr("{0}.rotateZ".format(obj)))
            print("Source: " + obj)
        else:
            target.append(cmds.getAttr("{0}.translateX".format(obj)))
            target.append(cmds.getAttr("{0}.translateY".format(obj)))
            target.append(cmds.getAttr("{0}.translateZ".format(obj)))
            target.append(cmds.getAttr("{0}.rotateX".format(obj)))
            target.append(cmds.getAttr("{0}.rotateY".format(obj)))
            target.append(cmds.getAttr("{0}.rotateZ".format(obj)))
            print("Target: " + obj)
        c += 1
    
    c = 0
    for obj in objs:
        if c == 0:
            #cmds.setAttr("{0}.translateX".format(obj), -1 * target[0])
            cmds.setAttr("{0}.translateY".format(obj), target[1])
            cmds.setAttr("{0}.translateZ".format(obj), target[2])
            cmds.setAttr("{0}.rotateX".format(obj), target[3])
            cmds.setAttr("{0}.rotateY".format(obj), target[4])
            cmds.setAttr("{0}.rotateZ".format(obj), target[5])

            print("Copied to " + obj)
        else:
            #cmds.setAttr("{0}.translateX".format(obj), -1 * src[0])
            cmds.setAttr("{0}.translateY".format(obj), src[1])
            cmds.setAttr("{0}.translateZ".format(obj), src[2])
            cmds.setAttr("{0}.rotateX".format(obj), src[3])
            cmds.setAttr("{0}.rotateY".format(obj), src[4])
            cmds.setAttr("{0}.rotateZ".format(obj), src[5])

            print("Copied to " + obj)
        c += 1
    print("Mirror Keyable - Done")

def eh_mirror_rot(*pArgs):
    print("Mirror Keyable")
    objs = cmds.ls(sl=True)
    c = 0
    src = []
    target = []
    for obj in objs:
        if c == 0:
            src.append(cmds.getAttr("{0}.rotateX".format(obj)))
            src.append(cmds.getAttr("{0}.rotateY".format(obj)))
            src.append(cmds.getAttr("{0}.rotateZ".format(obj)))
            print("Source: " + obj)
        else:
            target.append(cmds.getAttr("{0}.rotateX".format(obj)))
            target.append(cmds.getAttr("{0}.rotateY".format(obj)))
            target.append(cmds.getAttr("{0}.rotateZ".format(obj)))
            print("Target: " + obj)
        c += 1
    
    c = 0
    for obj in objs:
        if c == 0:
            cmds.setAttr("{0}.rotateX".format(obj), target[1])
            cmds.setAttr("{0}.rotateY".format(obj), target[2])
            cmds.setAttr("{0}.rotateZ".format(obj), target[3])

            print("Copied to " + obj)
        else:
            cmds.setAttr("{0}.rotateX".format(obj), src[1])
            cmds.setAttr("{0}.rotateY".format(obj), src[2])
            cmds.setAttr("{0}.rotateZ".format(obj), src[3])

            print("Copied to " + obj)
        c += 1
    print("Mirror Keyable - Done")