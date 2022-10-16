""" Written by Benjamin Jack Cullen aka Holographic_Sol

OMEGA FIND

Intention 1: To find/expose files that may be pretending to be a file type other than the files real file type.

    Example: secret_file.mp4 has been renamed to anything.anything and buried somewhere in a drive.
        OMEGA FIND seeks to expose these files for what they really are.
        (A double-edged blade. agent exposes you/you expose an agent)

Intention 2: To find files not by name or filename suffix matching but by reading each file into memory and comparing
    the buffer to known buffer reads for the suffix specified.

Intention 3: Define. Specify a filename suffix and return a concise/verbose description of the file type specified.

Modes of operation:

    Learn: Provide OMEGA FIND with a directory path of trusted file(s) to learn from to build OMEGA FINDS knowledge of
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
import time
import re
import magic
import unicodedata
import distutils.dir_util
import mimetypes
import codecs
from colorama import Fore, Back, Style
import psutil
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

    if not os.path.exists('./log/'):
        distutils.dir_util.mkpath('./log/')

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
        distutils.dir_util.mkpath('./data/')

    if not os.path.exists(log_file):
        open(log_file, 'w').close()

    log_tm_stamp = str(datetime.datetime.now())
    to_file = str('[' + log_tm_stamp + '] [PATH] ' + str(fullpath)).strip() + ' [BUFFER] ' + str(buffer)

    with codecs.open(log_file, 'a', encoding='utf8') as fo:
        fo.write(to_file + '\n')
    fo.close()


def run_function_1(target_path, buffer_size=2048):
    global ei
    global learn

    cp.cpi('-- attempting to clear screen.')

    cc()

    cp.cpi('-- attempting to create new timestamped directory for results.')

    mime_type_database = './db/database_file_mime_types.txt'

    """ Create A Time Stamped Directory """
    time_now = str(datetime.datetime.now())
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

        """ Read Mime Type Database """
        cp.cpi('-- attempting to read mime type database: ' + mime_type_database)

        """ Check Directory Exists """

        db_all = []
        lmt = []
        suffixes_mt = []
        total_undefined_suffixes = []

        """ Only Read Database If Exist And Continue (Pure logger mode) """
        if os.path.exists(mime_type_database):
            cp.cpi(str('-- successfully found mime types database: ') + str(dir_now))
            with codecs.open(mime_type_database, 'r', encoding='utf8') as fo:
                for line in fo:
                    line = line.strip()
                    line = line.lower()
                    db_all.append(line)
                    if line != '':
                        line_split = line.split(' ')
                        line_split_0 = line_split[0].strip()

                        if line == line_split_0:
                            total_undefined_suffixes.append(line)

                        if line_split_0.endswith('-mime-types'):
                            suffix_var = line_split_0.replace('-mime-types', '')

                            """ Add Suffix To List """
                            if suffix_var not in suffixes_mt:
                                suffixes_mt.append(suffix_var)

                            """ Add Mime Type Line To List """
                            lmt.append(line)

                        else:
                            cp.cpi('-- mime type database anomaly:' + str(line))
            fo.close()

        """ Read Database (Learned Buffer Read Results Mapped To File Suffixes) """
        learn_database = './db/database_learning.txt'
        cp.cpi(str('-- attempting to read database:   ') + str(learn_database))
        trf = learn_database
        learning_br = []
        suffixes_br = []
        line_count = 0

        if os.path.exists(trf):
            cp.cpi(str('-- reading learning database:              ') + str(learn_database))
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

                        """ Add Suffix To List """
                        suffix_var = line_split_0.replace('-buffer-read', '')
                        if suffix_var not in suffixes_br:
                            suffixes_br.append(suffix_var)

                    if '-buffer-read' not in line.replace(' ', ''):
                        print('-- learning database anomaly:', line)
            fo.close()
        else:
            print()

        """ Set Counters """
        buffer_read_exception_count_0 = 0
        buffer_read_exception_count_1 = 0
        buffer_read_exception_permssion_count_0 = 0
        buffer_read_exception_permssion_count_1 = 0
        total_files_encountered = 0
        learn_count = 0
        buffer_failed_count = 0
        buffer_passed_count = 0
        buffer_read_exception_count_recovered = 0
        error_getting_suffix_count = 0
        error_getsize_count = 0
        mime_type_read_exception_count_0 = 0
        mime_type_read_exception_count_1 = 0
        mime_passed_inspection_count = 0
        mime_failed_inspection_count = 0
        bool_buffer_data_true_count = 0
        bool_buffer_data_false_count = 0

        mime_exception_permssion_count_0 = 1
        mime_permission_denied_attempt_1 = False

        mime_exception_permssion_count_1 = 1
        mime_permission_denied_attempt_2 = False

        last_learned = ''

        new_file_extension_mt = []
        new_file_extension_br = []
        new_learned = []

        unrecognized_buffer = []
        unrecognized_mime = []

        """ Display Scan Criteria And Present Confirmation Opportunity """
        print('')
        pr_row(limit_char)

        # Header
        if learn is True:
            cp.cpf('[WARNING!]      [WARNING!]      [WARNING!]      [WARNING!]      [WARNING!]      [WARNING!]       [WARNING!]')
            pr_row(limit_char)
            print('')
            cp.cpi('[LEARNING CRITERIA]')
        elif learn is False:
            print('')
            cp.cpi('[SCAN CRITERIA]')
        print('')

        # Details
        print(Style.BRIGHT+Fore.MAGENTA + '[SPECIFIED LOCATION]                        ' + Style.BRIGHT+Fore.GREEN + str(target_path) + Style.RESET_ALL)
        if learn is True:
            print(Style.BRIGHT+Fore.MAGENTA+'[LEARNING]                          ' + Style.BRIGHT+Fore.RED+str(learn)+'   [WARNING!]' + Style.RESET_ALL)
        else:
            print(Style.BRIGHT+Fore.MAGENTA+'[LEARNING]                          ' + Style.BRIGHT+Fore.GREEN+str(learn)+Style.RESET_ALL)
        print('')
        print(Style.BRIGHT+Fore.MAGENTA+'[LEARNED DEFINITIONS]               ' + Style.BRIGHT+Fore.GREEN+str(len(learning_br))+Style.RESET_ALL)
        print('')
        pr_row(limit_char)

        if learn is True:
            print('')
            cp.cpf('[WARNING!]           LEARNING ENABLED')
            print('')
            print(Style.BRIGHT + Fore.MAGENTA + '[LEARNING]   ' + Style.BRIGHT+Fore.YELLOW + 'THIS IF SUCCESSFULL WILL ADD THE TRAINING DATA TO THE LEARNED DATABASE WHICH')
            print(Style.BRIGHT + Fore.YELLOW + '                     WILL BE USED IN DE-OBFUSCATION SCANS & PERFORMING REVERSE SEARCHES!' + Style.RESET_ALL)
            print('')
            cp.cpf('[CATION!]            ENSURE ONLY TRUSTED DATA SETS!')
            print('')
            pr_row(limit_char)
            print('')
            usr_choice = input('Press Y to learn or press any other key to abort [Enter] : ')
            print('')

        elif learn is False:
            print('')
            cp.cpp('[SCAN]   This program will attempt to de-obfuscate files in: ' + str(target_path))
            pr_row(limit_char)
            print('')
            usr_choice = input('Press Y to attempt de-obfuscation or press any other key to abort [Enter] : ')
            print('')

        """ Continue If Compiled Database Lists Are Aligned """
        if usr_choice.lower() == 'y':
            if learn is True:
                cp.cpi('-- attempting to learn about files in location:', target_path)
            elif learn is False:
                cp.cpi('-- scanning location:', target_path)

            """ Walk User Specified Directory """
            for dirName, subdirList, fileList in os.walk(target_path):
                for fname in fileList:

                    # Count Files
                    total_files_encountered += 1

                    file_encountered_time_stamp = '[' + str(datetime.datetime.now()) + ']'

                    """ Create A Full Path To File From Root """
                    f = os.path.join(dirName, fname)
                    f = f.strip()

                    """ Header """
                    print('')
                    pr_row(limit_char)
                    print('')
                    if learn is True:
                        cp.cpi('[LEARNING]')
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
                    bool_new_mt_suffix = False
                    bool_new_br_suffix = False
                    if fe == '':
                        fe = 'no_file_extension'
                    if fe not in suffixes_mt:
                        bool_new_mt_suffix = True
                        if fe not in new_file_extension_mt:
                            new_file_extension_mt.append(fe)
                    if fe not in suffixes_br:
                        bool_new_br_suffix = True
                        if fe not in new_file_extension_br:
                            new_file_extension_br.append(fe)
                    print(Style.BRIGHT + Fore.MAGENTA + '[ALLEGED SUFFIX] ' + Style.BRIGHT + Fore.GREEN + str(fe) + Style.RESET_ALL)

                    """ Initiate And Clear Each Iteration """
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
                        e = '[error reading buffer (first try)] ' + str(e)
                        e_tmp = e
                        log_file = ef
                        # logger(log_file, e, f)  # Uncomment to debug
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
                            logger(log_file, e, f)

                    """ Use Most Defined Buffer String """
                    b_1_len = len(b_1)
                    b_2_len = len(b_2)
                    if b_1_len >= b_2_len:
                        b = b_1
                    elif b_2_len > b_1_len:
                        b = b_2

                    """ Read File Mime Type And If Fail Then Try Something Else """
                    m = ''
                    e_tmp_2 = ''
                    try:
                        m = magic.from_file(str(f).encode('UTF-8'), mime=True)
                        m = m.lower()
                    except Exception as e:
                        mime_type_read_exception_count_0 += 1
                        if 'permission denied' in str(e).lower():
                            mime_exception_permssion_count_0 += 1
                            mime_permission_denied_attempt_1 = True
                        mime_type_read_exception_count_0 += 1
                        e = '[error reading mime type (first try)] ' + str(e)
                        e_tmp_2 = e
                        log_file = ef
                        # logger(log_file, e, f)  # Uncomment to debug
                    if e_tmp_2 != '':
                        try:
                            m = magic.from_buffer(str(f).encode('UTF-8'), mime=True)
                            m = m.lower()
                        except Exception as e:
                            mime_type_read_exception_count_1 += 1
                            if 'permission denied' in str(e).lower():
                                mime_exception_permssion_count_1 += 1
                                mime_permission_denied_attempt_2 = True
                            e = '[error reading mime type (second try)] ' + str(e)
                            log_file = ef
                            logger(log_file, e, f)
                    print(Style.BRIGHT + Fore.MAGENTA + '[MIME TYPE] ' + Style.BRIGHT + Fore.GREEN + str(m) + Style.RESET_ALL)

                    """ Look For Suffix In Database And Store Associated Mime Types In A List """
                    mime_passed_inspection = False
                    if m != '':
                        key_mime = str(fe) + '-mime-types'
                        i = 0
                        for lmts in lmt:

                            """ Look For Suffix """
                            if lmt[i].split()[0] == str(key_mime).lower():

                                """"" Split Found Item So That Each Mime Type Can Be Compared """
                                database_mime_type = lmt[i].split()

                                """ Compare Mime Type To Each Item In The List """
                                ii = 0
                                for database_mime_types in database_mime_type:
                                    if database_mime_type[ii] == m:
                                        print(Style.BRIGHT + Fore.MAGENTA + '[COMPARING] ' + Style.BRIGHT + Fore.GREEN + str(m) + Style.BRIGHT + Fore.MAGENTA + ' [AGAINST] ' + Style.BRIGHT + Fore.GREEN + str(database_mime_type[ii]) + Style.RESET_ALL)
                                        mime_passed_inspection = True
                                        mime_passed_inspection_count += 1
                                    else:
                                        print(Style.BRIGHT + Fore.MAGENTA + '[COMPARING] ' + Style.BRIGHT + Fore.GREEN + str(m) + Style.BRIGHT + Fore.MAGENTA + ' [AGAINST] ' + Style.BRIGHT + Fore.RED + str(database_mime_type[ii]) + Style.RESET_ALL)
                                    ii += 1
                                if mime_passed_inspection is False:
                                    mime_failed_inspection_count += 1
                            i += 1
                    else:
                        mime_passed_inspection = False
                        mime_failed_inspection_count += 1
                        print(Style.BRIGHT + Fore.MAGENTA + '[MIME TYPE EMPTY STRING] ' + Style.BRIGHT + Fore.GREEN + 'skipping comparison check' + Style.RESET_ALL)
                    print(Style.BRIGHT + Fore.MAGENTA + '[BUFFER READ] ' + Style.BRIGHT + Fore.GREEN + str(b) + Style.RESET_ALL)

                    """ Continue If Buffer String & Set Default Boolean """
                    bool_learn = False
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
                        for learning_brs in learning_br:
                            y_re = re.sub(digi_str, '', learning_br[i])
                            if y_re == x_re:
                                print(Style.BRIGHT + Fore.MAGENTA + '[REGEX BUFFER MATCH] ' + Style.BRIGHT + Fore.GREEN + str(x_re) + Style.RESET_ALL)
                                buffer_passed_inspection = True
                                break
                            i += 1

                        """ regex x == regex y so continue """
                        if buffer_passed_inspection is True:
                            buffer_passed_count += 1
                            bool_learn = False
                            if learn is True:
                                print(Style.BRIGHT + Fore.MAGENTA + '[LEARNED COUNTER] ' + Style.BRIGHT + Fore.GREEN + str(learn_count) + Style.RESET_ALL)
                                print(Style.BRIGHT + Fore.MAGENTA + '[LEARNED] ' + Style.BRIGHT + Fore.RED + str(bool_learn) + Style.RESET_ALL)
                                print(Style.BRIGHT + Fore.MAGENTA + '[LAST LEARNED] ' + Style.BRIGHT + Fore.GREEN + str(last_learned) + Style.RESET_ALL)

                        elif buffer_passed_inspection is False:
                            unrecognized_buffer.append(f)
                            buffer_failed_count += 1

                            if learn is True:
                                print(Style.BRIGHT + Fore.MAGENTA + '[LEARNED COUNTER] ' + Style.BRIGHT + Fore.GREEN + str(learn_count) + Style.RESET_ALL)
                                if key_buff_read not in new_learned:
                                    last_learned = str(datetime.datetime.now())
                                    new_learned.append(key_buff_read)
                                    learn_count += 1
                                    bool_learn = True
                                    print(Style.BRIGHT + Fore.MAGENTA + '[LEARNED] ' + Style.BRIGHT + Fore.GREEN + str(bool_learn) + Style.RESET_ALL)
                                    with codecs.open(learn_database, 'a', encoding='utf8') as fo:
                                        to_file = key_buff_read
                                        fo.write(to_file + '\n')
                                elif key_buff_read in new_learned:
                                    bool_learn = False
                                    print(Style.BRIGHT + Fore.MAGENTA + '[LEARNED] ' + Style.BRIGHT + Fore.RED + str(bool_learn) + Style.RESET_ALL)
                                print(Style.BRIGHT + Fore.MAGENTA + '[LAST LEARNED] ' + Style.BRIGHT + Fore.GREEN + str(last_learned) + Style.RESET_ALL)

                    else:
                        bool_buffer_data_false_count += 1
                        if learn is True:
                            bool_data_buffer = False
                            print(Style.BRIGHT + Fore.MAGENTA + '[LEARNED COUNTER] ' + Style.BRIGHT + Fore.GREEN + str(learn_count) + Style.RESET_ALL)
                            bool_learn = False
                            print(Style.BRIGHT + Fore.MAGENTA + '[LEARNED] ' + Style.BRIGHT + Fore.GREEN + str(bool_learn) + Style.RESET_ALL)
                        elif learn is False:
                            buffer_failed_count += 1
                            buffer_passed_inspection = False
                            bool_data_buffer = False

                    if learn is False:
                        if mime_passed_inspection is True:
                            print(Style.BRIGHT + Fore.MAGENTA + '[MIME RECOGNIZED IN RELATION TO ALLEGED SUFFIX] ' + Style.BRIGHT + Fore.GREEN + str(mime_passed_inspection) + Style.RESET_ALL)
                        elif mime_passed_inspection is False:
                            print(Style.BRIGHT + Fore.MAGENTA + '[MIME RECOGNIZED IN RELATION TO ALLEGED SUFFIX] ' + Style.BRIGHT + Fore.RED + str(mime_passed_inspection) + Style.RESET_ALL)
                        if buffer_passed_inspection is True:
                            print(Style.BRIGHT + Fore.MAGENTA + '[BUFFER RECOGNIZED IN RELATION TO ALLEGED SUFFIX] ' + Style.BRIGHT + Fore.GREEN + str(buffer_passed_inspection) + Style.RESET_ALL)
                        elif buffer_passed_inspection is False:
                            print(Style.BRIGHT + Fore.MAGENTA + '[BUFFER RECOGNIZED IN RELATION TO ALLEGED SUFFIX] ' + Style.BRIGHT + Fore.RED + str(buffer_passed_inspection) + Style.RESET_ALL)
                        print(Style.BRIGHT + Fore.MAGENTA + '[NEW MIME DATABASE SUFFIX] ' + Style.BRIGHT + Fore.GREEN + str(bool_new_mt_suffix) + Style.RESET_ALL)
                        print(Style.BRIGHT + Fore.MAGENTA + '[NEW BUFFER DATABASE SUFFIX] ' + Style.BRIGHT + Fore.GREEN + str(bool_new_br_suffix) + Style.RESET_ALL)
                    print(Style.BRIGHT + Fore.MAGENTA + '[BUFFER PERMISSION DENIED ATTEMPT 1] ' + Style.BRIGHT + Fore.GREEN + str(buffer_permission_denied_attempt_1) + Style.RESET_ALL)
                    print(Style.BRIGHT + Fore.MAGENTA + '[BUFFER PERMISSION DENIED ATTEMPT 2] ' + Style.BRIGHT + Fore.GREEN + str(buffer_permission_denied_attempt_2) + Style.RESET_ALL)
                    print(Style.BRIGHT + Fore.MAGENTA + '[MIME PERMISSION DENIED ATTEMPT 1] ' + Style.BRIGHT + Fore.GREEN + str(mime_permission_denied_attempt_1) + Style.RESET_ALL)
                    print(Style.BRIGHT + Fore.MAGENTA + '[MIME PERMISSION DENIED ATTEMPT 2] ' + Style.BRIGHT + Fore.GREEN + str(mime_permission_denied_attempt_2) + Style.RESET_ALL)
                    # print(Style.BRIGHT + Fore.MAGENTA + '[BUFFER DATA EXISTS] ' + Style.BRIGHT + Fore.GREEN + str(bool_data_buffer) + Style.RESET_ALL)

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
                    to_file_5 = '[MIME TYPE] ' + str(m)
                    to_file_6 = '[BUFFER] ' + str(key_buff_read)
                    to_file_7 = str('[BUFFER RECOGNIZED IN RELATION TO ALLEGED SUFFIX] ' + str(buffer_passed_inspection))
                    to_file_8 = str('[MIME RECOGNIZED IN RELATION TO ALLEGED SUFFIX] ' + str(mime_passed_inspection))
                    to_file_9 = str('[NEW MIME DATABASE SUFFIX] ' + str(bool_new_mt_suffix))
                    to_file_10 = str('[NEW BUFFER DATABASE SUFFIX] ' + str(bool_new_br_suffix))
                    to_file_11 = str('[PERMISSION DENIED ATTEMPT 1] ' + str(buffer_permission_denied_attempt_1))
                    to_file_12 = str('[PERMISSION DENIED ATTEMPT 2] ' + str(buffer_permission_denied_attempt_2))
                    to_file_13 = str('[MIME PERMISSION DENIED ATTEMPT 1] ' + str(mime_permission_denied_attempt_1))
                    to_file_14 = str('[MIME PERMISSION DENIED ATTEMPT 2] ' + str(mime_permission_denied_attempt_2))
                    to_file_15 = str('[BUFFER DATA EXISTS] ' + str(bool_data_buffer))

                    with codecs.open(log_file_inspection, 'a', encoding='utf-8') as fo:
                        fo.write(to_file_1 + '\n')
                        fo.write(to_file_2 + '\n')
                        fo.write(to_file_3 + '\n')
                        fo.write(to_file_4 + '\n')
                        fo.write(to_file_5 + '\n')
                        fo.write(to_file_6 + '\n')
                        fo.write(to_file_7 + '\n')
                        fo.write(to_file_8 + '\n')
                        fo.write(to_file_9 + '\n')
                        fo.write(to_file_10 + '\n')
                        fo.write(to_file_11 + '\n')
                        fo.write(to_file_12 + '\n')
                        fo.write(to_file_13 + '\n')
                        fo.write(to_file_14 + '\n')
                        fo.write(to_file_15 + '\n')
                        fo.write(''+'\n')
                    fo.close()
            print('')
            pr_row(limit_char)
            print('')

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
                fo_report.write('[PASSED MIME INSPECTION] ' + str(mime_passed_inspection_count) + '\n')
                fo_report.write('[FAILED MIME INSPECTION] ' + str(mime_failed_inspection_count) + '\n')
                fo_report.write('[BUFFER EXCEPTIONS ATTEMPT 1] ' + str(buffer_read_exception_count_0) + '\n')
                fo_report.write('[BUFFER EXCEPTIONS ATTEMPT 2] ' + str(buffer_read_exception_count_1) + '\n')
                fo_report.write('[FOUND BUFFER DATA] ' + str(bool_buffer_data_true_count) + '\n')
                fo_report.write('[DID NOT FIND BUFFER DATA] ' + str(bool_buffer_data_false_count) + '\n')
                fo_report.write('[BUFFER PERMISSION EXCEPTIONS ATTEMPT 1] ' + str(buffer_read_exception_permssion_count_0) + '\n')
                fo_report.write('[BUFFER PERMISSION EXCEPTIONS ATTEMPT 2] ' + str(buffer_read_exception_permssion_count_1) + '\n')
                fo_report.write('[MIME EXCEPTIONS ATTEMPT 1] ' + str(mime_type_read_exception_count_0) + '\n')
                fo_report.write('[MIME EXCEPTIONS ATTEMPT 2] ' + str(mime_type_read_exception_count_1) + '\n')
                fo_report.write('[MIME PERMISSION DENIED ATTEMPT 1] ' + str(mime_exception_permssion_count_0) + '\n')
                fo_report.write('[MIME PERMISSION DENIED ATTEMPT 2] ' + str(mime_exception_permssion_count_1) + '\n')
                fo_report.write('[NEW SUFFIXES ENCOUNTERED NOT IN MIME DATABASE COUNT] ' + str(len(new_file_extension_mt)) + '\n')
                fo_report.write('[NEW SUFFIXES ENCOUNTERED NOT IN BUFFER DATABASE COUNT] ' + str(len(new_file_extension_br)) + '\n')
                fo_report.write('[NEW SUFFIXES ENCOUNTERED NOT IN MIME DATABASE] ' + str(new_file_extension_mt) + '\n')
                fo_report.write('[NEW SUFFIXES ENCOUNTERED NOT IN BUFFER DATABASE] ' + str(new_file_extension_br) + '\n')
            fo_report.close()

            if learn is True:
                cp.cpi('[LEARNING RESULTS]')
            elif learn is False:
                cp.cpi('[SCAN RESULTS]')

            print('')
            print(Style.BRIGHT + Fore.MAGENTA + '[INITIATION TIME] ' + Style.BRIGHT + Fore.GREEN + str(time_now) + Style.RESET_ALL)
            print(Style.BRIGHT + Fore.MAGENTA + '[COMPLETION TIME] ' + Style.BRIGHT + Fore.GREEN + str(datetime.datetime.now()) + Style.RESET_ALL)
            print('')
            print(Style.BRIGHT + Fore.MAGENTA + '[LOCATION] ' + Style.BRIGHT + Fore.GREEN + str(target_path) + Style.RESET_ALL)
            print(Style.BRIGHT + Fore.MAGENTA + '[TOTAL FILES ENCOUNTERED] ' + Style.BRIGHT + Fore.GREEN + str(total_files_encountered) + Style.RESET_ALL)
            print('')
            if learn is True:
                print(Style.BRIGHT + Fore.MAGENTA + '[LEARNED] ' + Style.BRIGHT + Fore.GREEN + str(learn_count) + Style.RESET_ALL)
            elif learn is False:
                print(Style.BRIGHT + Fore.MAGENTA + '[PASSED BUFFER INSPECTION] ' + Style.BRIGHT + Fore.GREEN + str(buffer_passed_count) + Style.RESET_ALL)
                print(Style.BRIGHT + Fore.MAGENTA + '[FAILED BUFFER INSPECTION] ' + Style.BRIGHT + Fore.GREEN + str(buffer_failed_count) + Style.RESET_ALL)
                print(Style.BRIGHT + Fore.MAGENTA + '[PASSED MIME INSPECTION] ' + Style.BRIGHT + Fore.GREEN + str(mime_passed_inspection_count) + Style.RESET_ALL)
                print(Style.BRIGHT + Fore.MAGENTA + '[FAILED MIME INSPECTION] ' + Style.BRIGHT + Fore.GREEN + str(mime_failed_inspection_count) + Style.RESET_ALL)

            print(Style.BRIGHT + Fore.MAGENTA + '[BUFFER EXCEPTIONS ATTEMPT 1] ' + Style.BRIGHT + Fore.GREEN + str(buffer_read_exception_count_0) + Style.RESET_ALL)
            print(Style.BRIGHT + Fore.MAGENTA + '[BUFFER EXCEPTIONS ATTEMPT 2] ' + Style.BRIGHT + Fore.GREEN + str(buffer_read_exception_count_1) + Style.RESET_ALL)
            print(Style.BRIGHT + Fore.MAGENTA + '[FOUND BUFFER DATA] ' + Style.BRIGHT + Fore.GREEN + str(bool_buffer_data_true_count) + Style.RESET_ALL)
            print(Style.BRIGHT + Fore.MAGENTA + '[DID NOT FIND BUFFER DATA] ' + Style.BRIGHT + Fore.GREEN + str(bool_buffer_data_false_count) + Style.RESET_ALL)
            print(Style.BRIGHT + Fore.MAGENTA + '[BUFFER PERMISSION EXCEPTIONS ATTEMPT 1] ' + Style.BRIGHT + Fore.GREEN + str(buffer_read_exception_permssion_count_0) + Style.RESET_ALL)
            print(Style.BRIGHT + Fore.MAGENTA + '[BUFFER PERMISSION EXCEPTIONS ATTEMPT 2] ' + Style.BRIGHT + Fore.GREEN + str(buffer_read_exception_permssion_count_1) + Style.RESET_ALL)
            print(Style.BRIGHT + Fore.MAGENTA + '[MIME EXCEPTIONS ATTEMPT 1] ' + Style.BRIGHT + Fore.GREEN + str(mime_type_read_exception_count_0) + Style.RESET_ALL)
            print(Style.BRIGHT + Fore.MAGENTA + '[MIME EXCEPTIONS ATTEMPT 2] ' + Style.BRIGHT + Fore.GREEN + str(mime_type_read_exception_count_1) + Style.RESET_ALL)
            print(Style.BRIGHT + Fore.MAGENTA + '[NEW SUFFIXES ENCOUNTERED NOT IN MIME DATABASE COUNT] ' + Style.BRIGHT + Fore.GREEN + str(len(new_file_extension_mt)) + Style.RESET_ALL)
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
            cp.cpi('[POST SCAN OPTIONS]')
            print('')
            cp.cpi('1. Display all obfuscated or unrecognized files.')
            print('')
            usr_choice_1 = input('Enter: ')
            if usr_choice_1 == '1':
                for _ in unrecognized_buffer:
                    print(Style.BRIGHT + Fore.MAGENTA + '[OBFUSCATED OR UNRECOGNIZED] ' + Style.BRIGHT + Fore.GREEN + str(_) + Style.RESET_ALL)
            print('')
            pr_row(limit_char)
            print('')


def omega_find(target_path='', suffix='', buffer_size=2048, first_pass=True, verbosity=False):
    """ uses database to perform a special search """

    char_limit = 0
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
        print(Style.BRIGHT + Fore.GREEN + '[DATABASE] ' + Style.RESET_ALL + 'Found (' + str(target_path) + ')')
        with codecs.open('./db/database_learning.txt', 'r', encoding='utf8') as fo:
            for line in fo:
                line = line.strip()
                if line.startswith(suffix):
                    known_buffer.append(line)

                    # update displayed known associations in loop for large databases to show progress.
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

                # update displayed known associations in loop for large databases to show progress.
                pr_str = str(Style.BRIGHT + Fore.GREEN + '[FILES] ' + Style.RESET_ALL + str(f_count))
                pyprogress.pr_technical_data(pr_str)
        print('')
    else:
        print(str(' ' * 43) + Style.BRIGHT + Fore.GREEN + '[SKIPPING SCANNING TARGET LOCATION]' + Style.RESET_ALL)
        print('')
    print('')
    print('-' * 120)

    # omega find
    print('')
    print(str(' ' * 40) + Style.BRIGHT + Fore.GREEN + '[PERFORMING PRIMARY OPERATION] OMEGA FIND' + Style.RESET_ALL)
    print('')
    print(Style.BRIGHT + Fore.GREEN + '[OMEGA FIND]  ' + Style.RESET_ALL + 'Attempting to read each file into memory and compare buffer to known buffers for suffix specified.')
    print(Style.BRIGHT + Fore.GREEN + '[INFORMATION] ' + Style.RESET_ALL + 'Like files may be included in results. This is normal and expected behaviour.')
    print('')
    f_i = 0
    f_match = []
    f_error = []
    f_all = []
    for dirName, subdirList, fileList in os.walk(target_path):
        for fname in fileList:
            fullpath = os.path.join(dirName, fname)
            f_i += 1

            if verbosity is True and first_pass is True:
                try:
                    pyprogress.progress_bar(part=int(f_i), whole=int(f_count),
                                            pre_append=str(Style.BRIGHT + Fore.GREEN + '[SCANNING] '+Style.RESET_ALL),
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
                    print('')
                    print(e)
                    pass
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

                # logger(log_file=log_error_file, e=str(e), f=fullpath) # uncomment for verbose logging

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

                    logger(log_file=log_error_file, e=str(e), f=fullpath)

                    break

            """ Use Most Defined Buffer String """
            b_1_len = len(b_1)
            b_2_len = len(b_2)
            if b_1_len >= b_2_len:
                b = b_1
            elif b_2_len > b_1_len:
                b = b_2

            """ Buffer output may yield digits for timestamps, dimensions etc. compare not the digits (keeping only the full line of data in the file and in memory for potential extreme strictness) """
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
    print(str(' ' * 56) + Style.BRIGHT + Fore.GREEN + '[MENU]' + Style.RESET_ALL)
    print('')
    print(Style.BRIGHT + Fore.GREEN + ' [OPEN RESULTS FILE] ' + Style.RESET_ALL + '1' + '                                                                           ' + Style.BRIGHT + Fore.GREEN + ' [DISPLAY RESULTS]   ' + Style.RESET_ALL + '3')
    print(Style.BRIGHT + Fore.GREEN + ' [OPEN ERROR FILE]   ' + Style.RESET_ALL + '2' + '                                                                           ' + Style.BRIGHT + Fore.GREEN + ' [DISPLAY ERRORS]    ' + Style.RESET_ALL + '4')
    print(Style.BRIGHT + Fore.GREEN + '                                                                                                  [DISPLAY ALL]       ' + Style.RESET_ALL + '5')
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
        print('-' * 120)
        for _ in f_match:
            print(Style.BRIGHT + Fore.GREEN + '[BUFFER MATCH] ' + Style.RESET_ALL + str(_))
    elif menu_input == '4':
        print(str(' ' * 50) + Style.BRIGHT + Fore.GREEN + '[DISPLAYING ERRORS]' + Style.RESET_ALL)
        print('-' * 120)
        for _ in f_error:
            print(Style.BRIGHT + Fore.GREEN + '[ERROR] ' + Style.RESET_ALL + str(_))
    elif menu_input == '5':
        print(str(' ' * 52) + Style.BRIGHT + Fore.GREEN + '[DISPLAYING ALL]' + Style.RESET_ALL)
        print('-' * 120)
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
    print('    -scan             Specifies a directory to scan. [ -scan directory_name ]')
    print('    -learn            Instructs the program to train from a specified location. [ -learn directory_name ]')
    print('    -define           Attempts to lookup a definition for suffix (not file/directory name) given. [ -define exe ]')
    print('    -find             Specify path. Finds files predicated upon known buffer read associations created by learning.')
    print('                      Example: -find C:/')
    print('                      A special and powerful search feature.')
    print('    --buffer-size     Specify in bytes how much of each file will be read into the buffer.')
    print('                      Example: --buffer-size 1024')
    print('                      Example: --buffer-size full')
    print('                      If using --buffer-size full, then a scan/learning/find operation could take a much longer time.')
    print('                      --buffer-size can be used in combination with -scan, -learn and -find.')
    print('    --first-pass      Used in conjunction with -find.')
    print('                      Allows preliminary enumeration to be used for progress. Adds time to total time to complete while')
    print('                      allowing progress to be displayed.')
    print('    -suffix           Specify suffix. Used in combination with -find.')
    print('    -v                Output verbose.')
    print('    -h                Displays this help message')
    print('')
    print('    Example: omega_find --first-pass --buffer-size 2048 -find C:\ -suffix mp4')
    print('    Example: omega_find --buffer-size 2048 -learn C:\\')
    print('    Example: omega_find --buffer-size full -scan C:\\')
    print('    Example: omega_find -define jpg')
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
        run_function_1(target_path, buffer_size=buffer_size)
    else:
        print('-- invalid path')

elif '-learn' in sys.argv:
    learn = True

    idx = sys.argv.index('-learn')
    target_path = sys.argv[idx+1]

    if os.path.exists(target_path) and os.path.isdir(target_path) is True:
        run_function_1(target_path, buffer_size=buffer_size)
    else:
        print('-- invalid path')

elif '-find' in sys.argv and '-suffix' in sys.argv:

        idx = sys.argv.index('-find')
        target_path = sys.argv[idx+1]

        idx = sys.argv.index('-suffix')
        suffix = sys.argv[idx+1]

        if os.path.exists(target_path):
            omega_find(target_path=target_path, suffix=suffix, buffer_size=buffer_size, first_pass=first_pass, verbosity=verbosity)
        else:
            print('-- invalid path')


Style.RESET_ALL
