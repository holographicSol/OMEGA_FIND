""" Written by Benjamin Jack Cullen aka Holographic_Sol

OmegaFind

Intention 1: To find/expose files that may be pretending to be a file type other than the files real file type.

    Example: secret_file.mp4 has been renamed to anything.anything and buried somewhere in a drive.
        OmegaFind seeks to expose these files for what they really are.
        (A double-edged blade. agent exposes you/you expose an agent)

Intention 2: To find files not by name or filename suffix matching but by reading each file into memory and comparing
    the buffer to known buffer reads for the suffix specified.

Intention 3: Define. Specify a filename suffix and return a concise/verbose description of the file type specified.

Modes of operation:

    Learn: Provide OmegaFind with a directory path of trusted file(s) to learn from to build OmegaFind's knowledge of
    what file types should look like.

    Scan: Scan a directory and try to ascertain if file(s) are what they claim to be.

    Find: A special search feature. Searches for file types not by suffix or MIME types but by reading the file into
    memory and comparing the read to known buffer reads compiled using -learn.

    Define: Return concise/verbose information about a filetype specified.

"""

import os
import sys
import pathlib
import datetime
import re
import magic
import codecs
from colorama import Fore, Style
import pyprogress

encode = u'\u5E73\u621015\u200e\U0001d6d1,'
verbosity = False
first_pass = True
ei = 0
rf = ()
learn = False
limit_char = 120
total_errors = 0
buffer_size = 2048
multiplier = pyprogress.multiplier_from_inverse_factor(factor=50)


def cc():
    cmd = 'clear'
    if os.name in ('nt', 'dos'):
        cmd = 'cls'
    os.system(cmd)


def run_function_0(v):
    global verbosity
    bne = True
    if verbosity is False:
        with codecs.open('./db/database_file_extension_light.txt', 'r', encoding='utf8') as fo:
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
    elif verbosity is True:
        with codecs.open('./db/database_file_extension_verbose.txt', 'r', encoding='utf-8') as fo:
            bpe = False
            for line in fo:
                line = line.strip()
                if line.startswith(v.lower()+'-file-extension'):
                    print('')
                    print(str('File Extension: ') + str(line.replace('-file-extension', '')))
                    print('')
                    bne = False
                    bpe = True
                elif bpe is True:
                    if line != '(end ' + v + ')':
                        print(line)
                    else:
                        break
    if bne is True:
        print('')
        print('No Entries Found for:', v)
    print('')
    fo.close()


def pr_row(limit_char):
    print(str('-' * limit_char))


def exception_logger(log_file, e, f):
    global total_errors
    total_errors += 1

    if not os.path.exists('./log/'):
        os.mkdir('./log/')

    if not os.path.exists(log_file):
        open(log_file, 'w').close()

    log_tm_stamp = str(datetime.datetime.now())
    e = str('[' + log_tm_stamp + '] [error_count ' + str(total_errors) + '] ' + str(e)).strip()
    path_associated = str('[' + log_tm_stamp + '] [error_count ' + str(total_errors) + '] ' + str(f)).strip()
    with codecs.open(log_file, 'a', encoding='utf8') as fo:
        fo.write(path_associated + '\n')
        fo.write(e + '\n')
    fo.close()


def logger_omega_find_result(log_file='', fullpath='', buffer=''):

    if not os.path.exists('./data/'):
        os.mkdir('./data/')

    if not os.path.exists(log_file):
        open(log_file, 'w').close()

    log_tm_stamp = str(datetime.datetime.now())
    to_file = str('[' + log_tm_stamp + '] [PATH] ' + str(fullpath)).strip() + ' [BUFFER] ' + str(buffer)

    with codecs.open(log_file, 'a', encoding='utf8') as fo:
        fo.write(to_file + '\n')
    fo.close()


