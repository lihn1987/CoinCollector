#!/bin/sh
nohup python3 -u start_depth_service.py > log/depth.log  2>&1 &
nohup python3 -u start_news_service.py > log/news.log  2>&1 &
nohup python3 -u start_detail_service.py > log/detail.log  2>&1 &
nohup python3 -u start_analyse.py > log/analyse.log  2>&1 &
nohup python3 -u start_price_service.py > log/price.log  2>&1 &
nohup python3 -u start_twitter_craw.py > log/price.log  2>&1 &
nohup python3 -u start_github_crawl.py > log/github.log  2>&1 &
nohup python3 -u start_score_service.py > log/score.log  2>&1 &