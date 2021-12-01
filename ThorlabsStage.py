# -*- coding: utf-8 -*-
"""
Created on Tue Jul 27 16:30:47 2021

@author: Sandora
"""

from pylablib.devices import Thorlabs
import time
import struct
from ThorlabsStageFunctions import *

print('Device found: ',Thorlabs.list_kinesis_devices())

step=0.0005 # mm, constant for this stage!


# BROKEN STAGE
# stage = Thorlabs.KinesisMotor("28250767",scale="step") 
# GOOD STAGE
# stage = Thorlabs.KinesisMotor("28250598",scale="step")

stage = Thorlabs.KinesisMotor(Thorlabs.list_kinesis_devices()[0][0],scale="step")
stage.open()


# USER DEFINED PARAMETERS
pos1=5 # mm
pos2=15 # mm
max_velocity=4 # mm/s
rel_step=-1 # in mm



try:
    # setup max velocity
    stage.setup_velocity(min_velocity=None, acceleration=None, max_velocity=int(max_velocity/step), channel=1, scale='step')
    
    # Set general trigger parameters
    trin_mode=b'\x03' 
    trin_polarity=b'\x01'
    trout_mode=b'\x00'
    trout_polarity=b'\x00'
    
    set_trigger_params(stage,trin_mode,trin_polarity,trout_mode,trout_polarity)
    
    

    # #  Set positions when to generate output trigger
    # # pulses when moving forward
    # start_pos_fw=39.9
    # interval_fw=50
    # num_pulses_fw=1
    # # pulses when moving backwards
    # start_pos_rev=25
    # interval_rev=50
    # num_pulses_rev=1
    # pulse_width=1e5 # in us
    # num_cycles=1e5
    
    # set_triggerout_position_params(stage,start_pos_fw,interval_fw,num_pulses_fw,start_pos_rev,interval_rev,num_pulses_rev,pulse_width,num_cycles)

    # # RELATIVE MOVE WITH EACH TRIGGER
    # set_triggerin_rel_move(stage,int(rel_step/step))

    # ABSOLUTE MOVE WITH ONLY ONE TRIGGER
    # stage.move_to(int(pos1/step))
    set_triggerin_abs_move(stage,int(pos1/step))
    
    while True:
        pos=stage.get_position(channel=1)
        if pos==int(pos1/step):
            set_triggerin_abs_move(stage,int(pos2/step))
            
        if pos==int(pos2/step):
            set_triggerin_abs_move(stage,int(pos1/step))
            
except KeyboardInterrupt:
    stage.close()
    print('Interrupted by user')    
        
except:
    stage.close()
    print('Sth not working here')
