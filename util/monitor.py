import time
import requests
import threading
from util import email
from util import config as c
from pprint import pprint

class Monitor:
    
    wait_seconds = 2
    
    wait_factor = 1
    
    def __init__(self):
        
        self.configurations = c.getConfiguations()
        self.setConfiguations()
       
             
    def setConfiguations(self):
        config = self.configurations
        
        if config is not None:

            self.wait_seconds = config['wait_seconds']
            #['wait_seconds']
            self.wait_factor = config['wait_factor']
        else:
            print("No configurations loaded")    
            
    def getHosts(self):
        
        return c.getHostList()  

    def cool_off_exponentially(self):
          
        self.wait_seconds = self.wait_seconds + 10
        self.wait_factor = self.wait_factor + 0.75
        
        return int(self.wait_seconds * self.wait_factor)

    def ping_server(self, server_url):
        r = None
        try:
            r = requests.get(server_url, timeout=5)
        except Exception as e:
            print(f"Couldnot find server: {server_url}:{e.message}")
        finally:
            return r   

    def send_failed_host_email(self, host):
        
        print("send email after grace period")
        mailer = email.Email()
        payload = { 'Message': '', 'Host': host}
        
        mailer.send_email(payload)
        print("email sent")
        
    def heart_beat(self, host, heart_beat_limit = 3):
                
        count = 0
        response = self.ping_server(host)
        
        if response is None:
            
            print(f"Host {host} failed to response. ")

            while count < int(heart_beat_limit):
                
                time_to_wait = self.cool_off_exponentially()

                print(f"Waiting for {time_to_wait} seconds")
                time.sleep(time_to_wait) #delay abit time_to_wait * 60 to get seconds
                response = self.ping_server(host)
                count += 1

            response = self.send_failed_host_email(host)
            print(response)
        
        else:
            print(f"All systems green for {host} with status_code: {response.status_code}")  


    def run_health_check(self):
            
        config = self.getHosts() 
                
        if 'hosts' not in config and 'heart_beat_limit' not in config:   
            
            raise Exception("Please specify hosts and grace period in hosts.ini file")    
            
        heart_beat_limit = config['heart_beat_limit']
        hosts = config['hosts']
        
        for host, url in hosts.items():
            
            if url is None or url == '' or heart_beat_limit.get(host, None) == None:
                continue
            t = threading.Thread(target=self.heart_beat, args=(url, heart_beat_limit[host] ))
            t.start()
                