def scan_learn(target_path, buffer_size=2048, first_pass=False):
    global ei
    global learn
    global verbosity

    if verbosity is True:
        print('-- attempting to create new timestamped directory for results.')

    """ Create A Time Stamped Directory """
    time_now = str(datetime.datetime.now())
    time_now = time_now.replace(':', '-')
    time_now = time_now.replace('.', '')
    tm_stamp = time_now.replace(' ', '_')
    dir_now = './data/' + tm_stamp + '/'
    if not os.path.exists(dir_now):
        os.mkdir(dir_now)

    """ Check Directory Exists """
    bool_created_tm_stamp_dir = False
    if os.path.exists(dir_now):
        if verbosity is True:
            print(str('-- successfully created new directory: ') + str(dir_now))
        bool_created_tm_stamp_dir = True
    else:
        if verbosity is True:
            print(str('-- failed to create new timestamped directory: ') + str(dir_now))

    if bool_created_tm_stamp_dir is True:
        ef = dir_now + 'log_exception.txt'
        log_file_failed_inspection = dir_now + 'log_file_unrecognized.txt'
        log_file_passed_inspection = dir_now + 'log_file_recognized.txt'
        log_file_permission_denied = dir_now + 'log_file_permission_denied.txt'
        log_file_empty_buffer_read = dir_now + 'log_file_buffer_string_empty.txt'
        if verbosity is True:
            print(str('-- creating new file name value: ') + str(log_file_failed_inspection))
            print(str('-- creating new file name value: ') + str(ef))
        print('')
        print('-' * limit_char)

        # Header
        if learn is True:
            str_ = '[OMEGA FIND] LEARNING MODE'
            print(str(' ' * int(int(limit_char / 2) - int(len(str_) / 2))) + Style.BRIGHT + Fore.GREEN + str_ + Style.RESET_ALL)
            print('-' * limit_char)
            str_ = '[LEARNING CRITERIA]'
            print(str(' ' * int(
                int(limit_char / 2) - int(len(str_) / 2))) + Style.BRIGHT + Fore.GREEN + str_ + Style.RESET_ALL)
        elif learn is False:
            str_ = '[OMEGA FIND] DE-OBFUSCATION MODE'
            print(str(' ' * int(int(limit_char / 2) - int(len(str_) / 2))) + Style.BRIGHT + Fore.GREEN + str_ + Style.RESET_ALL)
            print('-' * limit_char)
            str_ = '[SCAN CRITERIA]'
            print(str(' ' * int(int(limit_char / 2) - int(len(str_) / 2))) + Style.BRIGHT + Fore.GREEN + str_ + Style.RESET_ALL)
        print('')
        print(Style.BRIGHT + Fore.GREEN + '[SPECIFIED LOCATION] ' + Style.RESET_ALL + str(target_path))
        if learn is True:
            print(Style.BRIGHT + Fore.GREEN + '[LEARNING] ' + Style.RESET_ALL + str(learn))
        else:
            print(Style.BRIGHT + Fore.GREEN + '[LEARNING] ' + Style.RESET_ALL + str(learn))

        """ Read Database (Learned Buffer Read Results Mapped To Filename Suffixes) """
        learn_database = './db/database_learning.txt'
        if verbosity is True:
            print(str('-- attempting to read database:   ') + str(learn_database))
        trf = learn_database
        learning_br = []
        suffixes_br = []
        line_count = 0

        if os.path.exists(trf):
            if verbosity is True:
                print(str('-- reading learning database:              ') + str(learn_database))
            with codecs.open(trf, 'r', encoding='utf8') as fo:
                for line in fo:
                    line_count += 1
                    line = line.strip()
                    line = line.lower()
                    line_split = line.split(' ')
                    line_split_0 = line_split[0].strip()

                    """ Add Learnt Buffer Data To List """
                    if line not in learning_br:
                        learning_br.append(line)
                        pr_str = str(Style.BRIGHT + Fore.GREEN + '[LEARNED DEFINITIONS] ' + Style.RESET_ALL + str(len(learning_br)))
                        pyprogress.pr_technical_data(pr_str)

                        """ Add Suffix To List """
                        suffix_var = line_split_0.replace('-buffer-read', '')
                        if suffix_var not in suffixes_br:
                            suffixes_br.append(suffix_var)

                    if '-buffer-read' not in line.replace(' ', ''):
                        if verbosity is True:
                            print('-- learning database anomaly:', line)
            fo.close()
        print('')

        # preliminarily scan target location
        f_count = 0
        if first_pass is True:
            for dirName, subdirList, fileList in os.walk(target_path):
                for fname in fileList:
                    f_count += 1
                    pr_str = str(Style.BRIGHT + Fore.GREEN + '[FILES] ' + Style.RESET_ALL + str(f_count))
                    pyprogress.pr_technical_data(pr_str)
        else:
            print(Style.BRIGHT + Fore.GREEN + '[SKIPPING PRELIMINARY SCAN]' + Style.RESET_ALL)
        print('')
        print('-' * 120)

        """ Set Counters """
        buffer_read_exception_count_0 = 0
        buffer_read_exception_count_1 = 0
        buffer_read_exception_permssion_count_0 = 0
        buffer_read_exception_permssion_count_1 = 0
        total_files_encountered = 0
        learn_count = 0
        buffer_failed_count = 0
        buffer_passed_count = 0
        error_getting_suffix_count = 0
        bool_buffer_data_true_count = 0
        bool_buffer_data_false_count = 0

        last_learned = ''
        new_file_extension_br = []
        new_learned = []
        unrecognized_buffer = []
        progress_bar_color = 'CYAN'

        if learn is True:
            usr_choice = input('Press Y to learn or press any other key to abort [Enter] : ')
            print('-' * limit_char)
            str_ = '[OMEGA FIND] LEARNING'
            print(str(' ' * int(int(limit_char / 2) - int(len(str_) / 2))) + Style.BRIGHT + Fore.GREEN + str_ + Style.RESET_ALL)
        elif learn is False:
            usr_choice = input('Press Y to attempt de-obfuscation or press any other key to abort [Enter] : ')
            print('-' * limit_char)
            str_ = '[OMEGA FIND] DE-OBFUSCATING'
            print(str(' ' * int(int(limit_char / 2) - int(len(str_) / 2))) + Style.BRIGHT + Fore.GREEN + str_ + Style.RESET_ALL)
            progress_bar_color = 'RED'
        print('')

        """ Continue If Compiled Database Lists Are Aligned """
        if usr_choice.lower() == 'y':

            """ Walk User Specified Directory """
            for dirName, subdirList, fileList in os.walk(target_path):
                for fname in fileList:
                    total_files_encountered += 1
                    file_encountered_time_stamp = '[' + str(datetime.datetime.now()) + ']'
                    f = os.path.join(dirName, fname)
                    f = f.strip()

                    if verbosity is True:
                        print('')
                        print('-' * limit_char)
                        print('')
                        if learn is True:
                            print(Style.BRIGHT + Fore.GREEN + '[OMEGA FIND] ' + Style.RESET_ALL + 'Learning')
                        elif learn is False:
                            print(Style.BRIGHT + Fore.GREEN + '[OMEGA FIND] ' + Style.RESET_ALL + 'Attempting de-obfuscation')
                        print(Style.BRIGHT+Fore.GREEN+'[FILES ENCOUNTERED] ' + Style.RESET_ALL + str(total_files_encountered))
                        print(Style.BRIGHT+Fore.GREEN+'[TIME NOW] ' + Style.RESET_ALL + str(file_encountered_time_stamp))
                        print(Style.BRIGHT+Fore.GREEN+'[PATH] ' + Style.RESET_ALL + str(f))
                    else:
                        try:
                            pyprogress.progress_bar(part=int(total_files_encountered), whole=int(f_count),
                                                    pre_append=str(Style.BRIGHT + Fore.GREEN + '[LEARNING] ' + Style.RESET_ALL),
                                                    append=str(' ' + str(total_files_encountered) + '/' + str(f_count) + Style.BRIGHT + Fore.GREEN + '  [' + str(learn_count) + ']' + Fore.RED + ' [' + str(buffer_read_exception_count_1) + ']' + Style.RESET_ALL),
                                                    encapsulate_l='|',
                                                    encapsulate_r='|',
                                                    encapsulate_l_color=progress_bar_color,
                                                    encapsulate_r_color=progress_bar_color,
                                                    progress_char=' ',
                                                    bg_color=progress_bar_color,
                                                    factor=50,
                                                    multiplier=multiplier)
                        except Exception as e:
                            print(e)

                    """ Get File Name Suffix """
                    fe = ''
                    try:
                        fe = pathlib.Path(f).suffix
                        fe = fe.replace('.', '').lower()
                    except Exception as e:
                        error_getting_suffix_count += 1
                        log_file = ef
                        e = '[suffix error] ' + str(e)
                        exception_logger(log_file, e, f)

                    """ Check If Suffix In Databases """
                    bool_new_br_suffix = False
                    if fe == '':
                        fe = 'no_file_extension'
                    if fe not in suffixes_br:
                        bool_new_br_suffix = True
                        if fe not in new_file_extension_br:
                            new_file_extension_br.append(fe)
                    if verbosity is True:
                        print(Style.BRIGHT + Fore.GREEN + '[ALLEGED SUFFIX] ' + Style.RESET_ALL + str(fe))

                    b = ''
                    b_1 = ''
                    b_2 = ''
                    e_tmp = ''
                    key_buff_read = ''
                    buffer_permission_denied_attempt_1 = False
                    buffer_permission_denied_attempt_2 = False
                    try:
                        """ Allocate buffer size and read the file. """
                        b_1 = magic.from_buffer(codecs.open(f, "rb").read(buffer_size))
                        b_1 = str(b_1)
                        b_1 = b_1.lower()
                        b_1 = b_1.strip()
                    except Exception as e:
                        if 'permission denied' in str(e).lower():
                            buffer_read_exception_permssion_count_0 += 1
                            buffer_permission_denied_attempt_1 = True
                        buffer_read_exception_count_0 += 1
                    if e_tmp != '':
                        try:
                            """ Allocate buffer size and read the file. """
                            b_2 = magic.from_buffer(open(f, "r").read(buffer_size))
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
                            exception_logger(log_file, e, f)

                    """ Use Most Defined Buffer String """
                    b_1_len = len(b_1)
                    b_2_len = len(b_2)
                    if b_1_len >= b_2_len:
                        b = b_1
                    elif b_2_len > b_1_len:
                        b = b_2

                    if verbosity is True:
                        print(Style.BRIGHT + Fore.GREEN + '[BUFFER READ] ' + Style.RESET_ALL + str(b))

                    """ Continue If Buffer String & Set Default Boolean """
                    bool_learn = False
                    buffer_passed_inspection = False
                    bool_data_buffer = False
                    if len(b) > 0:
                        key_buff_read = str(fe) + '-buffer-read ' + str(b)
                        bool_buffer_data_true_count += 1
                        bool_data_buffer = True

                        """ Buffer output may yield digits for timestamps, dimensions etc. """
                        digi_str = r'[0-9]'
                        x_re = re.sub(digi_str, '', key_buff_read)

                        """ Iterate Comparing regex x to regex y """
                        i = 0
                        for learning_brs in learning_br:
                            y_re = re.sub(digi_str, '', learning_br[i])
                            if y_re == x_re:
                                if verbosity is True:
                                    print(Style.BRIGHT + Fore.GREEN + '[REGEX BUFFER MATCH] ' + Style.RESET_ALL + str(x_re))
                                buffer_passed_inspection = True
                                break
                            i += 1

                        if buffer_passed_inspection is True:
                            buffer_passed_count += 1
                            bool_learn = False
                            if verbosity is True:
                                if learn is True:
                                    print(Style.BRIGHT + Fore.GREEN + '[LEARNED COUNTER] ' + Style.RESET_ALL + str(learn_count))
                                    print(Style.BRIGHT + Fore.GREEN + '[LEARNED] ' + Style.RESET_ALL + str(bool_learn))
                                    print(Style.BRIGHT + Fore.GREEN + '[LAST LEARNED] ' + Style.RESET_ALL + str(last_learned))
                        elif buffer_passed_inspection is False:
                            unrecognized_buffer.append(f)
                            buffer_failed_count += 1
                            if learn is True:
                                if verbosity is True:
                                    print(Style.BRIGHT + Fore.GREEN + '[LEARNED COUNTER] ' + Style.RESET_ALL + str(learn_count))
                                if key_buff_read not in new_learned:
                                    last_learned = str(datetime.datetime.now())
                                    new_learned.append(key_buff_read)
                                    learn_count += 1
                                    bool_learn = True
                                    if verbosity is True:
                                        print(Style.BRIGHT + Fore.GREEN + '[LEARNED] ' + Style.RESET_ALL + str(bool_learn))
                                    with codecs.open(learn_database, 'a', encoding='utf8') as fo:
                                        to_file = key_buff_read
                                        fo.write(to_file + '\n')
                                elif key_buff_read in new_learned:
                                    bool_learn = False
                                    if verbosity is True:
                                        print(Style.BRIGHT + Fore.GREEN + '[LEARNED] ' + Style.RESET_ALL + str(bool_learn))
                                if verbosity is True:
                                    print(Style.BRIGHT + Fore.GREEN + '[LAST LEARNED] ' + Style.RESET_ALL + str(last_learned))
                    else:
                        bool_buffer_data_false_count += 1
                        if learn is True:
                            bool_data_buffer = False
                            bool_learn = False
                            if verbosity is True:
                                print(Style.BRIGHT + Fore.GREEN + '[LEARNED COUNTER] ' + Style.RESET_ALL + str(learn_count))
                                print(Style.BRIGHT + Fore.GREEN + '[LEARNED] ' + Style.RESET_ALL + str(bool_learn))
                        elif learn is False:
                            buffer_failed_count += 1
                            buffer_passed_inspection = False
                            bool_data_buffer = False
                    if verbosity is True:
                        if learn is False:
                            if buffer_passed_inspection is True:
                                print(Style.BRIGHT + Fore.GREEN + '[BUFFER RECOGNIZED IN RELATION TO ALLEGED SUFFIX] ' + Style.BRIGHT + str(buffer_passed_inspection))
                            elif buffer_passed_inspection is False:
                                print(Style.BRIGHT + Fore.GREEN + '[BUFFER RECOGNIZED IN RELATION TO ALLEGED SUFFIX] ' + Style.BRIGHT + str(buffer_passed_inspection))
                            print(Style.BRIGHT + Fore.GREEN + '[NEW BUFFER DATABASE SUFFIX] ' + Style.RESET_ALL + str(bool_new_br_suffix))
                        print(Style.BRIGHT + Fore.GREEN + '[BUFFER PERMISSION DENIED ATTEMPT 1] ' + Style.RESET_ALL + str(buffer_permission_denied_attempt_1))
                        print(Style.BRIGHT + Fore.GREEN + '[BUFFER PERMISSION DENIED ATTEMPT 2] ' + Style.RESET_ALL + str(buffer_permission_denied_attempt_2))
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

            print('\n')
            print('-'*limit_char)
            log_report = dir_now + '/log_report.txt'

            if not os.path.exists(log_report):
                open(log_report, 'w').close()
            with codecs.open(log_report, 'a', encoding='utf8') as fo_report:
                if learn is True:
                    fo_report.write('[LEARNING RESULTS]'+'\n')
                elif learn is False:
                    fo_report.write('[SCAN RESULTS]' + '\n')
                fo_report.write('' + '\n')
                fo_report.write('[LEARN] ' + str(learn) + '\n')
                fo_report.write('[INITIATION TIME] ' + str(time_now) + '\n')
                fo_report.write('[COMPLETION TIME] ' + str(datetime.datetime.now()) + '\n')
                fo_report.write('[LOCATION] ' + str(target_path) + '\n')
                fo_report.write('[TOTAL FILES ENCOUNTERED] ' + str(total_files_encountered) + '\n')
                if learn is True:
                    fo_report.write('[LEARNED] ' + str(learn_count) + '\n')
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
                str_ = '[LEARNING RESULTS]'
                print(str(' ' * int(int(limit_char / 2) - int(len(str_) / 2))) + Style.BRIGHT + Fore.GREEN + str_ + Style.RESET_ALL)
            elif learn is False:
                str_ = '[SCAN RESULTS]'
                print(str(' ' * int(int(limit_char / 2) - int(len(str_) / 2))) + Style.BRIGHT + Fore.GREEN + str_ + Style.RESET_ALL)
            print('')
            print(Style.BRIGHT + Fore.GREEN + '[INITIATION TIME] ' + Style.RESET_ALL + str(time_now))
            print(Style.BRIGHT + Fore.GREEN + '[COMPLETION TIME] ' + Style.RESET_ALL + str(datetime.datetime.now()))
            print(Style.BRIGHT + Fore.GREEN + '[TOTAL FILES ENCOUNTERED] ' + Style.RESET_ALL + str(total_files_encountered))
            if learn is True:
                print(Style.BRIGHT + Fore.GREEN + '[LEARNED] ' + Style.RESET_ALL + str(learn_count))
            elif learn is False:
                print(Style.BRIGHT + Fore.GREEN + '[PASSED BUFFER INSPECTION] ' + Style.RESET_ALL + str(buffer_passed_count))
                print(Style.BRIGHT + Fore.GREEN + '[FAILED BUFFER INSPECTION] ' + Style.RESET_ALL + str(buffer_failed_count))
            print(Style.BRIGHT + Fore.GREEN + '[BUFFER EXCEPTIONS ATTEMPT 1] ' + Style.RESET_ALL + str(buffer_read_exception_count_0))
            print(Style.BRIGHT + Fore.GREEN + '[BUFFER EXCEPTIONS ATTEMPT 2] ' + Style.RESET_ALL + str(buffer_read_exception_count_1))
            print(Style.BRIGHT + Fore.GREEN + '[FOUND BUFFER DATA] ' + Style.RESET_ALL + str(bool_buffer_data_true_count))
            print(Style.BRIGHT + Fore.GREEN + '[DID NOT FIND BUFFER DATA] ' + Style.RESET_ALL + str(bool_buffer_data_false_count))
            print(Style.BRIGHT + Fore.GREEN + '[BUFFER PERMISSION EXCEPTIONS ATTEMPT 1] ' + Style.RESET_ALL + str(buffer_read_exception_permssion_count_0))
            print(Style.BRIGHT + Fore.GREEN + '[BUFFER PERMISSION EXCEPTIONS ATTEMPT 2] ' + Style.RESET_ALL + str(buffer_read_exception_permssion_count_1))
            print(Style.BRIGHT + Fore.GREEN + '[NEW SUFFIXES ENCOUNTERED NOT IN BUFFER DATABASE COUNT] ' + Style.RESET_ALL + str(len(new_file_extension_br)))
            if len(unrecognized_buffer) == 1:
                print(Style.BRIGHT + Fore.GREEN + '[OBFUSCATED OR UNRECOGNIZED] ' + Style.RESET_ALL + str(unrecognized_buffer[0]))
            if len(unrecognized_buffer) == 2:
                print(Style.BRIGHT + Fore.GREEN + '[OBFUSCATED OR UNRECOGNIZED] ' + Style.RESET_ALL + str(unrecognized_buffer[1]))
            if len(unrecognized_buffer) == 3:
                print(Style.BRIGHT + Fore.GREEN + '[OBFUSCATED OR UNRECOGNIZED] ' + Style.RESET_ALL + str(unrecognized_buffer[2]))
            if len(unrecognized_buffer) > 3:
                print(Style.BRIGHT + Fore.GREEN + '[MORE OBFUSCATED OR UNRECOGNIZED FILES AVAILABLE IN LOG FILE] ' + Style.RESET_ALL + str(log_file_failed_inspection))
            print(Style.BRIGHT + Fore.GREEN + '[LOG FILES] ' + Style.RESET_ALL + str(dir_now))
            print('')
            print('-'*limit_char)
            if learn is False:
                str_ = '[POST SCAN OPTIONS]'
                print(str(' ' * int(int(limit_char / 2) - int(len(str_) / 2))) + Style.BRIGHT + Fore.GREEN + str_ + Style.RESET_ALL)
                print('')
                print('1. Display all obfuscated or unrecognized files.')
                print('')
                usr_choice_1 = input('Enter: ')
                print('-' * limit_char)
                if usr_choice_1 == '1':
                    str_ = '[DISPLAYING POTENTIALLY DE-OBFUSCATED FILES]'
                    print(str(' ' * int(int(limit_char / 2) - int(len(str_) / 2))) + Style.BRIGHT + Fore.GREEN + str_ + Style.RESET_ALL)
                    print('')
                    for _ in unrecognized_buffer:
                        print(Style.BRIGHT + Fore.GREEN + '[OBFUSCATED OR UNRECOGNIZED] ' + Style.RESET_ALL + str(_))
                print('')
                print('-'*limit_char)
            str_ = '[COMPLETE]'
            print(str(' ' * int(int(limit_char / 2) - int(len(str_) / 2))) + Style.BRIGHT + Fore.GREEN + str_ + Style.RESET_ALL)
            print('-' * limit_char)
            print('')


