import os
import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
import lib.config as config
from datetime import date
import collections
from collections import defaultdict
from datetime import timedelta, date

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

def build_work_path(directory, day_iter):
    year_dir = os.path.join(directory, str(day_iter.year))
    month_dir = os.path.join(year_dir, '{:02d}'.format(day_iter.month))
    return os.path.join(month_dir, '{:02d}'.format(day_iter.day))
    
def parse_date(date_str):
    """
        date_str(str): date string specification with format yyyy-mm-dd
    """
    split = date_str.split('-')
    return date(int(split[0]), int(split[1]), int(split[2])) 
    
def linux_input(log_directory, channel_list, starting_date, ending_date):
    """  
        reads the IRC-Logs files in linux environment

    Args:
        log_directory (str): Location of the logs (Assumed to be arranged in directory structure as : <year>/<month>/<day>/<log-file-for-channel>.txt)
        here log_directory will have the directory where all the folders 2013 2014 2015 etc are stored
        channels_list (list): list of channels to be perform analysis on OR one element list ["ALL"] to perform analyis on all channels in the folder
        starting_date(date object): Starting date 
        ending_date(date object)  : Ending date in the format yyyy-mm-dd

    Returns:
        logs (dict) : dictionary with key(str) as 'yyyy-mm-dd' and value as another dictionary {"data":day_data,"channel":channel_name}

    """
    start_date = parse_date(starting_date)
    end_date = parse_date(ending_date)
    
    logs = defaultdict(list)
    
    for day_iter in daterange(start_date, end_date):
        
        work_path = build_work_path(log_directory, day_iter)
        
        if not os.path.exists(work_path):
            print "Log doest not exist for %s", work_path
        else:
            if (len(channel_list) == 1 and channel_list[0] == "ALL"):
                channel_list = [channel[:-4] for channel in os.listdir(work_path)]
            
            for channel in channel_list:
                file_path = os.path.join(work_path, channel + '.txt')
                    
                if not os.path.exists(file_path):
                    print "[Error | io/linuxInput] Channel " + file_path + " doesn't exist"
                    continue
                    
                with open(file_path) as f:
                    """ day_data stores all the lines of the file channel_name """
                    if config.DEBUGGER:
                        print "Working on: " + file_path
                    
                    day_data = f.readlines()             
                
                f.close()

                value = {
                    "log_data": day_data, 
                    "auxiliary_data": {
                            "channel": channel,
                            "year": day_iter.year,
                            "month": day_iter.month,
                            "day": day_iter.day
                        }
                    }

                logs[day_iter].append(value)
                    
    return collections.OrderedDict(sorted(logs.items()))
