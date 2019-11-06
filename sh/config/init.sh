#!/bin/bash
echo "----------------------------------"
echo "Initializing HTCondor Execute Node"
echo "----------------------------------"
echo "Copying config files from $SMIPLE_CONFIG_DIR/config to $HTCONDOR_CONFIIG_DIR/config.d"
cp $SIMPLE_CONFIG_DIR/config/50PC.conf $HTCONDOR_CONFIG_DIR/config.d/50PC.conf

echo "Copying supplemental configs..."
while IFS=":" read -r source dest; do
  mkdir -p $(dirname ${dest}) && cp $SIMPLE_CONFIG_DIR/config/$source ${dest}
done < ${SIMPLE_CONFIG_DIR}/config/supplemental_mapfile

echo "----------------------------------"
echo "Starting daemons"
echo "----------------------------------"
echo "Starting HTCondor"
systemctl start condor
echo "Starting crond"
systemctl start crond

echo "Initialization Complete!"