def omega_find(target_path='', suffix='', buffer_size=2048, first_pass=True, verbosity=False):
    """ uses database to perform a special search """

    buffer_read_exception_permssion_count_0 = 0
    buffer_read_exception_permssion_count_1 = 0
    buffer_read_exception_count_0 = 0
    buffer_read_exception_count_1 = 0

    dt = str(datetime.datetime.now())
    log_error_file = os.getcwd() + '/log/log_error_omega_find_[' + str(suffix) + ']_' + dt + '.txt'
    log_result_file = os.getcwd() + '/data/log_result_omega_find_[' + str(suffix) + ']_' + dt.replace(':', '') + '.txt'

    # header
    print('\n')
    print('-' * 120)
    print('')
    print(str(' '*54) + Style.BRIGHT + Fore.GREEN + '[OMEGA FIND]' + Style.RESET_ALL)
    print('')
    print('-' * 120)

    # scan criteria
    print('')
    print(str(' '*52) + Style.BRIGHT + Fore.GREEN + '[SCAN CRITERIA]' + Style.RESET_ALL)
    print(Style.BRIGHT + Fore.GREEN + '[LOCATION] ' + Style.RESET_ALL + str(target_path))
    print(Style.BRIGHT + Fore.GREEN + '[FILE TYPE] ' + Style.RESET_ALL + str(suffix))
    print(Style.BRIGHT + Fore.GREEN + '[BUFFER SIZE] ' + Style.RESET_ALL + str(buffer_size))
    print('')
    print('-' * 120)

    # read database
    print('')
    print(str(' ' * 51) + Style.BRIGHT + Fore.GREEN + '[READING DATABASE]' + Style.RESET_ALL)
    known_buffer = []
    if os.path.exists('./db/database_learning.txt'):
        print(Style.BRIGHT + Fore.GREEN + '[DATABASE] ' + Style.RESET_ALL + 'Found')
        with codecs.open('./db/database_learning.txt', 'r', encoding='utf8') as fo:
            for line in fo:
                line = line.strip()
                if line.startswith(suffix):
                    known_buffer.append(line)
                    pr_str = str(Style.BRIGHT + Fore.GREEN + '[FILETYPE BUFFER ASSOCIATIONS] ' + Style.RESET_ALL + str(len(known_buffer)))
                    pyprogress.pr_technical_data(pr_str)
    else:
        print(Style.BRIGHT + Fore.RED + '[DATABASE] ' + Style.RESET_ALL + 'Could not find database.')
    print('')
    print('')
    print('-' * 120)

    # preliminarily scan target location
    if first_pass is True:
        print('')
        print(str(' ' * 47) + Style.BRIGHT + Fore.GREEN + '[SCANNING TARGET LOCATION]' + Style.RESET_ALL)
        f_count = 0
        for dirName, subdirList, fileList in os.walk(target_path):
            for fname in fileList:
                f_count += 1
                pr_str = str(Style.BRIGHT + Fore.GREEN + '[FILES] ' + Style.RESET_ALL + str(f_count))
                pyprogress.pr_technical_data(pr_str)
        print('')
    else:
        print(str(' ' * 43) + Style.BRIGHT + Fore.GREEN + '[SKIPPING SCANNING TARGET LOCATION]' + Style.RESET_ALL)
        print('')
    print('')
    print('-' * 120)
    print('')
    print(str(' ' * 40) + Style.BRIGHT + Fore.GREEN + '[PERFORMING PRIMARY OPERATION] OMEGA FIND' + Style.RESET_ALL)
    print('')
    print(Style.BRIGHT + Fore.GREEN + '[OMEGA FIND]  ' + Style.RESET_ALL + 'Attempting to read each file into memory and compare buffer to known buffers for suffix specified.')
    print(Style.BRIGHT + Fore.GREEN + '[INFORMATION] ' + Style.RESET_ALL + 'Similar files may be included in results. This is normal and expected behaviour.')
    print('')
    f_i = 0
    f_match = []
    f_error = []
    f_all = []
    for dirName, subdirList, fileList in os.walk(target_path):
        for fname in fileList:
            fullpath = os.path.join(dirName, fname)
            f_i += 1

            if verbosity is False and first_pass is True:
                try:
                    pyprogress.progress_bar(part=int(f_i), whole=int(f_count),
                                            pre_append=str(Style.BRIGHT + Fore.GREEN + '[SCANNING] ' + Style.RESET_ALL),
                                            append=str(' ' + str(f_i) + '/' + str(f_count) + Style.BRIGHT + Fore.GREEN + '  [' + str(len(f_match)) + ']' + Fore.RED + ' [' + str(buffer_read_exception_count_1) + ']' + Style.RESET_ALL),
                                            encapsulate_l='|',
                                            encapsulate_r='|',
                                            encapsulate_l_color='RED',
                                            encapsulate_r_color='RED',
                                            progress_char=' ',
                                            bg_color='RED',
                                            factor=50,
                                            multiplier=multiplier)
                except Exception as e:
                    print(e)
            else:
                print('-' * 120)
                print(Style.BRIGHT + Fore.GREEN + '[PROGRESS] ' + Style.RESET_ALL + str(f_i) + ' / ' + str(f_count))
                print(Style.BRIGHT + Fore.GREEN + '[BUFFER MATCHES] ' + Style.RESET_ALL + str(len(f_match)))
                print(Style.BRIGHT + Fore.GREEN + '[PERMISSION ERRORS] ' + Style.RESET_ALL + str(buffer_read_exception_permssion_count_1))
                print(Style.BRIGHT + Fore.GREEN + '[TOTAL ERRORS] ' + Style.RESET_ALL + str(buffer_read_exception_count_1))
                print(Style.BRIGHT + Fore.GREEN + '[READING] ' + Style.RESET_ALL + str(fullpath))

            """ Initiate And Clear Each Iteration """
            b = ''
            b_1 = ''
            b_2 = ''
            key_buff_read = ''
            try:
                """ Allocate buffer size and read the file. """
                if buffer_size == 'full':
                    sz = int(os.path.getsize(fullpath))
                    b_1 = magic.from_buffer(codecs.open(fullpath, "rb").read(sz))
                else:
                    b_1 = magic.from_buffer(codecs.open(fullpath, "rb").read(buffer_size))
                b_1 = str(b_1)
                b_1 = b_1.lower()
                b_1 = b_1.strip()

            except Exception as e:
                if 'permission denied' in str(e).lower():
                    buffer_read_exception_permssion_count_0 += 1
                buffer_read_exception_count_0 += 1
                f_error.append('[ERROR 0] [' + fullpath + '] ' + str(e))
                f_all.append('[ERROR 0] [' + fullpath + '] ' + str(e))
                if verbosity is True:
                    print(fullpath, e)
                # exception_logger(log_file=log_error_file, e=str(e), f=fullpath) # uncomment for verbose logging

                try:
                    """ Allocate buffer size and read the file. """
                    if buffer_size == 'full':
                        sz = int(os.path.getsize(fullpath))
                        b_2 = magic.from_buffer(open(fullpath, "r").read(sz))
                    else:
                        b_2 = magic.from_buffer(open(fullpath, "r").read(buffer_size))
                    b_2 = str(b_2)
                    b_2 = b_2.lower()
                    b_2 = b_2.strip()

                except Exception as e:
                    if 'permission denied' in str(e).lower():
                        buffer_read_exception_permssion_count_1 += 1
                    buffer_read_exception_count_1 += 1
                    f_error.append('[ERROR 1] [' + fullpath + '] ' + str(e))
                    f_all.append('[ERROR 1] [' + fullpath + '] ' + str(e))
                    if verbosity is True:
                        print(fullpath, e)
                    exception_logger(log_file=log_error_file, e=str(e), f=fullpath)
                    break

            """ Use Most Defined Buffer String """
            b_1_len = len(b_1)
            b_2_len = len(b_2)
            if b_1_len >= b_2_len:
                b = b_1
            elif b_2_len > b_1_len:
                b = b_2

            """ Buffer output may yield digits for timestamps, dimensions etc. """
            key_buff_read = str(suffix) + '-buffer-read ' + str(b)
            digi_str = r'[0-9]'
            x_re = re.sub(digi_str, '', key_buff_read)

            """ Iterate Comparing regex x to regex y """
            i = 0
            for _ in known_buffer:
                y_re = re.sub(digi_str, '', _)
                if y_re == x_re:
                    if first_pass is False:
                        print(Style.BRIGHT + Fore.GREEN + '[REGEX BUFFER MATCH] [FILE] ' + Style.RESET_ALL + str(fullpath))
                        print(Style.BRIGHT + Fore.GREEN + '[BUFFER] ' + Style.RESET_ALL + str(x_re))
                    f_match.append(fullpath)
                    f_all.append('[BUFFER MATCH] [' + fullpath + '] ' + str(x_re))
                    logger_omega_find_result(log_file=log_result_file, fullpath=fullpath, buffer=x_re)
                i += 1
    print('')
    print('')
    print('-' * 120)
    print('')
    print(str(' ' * 56) + Style.BRIGHT + Fore.GREEN + '[MENU]')
    print('')
    str_idx = (120 - int(len('[DISPLAY RESULTS]   '))) - int(len(' [OPEN RESULTS FILE]     '))
    print(Style.BRIGHT + Fore.GREEN + ' [OPEN RESULTS FILE] ' + Style.RESET_ALL + '1' + str(' '*str_idx) + Style.BRIGHT + Fore.GREEN + '[DISPLAY RESULTS]   ' + Style.RESET_ALL + '3')
    print(Style.BRIGHT + Fore.GREEN + ' [OPEN ERROR FILE]   ' + Style.RESET_ALL + '2' + str(' '*str_idx) + Style.BRIGHT + Fore.GREEN + '[DISPLAY ERRORS]    ' + Style.RESET_ALL + '4')
    print(Style.BRIGHT + Fore.GREEN + str(' '*(str_idx+int(len(' [OPEN ERROR FILE]    ')))) + '[DISPLAY ALL]       ' + Style.RESET_ALL + '5')
    print('')
    print('-' * 120)
    menu_input = input('[select] ')
    print('-' * 120)
    print('')
    if menu_input == '1':
        if os.path.exists(log_result_file):
            print(str(' ' * 48) + Style.BRIGHT + Fore.GREEN + '[OPENING RESULTS FILE]' + Style.RESET_ALL)
            os.startfile('"' + log_result_file + '"')
        else:
            print(str(' ' * 44) + Style.BRIGHT + Fore.GREEN + '[RESULTS FILE COULD NOT BE FOUND]' + Style.RESET_ALL)
    elif menu_input == '2':
        if os.path.exists(log_error_file):
            print(str(' ' * 50) + Style.BRIGHT + Fore.GREEN + '[OPENING ERROR FILE]' + Style.RESET_ALL)
            os.startfile('"' + log_error_file + '"')
        else:
            print(str(' ' * 47) + Style.BRIGHT + Fore.GREEN + '[ERROR FILE COULD NOT BE FOUND]' + Style.RESET_ALL)
    elif menu_input == '3':
        print(str(' ' * 46) + Style.BRIGHT + Fore.GREEN + '[DISPLAYING BUFFER MATCHES]' + Style.RESET_ALL)
        print('')
        for _ in f_match:
            print(Style.BRIGHT + Fore.GREEN + '[BUFFER MATCH] ' + Style.RESET_ALL + str(_))
    elif menu_input == '4':
        print(str(' ' * 50) + Style.BRIGHT + Fore.GREEN + '[DISPLAYING ERRORS]' + Style.RESET_ALL)
        print('')
        for _ in f_error:
            print(Style.BRIGHT + Fore.GREEN + '[ERROR] ' + Style.RESET_ALL + str(_))
    elif menu_input == '5':
        print(str(' ' * 52) + Style.BRIGHT + Fore.GREEN + '[DISPLAYING ALL]' + Style.RESET_ALL)
        print('')
        for _ in f_all:
            print(Style.BRIGHT + Fore.GREEN + '[OUTPUT] ' + Style.RESET_ALL + str(_))
    print('')
    print('-' * 120)
    print('')


