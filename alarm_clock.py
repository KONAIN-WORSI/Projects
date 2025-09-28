import time
import winsound

def set_alarm():
    alarm_time = input('Select the alarm time (HH:MM):  ')

    while True:
        current_time = time.strftime("%H:%M")
        if current_time == alarm_time:
            print('Wake up!')
            winsound.Beep(3000,3000)
            break



def snooze_alarm():
    snooze_time = 5
    alarm_end = time.time() + snooze_time * 60

    while time.time() < alarm_end:
        time.sleep(1)
    print('Snooze time is over,Wake up!')
    winsound.Beep(3000,3000)

def stop_alarm():
    print('Alarm stopped!')

while True:
     print('Options!')
     print('Option: 1, this will set the alarm')
     print('Option: 2, this will snooze the alarm')   
     print('option: 3, this will stop the alarm')
     print('Option: 4, exit!')

     it =  input('Your choice: ')

     if it == '1':
         set_alarm()
     elif it == '2':
         snooze_alarm()
     elif it == '3':
         stop_alarm()
     elif it == '4':
         break
     else:
         print('Invalid syntax; please choose the given option')



