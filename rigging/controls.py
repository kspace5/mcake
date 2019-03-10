import maya.cmds as cmds
import mcake.generic_utils.base as gu
reload(gu)

class BipedControlBuilder:
    def __init__(self, charName):
        self.cn = charName
        self.CONTROLS_TOP_GROUP = self.cn + '_ctrl_Reference'
        self.CONTROLS_EXTRAS_GROUP = self.cn + '_ctrl_Extras'
        self.MAYA_HIK_REFERENCE = self.cn + '_Reference'

    def build_global_control(self):
        ctrl_name = self.cn + '_ctrl_global'
        cmds.curve( p=[(0 ,0 ,40),(-30 ,0 ,30),(-30, 0, 0),(30, 0, 0),(30 ,0 ,30),(0, 0, 40)],d=2, n=ctrl_name)
        cmds.move(0, 0, -20, ctrl_name, r=True, os=True, wd=True)
        gu.freeze_and_center_by_name(ctrl_name)
        cmds.group( ctrl_name, n=self.CONTROLS_TOP_GROUP, w=True)
        cmds.group( n=self.CONTROLS_EXTRAS_GROUP, em=True, w=True)
        gu.freeze_and_center_by_name(self.CONTROLS_TOP_GROUP)
        return ctrl_name
        
    def bind_global_control(self):
        n=self.cn + '_ctrl_global_parentConstraint'
        cmds.parentConstraint( self.cn + '_ctrl_global', self.MAYA_HIK_REFERENCE, mo=True, n=n)
        cmds.parent(n, self.CONTROLS_EXTRAS_GROUP)
        n=self.cn + '_ctrl_global_scaleConstraint'
        cmds.scaleConstraint( self.cn + '_ctrl_global', self.MAYA_HIK_REFERENCE, mo=True, n=n)
        cmds.parent(n, self.CONTROLS_EXTRAS_GROUP)

    def build_circle_control(self, prefix, radius=25, axis=(0, 1, 0)):
        n=self.cn + '_ctrl_' + prefix
        cmds.circle( nr=axis, c=(0, 0, 0), r=radius ,n=n)
        #cmds.scale( 3, 3, 3, 'curve1', pivot=(1, 0, 0), absolute=True )
        return n

    def pvt_align_control(self, trg_obj, ctrl_obj, parent):
        cmds.parent(ctrl_obj, parent)
        gu.move_to_pos_of(trg_obj, ctrl_obj)
        gu.freeze_transformations_by_name(ctrl_obj)

    def add_orient_constraint_control(self, trg_obj, parent, ctrl_obj=None):
        ctrl_obj = ctrl_obj or self.cn + '_ctrl_' + trg_obj
        trg_obj = self.cn + '_' + trg_obj
        print(ctrl_obj)
        self.pvt_align_control(trg_obj, ctrl_obj, parent)
        n=ctrl_obj + '_orientConstraint'
        cmds.orientConstraint( ctrl_obj, trg_obj, mo=True, n=n)
        cmds.parent(n, self.CONTROLS_EXTRAS_GROUP)

    def add_parent_constraint_control(self, trg_obj, parent, ctrl_obj=None):
        ctrl_obj = ctrl_obj or self.cn + '_ctrl_' + trg_obj
        trg_obj = self.cn + '_' + trg_obj
        self.pvt_align_control(trg_obj, ctrl_obj, parent)
        n=ctrl_obj + '_parentConstraint'
        cmds.parentConstraint( ctrl_obj, trg_obj, mo=True, n=n)
        cmds.parent(n, self.CONTROLS_EXTRAS_GROUP)

    def add_scale_constraint_control(self, trg_obj, parent, ctrl_obj=None):
        ctrl_obj = ctrl_obj or self.cn + '_ctrl_' + trg_obj
        trg_obj = self.cn + '_' + trg_obj
        self.pvt_align_control(trg_obj, ctrl_obj, parent)
        n=ctrl_obj + '_scaleConstraint'
        cmds.scaleConstraint( ctrl_obj, trg_obj, mo=True, n=n)
        cmds.parent(n, self.CONTROLS_EXTRAS_GROUP)

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