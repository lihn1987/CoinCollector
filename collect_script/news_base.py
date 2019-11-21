class article_info:
    def __init__(self, author, time_utc, title, desc, content, source_addr, source_media):
        self.author = author
        self.time_utc = time_utc
        self.title = title
        self.desc = desc
        self.content = content
        self.source_addr = source_addr
        self.source_media = source_media
    def __str__(self):
        return("""==========================
author:%s
time_utc:%d
title:%s
desc:%s
content:%s
source_addr:%s
source_media:%s"""%(self.author, self.time_utc, self.title, self.desc, 'self.content', self.source_addr, self.source_media))