
Some notes about the sensor used to collect the power out of solar panels.
# Datasheet
`PZEM-017` - measure current under external shunt specification
There're a total of 8 registers addresses

| Register Address | Description | Resolution
| --- | --- | --- |
| 0x0000 | Voltage value | 1LSB correspond to 0.01V
| 0x0001 | Current value | 1LSB correspond to 0.01A
| 0x0002 | Power value low 16 bits | 1LSB correspond to 0.1W
| 0x0003 | Power value high 16 bits | *
| 0x0004 | Energy value low 16 bits | 1LSB correspond to 1wh
| 0x0005 | Energy value high 16 bits | *
| 0x0006 | High voltage alarm status | --
| 0x0007 | Low voltage alarm status | --

# Modify slave parameters

| Register Address | Description | Resolution
| --- | --- | --- |
| 0x0003 | The current range (**Pzem-017**) | 0001: 50A
                                            |hjkl



 
