#!/bin/bash

cd /home/mastostatus/mastostatus/

sed -i 's/ignore_test_toot: True/ignore_test_toot: False/g' config.yaml
sed -i 's/disable_post: False/disable_post: True/g' config.yaml
sed -i 's/disable_dismiss: False/disable_dismiss: True/g' config.yaml
sed -i 's/force_programmer: False/force_programmer: True/g' config.yaml
sed -i 's/disable_write: False/disable_write: True/g' config.yaml
sed -i 's/loglevel: 20/loglevel: 10/g' config.yaml
          

