import multiprocessing

bind = "127.0.0.1:8000"  
workers = 2               
errorlog = '/data/logs/django/gunicorn.error.log'
accesslog = '/data/logs/django/gunicorn.access.log'
loglevel = 'info'   
proc_name = 'omsBackend' 
