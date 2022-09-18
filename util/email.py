import boto3
from util import config as c

class Email:
    
    boto3_client = None
    config = None
    
    def __init__(self):
        
        self.config = c.getConfiguations()
        self.intializeBoto3Client()
        

    def intializeBoto3Client(self):
        
        print("==>", self.config['region_name'])
        if self.config.get('region_name', None) and self.config.get('aws_access_key_id', None) and self.config.get('aws_secret_access_key', None) :
            
            self.boto3_client = boto3.client(
                'ses',
                region_name= self.config['region_name'],
                aws_access_key_id= self.config['aws_access_key_id'],
                aws_secret_access_key= self.config['aws_secret_access_key'] 
            )
            
        else:
            self.boto3_client = boto3.client('ses')    
                
    
    def send_email(self, message):
        
        emailToAddress = self.config['email_to_address']
        emailSource = self.config['email_source']
        
        if self.boto3_client is None:
            raise Exception('No boto3 client defined. Check your configuration')
        
        if message is None:
            raise TypeError('Message must not be None')
            
        CHAR_SET="UTF-8"
        HTML_CONTENT= self.build_html_body(message)
        
        response = self.boto3_client.send_email(
            Destination={
                "ToAddresses": [
                    emailToAddress,
                ],
            },
            Message={
                "Body": {
                    "Html": {
                        "Charset": CHAR_SET,
                        "Data": HTML_CONTENT,
                    }
                },
                "Subject": {
                    "Charset": CHAR_SET,
                    "Data": "Heartbeat Alert",
                },
                
            },
            Source= emailSource
        )
        
        return response
        
        
    def build_html_body(self, msg):
        
        host = msg.get('Host',None)
        message_body = msg.get('Message',None)
        
        return f"""
        
            <html>
                <head>Alert</head>
                <body>
                    <h1 style='text-align:center'>YOUR SITE IS DOWN</h1>
                    <div style='text-align:center'>
                        <p>Make sure the server, <a href='{host}'>{host}</a> is restarted and booted up</p>
                        <p>{ message_body}<p>
                    </div>
                </body>
            
            </html>

        """
     
        