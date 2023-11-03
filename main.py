import wmi
import os

def find_files(directory, extension):
    # Знаходить файли з конкретним розширенням.
    for filename in os.listdir(directory):
        filename, extension = os.path.splitext(filename)
        if extension == '.inf':
            yield filename

def find_file(directory, pattern):
    # Знаходить файл, в якому міститься заданий рядок.
    for filename in find_files(directory, extension):
        with open(f'{directory}{filename}{extension}', 'r', encoding='UTF-16 LE') as f:
            try:
                for line in f:
                    x = line.upper()
                    if pattern in x:
                        driver_path = f'{directory}{filename}{extension}'
                        return driver_path
            except UnicodeDecodeError:
                continue

def update_driver(driver_path):
    os.system(f'pnputil /add-driver {driver_path} /install')
    print(f'Update "{device.HardwareID[1]}" done')


if __name__ == "__main__":

    # Отримати список пристроїв
    devices = wmi.WMI().Win32_PnPEntity()
    directory = 'C:\\Windows\\INF\\'
    extension = '.inf'

    # Перевірити кожний пристрій
    for device in devices:
        if device.ConfigManagerErrorCode == 1 or device.ConfigManagerErrorCode == 28:
            pattern = device.HardwareID[1]
            driver_path = find_file(directory, pattern)
            update_driver(driver_path)
    else:
        print('No updateable devices')
