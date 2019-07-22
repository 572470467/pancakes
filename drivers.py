import RPi.GPIO as GPIO
import time
import math

l0 = 280
l1=l2=l3=l4=230

class Button():
    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(pin, GPIO.IN)

    def waitforpress(self):
        GPIO.wait_for_edge(self.pin, GPIO.FALLING)
        
    def getinput(self):
        return (not GPIO.input(self.pin))

class InfraredPair():
    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def waitforpress(self):
        GPIO.wait_for_edge(self.pin, GPIO.FALLING)
        
    def getinput(self):
        return GPIO.input(self.pin)

    def getneginput(self):
        return (not GPIO.input(self.pin))

class Relay():
    def __init__(self, pin, init=0):
        self.pin = pin
        GPIO.setup(pin, GPIO.OUT, initial=init)

    def trigger(self,signal):
        GPIO.output(self.pin, signal)
        

class Stepper():
    def __init__(self, pen, pdr, ppl):
        self.pen = pen
        self.pdr = pdr
        self.ppl = ppl
        GPIO.setup([pen,pdr,ppl], GPIO.OUT, initial=0)

    def enable(self):
        GPIO.output(self.pen, 0)

    def disable(self):
        GPIO.output(self.pen, 1)

    def step(self, d):
        GPIO.output(self.pdr,d)
        GPIO.output(self.ppl,1)
        GPIO.output(self.ppl,0)
                
    def rotate(self, d, nstep, cond=lambda:True):
    # def rotate(self, d, nstep, cond=lambda:True):
        self.enable()
        GPIO.output(self.pdr, d)
        i = 0;
        while i<nstep and cond():
#            tau = 0.002   #guoce
            tau = 0.002   #nwl
            GPIO.output(self.ppl,1)
            time.sleep(tau/2)
            GPIO.output(self.ppl,0)
            time.sleep(tau/2)
            i = i + 1
        return i

    def execute(self, d, l):
        GPIO.output(self.pdr, d)
        for i in range(len(l)):
            GPIO.output(self.ppl, 1)
            GPIO.output(self.ppl, 0)
            time.sleep(l[i])

    def execute(self, d, l, cond):
        GPIO.output(self.pdr, d)
        i = 0
        while i < len(l) and cond():
            GPIO.output(self.ppl, 1)
            GPIO.output(self.ppl, 0)
            time.sleep(l[i])
            i = i + 1
        return i

class Stepper_slow():
    def __init__(self, pen, pdr, ppl):
        self.pen = pen
        self.pdr = pdr
        self.ppl = ppl
        GPIO.setup([pen,pdr,ppl], GPIO.OUT, initial=0)

    def enable(self):
        GPIO.output(self.pen, 0)

    def disable(self):
        GPIO.output(self.pen, 1)

    def step(self, d):
        GPIO.output(self.pdr,d)
        GPIO.output(self.ppl,1)
        GPIO.output(self.ppl,0)
                
    def rotate(self, d, nstep, cond=lambda:True):
    # def rotate(self, d, nstep, cond=lambda:True):
        self.enable()
        GPIO.output(self.pdr, d)
        i = 0;
        while i<nstep and cond():
#            tau = 0.002   #guoce
            tau = 0.01   #nwl
            GPIO.output(self.ppl,1)
            time.sleep(tau/2)
            GPIO.output(self.ppl,0)
            time.sleep(tau/2)
            i = i + 1
        return i

    def execute(self, d, l):
        GPIO.output(self.pdr, d)
        for i in range(len(l)):
            GPIO.output(self.ppl, 1)
            GPIO.output(self.ppl, 0)
            time.sleep(l[i])

    def execute(self, d, l, cond):
        GPIO.output(self.pdr, d)
        i = 0
        while i < len(l) and cond():
            GPIO.output(self.ppl, 1)
            GPIO.output(self.ppl, 0)
            time.sleep(l[i])
            i = i + 1
        return i

