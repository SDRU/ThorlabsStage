# -*- coding: utf-8 -*-
"""
Created on Tue Jul 20 10:48:29 2021

@author: OceanSpectro
"""

from pylablib.devices import Thorlabs
import time
import struct

print(Thorlabs.list_kinesis_devices())


stage = Thorlabs.KinesisMotor("28250598",scale="step")
stage.open()
    
try:
    step=0.0005 # mm
    pos1=int(5/step)
    pos2=int(45/step)
    max_velocity=int(8/step)
    
    # get status
    # A=stage.query(0x0005,param1=0x00,param2=0x00,source=0x01,dest=0x50).data
    # get serial number
    # print(struct.unpack("<I",A[0:4]))
    
    print(stage.get_velocity_parameters(scale="step"))
    stage.setup_velocity(min_velocity=None, acceleration=None, max_velocity=max_velocity, channel=1, scale='step')
    
    # set trigger output settings
    channel=b'\x01\x00'
    ECT=2000 # encoder counts per mm
    start_pos_fw=struct.pack("<l",int(44.999*ECT))
    interval_fw=struct.pack("<l",int(50*ECT))
    num_pulses_fw=struct.pack("<l",1)
    start_pos_rev=struct.pack("<l",int(25*ECT))
    interval_rev=struct.pack("<l",int(50*ECT))
    num_pulses_rev=struct.pack("<l",1)
    pulse_width=struct.pack("<l",int(1e5))
    num_cycles=struct.pack("<l",10000)
    
    
    triggerposp=stage.query(0x0527,param1=0x01,param2=0x00,source=0x01,dest=0x50).data
    
    
    
    Lp=len(triggerposp)
    triggerout=channel+start_pos_fw+interval_fw+num_pulses_fw+start_pos_rev+interval_rev+num_pulses_rev+pulse_width+num_cycles
    while len(triggerout)<Lp:
        triggerout=triggerout+b'\x00'
        
        
    stage.send_comm(0x0526,param1=0x22,param2=0x00,source=0x01,dest=0x50)
    stage.send_comm_data(0x0526,data=triggerout,source=0x01,dest=0x50)
    
    

    # get trigger parameters
    triggerp=stage.query(0x0524,param1=0x01,param2=0x00,source=0x01,dest=0x50).data
    L=len(triggerp)

    # set generic trigger parameters
    channel=b'\x01\x00'
    trin_mode=b'\x03\x00'
    trin_polarity=b'\x01\x00'
    trout_mode=b'\x0D\x00'
    trout_polarity=b'\x01\x00'
    
    trigger=channel+trin_mode+trin_polarity+trout_mode+trout_polarity
    while len(trigger)<L:
        trigger=trigger+b'\x00'
       
    
    stage.send_comm(0x0523,param1=0x0C,param2=0x00,source=0x01,dest=0x50)
    stage.send_comm_data(0x0523,data=trigger,source=0x01,dest=0x50)
    print('Trigger setting were set')
    
    # # get trigger parameters
    # triggerp=stage.query(0x0524,param1=0x01,param2=0x00,source=0x01,dest=0x50).data
    # trin_mode,trin_polarity,trout_mode,trout_polarity=struct.unpack("<HHHH",triggerp[2:10])
    
    
    # # set absolute trigger move parameter
    # abs_pos=struct.pack("<l",pos1)
    # stage.send_comm(0x0450,param1=0x06,param2=0x00,source=0x01,dest=0x50)
    # stage.send_comm_data(0x0450,data=channel+abs_pos,source=0x01,dest=0x50)
    
    
   
    
    # set absolute trigger move parameter, moving from pos1 to pos2
    while True:
        pos=stage.get_position(channel=1)
        if pos==pos1:
            abs_pos=struct.pack("<l",pos2)
            stage.send_comm(0x0450,param1=0x06,param2=0x00,source=0x01,dest=0x50)
            stage.send_comm_data(0x0450,data=channel+abs_pos,source=0x01,dest=0x50)
            
            # stage.send_comm(0x0526,param1=0x22,param2=0x00,source=0x01,dest=0x50)
            # stage.send_comm_data(0x0526,data=triggerout,source=0x01,dest=0x50)
        if pos==pos2:
            time.sleep(5)
            abs_pos=struct.pack("<l",pos1)
            stage.send_comm(0x0450,param1=0x06,param2=0x00,source=0x01,dest=0x50)
            stage.send_comm_data(0x0450,data=channel+abs_pos,source=0x01,dest=0x50)
            
            # stage.send_comm(0x0526,param1=0x22,param2=0x00,source=0x01,dest=0x50)
            # stage.send_comm_data(0x0526,data=triggerout,source=0x01,dest=0x50)
    
    
    
    
    # print(stage.get_scale())
    # stage.send_comm(0x0223,param1=0x01,param2=0x00,source=0x01,dest=0x50) # stage.blink()
        
    # stage.move_by(6000)
    # stage.home()
    # stage.move_to(-20000)
    # print(stage.get_velocity_parameters(scale="step"))
    
    # stage.get_trigger_mode()
    # stage.setup_jog(step_size=20000,max_velocity=16000) # 1 cm step, 0.8 cm/s speed
    # print(stage.get_jog_parameters())
    # for i in range(4):
    #     start_time = time.time()
    #     stage.jog("+",channel=1,kind='builtin')
    #     elapsed = time.time()
    #     print("--- %s seconds ---" % (elapsed - start_time))
    # stage.stop()
    stage.close()
    
except:
     stage.close()
     print('Sth not working here')
     
     
     