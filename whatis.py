""" Written by Benjamin Jack Cullen aka Holographic_Sol

Step 1: Read file(s) into the buffer to try and check its true file type.
Step 2. Scan for the file(s) suffix in the database.
Step 3. Compare the database definition of the files suffix to the results from step 1.

Designed to distinguish between obfuscated files and non-obfuscated files.

An in this case definition of what is meant by obfuscated file: A file that has had its file name suffix modified in attempt to
disguise the file as another file type.
Example: File foobar.mp4 has been renamed to anything.exe

This program can be used as is to scan for obfuscated files, define file types and machine learn. Can also be used creatively to create
technologies that use this programs ability to distinguish between known files and obfuscated files as part of some
other function. For example Apple does this to prevent performing certain actions with some file types regardless of
the files alleged suffix.

"""

import os
import sys
import pathlib
import datetime
import re
import magic
import distutils.dir_util
import codecs
from colorama import Fore, Style

encode = u'\u5E73\u621015\u200e\U0001d6d1,'
vf = False
ei = 0
rf = ()
fl = False
learn = False
limit_char = 126
total_errors = 0


class cp:
    @staticmethod
    def cpf(message, end='\n'):
        sys.stderr.write('\x1b[1;31m' + message.strip() + '\x1b[0m' + end)

    @staticmethod
    def cpp(message, end='\n'):
        sys.stdout.write('\x1b[1;32m' + message.strip() + '\x1b[0m' + end)

    @staticmethod
    def cpw(message, end='\n'):
        sys.stderr.write('\x1b[1;33m' + message.strip() + '\x1b[0m' + end)

    @staticmethod
    def cpi(message, end='\n'):
        sys.stdout.write('\x1b[1;34m' + message.strip() + '\x1b[0m' + end)

    @staticmethod
    def cpb(message, end='\n'):
        sys.stdout.write('\x1b[1;37m' + message.strip() + '\x1b[0m' + end)


def cc():
    cmd = 'clear'
    if os.name in ('nt', 'dos'):
        cmd = 'cls'
    os.system(cmd)


def run_function_0(v):
    global vf
    bne = True
    if vf is False:
        with open('./database_file_extension_light.txt', 'r') as fo:
            for line in fo:
                line = line.strip()
                if line.startswith(v.lower()+'-file-extension'):
                    print('')

                    print('File Extension: ' + str(line.replace('-file-extension', '')))
                    print('')

                    bne = False
                if line.startswith(v.lower()+'-file-description'):
                    print(line.replace(v+'-file-description ', ''))
                    bne = False
    elif vf is True:
        with open('./database_file_extension_verbose.txt', 'r', encoding='utf-8') as fo:
            bpe = False
            for line in fo:

                line = line.strip()
                line = line.strip()
                if line.startswith(v.lower()+'-file-extension'):
                    print('')
                    cp.cpp(str('File Extension: ') + str(line.replace('-file-extension', '')))
                    print('')
                    bne = False
                    bpe = True
                elif bpe is True:
                    if line != '(end ' + v + ')':
                        print(line)
                    else:
                        bpe = False
                        break
    if bne is True:
        print('')
        print('No Entries Found for:', v)
    print('')
    fo.close()


def pr_row(limit_char):
    cp.cpf(str('-' * limit_char))


def logger(log_file, e, f):
    global total_errors
    total_errors += 1

    if not os.path.exists(log_file):
        open(log_file, 'w').close()

    log_tm_stamp = str(datetime.datetime.now())
    e = str('[' + log_tm_stamp + '] [error_count ' + str(total_errors) + '] ' + str(e)).strip()
    path_associated = str('[' + log_tm_stamp + '] [error_count ' + str(total_errors) + '] ' + str(f)).strip()
    with open(log_file, 'a') as fo:
        fo.write(path_associated + '\n')
        fo.write(e + '\n')
    fo.close()