class DualStepper:
    def __init__(self, ena0, dir0, pul0, ena1, dir1, pul1):
        GPIO.setup([ena0, dir0, pul0, ena1, dir1, pul1], GPIO.OUT, initial = 0)
        self.ena0 = ena0
        self.dir0 = dir0
        self.pul0 = pul0
        self.ena1 = ena1
        self.dir1 = dir1
        self.pul1 = pul1

    def rotate(self, nstep0, nstep1, display=True):
        # tau = 0.002
        tau = 0.004
        # Divide the time
        if nstep0 > 0:
            sgn0 = 1
        else:
            sgn0 = 0

        if nstep1 > 0:
            sgn1 = 1
        else:
            sgn1 = 0

        GPIO.output(self.dir0, sgn0)
        GPIO.output(self.dir1, sgn1)
        countdown0 = abs(nstep0)
        countdown1 = abs(nstep1)
        slotsize = max(min(countdown0, countdown1),1)
        # slot0 = countdown0/slotsize
        # slot1 = countdown1/slotsize
        slot0 = math.floor(countdown0/slotsize)
        slot1 = math.floor(countdown1/slotsize)
        # if display:
        #     print('Directions %d %d' % (sgn0, sgn1))
        #     print('Slots %d %d' % (slot0, slot1))
        #     print('Slotssize %d'  % (slotsize))
        #     print('Remaining steps %d %d' % (countdown0, countdown1))
        # Alternate between two motors
        while countdown0 > 0 and countdown1 > 0:
            for i in range(slot0):
#                if display:
#                    print('0')
                countdown0 = countdown0 - 1
                GPIO.output(self.pul0,1)
                time.sleep(tau)
                GPIO.output(self.pul0,0)
                time.sleep(tau)

            for i in range(slot1):
                # if display:
                #     print('1')
                countdown1 = countdown1 - 1
                GPIO.output(self.pul1,1)
                time.sleep(tau)
                GPIO.output(self.pul1,0)
                time.sleep(tau)

#         Remaining steps for motor 0
        while countdown0 > 0:
            # if display:
            #     print('0')
            countdown0 = countdown0 - 1
            GPIO.output(self.pul0,1)
            time.sleep(tau)
            GPIO.output(self.pul0,0)
            time.sleep(tau)

        # Remaining steps for motor 0
        while countdown1 > 0:
            # if display:
            #     print('1')
            countdown1 = countdown1 - 1
            GPIO.output(self.pul0,1)
            time.sleep(tau)
            GPIO.output(self.pul0,0)
            time.sleep(tau)


    
# L298 motor driver
class L298():
    def __init__(self, ppwma, ppwmb, f):
        GPIO.setup([ppwma,ppwmb], GPIO.OUT, initial=0)
        self.pwma = GPIO.PWM(ppwma, f)
        self.pwmb = GPIO.PWM(ppwmb, f)
        
    def start(self, cyclea, cycleb):
        self.pwma.start(cyclea)
        self.pwmb.start(cycleb)
        
    def change(self, cyclea, cycleb):
        self.pwma.ChangeDutyCycle(cyclea)
        self.pwmb.ChangeDutyCycle(cycleb)

    def stop(self):
        self.pwma.stop()
        self.pwmb.stop()

class Servo():
    def __init__(self, pin):
        GPIO.setup(pin,GPIO.OUT)
        self.pwm = GPIO.PWM(pin, 50)
    def start(self, d):
        self.pwm.start(d)
    def change(self, d):
        self.pwm.ChangeDutyCycle(d)
    def stop(self):
        self.pwm.stop()

        
