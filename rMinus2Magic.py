import random
import pypot.dynamixel
import time
import numpy as np
from pprint import pprint
import xml.etree.cElementTree as ET
from collections import Counter
from copy import deepcopy
from pygame import mixer

mixer.init()

class Dxl(object):
    def __init__(self,port_id=0, scan_limit=25, lock=-1,debug=False):
        # Initializes Dynamixel Object
        # Port ID is zero by default
        ports = pypot.dynamixel.get_available_ports()
        if not ports:
            raise IOError('no port found!')

        print('ports found', ports)
        print('connecting on the first available port:', ports[port_id])
        dxl_io = pypot.dynamixel.DxlIO(ports[port_id])
        ids = dxl_io.scan(range(25))
        print(ids)

        if lock > 0:
            if len(ids) < lock:
                raise RuntimeError("Couldn't detect all motors.")

        self.dxl_io = dxl_io
        self.ids = ids
        debug_speeds = [90 for x in ids]
        unleash = [1023 for x in ids]
        if debug:
            dxl_io.set_moving_speed(dict(zip(ids,debug_speeds)))
        else:
            dxl_io.set_moving_speed(dict(zip(ids, unleash)))

    def directWrite(self,dicta):
        self.dxl_io.set_goal_position(dicta)

    def setPos(self,pose):
        '''
        for k in pose.keys():
            if k not in self.ids:
                del pose[k]
        '''
        writ = {key: value for key, value in pose.items() if key in self.ids}
        #print writ
        self.dxl_io.set_goal_position(writ)

    def getPos(self):
        return Motion(1," ".join(map(str,self.dxl_io.get_present_position(self.ids))),0)

    def setMotor(self,id,angle):
        self.dxl_io.set_goal_position({id:angle})




class XmlTree(object):

    def __init__(self,str):
        try:
            with open(str) as f:
                pass
            self.tree = ET.ElementTree(file=str)
        except:
            raise RuntimeError("File not found.")

    def parsexml(self,text):
        find = "PageRoot/Page[@name='" + text + "']/steps/step"
        motions = []
        prev_frame = 0
        steps = [x for x in self.tree.findall(find)]
        if len(steps)==0:
            # print find
            raise RuntimeError("ParseFail!")
        for step in steps:
            motion = Motion(step.attrib['frame'], step.attrib['pose'], prev_frame)
            prev_frame = step.attrib['frame']
            motions.append(motion)

        return motions

    def superparsexml(self,text,exclude=[],offsets=[]):
        find = "FlowRoot/Flow[@name='"+text+"']/units/unit"
        steps = [x for x in self.tree.findall(find)]
        if len(steps)==0:
            # print find
            raise RuntimeError("ParseFail!")
        motionsets = []
        for step in steps:
            motionsets.append(MotionSet(self.parsexml(step.attrib['main']),speed=float(step.attrib['mainSpeed']),exclude=exclude,offsets=offsets))

        return motionsets



class Motion(object):
    def __init__(self,frame,pose,prev_frame):
        self.frame = int(frame)
        self.pose = {}
        self.delay = self.frame-int(prev_frame)
        for i,p in enumerate(pose.split()):
            self.pose[i+1] =float(p)

    def __str__(self):
        return "Frame:"+str(self.frame) + "      Delay:"+str(self.delay) + "     Pose:"+" ".join(map(str,self.pose.values()))

    def updatePose(self,offset,add=True):
        if add:
            for k in offset.keys():
                if offset[k]=='i':
                    self.pose[k]=-self.pose[k]
                else:
                    self.pose[k] += offset[k]
        else:
            for k in offset.keys():
                if offset[k]=='i':
                    self.pose[k]=-self.pose[k]
                else:
                    self.pose[k] -= offset[k]


    def write(self,state, speed,exclude=[],offset={}):
        begpos = state.pose
        endpos = self.pose
        frames = []
        ids = []
        for k in endpos.keys():
            try:
                begpos[k]
            except:
                begpos[k]=0
            if begpos[k]!=endpos[k] and k not in exclude:
                frames.append(np.linspace(begpos[k],endpos[k],self.delay))
                ids.append(k)

        frames = zip(*frames)
        for f in frames:
            writ = dict(zip(ids, f))
            dxl.setPos(writ)
            time.sleep(0.008 / speed)
            # print writ



class MotionSet(object):
    def __init__(self,motions,speed=1.0,exclude =[],offsets=[]):
        self.motions = motions
        self.speed = speed
        self.exclude = exclude
        self.offsets = offsets
        self.loaded = False

    def setExclude(self,list):
        self.exclude = list

    def setSpeed(self,speed):
        self.speed = speed

    def stateUpdater(self,motion):
        global state
        for k in motion.pose.keys():
            state.pose[k]=motion.pose[k]

    def execute(self,speed=-1,iter=1):
        if speed<0:
            speed = self.speed
        if not self.loaded:
            for offset in self.offsets:
                for motion in self.motions:
                    motion.updatePose(offset)
            self.loaded = True

        while iter>0:
            for motion in self.motions:
                motion.write(state,speed,self.exclude)
                self.stateUpdater(motion)
            iter-=1

