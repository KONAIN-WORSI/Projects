import time
import datetime
import winsound

def display_current_date():
    now = datetime.datetime.now()
    print(f'Current Date: {now.strftime('%Y-%m-%d')}')


def display_current_time():
    now = datetime.datetime.now()
    print(f'Current Time: {now.strftime('%H:%M:%S')}')

def set_alarm():
    alarm_time = input('Set alarm time (HH:MM): ')

    while True:
        current_time = time.strftime('%H:%M')
        if alarm_time == current_time:
            print('Wake Up')
            winsound.Beep(3000, 3000)
            break

def snooze_alarm():
    snooze = 3
    snooze_time = time.time() + snooze * 60

    while time.time() < snooze_time:
        time.sleep(1)
        print('Snoozing...')
    print('Snooze over! Wake Up!')
    winsound.Beep(3000, 3000)

def stop_alarm():
    print('Alarm stopped!')


def clock():
    print('Welcome to the Konain Clock!')
    print('='*50)

    while True:
        try:
            x = input('Enter (date/time/alarm set up/alarm snooze/exit) to see results: ').lower()

            if x == 'date':
                display_current_date()
            elif x == 'time':
                display_current_time()
            elif x == 'set alarm':
                set_alarm()
            elif x == 'snooze':
                snooze_alarm()
            elif x == 'stop':
                stop_alarm()
            elif x == 'exit':
                print('Exiting Clock. Goodbye!')
                break
            else:
                print('Invalid input! Please enter date, time, exit and others.')
        except Exception as e:
            print(f'Invalid syntax, Error occured: {e}')


if __name__ == '__main__':
    clock() 