if len(sys.argv) == 2 and sys.argv[1] == '-h':
    print('')
    print('-' * limit_char)
    print('')
    print('OMEGA FIND')
    print('    - Exposes file(s) that may be pretending to be a file type other than the files real file type.')
    print('    - Powerful find feature.')
    print('    - Extensively define filename suffixes.')
    print('    - Written by Benjamin Jack Cullen.')
    print('')
    print('Command line arguments:')
    print('    -scan             Specifies a directory to scan.')
    print('    -learn            Instructs the program to learn from a specified location. Only use trusted locations/files.')
    print('    -define           Attempts to lookup a definition for suffix specified.')
    print('    -find             Specify path. Finds files predicated upon known buffer read associations created by learning.')
    print('                      A special and powerful search feature.')
    print('    --buffer-size     Specify in bytes how much of each file will be read into the buffer.')
    print('                      If using --buffer-size full, then a scan/learning/find operation could take a much longer time.')
    print('                      --buffer-size can be used in combination with -scan, -learn and -find.')
    print('    --first-pass      Used in conjunction with -find.')
    print('                      Allows preliminary enumeration to be used for progress. Adds time to total time to complete while')
    print('                      allowing progress to be displayed.')
    print('    -suffix           Specify suffix. Used in combination with -find.')
    print('    -v                Output verbose. Only recommended when using -define and for development purposes. Else use --first-pass.')
    print('    -h                Displays this help message')
    print('')
    print('    Example: omega_find --first-pass --buffer-size 2048 -find C:\ -suffix mp4')
    print('    Example: omega_find --first-pass --buffer-size 2048 -learn C:\\')
    print('    Example: omega_find --first-pass --buffer-size full -scan C:\\')
    print('    Example: omega_find -v -define jpg')
    print('')
    print('OmegaFind is only as good as its implementation. A working knowledge of filesystems is recommended in order to best')
    print('implement OmegaFind.')
    print('-' * limit_char)
    print('')


