#!/bin/bash
#check Raid card vd and pd state
CARD=`/opt/MegaRAID/MegaCli/MegaCli64 -adpallinfo -a0 | grep "Product Name" | cut -d ':' -f2`
VDSTATE1=`/opt/MegaRAID/MegaCli/MegaCli64 -AdpAllInfo -aALL | grep "Serial No"| cut -d ':' -f2`
VDSTATE2=`/opt/MegaRAID/MegaCli/MegaCli64 -AdpAllInfo -aALL | grep "Memory Size"| cut -d ':' -f2`
PDSTATE1=`/opt/MegaRAID/MegaCli/MegaCli64 -cfgdsply -aALL | grep "Online" | wc -l | sed 's/       //'`
PDSTATE2=`/opt/MegaRAID/MegaCli/MegaCli64 -cfgdsply -aALL | grep "Rebuild" | wc -l | sed 's/       //'`
PDSTATE3=`/opt/MegaRAID/MegaCli/MegaCli64 -AdpAllInfo -aALL | grep "Critical Disks"`
PDSTATE4=`/opt/MegaRAID/MegaCli/MegaCli64 -AdpAllInfo -aALL | grep "Disks"`

echo "productName  : $CARD"
echo "serialNo     : $VDSTATE1"
echo "memorySize   : $VDSTATE2"
echo "Online Disk       : $PDSTATE1"
echo "Rebuild Disk      : $PDSTATE2"
echo "$PDSTATE3"
echo "$PDSTATE4"

