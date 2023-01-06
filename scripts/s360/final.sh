#!/bin/bash
curl https://s360.s3.eu-central-1.amazonaws.com/tegra210-p3448-0002-s360v0-2-b00.dts --output /boot/tegra210-p3448-0002-s360v0-2-b00.dts   
curl https://s360.s3.eu-central-1.amazonaws.com/set_mac.py --output set_mac.py
python3 set_mac.py
