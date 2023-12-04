import os
import colorama
import ntplib
from time import ctime

# Initialize colorama for cross-platform ANSI color support
colorama.init()

# Dictionary to map status numbers to color and background color
status_colors = {
    0: (colorama.Fore.GREEN, colorama.Back.BLACK),   # neutral
    1: (colorama.Fore.YELLOW, colorama.Back.BLACK),  # warning
    2: (colorama.Fore.LIGHTRED_EX, colorama.Back.BLACK),  # error
    3: (colorama.Fore.RED, colorama.Back.BLACK)      # fatal
}

# Default values
project_Name = ""
project_Version = ""
log_folder = 'log'

def create_log_folder():
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

def save_to_log_file(log_data, timestamp):
    log_file = os.path.join(log_folder, f"log_{timestamp}.txt")
    with open(log_file, 'w') as file:
        file.write(log_data)

def get_ntp_time(server='pool.ntp.org'):
    try:
        client = ntplib.NTPClient()
        response = client.request(server, version=3)
        return ctime(response.tx_time)
    except ntplib.NTPException as e:
        return f"Error: {e}"

def formatSend(status_num, prompt):
    global project_Name, project_Version
    
    # Get the time from the NTP server
    time = get_ntp_time()

    # Using the values set from the main script
    if project_Name and project_Version:
        if status_num in status_colors:
            status_color, status_bg_color = status_colors[status_num]
            status_labels = ['neutral', 'warning', ' error ', ' fatal ']
            status_label = status_labels[status_num]

            formatted_message = (
                f"{colorama.Fore.CYAN}<{time}>{colorama.Style.RESET_ALL} "
                f"{colorama.Fore.BLUE}<{project_Name} | {project_Version}>{colorama.Style.RESET_ALL} "
                f"{status_bg_color}{status_color}<{status_label.upper()}>{colorama.Style.RESET_ALL} :"
                f"{status_color}{prompt}{colorama.Style.RESET_ALL}"
            )
            create_log_folder()
            save_to_log_file(formatted_message, time.replace(':', '-').replace(' ', '_'))

            return formatted_message
        else:
            return f"Invalid status number: {status_num}"
    else:
        return "Please project_Name, and project_Version before using formatSend"
