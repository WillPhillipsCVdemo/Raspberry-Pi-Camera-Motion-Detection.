import RPi.GPIO as GPIO
import time
import datetime
import picamera
import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart


camera = picamera.PiCamera()
GPIO.setmode(GPIO.BCM)

GPIO.setup(23, GPIO.IN) #PIR
GPIO.setup(24, GPIO.OUT) #BUzzer

'''
ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
'''



COMMASPACE = ', '

def Send_Email(image):
    sender = '###YOUREMAIL###'
    gmail_password = '###YOURPASSWORD###'
    recipients = ['##YOURRECIPENTEMAIL###']

    # Create the enclosing (outer) message
    outer = MIMEMultipart()
    outer['Subject'] = 'Attachment Test'
    outer['To'] = COMMASPACE.join(recipients)
    outer['From'] = sender
    outer.preamble = 'You will not see this in a MIME-aware mail reader.\n'

    # List of attachments
    attachments = [image]

    # Add the attachments to the message
    for file in attachments:
        try:
            with open(file, 'rb') as fp:
                msg = MIMEBase('application', "octet-stream")
                msg.set_payload(fp.read())
            encoders.encode_base64(msg)
            msg.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file))
            outer.attach(msg)
        except:
            print("Unable to open one of the attachments. Error: ", sys.exc_info()[0])
            raise

    composed = outer.as_string()

    # Send the email
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as s:
            s.ehlo()
            s.starttls()
            s.ehlo()
            s.login(sender, gmail_password)
            s.sendmail(sender, recipients, composed)
            s.close()
        print("Email sent!")
    except:
        print("Unable to send the email. Error: ", sys.exc_info()[0])
        raise



try:
    time.sleep(2) # to stabilize sensor
    
            
    while True:
        ##Timeloop
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        if GPIO.input(23):
            ##If loop
            GPIO.output(24, True)
            time.sleep(0.5) #Buzzer turns on for 0.5 sec
            print("Motion Detected at {}".format(st))
            ##Adds timestamp to image
            camera.capture('image_Time_{}.jpg'.format(st))
            image = ('image_Time_{}.jpg'.format(st))
            Send_Email(image)
            time.sleep(2)
            GPIO.output(24, False)
            time.sleep(5) #to avoid multiple detection

        time.sleep(0.1) #loop delay, should be less than detection delay

except:
    GPIO.cleanup()