def run_function_1(vv):
    global vf
    global ei
    global learn

    cp.cpi('-- attempting to clear screen.')
    cc()

    """ Create A Time Stamped Directory """
    cp.cpi('-- attempting to create new timestamped directory for results.')
    time_now = str(datetime.datetime.now())
    time_now_str = time_now
    time_now = time_now.replace(':', '-')
    time_now = time_now.replace('.', '')
    tm_stamp = time_now.replace(' ', '_')
    dir_now = './data/' + tm_stamp + '/'
    distutils.dir_util.mkpath(dir_now)

    """ Check Directory Exists """
    bool_created_tm_stamp_dir = False
    if os.path.exists(dir_now):
        cp.cpi(str('-- successfully created new directory: ') + str(dir_now))
        bool_created_tm_stamp_dir = True
    else:
        cp.cpf(str('-- failed to create new timestamped directory: ') + str(dir_now))

    if bool_created_tm_stamp_dir is True:

        ef = dir_now + 'log_exception.txt'
        log_file_failed_inspection = dir_now + 'log_file_unrecognized.txt'
        log_file_passed_inspection = dir_now + 'log_file_recognized.txt'
        log_file_permission_denied = dir_now + 'log_file_permission_denied.txt'
        log_file_empty_buffer_read = dir_now + 'log_file_buffer_string_empty.txt'
        cp.cpi(str('-- creating new file name value: ') + str(log_file_failed_inspection))
        cp.cpi(str('-- creating new file name value: ') + str(ef))

        """ Read Machine Learning Database (Learned Buffer Read Results Mapped To File Suffixes) """
        machine_learn_database = './database_machine_learning.txt'
        cp.cpi(str('-- attempting to read machine learning database:   ') + str(machine_learn_database))
        trf = machine_learn_database
        machine_learning_br = []
        suffixes_br = []
        line_count = 0

        if os.path.exists(trf):
            cp.cpi(str('-- reading machine learning database:   ') + str(machine_learn_database))
            with open(trf, 'r') as fo:
                for line in fo:
                    line_count += 1
                    line = line.strip()
                    line = line.lower()
                    line_split = line.split(' ')
                    line_split_0 = line_split[0].strip()

                    """ Add Machine Learnt Buffer Data To List """
                    if line not in machine_learning_br:
                        machine_learning_br.append(line)

                        """ Add Suffix To List """
                        suffix_var = line_split_0.replace('-buffer-read', '')
                        if suffix_var not in suffixes_br:
                            suffixes_br.append(suffix_var)

                    if '-buffer-read' not in line.replace(' ', ''):
                        print('-- machine learning database anomaly:  ', line)
            fo.close()
        else:
            cp.cpi(str('-- machine learning database does not exist:   ') + str(machine_learn_database))

        """ Set Counters """
        buffer_read_exception_count_0 = 0
        buffer_read_exception_count_1 = 0
        buffer_read_exception_permssion_count_0 = 0
        buffer_read_exception_permssion_count_1 = 0
        total_files_encountered = 0
        machine_learn_count = 0
        buffer_failed_count = 0
        buffer_passed_count = 0
        error_getting_suffix_count = 0
        bool_buffer_data_true_count = 0
        bool_buffer_data_false_count = 0

        """ Remember When Machine Last Learned """
        machine_last_learned = ''

        """ Initiate Lists """
        new_file_extension_br = []
        new_machine_learned = []
        unrecognized_buffer = []

        """ Display Scan Criteria And Present Confirmation Opportunity """
        print('')
        pr_row(limit_char)

        """ Header """
        if learn is True:
            cp.cpf('[WARNING!]         [WARNING!]         [WARNING!]         [WARNING!]         [WARNING!]         [WARNING!]          [WARNING!]')
            print('')
            cp.cpi('[MACHINE LEARNING CRITERIA]')
            print('')
            print(Style.BRIGHT + Fore.MAGENTA + '[SPECIFIED LOCATION]                        ' + Style.BRIGHT + Fore.GREEN + str(vv) + Style.RESET_ALL)
            print(Style.BRIGHT + Fore.MAGENTA + '[MACHINE LEARNING]                          ' + Style.BRIGHT + Fore.RED + str(learn) + '   [WARNING!]' + Style.RESET_ALL)
            print(Style.BRIGHT + Fore.MAGENTA + '[MACHINE LEARNED DEFINITIONS]               ' + Style.BRIGHT + Fore.GREEN + str(len(machine_learning_br)) + Style.RESET_ALL)
            print('')
            print(Style.BRIGHT + Fore.MAGENTA + '[MACHINE LEARNING]   ' + Style.BRIGHT + Fore.YELLOW + 'THIS IF SUCCESSFULL WILL ADD THE TRAINING DATA TO THE MACHINE LEARNED DATABASE WHICH')
            print(Style.BRIGHT + Fore.YELLOW + '                     WILL BE USED IN DE-OBFUSCATION SCANS & PERFORMING REVERSE SEARCHES!' + Style.RESET_ALL)
            print('')
            cp.cpf('[WARNING!]   MACHINE LEARNING ENABLED')
            cp.cpf('[WARNING!]   ENSURE ONLY TRUSTED DATA SETS!')
            print('')
            pr_row(limit_char)
        elif learn is False:
            print('')
            cp.cpi('[SCAN CRITERIA]')
            print('')
            print(Style.BRIGHT + Fore.MAGENTA + '[SPECIFIED LOCATION]                        ' + Style.BRIGHT + Fore.GREEN + str(vv) + Style.RESET_ALL)
            print(Style.BRIGHT+Fore.MAGENTA+'[MACHINE LEARNING]                          ' + Style.BRIGHT+Fore.GREEN+str(learn)+Style.RESET_ALL)
            print(Style.BRIGHT+Fore.MAGENTA+'[MACHINE LEARNED DEFINITIONS]               ' + Style.BRIGHT+Fore.GREEN+str(len(machine_learning_br))+Style.RESET_ALL)
            print('')
            pr_row(limit_char)
        print('')
        usr_choice = input('Continue (Y/y)?: ')
        print('')

        """ Continue If usr_choice is Y/y """
        if usr_choice.lower() == 'y':
            if learn is True:
                cp.cpi('-- attempting to learn about files in location:', vv)
            elif learn is False:
                cp.cpi('-- scanning location:', vv)

            """ Walk User Specified Directory """
            for dirName, subdirList, fileList in os.walk(vv):
                for fname in fileList:

                    """ Count Files And Timestamp Time Encountered """
                    total_files_encountered += 1
                    file_encountered_time_stamp = '[' + str(datetime.datetime.now()) + ']'

                    """ Create A Full Path To File From Root """
                    f = os.path.join(dirName, fname)
                    f = f.strip()

                    """ Sub Header """
                    if vf is True:
                        print('')
                        pr_row(limit_char)
                        print('')
                        if learn is True:
                            cp.cpi('[MACHINE LEARNING]')
                        elif learn is False:
                            cp.cpi('[ATTEMPTING DE-OBFUSCATION]')
                        print('')
                        print(Style.BRIGHT+Fore.MAGENTA+'[FILES ENCOUNTERED] ' + Style.BRIGHT+Fore.GREEN+str(total_files_encountered)+Style.RESET_ALL)
                        print(Style.BRIGHT+Fore.MAGENTA+'[TIME NOW] ' + Style.BRIGHT+Fore.GREEN+str(file_encountered_time_stamp)+Style.RESET_ALL)
                        print(Style.BRIGHT+Fore.MAGENTA+'[PATH] ' + Style.BRIGHT+Fore.GREEN+str(f)+Style.RESET_ALL)

                    """ Get File Name Suffix """
                    fe = ''
                    try:
                        fe = pathlib.Path(f).suffix
                        fe = fe.replace('.', '').lower()
                    except Exception as e:
                        error_getting_suffix_count += 1
                        log_file = ef
                        e = '[suffix error] ' + str(e)
                        logger(log_file, e, f)

                    """ Check If Suffix In Databases """
                    bool_new_br_suffix = False
                    if fe == '':
                        fe = 'no_file_extension'
                    if fe not in suffixes_br:
                        bool_new_br_suffix = True
                        if fe not in new_file_extension_br:
                            new_file_extension_br.append(fe)
                    if vf is True:
                        print(Style.BRIGHT + Fore.MAGENTA + '[ALLEGED SUFFIX] ' + Style.BRIGHT + Fore.GREEN + str(fe) + Style.RESET_ALL)

                    """ Initiate And Clear Each Iteration """
                    b = ''
                    b_1 = ''
                    b_2 = ''
                    e_tmp = ''
                    key_buff_read = ''
                    buffer_permission_denied_attempt_1 = False
                    buffer_permission_denied_attempt_2 = False

                    """ Attempt 1 To Read Buffer """
                    try:
                        b_1 = magic.from_buffer(codecs.open(f, "rb").read(2048))
                        b_1 = str(b_1)
                        b_1 = b_1.lower()
                        b_1 = b_1.strip()
                    except Exception as e:
                        if 'permission denied' in str(e).lower():
                            buffer_read_exception_permssion_count_0 += 1
                            buffer_permission_denied_attempt_1 = True
                        buffer_read_exception_count_0 += 1
                        e = '[error reading buffer (first try)] ' + str(e)
                        # e_tmp = e
                        # log_file = ef
                        # logger(log_file, e, f)

                    """ Attempt 2 To Read Buffer """
                    if e_tmp != '':
                        try:
                            b_2 = magic.from_buffer(open(f, "r").read(2048))
                            b_2 = str(b_2)
                            b_2 = b_2.lower()
                            b_2 = b_2.strip()
                        except Exception as e:
                            if 'permission denied' in str(e).lower():
                                buffer_read_exception_permssion_count_1 += 1
                                buffer_permission_denied_attempt_2 = True
                            buffer_read_exception_count_1 += 1
                            log_file = ef
                            e = '[error reading buffer (second try)] ' + str(e)
                            logger(log_file, e, f)

                    """ Use Most Defined Buffer String """
                    b_1_len = len(b_1)
                    b_2_len = len(b_2)
                    if b_1_len >= b_2_len:
                        b = b_1
                    elif b_2_len > b_1_len:
                        b = b_2
                    if vf is True:
                        print(Style.BRIGHT + Fore.MAGENTA + '[BUFFER READ] ' + Style.BRIGHT + Fore.GREEN + str(b) + Style.RESET_ALL)

                    """ Continue If Buffer String & Set Default Boolean """
                    bool_machine_learn = False
                    buffer_passed_inspection = False
                    bool_data_buffer = False
                    if len(b) > 0:
                        key_buff_read = str(fe) + '-buffer-read ' + str(b)
                        bool_buffer_data_true_count += 1
                        bool_data_buffer = True

                        """ Buffer output may yield digits for timestamps, dimensions etc. compare not the digits (keeping only the full line of data in the file and in memory for potential extreme strictness) """
                        digi_str = r'[0-9]'
                        x_re = re.sub(digi_str, '', key_buff_read)

                        """ Iterate Comparing regex x to regex y """
                        i = 0
                        for machine_learning_brs in machine_learning_br:
                            y_re = re.sub(digi_str, '', machine_learning_br[i])
                            if y_re == x_re:
                                if vf is True:
                                    print(Style.BRIGHT + Fore.MAGENTA + '[REGEX BUFFER KEY] ' + Style.BRIGHT + Fore.GREEN + str(x_re) + Style.RESET_ALL)
                                buffer_passed_inspection = True
                                break
                            i += 1

                        """ Handle Regex Comparison True & False """
                        if buffer_passed_inspection is True:
                            buffer_passed_count += 1
                            bool_machine_learn = False
                            if vf is True:
                                if learn is True:
                                    print(Style.BRIGHT + Fore.MAGENTA + '[MACHINE LEARNED COUNTER] ' + Style.BRIGHT + Fore.GREEN + str(machine_learn_count) + Style.RESET_ALL)
                                    print(Style.BRIGHT + Fore.MAGENTA + '[MACHINE LEARNED] ' + Style.BRIGHT + Fore.RED + str(bool_machine_learn) + Style.RESET_ALL)
                                    print(Style.BRIGHT + Fore.MAGENTA + '[MACHINE LAST LEARNED] ' + Style.BRIGHT + Fore.GREEN + str(machine_last_learned) + Style.RESET_ALL)
                        elif buffer_passed_inspection is False:
                            unrecognized_buffer.append(f)
                            buffer_failed_count += 1
                            if learn is True:
                                if vf is True:
                                    print(Style.BRIGHT + Fore.MAGENTA + '[MACHINE LEARNED COUNTER] ' + Style.BRIGHT + Fore.GREEN + str(machine_learn_count) + Style.RESET_ALL)
                                if key_buff_read not in new_machine_learned:
                                    machine_last_learned = str(datetime.datetime.now())
                                    new_machine_learned.append(key_buff_read)
                                    machine_learn_count += 1
                                    bool_machine_learn = True
                                    if vf is True:
                                        print(Style.BRIGHT + Fore.MAGENTA + '[MACHINE LEARNED] ' + Style.BRIGHT + Fore.GREEN + str(bool_machine_learn) + Style.RESET_ALL)
                                    with open(machine_learn_database, 'a') as fo:
                                        to_file = key_buff_read
                                        fo.write(to_file + '\n')
                                elif key_buff_read in new_machine_learned:
                                    bool_machine_learn = False
                                    if vf is True:
                                        print(Style.BRIGHT + Fore.MAGENTA + '[MACHINE LEARNED] ' + Style.BRIGHT + Fore.RED + str(bool_machine_learn) + Style.RESET_ALL)
                                if vf is True:
                                    print(Style.BRIGHT + Fore.MAGENTA + '[MACHINE LAST LEARNED] ' + Style.BRIGHT + Fore.GREEN + str(machine_last_learned) + Style.RESET_ALL)

                    else:
                        bool_buffer_data_false_count += 1
                        if learn is True:
                            bool_data_buffer = False
                            if vf is True:
                                print(Style.BRIGHT + Fore.MAGENTA + '[MACHINE LEARNED COUNTER] ' + Style.BRIGHT + Fore.GREEN + str(machine_learn_count) + Style.RESET_ALL)
                            bool_machine_learn = False
                            if vf is True:
                                print(Style.BRIGHT + Fore.MAGENTA + '[MACHINE LEARNED] ' + Style.BRIGHT + Fore.GREEN + str(bool_machine_learn) + Style.RESET_ALL)
                        elif learn is False:
                            buffer_failed_count += 1
                            buffer_passed_inspection = False
                            bool_data_buffer = False

                    if vf is True:
                        if learn is False:
                            if buffer_passed_inspection is True:
                                print(Style.BRIGHT + Fore.MAGENTA + '[BUFFER RECOGNIZED IN RELATION TO ALLEGED SUFFIX] ' + Style.BRIGHT + Fore.GREEN + str(buffer_passed_inspection) + Style.RESET_ALL)
                            elif buffer_passed_inspection is False:
                                print(Style.BRIGHT + Fore.MAGENTA + '[BUFFER RECOGNIZED IN RELATION TO ALLEGED SUFFIX] ' + Style.BRIGHT + Fore.RED + str(buffer_passed_inspection) + Style.RESET_ALL)
                        print(Style.BRIGHT + Fore.MAGENTA + '[BUFFER PERMISSION DENIED ATTEMPT 1] ' + Style.BRIGHT + Fore.GREEN + str(buffer_permission_denied_attempt_1) + Style.RESET_ALL)
                        print(Style.BRIGHT + Fore.MAGENTA + '[BUFFER PERMISSION DENIED ATTEMPT 2] ' + Style.BRIGHT + Fore.GREEN + str(buffer_permission_denied_attempt_2) + Style.RESET_ALL)

                    """ Set Applicable Log File And Create Log File If Necessary (Keep Trucking If Log File Destroyed) """
                    if buffer_passed_inspection is True:
                        log_file_inspection = log_file_passed_inspection
                    elif buffer_passed_inspection is False:
                        if buffer_permission_denied_attempt_1 is True and buffer_permission_denied_attempt_2 is True:
                            log_file_inspection = log_file_permission_denied
                        elif bool_data_buffer is False:
                            log_file_inspection = log_file_empty_buffer_read
                        else:
                            log_file_inspection = log_file_failed_inspection
                    if not os.path.exists(log_file_inspection):
                        open(log_file_inspection, 'w').close()

                    """ Set Logging Contents """
                    to_file_1 = '[FILES ENCOUNTERED] ' + str(total_files_encountered)
                    to_file_2 = '[' + str(datetime.datetime.now()) + ']'
                    to_file_3 = '[PATH] ' + str(f)
                    to_file_4 = str('[ALLEGED SUFFIX] ' + str(fe))
                    to_file_6 = '[BUFFER] ' + str(key_buff_read)
                    to_file_7 = str('[BUFFER RECOGNIZED IN RELATION TO ALLEGED SUFFIX] ' + str(buffer_passed_inspection))
                    to_file_10 = str('[NEW BUFFER DATABASE SUFFIX] ' + str(bool_new_br_suffix))
                    to_file_11 = str('[PERMISSION DENIED ATTEMPT 1] ' + str(buffer_permission_denied_attempt_1))
                    to_file_12 = str('[PERMISSION DENIED ATTEMPT 2] ' + str(buffer_permission_denied_attempt_2))
                    to_file_15 = str('[BUFFER DATA EXISTS] ' + str(bool_data_buffer))

                    """ Write Log Entry """
                    with codecs.open(log_file_inspection, 'a', encoding='utf-8') as fo:
                        fo.write(to_file_1 + '\n')
                        fo.write(to_file_2 + '\n')
                        fo.write(to_file_3 + '\n')
                        fo.write(to_file_4 + '\n')
                        fo.write(to_file_6 + '\n')
                        fo.write(to_file_7 + '\n')
                        fo.write(to_file_10 + '\n')
                        fo.write(to_file_11 + '\n')
                        fo.write(to_file_12 + '\n')
                        fo.write(to_file_15 + '\n')
                        fo.write(''+'\n')
                    fo.close()
            print('')
            pr_row(limit_char)
            print('')

            """ Write Final Report """
            log_report = dir_now + '/log_report.txt'
            if not os.path.exists(log_report):
                open(log_report, 'w').close()
            with open(log_report, 'a') as fo_report:
                if learn is True:
                    fo_report.write('[MACHINE LEARNING RESULTS]'+'\n')
                elif learn is False:
                    fo_report.write('[SCAN RESULTS]' + '\n')
                fo_report.write('' + '\n')
                fo_report.write('[MACHINE LEARN] ' + str(learn) + '\n')
                fo_report.write('[INITIATION TIME] ' + str(time_now_str) + '\n')
                fo_report.write('[COMPLETION TIME] ' + str(datetime.datetime.now()) + '\n')
                fo_report.write('[LOCATION] ' + str(vv) + '\n')
                fo_report.write('[TOTAL FILES ENCOUNTERED] ' + str(total_files_encountered) + '\n')
                if learn is True:
                    fo_report.write('[MACHINE LEARNED] ' + str(machine_learn_count) + '\n')
                fo_report.write('[PASSED BUFFER INSPECTION] ' + str(buffer_passed_count) + '\n')
                fo_report.write('[FAILED BUFFER INSPECTION] ' + str(buffer_failed_count) + '\n')
                fo_report.write('[BUFFER EXCEPTIONS ATTEMPT 1] ' + str(buffer_read_exception_count_0) + '\n')
                fo_report.write('[BUFFER EXCEPTIONS ATTEMPT 2] ' + str(buffer_read_exception_count_1) + '\n')
                fo_report.write('[FOUND BUFFER DATA] ' + str(bool_buffer_data_true_count) + '\n')
                fo_report.write('[DID NOT FIND BUFFER DATA] ' + str(bool_buffer_data_false_count) + '\n')
                fo_report.write('[BUFFER PERMISSION EXCEPTIONS ATTEMPT 1] ' + str(buffer_read_exception_permssion_count_0) + '\n')
                fo_report.write('[BUFFER PERMISSION EXCEPTIONS ATTEMPT 2] ' + str(buffer_read_exception_permssion_count_1) + '\n')
                fo_report.write('[NEW SUFFIXES ENCOUNTERED NOT IN BUFFER DATABASE COUNT] ' + str(len(new_file_extension_br)) + '\n')
                fo_report.write('[NEW SUFFIXES ENCOUNTERED NOT IN BUFFER DATABASE] ' + str(new_file_extension_br) + '\n')
            fo_report.close()

            if learn is True:
                cp.cpi('[MACHINE LEARNING RESULTS]')
            elif learn is False:
                cp.cpi('[SCAN RESULTS]')

            """ Display Final Report """
            print('')
            print(Style.BRIGHT + Fore.MAGENTA + '[INITIATION TIME] ' + Style.BRIGHT + Fore.GREEN + str(time_now_str) + Style.RESET_ALL)
            print(Style.BRIGHT + Fore.MAGENTA + '[COMPLETION TIME] ' + Style.BRIGHT + Fore.GREEN + str(datetime.datetime.now()) + Style.RESET_ALL)
            print('')
            print(Style.BRIGHT + Fore.MAGENTA + '[LOCATION] ' + Style.BRIGHT + Fore.GREEN + str(vv) + Style.RESET_ALL)
            print(Style.BRIGHT + Fore.MAGENTA + '[TOTAL FILES ENCOUNTERED] ' + Style.BRIGHT + Fore.GREEN + str(total_files_encountered) + Style.RESET_ALL)
            print('')
            if learn is True:
                print(Style.BRIGHT + Fore.MAGENTA + '[MACHINE LEARNED] ' + Style.BRIGHT + Fore.GREEN + str(machine_learn_count) + Style.RESET_ALL)
            elif learn is False:
                print(Style.BRIGHT + Fore.MAGENTA + '[PASSED BUFFER INSPECTION] ' + Style.BRIGHT + Fore.GREEN + str(buffer_passed_count) + Style.RESET_ALL)
                print(Style.BRIGHT + Fore.MAGENTA + '[FAILED BUFFER INSPECTION] ' + Style.BRIGHT + Fore.GREEN + str(buffer_failed_count) + Style.RESET_ALL)

            print(Style.BRIGHT + Fore.MAGENTA + '[BUFFER EXCEPTIONS ATTEMPT 1] ' + Style.BRIGHT + Fore.GREEN + str(buffer_read_exception_count_0) + Style.RESET_ALL)
            print(Style.BRIGHT + Fore.MAGENTA + '[BUFFER EXCEPTIONS ATTEMPT 2] ' + Style.BRIGHT + Fore.GREEN + str(buffer_read_exception_count_1) + Style.RESET_ALL)
            print(Style.BRIGHT + Fore.MAGENTA + '[FOUND BUFFER DATA] ' + Style.BRIGHT + Fore.GREEN + str(bool_buffer_data_true_count) + Style.RESET_ALL)
            print(Style.BRIGHT + Fore.MAGENTA + '[DID NOT FIND BUFFER DATA] ' + Style.BRIGHT + Fore.GREEN + str(bool_buffer_data_false_count) + Style.RESET_ALL)
            print(Style.BRIGHT + Fore.MAGENTA + '[BUFFER PERMISSION EXCEPTIONS ATTEMPT 1] ' + Style.BRIGHT + Fore.GREEN + str(buffer_read_exception_permssion_count_0) + Style.RESET_ALL)
            print(Style.BRIGHT + Fore.MAGENTA + '[BUFFER PERMISSION EXCEPTIONS ATTEMPT 2] ' + Style.BRIGHT + Fore.GREEN + str(buffer_read_exception_permssion_count_1) + Style.RESET_ALL)
            print(Style.BRIGHT + Fore.MAGENTA + '[NEW SUFFIXES ENCOUNTERED NOT IN BUFFER DATABASE COUNT] ' + Style.BRIGHT + Fore.GREEN + str(len(new_file_extension_br)) + Style.RESET_ALL)
            if len(unrecognized_buffer) == 1:
                print(Style.BRIGHT + Fore.MAGENTA + '[OBFUSCATED OR UNRECOGNIZED] ' + Style.BRIGHT + Fore.GREEN + str(unrecognized_buffer[0]) + Style.RESET_ALL)
            if len(unrecognized_buffer) == 2:
                print(Style.BRIGHT + Fore.MAGENTA + '[OBFUSCATED OR UNRECOGNIZED] ' + Style.BRIGHT + Fore.GREEN + str(unrecognized_buffer[1]) + Style.RESET_ALL)
            if len(unrecognized_buffer) == 3:
                print(Style.BRIGHT + Fore.MAGENTA + '[OBFUSCATED OR UNRECOGNIZED] ' + Style.BRIGHT + Fore.GREEN + str(unrecognized_buffer[2]) + Style.RESET_ALL)
            if len(unrecognized_buffer) > 3:
                print(Style.BRIGHT + Fore.MAGENTA + '[MORE OBFUSCATED OR UNRECOGNIZED FILES AVAILABLE IN LOG FILE] ' + Style.BRIGHT + Fore.GREEN + str(log_file_failed_inspection) + Style.RESET_ALL)
            print(Style.BRIGHT + Fore.MAGENTA + '[LOG FILES] ' + Style.BRIGHT + Fore.GREEN + str(dir_now) + Style.RESET_ALL)
            print('')
            pr_row(limit_char)
            print('')

            """ Post Scan Options """
            if learn is False:
                cp.cpi('[POST SCAN OPTIONS]')
                print('')
                cp.cpi('Display all obfuscated or unrecognized files (Y/y)?')
                print('')
                usr_choice_1 = input('Enter: ')
                if usr_choice_1.lower() == 'y':
                    for _ in unrecognized_buffer:
                        print(Style.BRIGHT + Fore.MAGENTA + '[OBFUSCATED OR UNRECOGNIZED] ' + Style.BRIGHT + Fore.GREEN + str(_) + Style.RESET_ALL)
                print('')
                pr_row(limit_char)
                print('')