if '-v' in sys.argv:
    verbosity = True

if '--buffer-size' in sys.argv:
    idx = sys.argv.index('--buffer-size')
    if sys.argv[idx + 1].isdigit():
        buffer_size = int(sys.argv[idx + 1])
    elif sys.argv[idx + 1] == 'full':
        buffer_size = sys.argv[idx + 1]

if '--first-pass' in sys.argv:
    first_pass = True

if '-define' in sys.argv:
    idx = sys.argv.index('-define')
    suffix = sys.argv[idx+1]

    run_function_0(suffix)

elif '-scan' in sys.argv:
    idx = sys.argv.index('-scan')
    target_path = sys.argv[idx+1]

    if os.path.exists(target_path) and os.path.isdir(target_path) is True:
        cc()
        scan_learn(target_path=target_path, buffer_size=buffer_size, first_pass=first_pass)
    else:
        print('-- invalid path')

elif '-learn' in sys.argv:
    learn = True

    idx = sys.argv.index('-learn')
    target_path = sys.argv[idx+1]

    if os.path.exists(target_path) and os.path.isdir(target_path) is True:
        cc()
        scan_learn(target_path=target_path, buffer_size=buffer_size, first_pass=first_pass)
    else:
        print('-- invalid path')

elif '-find' in sys.argv and '-suffix' in sys.argv:

        idx = sys.argv.index('-find')
        target_path = sys.argv[idx+1]

        idx = sys.argv.index('-suffix')
        suffix = sys.argv[idx+1]

        if os.path.exists(target_path):
            cc()
            omega_find(target_path=target_path, suffix=suffix, buffer_size=buffer_size, first_pass=first_pass, verbosity=verbosity)
        else:
            print('-- invalid path')


Style.RESET_ALL
