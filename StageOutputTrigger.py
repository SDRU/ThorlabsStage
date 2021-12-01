# -*- coding: utf-8 -*-
"""
Created on Wed Dec  1 14:54:01 2021

@author: Sandora and Thorlabs
"""


# USER DEFINED PARAMETERS
# loop settings
pos1=15 # mm
pos2=45 # mm
max_velocity=8 # mm/s




# CONSTANTS
STEP=0.0005 # mm, constant for DDSM50 stage, DO NOT CHANGE!

from pylablib.devices import Thorlabs
import sys


sys.path.append("C:\\Users\\OceanSpectro\\AppData\\Roaming\\Python\\Python38\\site-packages\\pylablib\\devices\\Thorlabs\\")
devices = Thorlabs.list_kinesis_devices()
print('Devices found: ',devices)


for device in devices:
        serial_nr = device[0]
        if serial_nr.startswith("2"):
            stage = Thorlabs.KinesisMotor(serial_nr,scale="step")
            stage.open()


try:
    stage.setup_velocity(max_velocity=int(max_velocity/STEP), channel=1, scale='step')
    
     # Set general trigger parameters
    tr1_mode=b'\x00' 
    tr1_polarity=b'\x01'
    tr2_mode=b'\x0F'
    tr2_polarity=b'\x01'
    
    stage.set_trigger_params(tr1_mode=tr1_mode,tr1_polarity=tr1_polarity,tr2_mode=tr2_mode,tr2_polarity=tr2_polarity)
    
    #  Set positions when to generate output trigger
    # pulses when moving forward
    start_pos_fw=int(pos1/STEP)
    interval_fw=int(50/STEP)
    num_pulses_fw=1
    # pulses when moving backwards
    start_pos_rev=int(pos2/STEP)
    interval_rev=int(50/STEP)
    num_pulses_rev=1
    pulse_width=int(1e5) # in us
    num_cycles=int(1e5)
        
    stage.set_triggerout_position_params(start_pos_fw,interval_fw,num_pulses_fw,start_pos_rev,interval_rev,num_pulses_rev,pulse_width,num_cycles)
    
    # main loop
    stage.move_to(int(pos1/STEP))
    while True:
        pos=stage.get_position(channel=1,scale="step")
        if pos==int(pos1/STEP):
            stage.move_to(int(pos2/STEP))
            
        if pos==int(pos2/STEP):
            stage.move_to(int(pos1/STEP))
    
    stage.close()
            
except KeyboardInterrupt:
    stage.close()
    print('Interrupted by user')    
        
except:
    stage.close()
    print('Sth not working here')
