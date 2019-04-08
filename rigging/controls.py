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

    '''
    GENERIC CONTROLS
    ----------------
    Controls like curve, ellipse, torus are interface 
    compatible with each other. Just switch to work.
    '''
    def build_circle_control(self, **p):
        n=self.cn + '_ctrl_' + p['prefix']
        axis = p['axis'] if 'axis' in p else (0,1,0)
        r=p['radius']
        cmds.circle( nr=axis, c=(0, 0, 0), r=r, n=n)
        return n

    def build_torus_control(self, **p):
        n=self.cn + '_ctrl_' + p['prefix']
        axis = p['axis'] if 'axis' in p else (0,1,0)
        scale = p['scale'] if 'scale' in p else (1,1,1)
        hr = p['hr'] if 'hr' in p else 0.05 # height ratio
        r=p['radius']
        cmds.torus(ax=axis, ssw=0, esw=360, msw=360, r=r, hr=hr, d=3, ut=0, tol=0.01, s=8, nsp=4, ch=1, n=n)
        cmds.scale(scale[0], scale[1], scale[2], n, absolute=True)
        return n

    def build_ellipse_control(self, **p):
        n = self.build_circle_control(**p)
        s = p['scale']
        cmds.scale(s[0], s[1], s[2], n, absolute=True)
        return n
    #-------end generic controls-------#

    # Supports optional relative offset
    def pvt_align_control(self, trg_obj, ctrl_obj, parent=None, **p):
        if parent is not None:
            cmds.parent(ctrl_obj, parent)
        gu.move_to_pos_of(trg_obj, ctrl_obj)
        
        if 'offset' in p:
            loc = p['offset']
            cmds.move(loc[0],loc[1],loc[2], ctrl_obj, relative=True)

        gu.freeze_transformations_by_name(ctrl_obj)

    def add_orient_constraint_control(self, **p):
        ctrl_obj = self.cn + '_ctrl_' + p['target']
        target = self.cn + '_' + p['target']
        self.pvt_align_control(target, ctrl_obj, p['parent'])
        n = ctrl_obj + '_orientConstraint'
        cmds.orientConstraint( ctrl_obj, target, mo=True, n=n)
        cmds.parent(n, self.CONTROLS_EXTRAS_GROUP)

    def add_parent_constraint_control(self, **p):
        ctrl_obj = self.cn + '_ctrl_' + p['target']
        target = self.cn + '_' + p['target']
        self.pvt_align_control(target, ctrl_obj, p['parent'])
        n=ctrl_obj + '_parentConstraint'
        cmds.parentConstraint( ctrl_obj, target, mo=True, n=n)
        cmds.parent(n, self.CONTROLS_EXTRAS_GROUP)

    def add_scale_constraint_control(self, **p):
        ctrl_obj = self.cn + '_ctrl_' + p['target']
        target = self.cn + '_' + p['target']
        self.pvt_align_control(target, ctrl_obj, p['parent'])
        n=ctrl_obj + '_scaleConstraint'
        cmds.scaleConstraint( ctrl_obj, target, mo=True, n=n)
        cmds.parent(n, self.CONTROLS_EXTRAS_GROUP)

    def add_point_constraint_control(self, **p):
        ctrl_obj = self.cn + '_ctrl_' + p['target']
        target = self.cn + '_' + p['target']
        self.pvt_align_control(target, ctrl_obj, p['parent'])
        n=ctrl_obj + '_pointConstraint'
        cmds.pointConstraint( ctrl_obj, target, mo=True, n=n)
        cmds.parent(n, self.CONTROLS_EXTRAS_GROUP)

    def add_poleVector_constraint_control(self, **p):
        ctrl_obj = self.cn + '_ctrl_' + p['control']
        ik_handle = self.cn + '_' + p['ik_handle']
        align_joint = self.cn + '_' + p['align_joint']
        self.pvt_align_control(align_joint, ctrl_obj, p['parent'], offset=(0,0,40))
        n=ctrl_obj + '_poleVecConstraint'
        cmds.poleVectorConstraint( ctrl_obj, ik_handle, n=n)
        cmds.parent(n, self.CONTROLS_EXTRAS_GROUP)
        cmds.setAttr(ctrl_obj + '.ty', lock=True)
        cmds.setAttr(ctrl_obj + '.tz', lock=True)
        lock_rotate_and_scale(ctrl_obj)

    def create_IK_Handles(self, **p):
        cn = self.cn
        n = cn + '_RightFoot_ikHandle'
        cmds.ikHandle(n=n, sj=cn+'_RightUpLeg', ee=cn+'_RightFoot', sol='ikRPsolver')
        cmds.setAttr(n + '.stickiness', 1)
        gu.freeze_transformations_by_name(n)
        cmds.parent(n, self.CONTROLS_EXTRAS_GROUP)
        n = cn + '_LeftFoot_ikHandle'
        cmds.ikHandle(n=n, sj=cn+'_LeftUpLeg', ee=cn+'_LeftFoot', sol='ikRPsolver')
        cmds.setAttr(n + '.stickiness', 1)
        gu.freeze_transformations_by_name(n)
        cmds.parent(n, self.CONTROLS_EXTRAS_GROUP) 
    
    def create_footRoll_controls(self, **p):
        cn = self.cn
        
        # ---------RIGHT---------
        joint_n = cn + '_RightFoot'
        nD = cn + '_RightFoot_FRoll_LocD'
        cmds.spaceLocator(n=nD)
        self.pvt_align_control(joint_n, nD)
        
        joint_n = cn + '_RightToeBase'
        nC = cn + '_RightFoot_FRoll_LocC'
        cmds.spaceLocator(n=nC)
        self.pvt_align_control(joint_n, nC)
        
        joint_n = cn + '_RightToeEnd'
        nB = cn + '_RightFoot_FRoll_LocB'
        cmds.spaceLocator(n=nB)
        self.pvt_align_control(joint_n, nB)

        joint_n = cn + '_RightFoot'
        nA = cn + '_RightFoot_FRoll_LocA'
        cmds.spaceLocator(n=nA)
        #self.pvt_align_control(joint_n, nA)
        gu.move_to_x_pos_of(nD, nA)
        gu.move_to_z_pos_of(nD, nA)
        gu.move_to_y_pos_of(nC, nA)

        cmds.parent(nA, self.CONTROLS_EXTRAS_GROUP)
        cmds.parent(nB, nA) 
        cmds.parent(nC, nB)
        cmds.parent(nD, nC)
        gu.freeze_transformations_by_name(nD)
        gu.freeze_transformations_by_name(nC)
        gu.freeze_transformations_by_name(nB)
        gu.freeze_transformations_by_name(nA)

        #---- LEFT ----
        joint_n = cn + '_LeftFoot'
        nD = cn + '_LeftFoot_FRoll_LocD'
        cmds.spaceLocator(n=nD)
        self.pvt_align_control(joint_n, nD)
        
        joint_n = cn + '_LeftToeBase'
        nC = cn + '_LeftFoot_FRoll_LocC'
        cmds.spaceLocator(n=nC)
        self.pvt_align_control(joint_n, nC)
        
        joint_n = cn + '_LeftToeEnd'
        nB = cn + '_LeftFoot_FRoll_LocB'
        cmds.spaceLocator(n=nB)
        self.pvt_align_control(joint_n, nB)

        joint_n = cn + '_LeftFoot'
        nA = cn + '_LeftFoot_FRoll_LocA'
        cmds.spaceLocator(n=nA)
        #self.pvt_align_control(joint_n, nA)
        gu.move_to_x_pos_of(nD, nA)
        gu.move_to_z_pos_of(nD, nA)
        gu.move_to_y_pos_of(nC, nA)

        cmds.parent(nA, self.CONTROLS_EXTRAS_GROUP)
        cmds.parent(nB, nA) 
        cmds.parent(nC, nB)
        cmds.parent(nD, nC)
        gu.freeze_transformations_by_name(nD)
        gu.freeze_transformations_by_name(nC)
        gu.freeze_transformations_by_name(nB)
        gu.freeze_transformations_by_name(nA)

        #---constraints----
        nD = cn + '_RightFoot_FRoll_LocD'
        n = nD + '_pointConstraint_RightFoot_ikHandle'
        cmds.pointConstraint( nD, cn + '_RightFoot_ikHandle', mo=True, n=n)
        cmds.parent(n, self.CONTROLS_EXTRAS_GROUP)

        nD = cn + '_LeftFoot_FRoll_LocD'
        n = nD + '_pointConstraint_LeftFoot_ikHandle'
        cmds.pointConstraint( nD, cn + '_LeftFoot_ikHandle', mo=True, n=n)
        cmds.parent(n, self.CONTROLS_EXTRAS_GROUP)
        
        # orient constraint
        nB = cn + '_RightFoot_FRoll_LocB'
        n = nB + '_orientConstraint_RightToeBase'
        cmds.orientConstraint( nB, cn + '_RightToeBase', mo=True, n=n)
        cmds.parent(n, self.CONTROLS_EXTRAS_GROUP)

        nB = cn + '_LeftFoot_FRoll_LocB'
        n = nB + '_orientConstraint_LeftToeBase'
        cmds.orientConstraint( nB, cn + '_LeftToeBase', mo=True, n=n)
        cmds.parent(n, self.CONTROLS_EXTRAS_GROUP)

        nC = cn + '_RightFoot_FRoll_LocC'
        n = nC + '_orientConstraint_RightFoot'
        cmds.orientConstraint( nC, cn + '_RightFoot', mo=True, n=n)
        cmds.parent(n, self.CONTROLS_EXTRAS_GROUP)

        nC = cn + '_LeftFoot_FRoll_LocC'
        n = nC + '_orientConstraint_LeftFoot'
        cmds.orientConstraint( nC, cn + '_LeftFoot', mo=True, n=n)
        cmds.parent(n, self.CONTROLS_EXTRAS_GROUP)


def lock_trans(obj):
    cmds.setAttr(obj + '.tx', lock=True)
    cmds.setAttr(obj + '.ty', lock=True)
    cmds.setAttr(obj + '.tz', lock=True)

def lock_scale(obj):
    cmds.setAttr(obj + '.sx', lock=True)
    cmds.setAttr(obj + '.sy', lock=True)
    cmds.setAttr(obj + '.sz', lock=True)

def lock_rotate(obj):
    cmds.setAttr(obj + '.rx', lock=True)
    cmds.setAttr(obj + '.ry', lock=True)
    cmds.setAttr(obj + '.rz', lock=True)

def lock_trans_and_scale(obj):
    lock_trans(obj)
    lock_scale(obj) 

def lock_rotate_and_scale(obj):
    lock_rotate(obj)
    lock_scale(obj) 