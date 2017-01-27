#!/bin/sh

ps auxw | grep camera.py | grep -v

if [ $? != 0 ]
then
        python ~/scripts/camera.py
fi
