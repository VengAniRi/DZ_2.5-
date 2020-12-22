import csv
import re

with open("phonebook_raw.csv", 'r', encoding="utf-8") as f:
    d_reader = csv.DictReader(f)
    fieldnames = d_reader.fieldnames
    formatted_info = {}
    for info in d_reader:
        FIO = ' '.join([info["lastname"], info["firstname"], info["surname"]])
        FIO = FIO.split()

        lastname = FIO[0]
        if lastname not in formatted_info:
            formatted_info[lastname] = dict.fromkeys(fieldnames, '')
            formatted_info[lastname]["lastname"] = lastname

        firstname = FIO[1] if len(FIO) > 1 else ""
        if formatted_info[lastname]["firstname"] == "":
            formatted_info[lastname]["firstname"] = firstname

        surname = FIO[2] if len(FIO) > 2 else ""
        if formatted_info[lastname]["surname"] == "":
            formatted_info[lastname]["surname"] = surname

        if formatted_info[lastname]["organization"] == "":
            formatted_info[lastname]["organization"] = info["organization"]

        if formatted_info[lastname]["position"] == "":
            formatted_info[lastname]["position"] = info["position"]

        match = re.findall('[0-9]', info['phone'])
        if len(match) > 0:
            phone = ''.join(match)
            add_num = phone[11:]
            phone = phone[1:11]
            formatted_phone = f"+7({phone[:3]}){phone[3:6]}-{phone[6:8]}-{phone[8:]}"
            if add_num != "":
                formatted_phone += f" доб.{add_num}"
        else:
            formatted_phone = ""

        if formatted_info[lastname]["phone"] == "":
            formatted_info[lastname]["phone"] = formatted_phone
        if formatted_info[lastname]["email"] == "":
            formatted_info[lastname]["email"] = info["email"]

with open("phonebook.csv", "w", newline='', encoding="utf-8") as f:
    d_writer = csv.DictWriter(f, fieldnames, delimiter=',')
    d_writer.writerows(formatted_info.values())
