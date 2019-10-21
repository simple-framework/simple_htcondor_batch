#!/bin/bash
cp $SIMPLE_CONFIG_DIR/config/50PC.config $HTCONDOR_CONFIG_DIR/config.d/50PC.config
systemctl start condor