import csv
import random


def get_email():
    emails = []
    with open('./DATA/quickbooks.csv', 'r', encoding='utf8', newline='') as f:
        reader = csv.reader(f)

        [emails.extend(i) for i in reader]
    random.shuffle(emails)
    return random.choice(['a', 'b', 'c', 'd'])+emails[0]
    print(emails)


def get_unique_email_to_send():
    emails = []
    with open('./DATA/quickbooks.csv', 'r', encoding='utf8', newline='') as f:
        with open('./DATA/email_sent.csv', 'r', encoding='utf8', newline='') as f2:
            reader = csv.reader(f)
            reader2 = csv.reader(f2)
            _= list(map(lambda x: x[0], reader2))
            [emails.extend(i) for i in reader]
            emails= list(set(emails) - set(_))
            emails=list(filter(lambda x: len(x.strip()), emails))

    return emails[0]


def get_f_name():
    names = []
    with open('./DATA/content.csv', 'r', encoding='utf8', newline='') as f:
        reader = csv.reader(f)
        names = list(filter(lambda x: len(x.strip()),
                     map(lambda x: x[0], reader)))
    random.shuffle(names)
    return names[0]


def get_l_name():
    names = []
    with open('./DATA/content.csv', 'r', encoding='utf8', newline='') as f:
        reader = csv.reader(f)
        names = list(filter(lambda x: len(x.strip()),
                     map(lambda x: x[1], reader)))

    random.shuffle(names)
    return names[0]


def get_company_name():
    names = []
    with open('./DATA/content.csv', 'r', encoding='utf8', newline='') as f:
        reader = csv.reader(f)
        names = list(filter(lambda x: len(x.strip()),
                     map(lambda x: x[2], reader)))

    random.shuffle(names)
    return names[0]


def get_company_email():
    names = []
    with open('./DATA/content.csv', 'r', encoding='utf8', newline='') as f:
        reader = csv.reader(f)
        names = list(filter(lambda x: len(x.strip()),
                     map(lambda x: x[3], reader)))

    random.shuffle(names)
    return names[0]


def get_email_message():
    names = []
    with open('./DATA/content.csv', 'r', encoding='utf8', newline='') as f:
        reader = csv.reader(f)
        names = list(filter(lambda x: len(x.strip()),
                     map(lambda x: x[4], reader)))

    random.shuffle(names)
    return names[0]


def set_email_done(email):
    with open('./DATA/email_sent.csv', 'a') as f:
        csv.writer(f).writerow([email])


if __name__ == '__main__':
    print(get_unique_email_to_send())
