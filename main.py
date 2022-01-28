import re
import csv


def formatting(raw):
    duplicate_check = {}
    desync = 0
    formatted = [raw[0]]
    for i in range(1, len(raw)):
        temp_row = raw[i]
        # Форматирование ФИО по полям
        temp_lastname = re.split(r'\s', temp_row[0])
        if len(temp_lastname) == 2:
            temp_row[0] = temp_lastname[0]
            temp_row[1] = temp_lastname[1]
        elif len(temp_lastname) == 3:
            temp_row[0] = temp_lastname[0]
            temp_row[1] = temp_lastname[1]
            temp_row[2] = temp_lastname[2]
        temp_name = re.split(r'\s', temp_row[1])
        if len(temp_name) == 2:
            temp_row[1] = temp_name[0]
            temp_row[2] = temp_name[1]
        # Приведение телефона к формату +7(XXX)XXX-XX-XX доб.XXX
        if temp_row[5] != '':
            temp_phone = temp_row[5]
            phone_pattern = re.compile(
                r'(\+7|8)?[\s-]*\(?(\d{3})\)?[\s-]*(\d{3})[\s-]*(\d{2})[\s-]*(\d{2})[\s]?(\(?доб. (\d+))?')
            if 'доб.' in temp_phone:
                temp_phone = phone_pattern.sub(r'+7(\2)\3-\4-\5 доб. \7', temp_phone)
            else:
                temp_phone = phone_pattern.sub(r'+7(\2)\3-\4-\5', temp_phone)
            temp_row[5] = temp_phone
        # Объединение дублирующих записей
        unique_info = temp_row[0] + ' ' + temp_row[1]
        if unique_info in duplicate_check:
            master_pos = duplicate_check.get(unique_info) - desync
            temp_master_row = formatted[master_pos]
            for j in range(len(temp_master_row)):
                if temp_master_row[j] == '':
                    temp_master_row[j] = temp_row[j]
            formatted[master_pos] = temp_master_row
            desync += 1
        else:
            duplicate_check[unique_info] = i
            formatted.append(temp_row)
    return formatted


if __name__ == '__main__':
    with open("phonebook_raw.csv", encoding='UTF-8') as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list_raw = list(rows)

    contacts_list = formatting(contacts_list_raw)

    with open("phonebook.csv", "w") as f:
        data_writer = csv.writer(f, delimiter=',')
        data_writer.writerows(contacts_list)