def a1(p0,B0):
    global l0,l1,l2,l3,l4
    # 计算A点：

    g = (l1*l1-l0*l0/4+p0*p0-l2*l2)/(2*p0*math.cos(B0));
    k = (l0+2*p0*math.sin(B0))/(2*p0*math.cos(B0));
    a = k*k+1;
    b = l0-2*g*k;
    c = g*g+l0*l0/4-l1*l1;
    d = b*b-4*a*c
    ya = (-b-math.sqrt(b*b-4*a*c))/2/a;
    xa = math.sqrt(l1*l1-(ya+l0/2)*(ya+l0/2));

    yb = p0 * math.sin(B0)
    xb = p0 * math.cos(B0)

    l22 = round(math.sqrt((xb-xa)*(xb-xa)+(yb-ya)*(yb-ya)))
    if  l22 == l2:
        pass
    else:
        xa = -math.sqrt(l1*l1-(ya+l0/2)*(ya+l0/2));
    if B0 >= 0:
        a1 = math.atan((ya+l0/2)/xa);
        if xb == xa:
            a2 = math.pi/2
        elif xb > xa:
            a2 = math.atan((p0*math.sin(B0)+l0/2-l1*math.sin(a1))/(p0*math.cos(B0)-l1*math.cos(a1)));
        else:
            a2 = math.pi + math.atan((p0*math.sin(B0)+l0/2-l1*math.sin(a1))/(p0*math.cos(B0)-l1*math.cos(a1)));
    else:
        if xa == 0:
            a1 = -math.pi/2
        elif xa > 0:
            a1 = math.atan((ya+l0/2)/xa);
        else:
            a1 = -math.pi + math.atan((ya+l0/2)/xa);
        if xb == xa:
            a2 = -math.pi/2
        elif xb > xa:
            a2 = math.atan((p0*math.sin(B0)+l0/2-l1*math.sin(a1))/(p0*math.cos(B0)-l1*math.cos(a1)));
        else:
            a2 = math.pi - math.atan((p0*math.sin(B0)+l0/2-l1*math.sin(a1))/(p0*math.cos(B0)-l1*math.cos(a1)));

    # print("a1",int(a1*180/math.pi),"a2",int(a2*180/math.pi))
    return a1                   

def a4(p0,B0):                  
    global l0,l1,l2,l3,l4,a1
    # 计算C点：
    g1 = (l4*l4-l0*l0/4+p0*p0-l3*l3)/(2*p0*math.cos(B0))
    k1 = (l0-2*p0*math.sin(B0))/(2*p0*math.cos(B0))
    aa = 1+k1*k1
    b1 = 2*k1*g1-l0
    c1 = g1*g1+l0*l0/4-l4*l4

    yc = (-b1+math.sqrt(b1*b1-4*aa*c1))/2/aa
    xc = math.sqrt(l4*l4-(yc-l0/2)*(yc-l0/2))
    yb = p0 * math.sin(B0)
    xb = p0 * math.cos(B0)

    l33 = round(math.sqrt((xc-xb)*(xc-xb)+(yc-yb)*(yc-yb)))
    if l33 == l3:
        pass
    else:
        xc = -xc
    
    if B0 >= 0:
        if xc == 0:
            a4 = math.pi/2
        elif xc > 0:
            a4 = math.atan((yc-l0/2)/xc)
        else:
            a4 = math.pi + math.atan((yc-l0/2)/xc)
        if xc == xb:
            a3 = math.pi/2
        elif xc < xb:
            a3 = -math.atan((l4*math.sin(a4)+l0/2-p0*math.sin(B0))/(p0*math.cos(B0)-l4*math.cos(a4)));
        else:
            a3 = math.pi + math.atan((l4*math.sin(a4)+l0/2-p0*math.sin(B0))/(p0*math.cos(B0)-l4*math.cos(a4)));
    else:
        if xc == 0:
            a4 = -math.pi/2
        else:
            a4 = math.atan((yc-l0/2)/xc)
            # a4 = math.pi+math.atan((yc-l0/2)/xc)
        if xc == xb:
            a3 = -math.pi/2
        elif xc < xb:
            a3 = -math.atan((l4*math.sin(a4)+l0/2-p0*math.sin(B0))/(p0*math.cos(B0)-l4*math.cos(a4)));
        else:
            a3 = -math.pi - math.atan((l4*math.sin(a4)+l0/2-p0*math.sin(B0))/(p0*math.cos(B0)-l4*math.cos(a4)));
    
    # print("a3",int(a3*180/math.pi),"a4:",int(a4*180/math.pi))
    return a4

