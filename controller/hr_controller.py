import copy
from model.util import *
from model.util import get_date
from view import terminal as view
from model.data_manager import *
from view.terminal import *
from model.hr.hr import *



def list_employees():
    cls()
    print_table(hr_list, HEADERS)


def add_employee():
    new_employee = []
    new_id = generate_id()
    new_employee.append(new_id)
    for element in HEADERS[1:]:
        if element == HEADERS[BIRTH_DAY]:
            inf = get_date()
        elif element == HEADERS[CLEARANCE]: 
            min = 0
            max = 8
            inf = check_if_number(HEADERS[CLEARANCE],min,max)    
        else:
            inf = get_input(element)
        new_employee.append(inf)
    hr_list.append(new_employee)
    write_table_to_file(DATAFILE, hr_list, separator=';')


def update_employee():
    upd_index = int(get_input("Line number of record to update: "))-1
    update_customer = []
    update_customer.append(hr_list[upd_index][ID])
    k = 1
    for element in HEADERS[1:]:
        inf = get_input(element)
        if inf == '':
            update_customer.append(hr_list[upd_index][k])
        else:
            update_customer.append(inf)
        k+=1
    hr_list[upd_index] = update_customer
    write_table_to_file(DATAFILE, hr_list, separator=';')

def delete_employee():
    del_index = int(get_input("Line number of record to delete"))
    del hr_list[del_index-1]
    write_table_to_file(DATAFILE, hr_list, separator=';')

def get_oldest_and_youngest():
    
    birthday_dates = list_birthdates()

    birthday_dates.sort()

    oldest = birthday_dates[0]
    youngest = birthday_dates[-1]

    for i in range(len(hr_list)):
        if hr_list[i][2] == str(oldest):
            print(f"{hr_list[i][1]} is the oldest employee")
        if hr_list[i][2] == str(youngest):
            print(f"{hr_list[i][1]} is the youngest employee")



def get_average_age():
    birthday_strings = list_separated_strings_birthdays()
    sum_age = 0
    for i in range(len(birthday_strings)):
        YEAR = int(birthday_strings[i][0])
        MONTH = int(birthday_strings[i][1])
        DAY = int(birthday_strings[i][2])
        age = calculate_age(datetime.date(YEAR,MONTH,DAY))
        sum_age += age
    age_average = sum_age / len(birthday_strings)
    age_average = int(age_average) 
    print(f"The average employee age is {age_average} years")



    


def next_birthdays(number_of_days):
    birthday_strings = list_separated_strings_birthdays()
    upcoming_birthdays = []
    today = datetime.date.today()
    YEAR = int(today.year)
    for i in range(len(birthday_strings)):    
        MONTH = int(birthday_strings[i][1])
        DAY = int(birthday_strings[i][2])
        
        birthday = datetime.date(YEAR, MONTH, DAY)
        
        days_difference = birthday - today
        days_difference = days_difference.days

        if 0 < days_difference <= number_of_days:
            upcoming_birthdays.append([hr_list[i][NAME],hr_list[i][BIRTH_DAY]])
    if len(upcoming_birthdays) != 0:
        print(f"In the next {number_of_days} days the following are celebrating their birthday:")
        for i in range(len(upcoming_birthdays)):
            print(f" {'{:12s}'.format(upcoming_birthdays[i][0])} on {upcoming_birthdays[i][1]}")
    else:
        print(f"In the next {number_of_days} days, no one is celebrating their birthday")


def count_employees_with_clearance(clearance_level):
    
    number_of_employees_cleared = 0
    for i in range(len(hr_list)):
        if int(hr_list[i][CLEARANCE]) <= clearance_level:
            number_of_employees_cleared += 1

    return number_of_employees_cleared

    
    


def count_employees_per_department():
    employees_by_department = {}
    for i in range(len(hr_list)):
        if not hr_list[i][DEPARTMENT] in employees_by_department:
            employees_by_department[hr_list[i][DEPARTMENT]] = 1
        else:
            employees_by_department[hr_list[i][DEPARTMENT]] += 1

    return employees_by_department
        

def run_operation(option):
    if option == 1:
        list_employees()
        wait_enter()
    elif option == 2:
        list_employees()
        add_employee()
        list_employees()
        wait_enter()
    elif option == 3:
        list_employees()
        update_employee()
        list_employees()
        wait_enter()
    elif option == 4:
        list_employees()
        delete_employee()
        list_employees()
        wait_enter()
    elif option == 5:
        get_oldest_and_youngest()
        wait_enter()
    elif option == 6:
        get_average_age()
        wait_enter()
    elif option == 7:
        target_days = 14
        next_birthdays(target_days)
        wait_enter()
    elif option == 8:
        SAY = "Input clearance level under which you want to check"
        clearance_level = int(check_if_number(SAY, 0, 8))
        number = count_employees_with_clearance(clearance_level)
        print(f"There are a total of {number} employees with clearance level {clearance_level} or lower")
        wait_enter()
    elif option == 9:
        NumberOfEmployees = count_employees_per_department()
        print_general_results(NumberOfEmployees, "Here are the number of employees by department")
        wait_enter()
    elif option == 0:
        return
    else:
        raise KeyError("There is no such option.")


def display_menu():
    options = ["Back to main menu",
               "List employees",
               "Add new employee",
               "Update employee",
               "Remove employee",
               "Oldest and youngest employees",
               "Employees average age",
               "Employees with birthdays in the next two weeks",
               "Employees with clearance level",
               "Employee numbers by department"]
    view.print_menu("Human resources", options)


def menu():
    operation = None
    while operation != '0':
        display_menu()
        try:
            operation = view.get_input("Select an operation")
            run_operation(int(operation))
        except KeyError as err:
            view.print_error_message(err)
