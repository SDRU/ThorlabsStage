A code to inteface with translation stage controller KBD101 from Thorlabs. Translation stage DDSM50/M
<br>
https://www.thorlabs.de/thorproduct.cfm?partnumber=DDSM50/M
https://www.thorlabs.de/newgrouppage9.cfm?objectgroup_id=5698&pn=KBD101#8154


Useful links
https://pylablib.readthedocs.io/en/latest/.apidoc/pylablib.devices.Thorlabs.html#pylablib.devices.Thorlabs.kinesis.KinesisMotor.get_scale
https://docs.python.org/3/library/struct.html

ThorlabStageLoop.Sequence is a file for Kinesis software, pre-programmed loop sequence

kinesis.py contains custom triggering functions

StageOutputTrigger configures KBD101 to output TTL trigger pulses when stage is at specific locations