if len(sys.argv) == 2 and sys.argv[1] == '-h':
    print('')
    print('-' * limit_char)
    print('')
    print('De-Obfuscate (whatis) ~ Written by Benjamin Jack Cullen aka Holographic_Sol')
    print('')
    print('    Designed to distinguish between obfuscated files and non-obfuscated files.')
    print('    In this particular definition of what is meant by obfuscated file: A file that has had its file name suffix modified in')
    print('    attempt to disguise the file as another file type.')
    print('    Example: File foobar.mp4 has been renamed to anything.exe')
    print('')
    print('    This program also attempts to define a given extension for you.')
    print('    This program can also learn from user specified locations in order to potentially perform more accurate deobfuscation.')
    print('')
    print('Command line arguments:')
    print('    -s                Specifies a directory to scan. [whatis -s directory_name -v]')
    print('    -d                Attempts to lookup a definition for suffix (not file/directory name) given. [whatis -d exe -v]')
    print('    --machine-learn   Instructs the program to train from a specified location. [whatis --machine-learn directory_name -v]')
    print('    -v                Show verbose output')
    print('    -h                Displays this help message')
    print('')
    print('Scan:')
    print('    Scan a specified location for obfuscated files.')
    print('    Step 1: The file(s) read in buffer to try and check its true file type.')
    print('    Step 2: Scans for the file(s) alleged suffix in the database.')
    print('    Step 3: A digitless database definition is then compared to a digitless result from Step 1.')
    print('    Results are logged and also displayed during the scan and upon scan completion.')
    print('')
    print('Machine Learn:')
    print('    Learns from a specified location.')
    print('    Step 1: The file(s) read in buffer to try and check its file type.')
    print('    Step 2: New buffer/suffix associations are (learned) appended to the machine learning database.')
    print('    Results are logged and also displayed during machine learning and upon machine learning completion.')
    print('    Care should be taken that no obfuscated files are in the specified location.')
    print('')
    print('Summary:')
    print('    This program can be used as is to scan for obfuscated files, define file types and machine learn. Can also be used')
    print('    creatively in harmony with technologies that need to distinguish between known files and obfuscated files as part of')
    print('    some other function. For example Apple does this to prevent performing certain actions with some file types regardless')
    print('    of the files alleged suffix.')
    print('')
    print('-' * limit_char)
    print('')
