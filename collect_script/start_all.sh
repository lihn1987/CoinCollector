#!/bin/sh
nohup python3 -u start_depth_service.py > log/depth.log  2>&1 &
nohup python3 -u start_news_service.py > log/depth.log  2>&1 &
nohup python3 -u start_detail_service.py > log/depth.log  2>&1 &
nohup python3 -u start_analyse_service.py > log/depth.log  2>&1 &
