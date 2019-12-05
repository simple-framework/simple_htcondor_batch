#!/bin/bash
echo "----------------------------------"
echo "Initializing HTCondor Execute Node"
echo "----------------------------------"
echo "Copying config files from $SMIPLE_CONFIG_DIR/config to $HTCONDOR_CONFIIG_DIR/config.d"
cp $SIMPLE_CONFIG_DIR/config/50PC.conf $HTCONDOR_CONFIG_DIR/config.d/50PC.conf

echo "----------------------------------"
echo "Set Timezone"
echo "----------------------------------"
if [ ! -s $SIMPLE_CONFIG_DIR/config/timezone ]
then
    echo "No timezone info available in site_level_config_file."
else
    mv /etc/localtime /etc/localtime.backup
    ln -s /usr/share/zoneinfo/$(cat $SIMPLE_CONFIG_DIR/config/timezone) /etc/localtime
fi

echo "----------------------------------"
echo "Starting daemons"
echo "----------------------------------"
echo "Starting HTCondor"
systemctl start condor
echo "Starting crond"
systemctl start crond

echo "Initialization Complete!"
