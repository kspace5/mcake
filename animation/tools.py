# For reference - not used directly yet
def swap_key_values():
    objs = cmds.ls(sl=True)
    a = objs[0]
    b = objs[1]
    atx = cmds.getAttr(a + '.tx')
    aty = cmds.getAttr(a + '.ty')
    atz = cmds.getAttr(a + '.tz')
    arx = cmds.getAttr(a + '.rx')
    ary = cmds.getAttr(a + '.ry')
    arz = cmds.getAttr(a + '.rz')

    btx = cmds.getAttr(b + '.tx')
    bty = cmds.getAttr(b + '.ty')
    btz = cmds.getAttr(b + '.tz')
    brx = cmds.getAttr(b + '.rx')
    bry = cmds.getAttr(b + '.ry')
    brz = cmds.getAttr(b + '.rz')

    cmds.setAttr(a + '.tx',btx)
    cmds.setAttr(a + '.ty',bty)
    cmds.setAttr(a + '.tz',btz)
    cmds.setAttr(a + '.rx',brx)
    cmds.setAttr(a + '.ry',bry)
    cmds.setAttr(a + '.rz',brz)

    cmds.setAttr(b + '.tx',atx)
    cmds.setAttr(b + '.ty',aty)
    cmds.setAttr(b + '.tz',atz)
    cmds.setAttr(b + '.rx',arx)
    cmds.setAttr(b + '.ry',ary)
    cmds.setAttr(b + '.rz',arz)

    print("Done key values swap")