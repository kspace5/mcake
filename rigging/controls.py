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

    def create_footRoll_driven_keys(self, **p):
        cn = self.cn
        # Custom attributes and driven keys
        n = cn + '_ctrl_RightFoot_FRoll_LocA'
        gu.add_attribute(n, 'midRoll', type='float', min=0, max=50, default=0, keyable=True)
        nC = cn + '_RightFoot_FRoll_LocC.rotateX'
        gu.set_driven_key(n + '.midRoll',nC, 0, 0)
        gu.set_driven_key(n + '.midRoll',nC, 50, 50)

        n = cn + '_ctrl_LeftFoot_FRoll_LocA'
        gu.add_attribute(n, 'midRoll', type='float', min=0, max=50, default=0, keyable=True)
        nC = cn + '_LeftFoot_FRoll_LocC.rotateX'
        gu.set_driven_key(n + '.midRoll',nC, 0, 0)
        gu.set_driven_key(n + '.midRoll',nC, 50, 50)

        n = cn + '_ctrl_RightFoot_FRoll_LocA'
        gu.add_attribute(n, 'baseRoll', type='float', min=-90, max=90, default=0, keyable=True)
        nC = cn + '_RightFoot_FRoll_LocA.rotateX'
        gu.set_driven_key(n + '.baseRoll',nC, -90, -90)
        gu.set_driven_key(n + '.baseRoll',nC, 90, 90)

        n = cn + '_ctrl_LeftFoot_FRoll_LocA'
        gu.add_attribute(n, 'baseRoll', type='float', min=-90, max=90, default=0, keyable=True)
        nC = cn + '_LeftFoot_FRoll_LocA.rotateX'
        gu.set_driven_key(n + '.baseRoll',nC, -90, -90)
        gu.set_driven_key(n + '.baseRoll',nC, 90, 90)

        n = cn + '_ctrl_RightFoot_FRoll_LocA'
        gu.add_attribute(n, 'toeRaise', type='float', min=0, max=120, default=0, keyable=True)
        nC = cn + '_RightFoot_FRoll_LocB.rotateX'
        gu.set_driven_key(n + '.toeRaise',nC, 0, 0)
        gu.set_driven_key(n + '.toeRaise',nC, 120, 120)

        n = cn + '_ctrl_LeftFoot_FRoll_LocA'
        gu.add_attribute(n, 'toeRaise', type='float', min=0, max=120, default=0, keyable=True)
        nC = cn + '_LeftFoot_FRoll_LocB.rotateX'
        gu.set_driven_key(n + '.toeRaise',nC, 0, 0)
        gu.set_driven_key(n + '.toeRaise',nC, 120, 120)

    # Aggregate - finger driver builder
    def add_finger_bend_and_curl_attributes(self, **p):
        self.pvt_add_curl_drivers('RightHand')
        self.pvt_add_curl_drivers('LeftHand')
        
        self.pvt_add_bendBase_drivers('RightHand')
        self.pvt_add_bendBase_drivers('LeftHand')
        self.pvt_add_bendMid_drivers('RightHand')
        self.pvt_add_bendMid_drivers('LeftHand')

        self.pvt_add_spreadBase_drivers('RightHand')
        self.pvt_add_spreadBase_drivers('LeftHand')

    def pvt_add_curl_drivers(self, hand):
        n = self.cn + '_ctrl_' + hand
        gu.add_attribute(n, 'curlThumb', type='float', min=-100, max=100, default=0, keyable=True)
        gu.add_attribute(n, 'curlIndex', type='float', min=-100, max=100, default=0, keyable=True)
        gu.add_attribute(n, 'curlMiddle', type='float', min=-100, max=100, default=0, keyable=True)
        gu.add_attribute(n, 'curlRing', type='float', min=-100, max=100, default=0, keyable=True)
        gu.add_attribute(n, 'curlPinky', type='float', min=-100, max=100, default=0, keyable=True)
        gu.add_attribute(n, 'curlAll', type='float', min=-100, max=100, default=0, keyable=True)

        self.pvt_add_finger_driven_keys_curl(n, hand, 'Thumb')
        self.pvt_add_finger_driven_keys_curl(n, hand, 'Index')
        self.pvt_add_finger_driven_keys_curl(n, hand, 'Middle')
        self.pvt_add_finger_driven_keys_curl(n, hand, 'Ring')
        self.pvt_add_finger_driven_keys_curl(n, hand, 'Pinky')

        # Now set curl all drivers
        all = True
        self.pvt_add_finger_driven_keys_curl(n, hand, 'Thumb', all)
        self.pvt_add_finger_driven_keys_curl(n, hand, 'Index', all)
        self.pvt_add_finger_driven_keys_curl(n, hand, 'Middle', all)
        self.pvt_add_finger_driven_keys_curl(n, hand, 'Ring', all)
        self.pvt_add_finger_driven_keys_curl(n, hand, 'Pinky', all)

    def pvt_add_finger_driven_keys_curl(self, ctrl, prefix, f_name, all=False):
        finger_prefix = self.cn + '_' + prefix

        joint_rot_attr_proc = lambda name, i: finger_prefix + name + str(i) + '.rotateZ'
        attr_driver_proc = lambda f_name: ctrl + '.curlAll' if all is True else ctrl + '.curl' + f_name
        
        attr_driver = attr_driver_proc(f_name)
        
        attr_driven = joint_rot_attr_proc(f_name, 1)
        cur_val = cmds.getAttr(attr_driven)
        gu.set_driven_key(attr_driver, attr_driven, 0, cur_val)
        gu.set_driven_key(attr_driver, attr_driven, 100, cur_val + 100)
        attr_driven = joint_rot_attr_proc(f_name, 2)
        cur_val = cmds.getAttr(attr_driven)
        gu.set_driven_key(attr_driver, attr_driven, 0, cur_val)
        gu.set_driven_key(attr_driver, attr_driven, 100, cur_val + 100)
        attr_driven = joint_rot_attr_proc(f_name, 3)
        cur_val = cmds.getAttr(attr_driven)
        gu.set_driven_key(attr_driver, attr_driven, 0, cur_val)
        gu.set_driven_key(attr_driver, attr_driven, 100, cur_val + 100)

    def pvt_add_bendBase_drivers(self, hand):
        n = self.cn + '_ctrl_' + hand
        gu.add_attribute(n, 'bendBaseThumb', type='float', min=-100, max=100, default=0, keyable=True)
        gu.add_attribute(n, 'bendBaseIndex', type='float', min=-100, max=100, default=0, keyable=True)
        gu.add_attribute(n, 'bendBaseMiddle', type='float', min=-100, max=100, default=0, keyable=True)
        gu.add_attribute(n, 'bendBaseRing', type='float', min=-100, max=100, default=0, keyable=True)
        gu.add_attribute(n, 'bendBasePinky', type='float', min=-100, max=100, default=0, keyable=True)

        self.pvt_add_finger_driven_keys_bendBase(n, hand, 'Thumb')
        self.pvt_add_finger_driven_keys_bendBase(n, hand, 'Index')
        self.pvt_add_finger_driven_keys_bendBase(n, hand, 'Middle')
        self.pvt_add_finger_driven_keys_bendBase(n, hand, 'Ring')
        self.pvt_add_finger_driven_keys_bendBase(n, hand, 'Pinky')

    def pvt_add_finger_driven_keys_bendBase(self, ctrl, prefix, f_name):
        finger_prefix = self.cn + '_' + prefix

        joint_rot = lambda name, i: finger_prefix + name + str(i) + '.rotateZ'
        attr = joint_rot(f_name, 1)
        cur_val = cmds.getAttr(attr)
        gu.set_driven_key(ctrl + '.bendBase' + f_name,attr, 0, cur_val)
        gu.set_driven_key(ctrl + '.bendBase' + f_name,attr, 100, cur_val + 100)
       

    def pvt_add_bendMid_drivers(self, hand):
        n = self.cn + '_ctrl_' + hand
        gu.add_attribute(n, 'bendMidThumb', type='float', min=0, max=100, default=0, keyable=True)
        gu.add_attribute(n, 'bendMidIndex', type='float', min=0, max=100, default=0, keyable=True)
        gu.add_attribute(n, 'bendMidMiddle', type='float', min=0, max=100, default=0, keyable=True)
        gu.add_attribute(n, 'bendMidRing', type='float', min=0, max=100, default=0, keyable=True)
        gu.add_attribute(n, 'bendMidPinky', type='float', min=0, max=100, default=0, keyable=True)

        self.pvt_add_finger_driven_keys_bendMid(n, hand, 'Thumb')
        self.pvt_add_finger_driven_keys_bendMid(n, hand, 'Index')
        self.pvt_add_finger_driven_keys_bendMid(n, hand, 'Middle')
        self.pvt_add_finger_driven_keys_bendMid(n, hand, 'Ring')
        self.pvt_add_finger_driven_keys_bendMid(n, hand, 'Pinky')

    def pvt_add_finger_driven_keys_bendMid(self, ctrl, prefix, f_name):
        finger_prefix = self.cn + '_' + prefix

        joint_rot = lambda name, i: finger_prefix + name + str(i) + '.rotateZ'
        attr = joint_rot(f_name, 1)
       
        attr = joint_rot(f_name, 2)
        cur_val = cmds.getAttr(attr)
        gu.set_driven_key(ctrl + '.bendMid' + f_name,attr, 0, cur_val)
        gu.set_driven_key(ctrl + '.bendMid' + f_name,attr, 100, cur_val + 100)
        
    def pvt_add_spreadBase_drivers(self, hand):
        n = self.cn + '_ctrl_' + hand
        gu.add_attribute(n, 'spreadBaseAll', type='float', min=-100, max=100, default=0, keyable=True)

        # Each finger gets a scaled spread effect
        self.pvt_add_finger_driven_keys_spreadBase(n, hand, 'Thumb', 1.0)
        self.pvt_add_finger_driven_keys_spreadBase(n, hand, 'Index', 0.8)
        self.pvt_add_finger_driven_keys_spreadBase(n, hand, 'Middle', 0.4)
        self.pvt_add_finger_driven_keys_spreadBase(n, hand, 'Ring', -0.4)
        self.pvt_add_finger_driven_keys_spreadBase(n, hand, 'Pinky', -0.8)

    def pvt_add_finger_driven_keys_spreadBase(self, ctrl, prefix, f_name, scale):
        finger_prefix = self.cn + '_' + prefix

        joint_rot = lambda name, i: finger_prefix + name + str(i) + '.rotateY'
        attr = joint_rot(f_name, 1)
        cur_val = cmds.getAttr(attr)
        gu.set_driven_key(ctrl + '.spreadBaseAll',attr, 0, cur_val)
        gu.set_driven_key(ctrl + '.spreadBaseAll',attr, 100, cur_val + (100 * scale))

def lock_visibility(obj):
    cmds.setAttr(obj + '.v', lock=True)

def lock_trans(obj):
    cmds.setAttr(obj + '.tx', lock=True)
    cmds.setAttr(obj + '.ty', lock=True)
    cmds.setAttr(obj + '.tz', lock=True)
    cmds.setAttr(obj + '.v', lock=True)

def lock_scale(obj):
    cmds.setAttr(obj + '.sx', lock=True)
    cmds.setAttr(obj + '.sy', lock=True)
    cmds.setAttr(obj + '.sz', lock=True)
    cmds.setAttr(obj + '.v', lock=True)

def lock_rotate(obj):
    cmds.setAttr(obj + '.rx', lock=True)
    cmds.setAttr(obj + '.ry', lock=True)
    cmds.setAttr(obj + '.rz', lock=True)
    cmds.setAttr(obj + '.v', lock=True)

def lock_trans_and_scale(obj):
    lock_trans(obj)
    lock_scale(obj) 

def lock_rotate_and_scale(obj):
    lock_rotate(obj)
    lock_scale(obj) 