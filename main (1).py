import csv
import re

reg_st = r"(\+7|8)?\s*[\( -](\d+)[\) -]\s*(\d+)[- ]?(\d{2})?[- ]?(\d+)?\s*" \
         + r"(\(?\s*доб\.\s*(\d+)\s*\)?)?"
pattern = re.compile(reg_st)

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

        formatted_phone = pattern.sub(r"+7(\2)\3-\4-\5 доб.\7", info['phone'])
        if formatted_phone[-5:] == " доб.":
            formatted_phone = formatted_phone[:-5]

        if formatted_info[lastname]["phone"] == "":
            formatted_info[lastname]["phone"] = formatted_phone
        if formatted_info[lastname]["email"] == "":
            formatted_info[lastname]["email"] = info["email"]

with open("phonebook.csv", "w", newline='', encoding="utf-8") as f:
    d_writer = csv.DictWriter(f, fieldnames, delimiter=',')
    d_writer.writerows(formatted_info.values())
