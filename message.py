import pywhatkit as pk
from datetime import datetime


message = "hello i am using pywhatkit to send message"
number = "+977 9762980222"

# Get current time and add 1 minute for scheduling
now = datetime.now()
hour = now.hour
minute = now.minute + 1

pk.sendwhatmsg(number, message, hour, minute)