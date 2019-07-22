
from drivers import Stepper
from drivers import Stepper_slow
from drivers import DualStepper
from drivers import a1
from drivers import a4
from drivers import Button
from drivers import Relay

import drivers
import math
import time
import sys
import RPi.GPIO as GPIO

global l0,l1,l2,l3,l4,p0,B0,p1,B1,b0,b1,ms

# dir_steper:0or1:  0:down/1:up
#t0 预热时间120秒
# t1 加油时间
# t2 加面糊时间
# t3 第一面加热时间（加蛋前）
# t4 加蛋后加热时间 
# t5 烙饼的第二面

t0 = 120; t1 = 2; t2 = 5; t3 = 40; t4 = 40; t5 =40
#t0 = 2; t1 = 2; t2 = 2; t3 = 2; t4 = 2; t5 =2

ns = 1110  #下降到可摊饼高度
nsc = 1090  # 铲饼所需步数
        
def wubi(p0,b0,p1,b1):    
    p0 = p0
    B0 = math.atan(b0)
    a10 = a1(p0,B0,)
    a40 = a4(p0,B0)
    p0 = p1
    B0 = math.atan(b1)
    a11 = a1(p0,B0)
    a41 = a4(p0,B0)
    da1 = (a11 -a10)*180/math.pi
    da4 = (a41- a40)*180/math.pi
    step_da1 = round(4*200*da1/360)
    step_da4 = round(4*200*da4/360)

    ds.rotate(step_da1, step_da4)
    time.sleep(1)
    return
def SJ(dir,ns,cond=lambda:True):
    ks_sj = sj.rotate(dir,ns,btnZ.getinput)
    print("ks_sj",ks_sj)
    return
def BD(dir,bns,cond=lambda:True):
    ks_bd = bd.rotate(dir,bns,btnbd.getinput)
    print("ks_bd",ks_bd)
    return
def XZ(dir,ns,cond=lambda:True):
    ks_xz = xz.rotate(dir,ns,btnxz.getinput)
    print("ks_xz",ks_xz)
    return
    
def BDXZ(ms, msx, cond=lambda:True):
    bd_xz.rotate(ms, msx, btnbd.getinput)
    time.sleep(1)
    print("ms,msx",ms,msx)
    return

def resetZ():
    sj.rotate(1, ns, btnZ.getinput)    #升起到传感器0位

def resetbd():
    bd.rotate(0,120)
    time.sleep(1)
    bd.rotate(1,300,btnbd.getinput)  #摆动到鏊子边缘

def resetxz():
    xz.rotate(0,420,btnxz.getinput)   #旋转到可铲饼0位
        
    # work
def Work_prepare():
    print("step0:prepare")
    print("reset....")
    resetZ()
    resetbd()
    resetxz()
    # bd.rotate(0,20)   #旋转到可铲饼0位--越过传感器位
    print("reset-end")
    print("helt-start:Heltting....")
    print("aozi-rotateing....")
    #鏊子旋转启动
    Re.trigger(0)
    #鏊子加热启动
    t0 = 3    # 实际约120秒
    time.sleep(t0)   # t0 鏊子预热时间
    print("Ready")
def Work_one_times():
    ts =time.time()
    #加油（泵启动）
    print("step1:add & coating oil")
    time.sleep(t1)   # t1 加油时间
    print("coating oil")
    #电磁铁吸起毛刷
    wubi(300,1,300,0)      #刷匀油
    wubi(300,0,300,1)      #五边复位
    # 电磁铁放下毛刷
    wubi(300,1,280,1.3)   # 五边移动到鸡蛋容器处    
    bd.rotate(1,100)   #ns: 竹蜻蜓摆动到摊饼位置（鏊子中间）
    ks0 =  sj.rotate(0, ns)    #:下降到可摊饼高度
    print("step2:Add & coating batter")
    # 加面糊（泵启动）
    time.sleep(t2)   # t2 加面糊时间
    for i in range(4):
        sj.rotate(1, 10)    #提升（防止带饼）
        time.sleep(2)
        i = i +1
    time.sleep(3)
    resetZ()
    # ks3 =  sj.rotate(1, ns,btnZ.getinput)    #高度复位
    time.sleep(t3)   # t3 第一面加热时间（加蛋前）
    #加蛋
    print("step3: add & coating eggs")
    ks1 =  sj.rotate(0, ns-50)    #加蛋高度
    wubi(280,1.3,300,0)   # 五边加鸡蛋    
    wubi(300,0,280,1.3)   # 五边复位
    wubi(280,1.3,240,1.5)   # 五边移动到调料处
    resetZ()
    time.sleep(t4)   # t4 加蛋后加热时间 
    bd.rotate(0,120)   #摆臂复位
    time.sleep(1)
    bd.rotate(1,50,btnbd.getinput)   #摆臂复位
    ks2 =  sj.rotate(0, nsc)    #降到铲饼高度
    print("step4: Shovel cake....")
    bd.rotate(0,80)   #铲饼
    time.sleep(2)
    Re.trigger(1)
    bd.rotate(1,120,btnbd.getinput)   #后撤到卷饼起始位置
    time.sleep(0.5)
    bd.rotate(0,40)   #后撤到卷饼起始位置
    time.sleep(4)
    # resetZ()
    sj.rotate(1,0.3*ns)
    print("step5: Roll cake")
    BDXZ(-133,798)   #卷饼 ，zns:展饼所需步数
    resetZ()
    bd.rotate(1,200,btnbd.getinput)   #后撤至鏊子边缘，待展饼位置
    print("step6: Spread cake")
    BDXZ(-160,-800)   #展饼
    Re.trigger(0)
    time.sleep(t5)    #烙饼的第二面
    resetZ()
    bd.rotate(1,200,btnbd.getinput)   #复位
    print("step7: Spread sauce")
    wubi(230,1.3,300,0)
    wubi(300,0,230,1.3)
    wubi(230,1.3,200,1.6)
    print("step8: add Bocui")
    Re.trigger(1)
    wubi(200,1.6,300,0)
    wubi(300,0,200,1.6)
    
    # time.sleep(1)  #等待折叠后移动
    # # time.sleep(30)  #等待折叠后移动
    # t = time.time()-ts
    # print("t",t)
def Work_cycle():
    ts = time.time()
    Work_prepare()
    for i in range(1):
        print("No.",i,)
        Work_one_times()
        t = time.time()-ts
    with open("data.csv", "a") as logfile:
        logfile.write(time.strftime("%Y-%m-%d-%H-%M-%S"))
        logfile.write(", %d"%i)
        logfile.write(", %d\n"%t)
    t = time.time()-ts
    print("all_time",t)

if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)

    ds = DualStepper(26,19,13,6,5,0)
    bd_xz = DualStepper(22,27,17,18,15,14)
    sj = Stepper(11,9,10)
    bd = Stepper_slow(22,27,17)
    xz = Stepper_slow(18,15,14)
    # rotate the pancake-machine
    Re = Relay(2)
    
    # Buttons
    btnZ = Button(21)
    btnbd = Button(20)
    btnxz = Button(16)

    Work_cycle()
    
    GPIO.cleanup()
