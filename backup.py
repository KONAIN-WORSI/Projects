import os
import shutil
import schedule
import datetime
import time

source_dir = r'C:\Users\Nitro\Videos\Captures'
destination_dir = r'C:\Users\Nitro\Videos\AnyDesk'

def copy_folder_to_directory(source, dest):
    today = datetime.date.today()
    dest_dir = os.path.join(dest, str(today))

    if not os.path.exists(dest_dir):
        shutil.copytree(source, dest_dir)
        print(f'The folder copied to: {dest_dir}')
    else:
        print(f'Folder already exists in: {dest_dir}')
        # Optionally, copy files individually if needed

schedule.every().day.at('16:08').do(lambda: copy_folder_to_directory(source_dir, destination_dir))


while True:
    schedule.run_pending()
    time.sleep(60)

