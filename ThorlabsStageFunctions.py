# -*- coding: utf-8 -*-
"""
Created on Tue Jul 27 15:49:56 2021

@author: Sandra
"""

import struct

def get_triggerout_position_params(stage):
    params=stage.query(0x0527,param1=0x01,param2=0x00,source=0x01,dest=0x50).data
    start_pos_fw,interval_fw,num_pulses_fw,start_pos_rev,interval_rev,num_pulses_rev,pulse_width,num_cycles=struct.unpack("<LLLLLLLL",params[8:40])
    return start_pos_fw,interval_fw,num_pulses_fw,start_pos_rev,interval_rev,num_pulses_rev,pulse_width,num_cycles




def set_triggerout_position_params(stage,start_pos_fw,interval_fw,num_pulses_fw,start_pos_rev,interval_rev,num_pulses_rev,pulse_width,num_cycles):
    # all variables in the command should be in number of counts, function input needs to be scaled
    # The stage will not generate another trigger if number of pulses per cycles could not be completed
    CT=2000
    message=struct.pack("<HLLLLLLLL",1,int(start_pos_fw*CT),int(interval_fw*CT),int(num_pulses_fw),int(start_pos_rev*CT),int(interval_rev*CT),int(num_pulses_rev),int(pulse_width),int(num_cycles))

    # extra padding with zero bytes at the end
    params=stage.query(0x0527,param1=0x01,param2=0x00,source=0x01,dest=0x50).data
    while len(message)<len(params):
        message=message+b'\x00'        
        
    stage.send_comm(0x0526,param1=0x22,param2=0x00,source=0x01,dest=0x50)
    stage.send_comm_data(0x0526,data=message,source=0x01,dest=0x50)


    
    
def get_trigger_params(stage):
    params=stage.query(0x0524,param1=0x01,param2=0x00,source=0x01,dest=0x50).data
    trin_mode,trin_polarity,trout_mode,trout_polarity=struct.unpack("<HHHH",params[2:10])
    return trin_mode,trin_polarity,trout_mode,trout_polarity



def set_trigger_params(stage,trin_mode,trin_polarity,trout_mode,trout_polarity):
    #  trin_mode
    # 0x00 The trigger IO is disabled
    # 0x01 General purpose logic input 
    # 0x02 Input trigger for relative move.
    # 0x03 Input trigger for absolute move.
    # 0x04 Input trigger for home move.
    
    #  polarity 1/0 means rising or falling edge
    
    #  trout_mode
    # 0x0A General purpose logic output
    # 0x0B Trigger output active (level) when motor 'in motion'. 
    # 0x0C Trigger output active (level) when motor at 'max velocity'.
    # 0x0D Trigger output active (pulsed) at pre-defined positions moving forward
    # 0x0E Trigger output active (pulsed) at pre-defined positions moving backwards
    # 0x0F Trigger output active (pulsed) at pre-defined positions moving forwards and backward. 

 
    channel=b'\x01\x00'
    message=channel+trin_mode+b'\x00'+trin_polarity+b'\x00'+trout_mode+b'\x00'+trout_polarity+b'\x00'
    
    # extra padding with zero bytes at the end
    params=stage.query(0x0524,param1=0x01,param2=0x00,source=0x01,dest=0x50).data
    while len(message)<len(params):
        message=message+b'\x00' 
       
    stage.send_comm(0x0523,param1=0x0C,param2=0x00,source=0x01,dest=0x50)
    stage.send_comm_data(0x0523,data=message,source=0x01,dest=0x50)
    
    
    
    
def set_triggerin_abs_move(stage,position):
    message=struct.pack("<HL",1,position)
    stage.send_comm(0x0450,param1=0x06,param2=0x00,source=0x01,dest=0x50)
    stage.send_comm_data(0x0450,data=message,source=0x01,dest=0x50)
    
    
def set_triggerin_rel_move(stage,step):
    message=struct.pack("<Hl",1,step)
    stage.send_comm(0x0445,param1=0x06,param2=0x00,source=0x01,dest=0x50)
    stage.send_comm_data(0x0445,data=message,source=0x01,dest=0x50)
    
def set_motor_output_params(stage,cont_curr,energy_lim,motor_lim):
    # first three variables in the command should be in %, 0 to 32767 is 0 to 100 %
    C = 327.68

    message=struct.pack("<HHHHH",1,int(cont_curr*C-1),int(energy_lim*C-1),int(motor_lim*C-1),0)

    # extra padding with zero bytes at the end
    params=stage.query(0x04DB,param1=0x01,param2=0x00,source=0x01,dest=0x50).data
    while len(message)<len(params):
        message=message+b'\x00'        
        
    stage.send_comm(0x04DA,param1=0x0E,param2=0x00,source=0x01,dest=0x50)
    stage.send_comm_data(0x04DA,data=message,source=0x01,dest=0x50)
    
def get_motor_output_params(stage):
    C = 327.68
    
    params=stage.query(0x04DB,param1=0x01,param2=0x00,source=0x01,dest=0x50).data
    cont_curr, energy_lim, motor_lim, motor_bias=struct.unpack("<HHHH",params[2:10])
        
    return (cont_curr+1)/C, (energy_lim+1)/C, (motor_lim+1)/C, (motor_bias+1)/C


def get_limit_switch_params(stage):
    params = stage.query(0x0424,param1=0x01,param2=0x00,source=0x01,dest=0x50).data
    cw_hard, ccw_hard, cw_soft, ccw_soft, mode = struct.unpack("<HHiiH",params[2:16])
    return cw_hard, ccw_hard, cw_soft, ccw_soft, mode

def set_limit_switch_params(stage,cw_hard, ccw_hard, cw_soft, ccw_soft, mode):
    message = struct.pack("<HHHiiH",1,cw_hard, ccw_hard, cw_soft, ccw_soft, mode)

    # extra padding with zero bytes at the end
    params=stage.query(0x0424,param1=0x01,param2=0x00,source=0x01,dest=0x50).data
    print(params)
    while len(message)<len(params):
        message=message+b'\x00'        
        
    # stage.send_comm(0x0423,param1=0x10,param2=0x00,source=0x01,dest=0x50)
    stage.send_comm_data(0x0423,data=message,source=0x01,dest=0x50)
