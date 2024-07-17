# Set up  
### Before your first run  
  
```  
$ pip install virtualenv  
$ virtualenv venv  
$ .\venv\Scripts\activate
$ pip install -r requirements.txt  
$ python stylus-aux.py
```  
  
# Running   
  
```  
$ .\venv\Scripts\activate
$ python .\main.py --file myEmail_1.conf --which-action create    
$ python .\main.py --file myEmail_1.conf --which-action like   
```  
  
  
`--file` ==> filename in configs/...  
`--which-action` ==> "create" or "like"  

- in case  you dont know, you can cancel with ctrl+c in terminal
- comment out urls form LIKE_PAGES with # or //. ( highlight multi lines and ctrl+/ in your editor in case you didnt know)
- in your config file, `headless: True` = No graphics.  Idea is you can start up 10 or so programs simultaneously, with 10 differecnt config files
- there is a state file that saves your progress (`myEmail_1.conf.zstate.yaml`). Keeps track of where the app is in its process.

#### Vid  
1:00 demo "create" (account sign up)   
3:00 demo "like"   
5:10 set up two programs running   
6:50 two programs running   
8:40 demo headless mode   



--- 
This is a completely theoritical program only and is for educational purposes. If you choose to use it then you accept full responsability and indemnity. This program is not affiliated, associated, or partnered with webtoon in any way. The program is not authorized, endorsed, or sponsored.