if len(sys.argv) == 3 or len(sys.argv) == 4 and fl is False:
    if '-d' in sys.argv:
        fl = True
        idx = sys.argv.index('-d')
        if len(sys.argv) > idx+1:
            v = sys.argv[idx+1]
            if v != '-v':
                rf = 0
# if len(sys.argv) == 3 or len(sys.argv) == 4 and fl is False:
if len(sys.argv) == 3 or len(sys.argv) == 4 and fl is False:
    if '-s' in sys.argv:
        fl = True
        idx = sys.argv.index('-s')
        if len(sys.argv) > idx + 1:
            vv = sys.argv[idx+1]
            if vv != '-v':
                rf = 1
if len(sys.argv) == 3 or len(sys.argv) == 4 and fl is False:
    if '--machine-learn' in sys.argv:
        fl = True
        idx = sys.argv.index('--machine-learn')
        if len(sys.argv) > idx + 1:
            vv = sys.argv[idx+1]
            if vv != '-v':
                learn = True
                rf = 1

if '-d' in sys.argv or '-s' in sys.argv or '--machine-learn' in sys.argv:
    for _ in sys.argv:
        if _ == '-v':
            vf = True
if rf == 0:
    run_function_0(v)
elif rf == 1:
    if os.path.exists(vv) and os.path.isdir(vv) is True:
        run_function_1(vv)
    else:
        print('-- invalid path')