class Action():
    def __init__(self,motionsets):
        self.motionsets=motionsets

    def add(self,motionsets):
        self.motionsets.extend(motionsets)

    def execute(self,iter=1,speed=1):
        while iter>0:
            for motionset in self.motionsets:
                # for m in motionset.motions:
                #     print m
                orig = motionset.speed
                motionset.speed = motionset.speed*speed
                motionset.execute()
                motionset.speed = orig
            iter -= 1

class Head():
    def __init__(self,dxl):
        self.dxl = dxl
        self.pan_motor  = 19
        self.tilt_motor = 20
        self.pan_angle = 0
        self.tilt_angle = 90
        self.write()

    def updateState(self,dicta):
        global state
        state.updatePose(dicta)

    def write(self):
        self.dxl.directWrite({self.pan_motor:self.pan_angle,self.tilt_motor:self.tilt_angle})



    def pan_left(self,deg=10):
        self.pan_angle += deg
        self.updateState({self.pan_motor:deg})
        self.write()
        fac = abs(deg) / 10.0
        time.sleep(0.08*fac)

    def pan_right(self,deg=-10):
        self.pan_angle -= deg
        self.updateState({self.pan_motor: -1*abs(deg)})
        self.write()
        fac = abs(deg)/10.0
        time.sleep(0.08*fac)

    def tilt_up(self,deg=10):
        self.tilt_angle += deg
        self.updateState({self.tilt_motor: deg})
        self.write()
        fac = abs(deg) / 10.0
        time.sleep(0.08*fac)

    def tilt_down(self,deg=-10):
        self.tilt_angle -= deg
        self.updateState({self.tilt_motor: -1*abs(deg)})
        self.write()
        fac = abs(deg) / 10.0
        time.sleep(0.08*fac)

def rollDice():
    dxl.setMotor(21,0)
    time.sleep(0.5)
    for i in range(5):
        dxl.setMotor(5,60)
        #dxl.setMotor(21,c110)
        time.sleep(0.1)
        dxl.setMotor(5,30)
        #dxl.setMotor(21,70)
        time.sleep(0.1)
    dxl.setMotor(5,60)
    #dxl.setMotor(21,c110)
    time.sleep(0.1)
    dxl.setMotor(21,-120)
    time.sleep(1)
    dxl.setMotor(21,0)


#----------------------------------------------------------------------------------------------------------------
darwin = {1: 90, 2: -90, 3: 67.5, 4: -67.5, 7: 45, 8: -45, 9: 'i', 10: 'i', 13: 'i', 14: 'i', 17: 'i', 18: 'i'}
roll = {1:75,3:-28,5:60}
tree = XmlTree('data.xml')
#tree2 = XmlTree('Darwin.xml')
balance = MotionSet(tree.parsexml("152 Balance"), offsets=[darwin])
rollpose = MotionSet(tree.parsexml("152 Balance"), offsets=[darwin,roll])
kick = MotionSet(tree.parsexml("18 L kick"),speed=2,offsets=[darwin])
w1 = MotionSet(tree.parsexml("32 F_S_L"),speed=2.1,offsets=[darwin])
w2 = MotionSet(tree.parsexml("33 "),speed=2.1,offsets=[darwin])
w3 = MotionSet(tree.parsexml("38 F_M_R"),speed=2.7,offsets=[darwin])
w4 = MotionSet(tree.parsexml("39 "),speed=2.1,offsets=[darwin])
w5 = MotionSet(tree.parsexml("36 F_M_L"),speed=2.7,offsets=[darwin])
w6 = MotionSet(tree.parsexml("37 "),speed=2.1,offsets=[darwin])
#shake = MotionSet(tree2.parsexml("Kala"), speed = 2.1)
walk_init = Action([w1,w2])
walk_motion = Action([w3,w4,w5,w6])
done = []
#------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    dxl = Dxl(lock=1,debug=False)
    state = dxl.getPos()
    raw_input("Initialize?")
    balance.execute()
    raw_input()
    rollpose.execute()
    head = Head(dxl)
    print state
    while len(done) < 6:
        time.sleep(1)
        mixer.music.load('audio_files/Pass.mp3')
        rollpose.execute()
        mixer.music.play()
        raw_input("Roll?")
        rollDice()
        balance.execute()
        time.sleep(1)
        head.tilt_down(50)
        time.sleep(2)
        with open('x.txt', 'r') as file:
            num = file.readline().strip()[0]
        if int(num) not in done:
            done.append(int(num))
            print num
            mixer.music.load('audio_files/Die'+num+'.mp3')
            mixer.music.play()
            time.sleep(2)
            mixer.music.load('audio_files/Card'+num+'.mp3')
            mixer.music.play()
            time.sleep(3)
        raw_input("lift?")
        head.tilt_up(50)
