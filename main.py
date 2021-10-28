import flask
import requests
import json
from Task import Task
from flask import Flask, request, jsonify, url_for, abort, redirect, render_template
from markupsafe import escape

# I KNOW THIS IS VERY SCUFFED BUT YEAH

my_header = {'Accept': 'text/html,application/xhtml+xml,'
                       'application/xml;q=0.9,image/avif,'
                       'image/webp,/;q=0.8',
             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 '
                           'Firefox/93.0'}


def list_all_employees():
    resp = requests.get("https://dummy.restapiexample.com/api/v1/employees",
                        headers=my_header)
    if resp.status_code == 429:
        print("[429]-> TOO MANY REQUESTS")
        return
    json_response = resp.json()
    print_all(json_response)


def list_employee():
    emp_id = input("Enter id: ")
    resp = requests.get("https://dummy.restapiexample.com/api/v1/employee/" + emp_id,
                        headers=my_header)
    if resp.status_code == 429:
        print("[429]-> TOO MANY REQUESTS")
        return
    json_response = resp.json()
    print_one(json_response)


def create_employee():
    employee_object = {"employee_name": [], "employee_salary": [], "employee_age": []}
    emp_name = input("Enter name: ")
    emp_salary = input("Enter salary: ")
    emp_age = input("Enter age: ")

    employee_object["employee_name"].append(emp_name)
    employee_object["employee_salary"].append(emp_salary)
    employee_object["employee_age"].append(emp_age)

    response = requests.post('http://dummy.restapiexample.com/api/v1/create',
                             headers=my_header, data=employee_object)
    if response.status_code == 429:
        print("[429]-> TOO MANY REQUESTS")
        return
    json_resp = response.json()
    print_one(json_resp)


def update_employee():
    emp_id = input("Enter id: ")
    resp = requests.get("https://dummy.restapiexample.com/api/v1/employee/" + emp_id,
                        headers=my_header)
    if resp.status_code == 429:
        print("[429]-> TOO MANY REQUESTS")
        return
    json_response = resp.json()
    if json_response['data'] is None:
        print("[404]-> NO EMPLOYEE FOUND WITH ID: {}".format(emp_id))
        return
    print_one(json_response)
    emp_name = input("Enter new name: ")
    json_response['data']['employee_name'] = emp_name
    put_resp = requests.put("https://dummy.restapiexample.com/public/api/v1/update/" + emp_id,
                            headers=my_header, data=json_response['data'])
    if put_resp.status_code == 429:
        print("[429]-> TOO MANY REQUESTS")
        return
    json_put_response = put_resp.json()
    print_one(json_put_response)


def delete_employee():
    emp_id = input("Enter id: ")
    resp = requests.delete("https://dummy.restapiexample.com/api/v1/delete/" + emp_id,
                           headers=my_header)
    print(resp)
    if resp.status_code == 429:
        print("[429]-> TOO MANY REQUESTS")
        return

    print(resp.json())


def show_average_salary():
    resp = requests.get("https://dummy.restapiexample.com/api/v1/employees",
                        headers=my_header)
    count = 0
    total_salary = 0

    if resp.status_code == 429:
        print("[429]-> TOO MANY REQUESTS")
        return

    for e in resp.json()['data']:
        count += 1
        total_salary += e['employee_salary']

    average = total_salary / count

    print("Average salary: ${:,.2f}".format(average))


def show_age_info():
    min_age = int(input("Enter minimum age: "))
    max_age = int(input("Enter maximum age: "))

    total_salary = 0
    employees = []
    lowest_salary = 10000000000.0
    highest_salary = 0.0
    resp = requests.get("https://dummy.restapiexample.com/api/v1/employees",
                        headers=my_header)
    if resp.status_code == 429:
        print("[429]-> TOO MANY REQUESTS")
        return

    for e in resp.json()['data']:
        if min_age <= e['employee_age'] <= max_age:
            if e['employee_salary'] < lowest_salary:
                lowest_salary = e['employee_salary']
            if e['employee_salary'] > highest_salary:
                highest_salary = e['employee_salary']
            total_salary += e['employee_salary']
            employees.append(e)

    print("Lowest salary: ${:,.2f}".format(lowest_salary))
    print("Highest salary: ${:,.2f}".format(highest_salary))
    print("Average salary: ${:,.2f}".format(total_salary/len(employees)))


def print_one(json_resp):
    print("\nId: {}".format(json_resp['data']['id']))
    print("\tName: {}".format(json_resp['data']['employee_name']))
    print("\tSalary: ${:,.2f}".format(json_resp['data']['employee_salary']))
    print("\tAge: {}".format(json_resp['data']['employee_age']))


def print_all(json_resp):
    for e in json_resp['data']:
        print("\nId: {}".format(e['id']))
        print("\tName: {}".format(e['employee_name']))
        print("\tSalary: ${:,.2f}".format(e['employee_salary']))
        print("\tAge: {}".format(e['employee_age']))


user_input = 0

while user_input != -1:
    print("\nPlease choose an option:")
    print("1. List all Employees")
    print("2. Show Employee detail")
    print("3. Create Employee")
    print("4. Update Employee")
    print("5. Delete Employee")
    print("6. Show average salary")
    print("7. Show age info")
    user_input = input("\nEnter your selection-> ")
    print(user_input)

    if user_input == -1:
        exit(0)

    if str(user_input) == "1":
        list_all_employees()
    elif str(user_input) == "2":
        list_employee()
    elif str(user_input) == "3":
        create_employee()
    elif str(user_input) == "4":
        update_employee()
    elif str(user_input) == "5":
        delete_employee()
    elif str(user_input) == "6":
        show_average_salary()
    elif str(user_input) == "7":
        show_age_info()
