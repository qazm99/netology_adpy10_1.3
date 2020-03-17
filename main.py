from qazm import posintput


class Contact:
    def __init__(self, fname: str, lname: str, phone_number: (str, int), *args, special: bool = False, **kwargs):
        if isinstance(fname, str) and isinstance(lname, str) and isinstance(phone_number, (str, int)):

            self.contaсt_main_dict = dict(fname=fname, lname=lname,
                                          phone_number=phone_number if isinstance(phone_number, str) else str(
                                              phone_number), special=special)
            self.contaсt_add_inform = {}
            for num_argument, contact_argument in enumerate(args):
                self.contaсt_add_inform.update({f'Дополнительный контакт {num_argument + 1}': contact_argument})
            for contact_key, contact_argument in kwargs.items():
                self.contaсt_add_inform.update({contact_key: contact_argument})
        else:
            print(f'некорретные аргументы {fname}, {lname}, {phone_number}')

    def __str__(self):
        result_contact_info = f'Имя: {self.contaсt_main_dict.get("fname")}\n' + \
                              f'Фамилия: {self.contaсt_main_dict.get("lname")}\n' + \
                              f'Телефон: {self.contaсt_main_dict.get("phone_number")}\n' + \
                              f'В избранных: {"Да" if self.contaсt_main_dict.get("special") == True else "Нет"}\n'
        if len(self.contaсt_add_inform) > 0:
            result_contact_info += 'Дополнительная информация: \n'
            for contact_key, contact_argument in self.contaсt_add_inform.items():
                result_contact_info += f'{contact_key}: {contact_argument}\n'
        return result_contact_info


class PhoneBook:
    def __init__(self, name_phonebook):
        self.name_phonebook = name_phonebook
        self.contact_list = []

    def print_contacts(self):
        for contact in self.contact_list:
            print(contact)

    def add_contact(self, contact):
        if isinstance(contact, Contact):
            self.contact_list.append(contact)
            return True
        else:
            return False

    def del_contact_of_phone_number(self, phone_number):
        number_for_delete = []
        for number_contact, contact in enumerate(self.contact_list):
            if contact.contaсt_main_dict.get('phone_number') == phone_number:
                number_for_delete.append(number_contact)
        for number in reversed(number_for_delete):
            self.contact_list.pop(number)
        return len(number_for_delete)

    def find_all_special_phone(self):
        phones_number_special = set()
        for contact in self.contact_list:
            if contact.contaсt_main_dict.get('special'):
                phones_number_special.add(contact.contaсt_main_dict.get('phone_number'))
        return phones_number_special

    def find_contact_of_fname_lname(self, fname, lname):
        if isinstance(fname, str) and isinstance(lname, str):
            find_contact_set = set()
            for contact in self.contact_list:
                if contact.contaсt_main_dict.get('fname').upper().strip() == fname.upper().strip() \
                        and contact.contaсt_main_dict.get('lname').upper().strip() == lname.upper().strip():
                    find_contact_set.add(contact)
            return find_contact_set
        else:
            print('недопустимые аргументы, возможно только string')

    def read_from_file(self, filename):
        result_read = False
        with open(filename, encoding='utf-8') as file:
            for line in file.readlines():
                arguments_list = []
                karguments_dict = {}
                for argument in line.strip().split(','):
                    ready_argument = argument.strip()
                    is_dict = ready_argument.find('=', 1, len(ready_argument) - 1)
                    if is_dict != -1:
                        karguments_dict.update(
                            {ready_argument[0:is_dict]: ready_argument[is_dict + 1:len(ready_argument) + 1]})
                    else:
                        pass
                        arguments_list.append(ready_argument)
                    arguments_tuple = tuple(arguments_list[3:])
                if len(arguments_list) >= 3:
                    if self.add_contact(Contact(arguments_list[0], arguments_list[1], arguments_list[2],
                                                *arguments_tuple, **karguments_dict)):
                        result_read = True
                else:
                    print('Недостаточно аргументов для записи контакта')
        return result_read


def adv_print(*args, **kwargs):
    def log_print(string_to_print, file_log):
        print(string_to_print)
        with open(file_log, 'a', encoding='utf-8') as file:
            file.writelines(string_to_print + '\n')

    start_param = kwargs.get('start_param')
    max_line = kwargs.get('max_line')
    in_file = kwargs.get('in_file').strip()
    print(start_param if start_param else '')
    string_accum = ''
    for argument in args:
        string_accum += argument.__str__() + ' '
    string_accum.replace('\n', ' ')
    if max_line:
        while len(string_accum) > 0:
            log_print(string_accum[:max_line], in_file) if len(in_file) > 0 else print(string_accum[:max_line])
            string_accum = string_accum[max_line:]
    else:
        log_print(string_accum, in_file) if len(in_file) > 0 else print(string_accum)


if __name__ == '__main__':
    while True:
        print('Сейчас попробуем поработать с телефонной книгой \n' +
              'Давайте попробуем создать Телефонную книгу')
        main_phonebook = PhoneBook(input('Введите название телефонной книги: '))
        print(f'Работаем с книгой: {main_phonebook.name_phonebook}')
        read_success_flag = False
        while not read_success_flag:
            try:
                file_to_read = 'data_phone'
                if input('Заполнить телефонную книгу из вашего фала?(да/нет): ').upper().strip() == 'ДА':
                    file_to_read = input('Введите имя файла:')
                else:
                    print(f'Тогда я считаю файл {file_to_read}')
                read_success_flag = main_phonebook.read_from_file(file_to_read)
            except FileNotFoundError:
                print('Ошибка чтения из файла, такого файла не найдено')
        if input('Вывести информацию о контактах в телефонной книге?(да/нет): ').upper().strip() == 'ДА':
            main_phonebook.print_contacts()
        if input('Хотите удалить контакт из книжки по номеру телефона?(да/нет): ').upper().strip() == 'ДА':
            print('Всего удалено контактов: ' +
                  f'{main_phonebook.del_contact_of_phone_number(input("Введите номер телефона: "))}')
        if input('Показать все  телефоны избранных контактов?(да/нет): ').upper().strip() == 'ДА':
            for contact_phone in main_phonebook.find_all_special_phone():
                print(contact_phone)
        if input('Поищем контакт по имени и фамилии?(да/нет): ').upper().strip() == 'ДА':
            for contact in main_phonebook.find_contact_of_fname_lname(input('Введите имя для поиска:'),
                                                                      input('Введите фамилию для поиска:')):
                print(contact)
        while True:
            if input('Протестируем функцию параметризированного отображения строки?(да/нет): ').upper().strip() == 'ДА':
                adv_print(input('Введите строку для отображения: '),
                          max_line=posintput('Введите максимальное количество символов в строке: '),
                          start_param=input('Введите приветственное сообщение: '),
                          in_file=input('В какой файл будем писать лог? '))
            else:
                break
        if input('Попробуем снова?(да/нет): ').upper() != 'ДА':
            break
