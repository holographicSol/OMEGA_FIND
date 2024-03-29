""" Written by Benjamin Jack Cullen aka Holographic_Sol

OmegaFind

Intention 1: To de-obfuscate/expose files that may be pretending to be a file type other than the files real file type.

    Example: secret_file.mp4 has been renamed to anything.anything and buried somewhere in a drive.
        OmegaFind seeks to expose these files for what they really are.
        (A double-edged blade. agent exposes you/you expose an agent)

Intention 2: To scan files not by name or filename suffix matching but by reading each file into memory and comparing
    the buffer to known buffer reads for the suffix specified.

Intention 3: Define. Specify a filename suffix and return a concise/verbose description of the file type specified.

Modes of operation:

    Learn: Provide OmegaFind with a directory path of trusted file(s) to learn from to build OmegaFind's knowledge of
    what file types should look like.

    De-Obfuscate: de-obfuscate a directory and try to ascertain if file(s) are what they claim to be.

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
import ext_module

encode = u'\u5E73\u621015\u200e\U0001d6d1,'
verbosity = False
ei = 0
rf = ()
learn = False
limit_char = 120
total_errors = 0
multiplier = pyprogress.multiplier_from_inverse_factor(factor=20)
multiplier_2 = pyprogress.multiplier_from_inverse_factor(factor=10)


def cc():
    cmd = 'clear'
    if os.name in ('nt', 'dos'):
        cmd = 'cls'
    os.system(cmd)


def divide_chunks(_list=[], _max=int):
    for i in range(0, len(_list), _max):
        yield _list[i:i + _max]


def convert_bytes(num):
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB', 'PB']:
        if num < 1024.0:
            return ("%3.1f %s" % (num, x))
        num /= 1024.0


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


def exception_logger(log_file='', error='', fullpath=''):
    global total_errors
    total_errors += 1

    if not os.path.exists('./log/'):
        os.mkdir('./log/')

    if not os.path.exists(log_file):
        open(log_file, 'w').close()

    log_tm_stamp = str(datetime.datetime.now())
    error = str('[' + log_tm_stamp + '] [error_count ' + str(total_errors) + '] ' + str(error)).strip()
    path_associated = str('[' + log_tm_stamp + '] [error_count ' + str(total_errors) + '] ' + str(fullpath)).strip()
    with codecs.open(log_file, 'a', encoding='utf8') as fo:
        fo.write(path_associated + '\n')
        fo.write(error + '\n')
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


def scan_learn(target_path, buffer_size=2048, filesize_max=int):
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
    dir_now = '/data/' + tm_stamp + '/'
    if not os.path.exists(dir_now):
        os.mkdir(str('./' + dir_now))
    log_report = os.path.join(os.getcwd(), 'log_report.txt')

    """ Check Directory Exists """
    bool_created_tm_stamp_dir = False
    if os.path.exists(str('./' + dir_now)):
        if verbosity is True:
            print(str('-- successfully created new directory: ') + str(dir_now))
        bool_created_tm_stamp_dir = True
    else:
        if verbosity is True:
            print(str('-- failed to create new timestamped directory: ') + str(dir_now))

    if bool_created_tm_stamp_dir is True:
        ef = os.path.join(os.getcwd(), 'log_exception.txt')
        log_file_failed_inspection = os.getcwd() + dir_now + 'log_file_unrecognized.txt'
        log_file_passed_inspection = os.getcwd() + dir_now + 'log_file_recognized.txt'
        log_file_permission_denied = os.getcwd() + dir_now + 'log_file_permission_denied.txt'
        log_file_empty_buffer_read = os.getcwd() + dir_now + 'log_file_empty_buffer_read.txt'
        if verbosity is True:
            print(str('-- creating new file name value: ') + str(log_file_failed_inspection))
            print(str('-- creating new file name value: ') + str(ef))
        print('')
        print('-' * limit_char)

        # Header
        if learn is True:
            str_ = Style.BRIGHT + Fore.CYAN + '[OMEGA FIND] LEARNING MODE' + Style.RESET_ALL
            print(str(' ' * int(int(limit_char / 2) - int(len(str_) / 2))) + Style.BRIGHT + Fore.GREEN + str_ + Style.RESET_ALL)
            print('-' * limit_char)
            str_ = Style.BRIGHT + Fore.CYAN + ' [LEARNING CRITERIA]' + Style.RESET_ALL
            print(str(' ' * int(int(limit_char / 2) - int(len(str_) / 2))) + Style.BRIGHT + Fore.CYAN + str_ + Style.RESET_ALL)
        elif learn is False:
            str_ = Style.BRIGHT + Fore.RED + '[OMEGA FIND] DE-OBFUSCATION MODE' + Style.RESET_ALL
            print(str(' ' * int(int(limit_char / 2) - int(len(str_) / 2))) + str_)
            print('-' * limit_char)
            str_ = Style.BRIGHT + Fore.RED + ' [DE-OBFUSCATION CRITERIA]' + Style.RESET_ALL
            print(str(' ' * int(int(limit_char / 2) - int(len(str_) / 2))) + str_)
        print('')

        if learn is True:
            print(Style.BRIGHT + Fore.GREEN + '[LEARNING] ' + Fore.CYAN + str(learn) + Style.RESET_ALL)
        else:
            print(Style.BRIGHT + Fore.GREEN + '[LEARNING] ' + Fore.RED + str(learn) + Style.RESET_ALL)
        print(Style.BRIGHT + Fore.GREEN + '[BUFFER SIZE] ' + Style.RESET_ALL + str(buffer_size))
        print(Style.BRIGHT + Fore.GREEN + '[SPECIFIED LOCATION] ' + Style.RESET_ALL + str(target_path))

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
        print('')

        # preliminarily scan target location
        f_count = 0
        f_item = []
        f_total_size = 0
        f_size_max = 0
        skip_f_size_max = 0
        skip_file = 0
        for dirName, subdirList, fileList in os.walk(target_path):
            for fname in fileList:
                try:
                    fullpath = os.path.join(dirName, fname)
                    f_size = os.path.getsize(fullpath)

                    # check for f_size
                    if str(f_size).isdigit():

                        # limit file size max in bytes
                        if str(filesize_max).isdigit():
                            if int(f_size) <= int(filesize_max):
                                f_item.append([str(fullpath), str(f_size)])
                                f_total_size = int(f_total_size + f_size)
                                if int(f_size) > int(f_size_max):
                                    f_size_max = int(f_size)
                                f_count += 1
                            else:
                                if int(f_size) > int(skip_f_size_max):
                                    skip_f_size_max = int(f_size)

                        # file size max unlimited
                        else:
                            f_item.append([str(fullpath), str(f_size)])
                            f_total_size = int(f_total_size + f_size)
                            if int(f_size) > int(f_size_max):
                                f_size_max = int(f_size)
                            f_count += 1

                except Exception as e:
                    skip_file += 1
                    exception_logger(log_file=ef, error=e, fullpath=fullpath)
                pr_str = str(Style.BRIGHT + Fore.GREEN + '[FILES] ' + Style.RESET_ALL + str(f_count) + Style.BRIGHT + Fore.RED + ' [skipping:' + str(skip_file) + ']' + Style.RESET_ALL)
                pyprogress.pr_technical_data(pr_str)
        print('')
        human_f_total_size = str(convert_bytes(int(f_total_size))).replace(' ', '')
        print(Style.BRIGHT + Fore.GREEN + '[TOTAL SIZE] ' + Style.RESET_ALL + human_f_total_size)
        if str(filesize_max).isdigit():
            print(Style.BRIGHT + Fore.GREEN + '[FILESIZE MAX LIMIT] ' + Style.RESET_ALL + str(
                convert_bytes(int(filesize_max))))
        else:
            print(Style.BRIGHT + Fore.GREEN + '[FILESIZE MAX LIMIT] ' + Style.RESET_ALL + str(filesize_max))
        print(Style.BRIGHT + Fore.GREEN + '[LARGEST FILE SIZE] ' + Style.RESET_ALL + str(
            convert_bytes(int(f_size_max))) + Style.BRIGHT + Fore.RED + ' [largest-skipped-file:' + str(
            convert_bytes(int(skip_f_size_max))) + ']')
        print('')
        print(Style.BRIGHT + Fore.RED + '[WARNING] ' + Style.RESET_ALL + 'Each file will be allocated space in memory according to buffer size.')
        print('          If buffer size set to full, the whole file will be read into memory.')
        print('          Please ensure there is sufficient RAM/DISK-OVERFLOW/other-solution in place before continuing!')
        print('          The largest file found was ' + str(convert_bytes(int(f_size_max))) + '.')
        print('')
        print('-' * 120)

        """ Set Counters """
        buffer_read_exception_count_0 = 0
        buffer_read_exception_count_1 = 0
        buffer_read_exception_permssion_count_0 = 0
        buffer_read_exception_permssion_count_1 = 0
        total_files_encountered = 0

        error_getting_suffix_count = 0
        bool_buffer_data_true_count = 0
        bool_buffer_data_false_count = 0

        new_learned = []
        unrecognized_buffer = []
        progress_bar_color = 'CYAN'
        pre_append_mode = str(Style.BRIGHT + Fore.CYAN + str('[LEARNING] ') + Style.RESET_ALL)

        learn_count = 0
        buffer_failed_count = 0
        buffer_passed_count = 0
        buffer_passed_inspection_count = 0

        if learn is True:
            usr_choice = input('Press Y to learn or press any other key to abort [Enter] : ')
        elif learn is False:
            usr_choice = input('Press Y to attempt de-obfuscation or press any other key to abort [Enter] : ')

        """ Continue If Compiled Database Lists Are Aligned """
        bool_abort = False
        if usr_choice.lower() == 'y':
            if learn is True:
                print('-' * limit_char)
                str_ = Style.BRIGHT + Fore.CYAN + '[OMEGA FIND] LEARNING' + Style.RESET_ALL
                print(str(' ' * int(
                    int(limit_char / 2) - int(len(str_) / 2))) + Style.BRIGHT + Fore.GREEN + str_ + Style.RESET_ALL)
            elif learn is False:
                print('-' * limit_char)
                str_ = Style.BRIGHT + Fore.RED + '[OMEGA FIND] DE-OBFUSCATING' + Style.RESET_ALL
                print(str(' ' * int(
                    int(limit_char / 2) - int(len(str_) / 2))) + Style.BRIGHT + Fore.GREEN + str_ + Style.RESET_ALL)
                progress_bar_color = 'RED'
                pre_append_mode = str(Style.BRIGHT + Fore.RED + str('[DE-OBFUSCATING] ') + Style.RESET_ALL)

            print('')

            digi_str = r'[0-9]'
            count_f_size = 0

            """ Iterate files """
            for _ in f_item:
                if os.path.exists(_[0]):
                    total_files_encountered += 1
                    f = _[0].strip()
                    count_f_size = int(int(count_f_size) + int(_[1]))

                    """ Get File Name Suffix """
                    fe = pathlib.Path(f).suffix
                    fe = fe.replace('.', '').lower()

                    """ Check If Suffix In Databases """
                    if fe == '':
                        fe = 'no_file_extension'

                    if verbosity is True:
                        print(Style.BRIGHT + Fore.GREEN + '[ALLEGED SUFFIX] ' + Style.RESET_ALL + str(fe))

                    b = ''
                    key_buff_read = ''
                    buffer_permission_denied_attempt_1 = False
                    buffer_permission_denied_attempt_2 = False
                    try:
                        """ Allocate buffer size and read the file. """

                        if str(buffer_size) == 'full':

                            sz = int(os.path.getsize(f))
                            b = magic.from_buffer(codecs.open(f, "rb").read(int(sz)))
                            b = str(b).lower().strip()

                        elif str(buffer_size).isdigit():
                            b = magic.from_buffer(codecs.open(f, "rb").read(buffer_size))
                            b = str(b).lower().strip()

                    except Exception as e:
                        if 'permission denied' in str(e).lower():
                            buffer_read_exception_permssion_count_0 += 1
                            buffer_permission_denied_attempt_1 = True
                        buffer_read_exception_count_0 += 1
                        try:

                            if str(buffer_size) == 'full':
                                sz = int(os.path.getsize(f))
                                b = magic.from_buffer(open(f, "r").read(int(sz)))
                                b = str(b).lower().strip()

                            elif str(buffer_size).isdigit():
                                b = magic.from_buffer(open(f, "r").read(buffer_size))
                                b = str(b).lower().strip()

                        except Exception as e:
                            if 'permission denied' in str(e).lower():
                                buffer_read_exception_permssion_count_1 += 1
                                buffer_permission_denied_attempt_2 = True
                            buffer_read_exception_count_1 += 1
                            e_str = '[error reading buffer (second try)] ' + str(e)
                            exception_logger(log_file=ef, error=e_str, fullpath=f)

                    if verbosity is True:
                        print(Style.BRIGHT + Fore.GREEN + '[BUFFER READ] ' + Style.RESET_ALL + str(b))

                    """ Continue If Buffer String & Set Default Boolean """
                    bool_learn = False
                    buffer_passed_inspection = False
                    bool_data_buffer = False

                    if b:
                        key_buff_read = str(fe) + '-buffer-read ' + str(b)
                        bool_buffer_data_true_count += 1
                        bool_data_buffer = True

                        """ Buffer output may yield digits for timestamps, dimensions etc. """
                        x_re = re.sub(digi_str, '', key_buff_read)

                        """ Iterate Comparing regex x to regex y """
                        i = 0
                        for learning_brs in learning_br:
                            y_re = re.sub(digi_str, '', learning_br[i])
                            if y_re == x_re:
                                if verbosity is True:
                                    print(Style.BRIGHT + Fore.GREEN + '[REGEX BUFFER MATCH] ' + Style.RESET_ALL + str(x_re))
                                buffer_passed_inspection = True
                                buffer_passed_inspection_count += 1
                                break
                            i += 1

                        if buffer_passed_inspection is True:
                            buffer_passed_count += 1
                            bool_learn = False
                            if verbosity is True:
                                if learn is True:
                                    print(Style.BRIGHT + Fore.GREEN + '[LEARNED COUNTER] ' + Style.RESET_ALL + str(learn_count))
                                    print(Style.BRIGHT + Fore.GREEN + '[LEARNED] ' + Style.RESET_ALL + str(bool_learn))
                        elif buffer_passed_inspection is False:
                            unrecognized_buffer.append(f)
                            buffer_failed_count += 1
                            if learn is True:
                                if verbosity is True:
                                    print(Style.BRIGHT + Fore.GREEN + '[LEARNED COUNTER] ' + Style.RESET_ALL + str(learn_count))
                                if key_buff_read not in new_learned:
                                    new_learned.append(key_buff_read)
                                    learn_count += 1
                                    bool_learn = True
                                    if verbosity is True:
                                        print(Style.BRIGHT + Fore.GREEN + '[LEARNED] ' + Style.RESET_ALL + str(bool_learn))
                                    with codecs.open(learn_database, 'a', encoding='utf8') as fo:
                                        to_file = key_buff_read
                                        fo.write(to_file + '\n')
                                else:
                                    bool_learn = False
                                    if verbosity is True:
                                        print(Style.BRIGHT + Fore.GREEN + '[LEARNED] ' + Style.RESET_ALL + str(bool_learn))
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
                            print(Style.BRIGHT + Fore.GREEN + '[BUFFER RECOGNIZED IN RELATION TO ALLEGED SUFFIX] ' + Style.BRIGHT + str(buffer_passed_inspection))
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
                        fo.write(to_file_11 + '\n')
                        fo.write(to_file_12 + '\n')
                        fo.write(to_file_15 + '\n')
                        fo.write(''+'\n')
                    fo.close()

                    if verbosity is True:
                        print('')
                        print('-' * limit_char)
                        print('')
                        if learn is True:
                            print(Style.BRIGHT + Fore.GREEN + '[OMEGA FIND] ' + Style.RESET_ALL + 'Learning')
                        elif learn is False:
                            print(Style.BRIGHT + Fore.GREEN + '[OMEGA FIND] ' + Style.RESET_ALL + 'Attempting de-obfuscation')
                        print(Style.BRIGHT+Fore.GREEN+'[FILES ENCOUNTERED] ' + Style.RESET_ALL + str(total_files_encountered))
                        print(Style.BRIGHT+Fore.GREEN+'[TIME NOW] ' + Style.RESET_ALL + str(datetime.datetime.now()))
                        print(Style.BRIGHT+Fore.GREEN+'[PATH] ' + Style.RESET_ALL + str(f))
                    else:
                        if learn is True:
                            append_str_ = str(' [' + str(total_files_encountered) + '/' + str(f_count) + '] ' + Style.BRIGHT + Fore.GREEN + '[' + str(learn_count) + ']' + Fore.RED + ' [' + str(buffer_read_exception_count_1) + ']' + Style.RESET_ALL)
                        else:
                            append_str_ = str(' [' + str(total_files_encountered) + '/' + str(f_count) + '] ' + Style.BRIGHT + Fore.GREEN + '[' + str(buffer_passed_inspection_count) + ']' + Fore.RED + ' [' + str(buffer_failed_count) + ']' + Style.RESET_ALL)
                        try:
                            human_count_f_size = str(convert_bytes(int(count_f_size))).strip()
                            pyprogress.progress_bar(n_progress_bar=2,
                                                    n_progress_space_char='  ',
                                                    part=int(total_files_encountered), whole=int(f_count),
                                                    pre_append=str(pre_append_mode),
                                                    append=str(append_str_),
                                                    encapsulate_l='|',
                                                    encapsulate_r='|',
                                                    encapsulate_l_color=progress_bar_color,
                                                    encapsulate_r_color=progress_bar_color,
                                                    progress_char=' ',
                                                    bg_color=progress_bar_color,
                                                    factor=20,
                                                    multiplier=multiplier,
                                                    part_2=int(count_f_size), whole_2=int(f_total_size),
                                                    pre_append_2=str('[BYTES] '),
                                                    append_2=str(' ' + human_count_f_size),
                                                    encapsulate_l_2='|',
                                                    encapsulate_r_2='|',
                                                    encapsulate_l_color_2='GREEN',
                                                    encapsulate_r_color_2='GREEN',
                                                    progress_char_2=' ',
                                                    bg_color_2='GREEN',
                                                    factor_2=10,
                                                    multiplier_2=multiplier_2
                                                    )
                        except Exception as e:
                            print(e)
                else:
                    f_count -= 1
                    f_total_size -= int(_[1])

            print('\n')
            print('-'*limit_char)

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
            fo_report.close()
            if learn is True:
                str_ = Style.BRIGHT + Fore.CYAN + '[LEARNING RESULTS]' + Style.RESET_ALL
                print(str(' ' * int(
                    int(limit_char / 2) - int(len(str_) / 2))) + str_)
            elif learn is False:
                str_ = Style.BRIGHT + Fore.RED + '[SCAN RESULTS]' + Style.RESET_ALL
                print(str(' ' * int(
                    int(limit_char / 2) - int(len(str_) / 2))) + str_)
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
            print('')
            str_ = Style.BRIGHT + Fore.GREEN + '[MENU]' + Style.RESET_ALL
            print(str(' ' * int(int(limit_char / 2) - int(len(str_) / 2))) + str_)
            print('')
            print(Style.BRIGHT + Fore.GREEN + '[1] [OPEN RESULTS FILE]' + Style.RESET_ALL)
            print(Style.BRIGHT + Fore.GREEN + '[2] [OPEN ERROR FILE]' + Style.RESET_ALL)
            print('')
            print('-' * 120)
            menu_input = input('[select] ')
            print('-' * 120)

            if learn is False:
                if menu_input == '1':
                    if os.path.exists(log_file_failed_inspection):

                        str_ = Style.BRIGHT + Fore.GREEN + '[OPENING RESULTS FILE]' + Style.RESET_ALL
                        print(str(' ' * int(int(limit_char / 2) - int(len(str_) / 2))) + str_)
                        print('-' * 120)
                        os.startfile('"' + log_file_failed_inspection + '"')

                    else:
                        str_ = Style.BRIGHT + Fore.CYAN + '[RESULTS FILE COULD NOT BE FOUND]' + Style.RESET_ALL
                        print('-' * 120)
                        print(str(' ' * int(int(limit_char / 2) - int(len(str_) / 2))) + str_)

                elif menu_input == '2':
                    if os.path.exists(ef):
                        str_ = Style.BRIGHT + Fore.CYAN + '[OPENING ERROR FILE]' + Style.RESET_ALL
                        print('-' * 120)
                        print(str(' ' * int(int(limit_char / 2) - int(len(str_) / 2))) + str_)
                        os.startfile('"' + ef + '"')
                    else:
                        str_ = Style.BRIGHT + Fore.CYAN + '[ERROR FILE COULD NOT BE FOUND]' + Style.RESET_ALL
                        print('-' * 120)
                        print(str(' ' * int(int(limit_char / 2) - int(len(str_) / 2))) + str_)

        else:
            bool_abort = True
            if learn is True:
                str_ = Style.BRIGHT + Fore.CYAN + '[ABORTING]' + Style.RESET_ALL
            elif learn is False:
                str_ = Style.BRIGHT + Fore.RED + '[ABORTING]' + Style.RESET_ALL
            print(str(' ' * int(int(limit_char / 2) - int(len(str_) / 2))) + str_)

        if bool_abort is False:
            str_ = Style.BRIGHT + Fore.GREEN + '[COMPLETE]' + Style.RESET_ALL
            print(str(' ' * int(int(limit_char / 2) - int(len(str_) / 2))) + str_)
        print('-' * 120)
        print('')


def omega_find(target_path='', suffix='', buffer_size=2048, verbosity=False, filesize_max=False):
    """ uses database to perform a special search """

    buffer_read_exception_permssion_count_0 = 0
    buffer_read_exception_permssion_count_1 = 0
    buffer_read_exception_count_0 = 0
    buffer_read_exception_count_1 = 0

    dt = str(datetime.datetime.now())
    dt_str = dt.replace(':', '-')
    log_error_file = os.getcwd() + '/log/log_error_omega_find_[results]_' + dt_str + '.txt'
    log_result_file = os.getcwd() + '/data/log_result_omega_find_[results]_' + dt_str + '.txt'

    # header
    print('\n')
    print('-' * 120)
    str_ = Style.BRIGHT + Fore.RED + '[OMEGA FIND] SCAN MODE' + Style.RESET_ALL
    print(str(' ' * int(int(limit_char / 2) - int(len(str_) / 2))) + Style.BRIGHT + Fore.GREEN + str_ + Style.RESET_ALL)
    print('-' * 120)

    chunk_suffix = list(divide_chunks(_list=suffix, _max=12))

    # scan criteria
    str_ = Style.BRIGHT + Fore.RED + '[SCAN CRITERIA]' + Style.RESET_ALL
    print(str(' ' * int(int(limit_char / 2) - int(len(str_) / 2))) + Style.BRIGHT + Fore.GREEN + str_ + Style.RESET_ALL)
    if learn is True:
        print(Style.BRIGHT + Fore.GREEN + '[LEARNING] ' + Fore.CYAN + str(buffer_size) + Style.RESET_ALL)
    else:
        print(Style.BRIGHT + Fore.GREEN + '[LEARNING] ' + Fore.RED + str(buffer_size) + Style.RESET_ALL)

    print(Style.BRIGHT + Fore.GREEN + '[BUFFER SIZE] ' + Style.RESET_ALL + str(buffer_size))
    print(Style.BRIGHT + Fore.GREEN + '[SPECIFIED LOCATION] ' + Style.RESET_ALL + str(target_path))

    # read database
    known_buffer = []
    if os.path.exists('./db/database_learning.txt'):
        print(Style.BRIGHT + Fore.GREEN + '[DATABASE] ' + Style.RESET_ALL + 'Found')
        with codecs.open('./db/database_learning.txt', 'r', encoding='utf8') as fo:
            for line in fo:
                line = line.strip()
                if line.startswith(tuple(suffix)):
                    known_buffer.append(line)
                    pr_str = str(Style.BRIGHT + Fore.GREEN + '[LEARNED DEFINITIONS (for specified suffix(s))] ' + Style.RESET_ALL + str(len(known_buffer)))
                    pyprogress.pr_technical_data(pr_str)
    else:
        print(Style.BRIGHT + Fore.RED + '[DATABASE] ' + Style.RESET_ALL + 'Could not scan database.')
    print('\n')
    print(Style.BRIGHT + Fore.GREEN + '[FILE TYPE] ' + Style.RESET_ALL + str(chunk_suffix[0]))
    i = 0
    for _ in chunk_suffix:
        if i != 0:
            print('            ' + str(_))
        i += 1
    print('\n')

    # preliminarily scan target location
    f_count = 0
    f_item = []
    f_total_size = 0
    f_size_max = 0
    skip_f_size_max = 0
    skip_file = 0
    for dirName, subdirList, fileList in os.walk(target_path):
        for fname in fileList:
            try:
                fullpath = os.path.join(dirName, fname)
                f_size = os.path.getsize(fullpath)

                # check for f_size
                if str(f_size).isdigit():

                    # limit file size max in bytes
                    if str(filesize_max).isdigit():
                        if int(f_size) <= int(filesize_max):
                            f_item.append([str(fullpath), str(f_size)])
                            f_total_size = int(f_total_size + f_size)
                            if int(f_size) > int(f_size_max):
                                f_size_max = int(f_size)
                            f_count += 1
                        else:
                            if int(f_size) > int(skip_f_size_max):
                                skip_f_size_max = int(f_size)

                    # file size max unlimited
                    else:
                        f_item.append([str(fullpath), str(f_size)])
                        f_total_size = int(f_total_size + f_size)
                        if int(f_size) > int(f_size_max):
                            f_size_max = int(f_size)
                        f_count += 1

            except Exception as e:
                skip_file += 1
                exception_logger(log_file=log_error_file, error=e, fullpath=fullpath)
            pr_str = str(Style.BRIGHT + Fore.GREEN + '[FILES] ' + Style.RESET_ALL + str(f_count) + Style.BRIGHT + Fore.RED + ' [skipping:' + str(skip_file) + ']' + Style.RESET_ALL)
            pyprogress.pr_technical_data(pr_str)
    print('')
    human_f_total_size = str(convert_bytes(int(f_total_size))).replace(' ', '')
    print(Style.BRIGHT + Fore.GREEN + '[TOTAL SIZE] ' + Style.RESET_ALL + human_f_total_size)
    if str(filesize_max).isdigit():
        print(Style.BRIGHT + Fore.GREEN + '[FILESIZE MAX LIMIT] ' + Style.RESET_ALL + str(
            convert_bytes(int(filesize_max))))
    else:
        print(Style.BRIGHT + Fore.GREEN + '[FILESIZE MAX LIMIT] ' + Style.RESET_ALL + str(filesize_max))
    print(Style.BRIGHT + Fore.GREEN + '[LARGEST FILE SIZE] ' + Style.RESET_ALL + str(
        convert_bytes(int(f_size_max))) + Style.BRIGHT + Fore.RED + ' [largest-skipped-file:' + str(
        convert_bytes(int(skip_f_size_max))) + ']')
    print('')
    print(Style.BRIGHT + Fore.RED + '[WARNING] ' + Style.RESET_ALL + 'Each file will be allocated space in memory according to buffer size.')
    print('          If buffer size set to full, the whole file will be read into memory.')
    print('          Please ensure there is sufficient RAM/DISK-OVERFLOW/other-solution in place before continuing!')
    print('          The largest file found was ' + str(convert_bytes(int(f_size_max))) + '.')
    print('')
    print('-' * 120)

    usr_choice = input('Press Y to perform advanced scan operation or press any other key to abort [Enter] : ')
    bool_abort = False
    if usr_choice == 'y' or usr_choice == 'Y':
        print('-' * 120)
        str_ = Style.BRIGHT + Fore.RED + '[PERFORMING PRIMARY OPERATION] OMEGA SCAN' + Style.RESET_ALL
        print(str(' ' * int(int(limit_char / 2) - int(len(str_) / 2))) + Style.BRIGHT + str_)
        print('')
        print(Style.BRIGHT + Fore.GREEN + '[OMEGA FIND]  ' + Style.RESET_ALL + 'Attempting to read each file into memory and compare buffer to known buffers for suffix specified.')
        print(Style.BRIGHT + Fore.GREEN + '[INFORMATION] ' + Style.RESET_ALL + 'Similar files may be included in results. This is normal and expected behaviour.')
        print('')
        f_i = 0
        f_match = []
        f_error = []
        f_all = []
        digi_str = r'[0-9]'
        count_f_size = 0

        """ Iterate files """
        for _ in f_item:
            if os.path.exists(_[0]):
                f_i += 1
                fullpath = _[0].strip()
                count_f_size = int(int(count_f_size) + int(_[1]))

                """ Initiate And Clear Each Iteration """
                b = ''
                key_buff_read = ''
                try:
                    """ Allocate buffer size and read the file. """
                    if str(buffer_size) == 'full':
                        sz = int(os.path.getsize(fullpath))
                        b = magic.from_buffer(codecs.open(fullpath, "rb").read(int(sz)))
                        b = str(b).lower().strip()
                    elif str(buffer_size).isdigit():
                        b = str(magic.from_buffer(codecs.open(fullpath, "rb").read(buffer_size))).lower().strip()

                except Exception as e:
                    if 'permission denied' in str(e).lower():
                        buffer_read_exception_permssion_count_0 += 1
                    buffer_read_exception_count_0 += 1
                    f_error.append('[ERROR 0] [' + fullpath + '] ' + str(e))
                    f_all.append('[ERROR 0] [' + fullpath + '] ' + str(e))
                    if verbosity is True:
                        print(fullpath, e)
                    try:
                        """ Allocate buffer size and read the file. """
                        if str(buffer_size) == 'full':
                            sz = int(os.path.getsize(fullpath))
                            b = magic.from_buffer(open(fullpath, "r").read(int(sz)))
                            b = str(b).lower().strip()
                        elif str(buffer_size).isdigit():
                            b = str(magic.from_buffer(open(fullpath, "r").read(buffer_size))).lower().strip()

                    except Exception as e:
                        if 'permission denied' in str(e).lower():
                            buffer_read_exception_permssion_count_1 += 1
                        buffer_read_exception_count_1 += 1
                        f_error.append('[ERROR 1] [' + fullpath + '] ' + str(e))
                        f_all.append('[ERROR 1] [' + fullpath + '] ' + str(e))
                        if verbosity is True:
                            print(fullpath, e)
                        exception_logger(log_file=log_error_file, error=e, fullpath=fullpath)

                if b:

                    """ Buffer output may yield digits for timestamps, dimensions etc. """
                    i_suffix = 0
                    for suffixs in suffix:
                        key_buff_read = str(suffix[i_suffix]) + '-buffer-read ' + str(b)
                        x_re = re.sub(digi_str, '', key_buff_read)

                        """ Iterate Comparing regex x to regex y """
                        i = 0
                        for _ in known_buffer:
                            y_re = re.sub(digi_str, '', _)
                            if y_re == x_re:
                                if verbosity is True:
                                    print(Style.BRIGHT + Fore.GREEN + '[REGEX BUFFER MATCH] [FILE] ' + Style.RESET_ALL + str(fullpath))
                                    print(Style.BRIGHT + Fore.GREEN + '[BUFFER] ' + Style.RESET_ALL + str(x_re))
                                f_match.append(fullpath)
                                f_all.append('[BUFFER MATCH] [' + fullpath + '] ' + str(x_re))
                                logger_omega_find_result(log_file=log_result_file, fullpath=fullpath, buffer=x_re)
                                break
                            i += 1
                        i_suffix += 1

                    if verbosity is False:
                        try:
                            pyprogress.progress_bar(n_progress_bar=2,
                                                    n_progress_space_char='  ',
                                                    part=int(f_i), whole=int(f_count),
                                                    pre_append=str(Style.BRIGHT + Fore.RED + '[SCANNING] ' + Style.RESET_ALL),
                                                    append=str(' ' + str(f_i) + '/' + str(f_count) + Style.BRIGHT + Fore.GREEN + '  [' + str(len(f_match)) + ']' + Fore.RED + ' [' + str(buffer_read_exception_count_1) + ']' + Style.RESET_ALL),
                                                    encapsulate_l='|',
                                                    encapsulate_r='|',
                                                    encapsulate_l_color='RED',
                                                    encapsulate_r_color='RED',
                                                    progress_char=' ',
                                                    bg_color='RED',
                                                    factor=20,
                                                    multiplier=multiplier,
                                                    part_2=int(count_f_size), whole_2=int(f_total_size),
                                                    pre_append_2=str('[BYTES] '),
                                                    append_2=str(' [' + str(convert_bytes(int(count_f_size))).replace(' ','') + '/' + str(human_f_total_size).replace(' ', '') + ']'),
                                                    encapsulate_l_2='|',
                                                    encapsulate_r_2='|',
                                                    encapsulate_l_color_2='GREEN',
                                                    encapsulate_r_color_2='GREEN',
                                                    progress_char_2=' ',
                                                    bg_color_2='GREEN',
                                                    factor_2=10,
                                                    multiplier_2=multiplier_2
                                                    )
                        except Exception as e:
                            print(e)

                    else:
                        print('-' * 120)
                        print(Style.BRIGHT + Fore.GREEN + '[PROGRESS] ' + Style.RESET_ALL + str(f_i) + ' / ' + str(f_count))
                        print(Style.BRIGHT + Fore.GREEN + '[BUFFER MATCHES] ' + Style.RESET_ALL + str(len(f_match)))
                        print(Style.BRIGHT + Fore.GREEN + '[PERMISSION ERRORS] ' + Style.RESET_ALL + str(buffer_read_exception_permssion_count_1))
                        print(Style.BRIGHT + Fore.GREEN + '[TOTAL ERRORS] ' + Style.RESET_ALL + str(buffer_read_exception_count_1))
                        print(Style.BRIGHT + Fore.GREEN + '[READING] ' + Style.RESET_ALL + str(fullpath))
            else:
                f_count -= 1
                f_total_size -= int(_[1])
        print('')
        print('')
        print('-' * 120)
        str_ = Style.BRIGHT + Fore.GREEN + '[MENU]' + Style.RESET_ALL
        print(str(' ' * int(int(limit_char / 2) - int(len(str_) / 2))) + str_)
        print('')
        str_idx = (120 - int(len('[DISPLAY RESULTS]   '))) - int(len(' [OPEN RESULTS FILE]     '))
        print(Style.BRIGHT + Fore.GREEN + ' [OPEN RESULTS FILE] ' + Style.RESET_ALL + '1' + str(' '*str_idx) + Style.BRIGHT + Fore.GREEN + '[DISPLAY RESULTS]   ' + Style.RESET_ALL + '3')
        print(Style.BRIGHT + Fore.GREEN + ' [OPEN ERROR FILE]   ' + Style.RESET_ALL + '2' + str(' '*str_idx) + Style.BRIGHT + Fore.GREEN + '[DISPLAY ERRORS]    ' + Style.RESET_ALL + '4')
        print(Style.BRIGHT + Fore.GREEN + str(' '*(str_idx+int(len(' [OPEN ERROR FILE]    ')))) + '[DISPLAY ALL]       ' + Style.RESET_ALL + '5')
        print('')
        print('-' * 120)
        menu_input = input('[select] ')
        print('-' * 120)
        if menu_input == '1':
            if os.path.exists(log_result_file):
                str_ = Style.BRIGHT + Fore.GREEN + '[OPENING RESULTS FILE]' + Style.RESET_ALL
                print(str(' ' * int(int(limit_char / 2) - int(len(str_) / 2))) + str_)
                print('-' * 120)
                os.startfile('"' + log_result_file + '"')
            else:
                str_ = Style.BRIGHT + Fore.GREEN + '[RESULTS FILE COULD NOT BE FOUND]' + Style.RESET_ALL
                print(str(' ' * int(int(limit_char / 2) - int(len(str_) / 2))) + str_)
                print('-' * 120)
        elif menu_input == '2':
            if os.path.exists(log_error_file):
                str_ = Style.BRIGHT + Fore.GREEN + '[OPENING ERROR FILE]' + Style.RESET_ALL
                print(str(' ' * int(int(limit_char / 2) - int(len(str_) / 2))) + str_)
                print('-' * 120)
                os.startfile('"' + log_error_file + '"')
            else:
                str_ = Style.BRIGHT + Fore.GREEN + '[ERROR FILE COULD NOT BE FOUND]' + Style.RESET_ALL
                print(str(' ' * int(int(limit_char / 2) - int(len(str_) / 2))) + str_)
                print('-' * 120)
        elif menu_input == '3':
            str_ = Style.BRIGHT + Fore.GREEN + '[DISPLAYING BUFFER MATCHES]' + Style.RESET_ALL
            print(str(' ' * int(int(limit_char / 2) - int(len(str_) / 2))) + str_)
            print('')
            for _ in f_match:
                str_ = Style.BRIGHT + Fore.GREEN + '[BUFFER MATCH]' + Style.RESET_ALL
                print(str(' ' * int(int(limit_char / 2) - int(len(str_) / 2))) + str_)
        elif menu_input == '4':
            str_ = Style.BRIGHT + Fore.GREEN + '[DISPLAYING ERRORS]' + Style.RESET_ALL
            print(str(' ' * int(int(limit_char / 2) - int(len(str_) / 2))) + str_)
            print('')
            for _ in f_error:
                str_ = Style.BRIGHT + Fore.GREEN + '[ERROR]' + Style.RESET_ALL
                print(str(' ' * int(int(limit_char / 2) - int(len(str_) / 2))) + str_)
        elif menu_input == '5':
            str_ = Style.BRIGHT + Fore.GREEN + '[DISPLAYING ALL]' + Style.RESET_ALL
            print(str(' ' * int(int(limit_char / 2) - int(len(str_) / 2))) + str_)
            print('')
            for _ in f_all:
                print(Style.BRIGHT + Fore.GREEN + '[OUTPUT] ' + Style.RESET_ALL + str(_))
    else:
        bool_abort = True
        if learn is True:
            str_ = Style.BRIGHT + Fore.CYAN + '[ABORTING]' + Style.RESET_ALL

        elif learn is False:
            str_ = Style.BRIGHT + Fore.RED + '[ABORTING]' + Style.RESET_ALL
        print(str(' ' * int(int(limit_char / 2) - int(len(str_) / 2))) + str_)

    if bool_abort is False:
        str_ = Style.BRIGHT + Fore.GREEN + '[COMPLETE]' + Style.RESET_ALL
        print(str(' ' * int(int(limit_char / 2) - int(len(str_) / 2))) + str_)
    print('-' * 120)
    print('')


if len(sys.argv) == 2 and sys.argv[1] == '-h':
    print('')
    print('-' * limit_char)
    print('')
    print('OMEGA FIND')
    print('    - Exposes file(s) that may be pretending to be a file type other than the files real file type.')
    print('    - Powerful scan feature.')
    print('    - Extensively define filename suffixes.')
    print('    - Written by Benjamin Jack Cullen.')
    print('')
    print('Command line arguments:')
    print('    --de-obfuscate           Specifies a directory to attempt file de-obfuscation.')
    print('    -learn                   Instructs the program to learn from a specified location. Only use trusted locations/files.')
    print('    -define                  Attempts to lookup a definition for suffix specified.')
    print('    -scan                    Specify path. Finds files predicated upon known buffer read associations created by learning.')
    print('                             A special and powerful search feature.')
    print('    --buffer-size            Specify in bytes how much of each file will be read into the buffer.')
    print('                             If using --buffer-size full, then a scan/learning/de-obfuscation operation could take a much longer time.')
    print('                             --buffer-size can be used in combination with -scan, -learn and --de-obfuscate.')
    print('                             allowing progress to be displayed.')
    print('    -suffix                  Specify suffix. Used in combination with -scan.')
    print('    --group-suffix           Specify a suffix group. Used in combination with -scan.')
    print('                             --group-suffix archive')
    print('                             --group-suffix audio')
    print('                             --group-suffix book')
    print('                             --group-suffix code')
    print('                             --group-suffix executable')
    print('                             --group-suffix font')
    print('                             --group-suffix image')
    print('                             --group-suffix sheet')
    print('                             --group-suffix slide')
    print('                             --group-suffix text')
    print('                             --group-suffix video')
    print('                             --group-suffix web')
    print('    --custom-group-suffix    Specify a custom suffix group. Used in combination with -scan.')
    print('                             --custom-group-suffix mp3,mp4,jpg')
    print('                             Specify as many suffixes as required.')
    print('    -v                       Output verbose. Only recommended when using -define and for development purposes.')
    print('    -h                       Displays this help message')
    print('')
    print('    Example: omega_find --buffer-size 2048 -scan C:\ -suffix mp4')
    print('    Example: omega_find --buffer-size 2048 -learn C:\\')
    print('    Example: omega_find --buffer-size full -de-obfuscate C:\\')
    print('    Example: omega_find -v -define jpg')
    print('')
    print('OmegaFind is only as good as its implementation. A working knowledge of filesystems is recommended in order to best')
    print('implement OmegaFind.')
    print('-' * limit_char)
    print('')


def sysargv_filesizemax(filesize_max=False):
    if '--filesize-max' in sys.argv:
        idx = sys.argv.index('--filesize-max')
        if sys.argv[idx + 1].isdigit():
            filesize_max = int(sys.argv[idx + 1])
    return filesize_max


if '-v' in sys.argv:
    verbosity = True

if '--buffer-size' in sys.argv:
    idx = sys.argv.index('--buffer-size')
    if sys.argv[idx + 1].isdigit():
        buffer_size = int(sys.argv[idx + 1])
    elif sys.argv[idx + 1] == 'full':
        buffer_size = sys.argv[idx + 1].strip()


if '-define' in sys.argv:
    idx = sys.argv.index('-define')
    suffix = sys.argv[idx+1]

    run_function_0(suffix)

elif '--de-obfuscate' in sys.argv:
    idx = sys.argv.index('--de-obfuscate')
    target_path = sys.argv[idx+1]

    if os.path.exists(target_path) and os.path.isdir(target_path) is True:
        cc()
        filesize_max = False
        scan_learn(target_path=target_path, buffer_size=buffer_size, filesize_max=sysargv_filesizemax(filesize_max))
    else:
        print('-- invalid path')

elif '-learn' in sys.argv:
    learn = True

    idx = sys.argv.index('-learn')
    target_path = sys.argv[idx+1]

    if os.path.exists(target_path) and os.path.isdir(target_path) is True:
        cc()
        filesize_max = False
        scan_learn(target_path=target_path, buffer_size=buffer_size, filesize_max=sysargv_filesizemax(filesize_max))
    else:
        print('-- invalid path')

elif '-scan' in sys.argv:

    idx = sys.argv.index('-scan')
    target_path = sys.argv[idx+1]
    suffix = []

    if '-suffix' in sys.argv:
        idx = sys.argv.index('-suffix')
        suffix.append(sys.argv[idx+1].strip())

    elif '--group-suffix' in sys.argv:
        idx = sys.argv.index('--group-suffix')
        suffix_ = sys.argv[idx + 1]

        if suffix_ == 'archive':
            suffix = ext_module.ext_archive

        elif suffix_ == 'audio':
            suffix = ext_module.ext_audio

        elif suffix_ == 'book':
            suffix = ext_module.ext_book

        elif suffix_ == 'code':
            suffix = ext_module.ext_code

        elif suffix_ == 'executable':
            suffix = ext_module.ext_executable

        elif suffix_ == 'font':
            suffix = ext_module.ext_font

        elif suffix_ == 'image':
            suffix = ext_module.ext_image

        elif suffix_ == 'sheet':
            suffix = ext_module.ext_sheet

        elif suffix_ == 'slide':
            suffix = ext_module.ext_slide

        elif suffix_ == 'text':
            suffix = ext_module.ext_text

        elif suffix_ == 'video':
            suffix = ext_module.ext_video

        elif suffix_ == 'web':
            suffix = ext_module.ext_web

    elif '--custom-group-suffix' in sys.argv:
        cgs = []
        idx = sys.argv.index('--custom-group-suffix')
        suffix_ = sys.argv[idx + 1]
        suffix_ = suffix_.split(',')
        for _ in suffix_:
            cgs.append(_.strip())
        print(cgs)
        suffix = cgs

    if os.path.exists(target_path):
        if suffix:
            cc()
            filesize_max = False
            omega_find(target_path=target_path, suffix=suffix, buffer_size=buffer_size, verbosity=verbosity, filesize_max=sysargv_filesizemax(filesize_max))
        else:
            print('-- suffix unspecified.')
    else:
        print('-- invalid path.')


Style.RESET_ALL
