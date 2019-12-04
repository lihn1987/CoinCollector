#!/bin/sh
nohup python3 -u start_depth_service.py > log/depth.log  2>&1 &
nohup python3 -u start_news_service.py > log/news.log  2>&1 &
nohup python3 -u start_detail_service.py > log/detail.log  2>&1 &
nohup python3 -u start_analyse.py > log/analyse.log  2>&1 &
