from employee import *

"""
Exercise 1:
Inherit from the classes in employee to implement four roles of the company.
1. PlantDirector:
- has a stable salary and earns a bonus (Hint: Don't forget to override calculate_payroll)
- can increment the salary of all types of employees (Hint: Consider that the attribute to change depends on the employee 
 type. For commission employees increment both the salary and the commission. Google the function isinstance())
 
 2. Worker:
 - earns by the hour
 - works in a specific area
 
 3. Manager
 - has a stable salary
 - can transfer a worker to a specific area
 - raises an error if HR tells him to transfer a salesman to another area
 
 4. Salesman
 - has a stable salary and earns a commission if sales are good
 
Exercise 2:
 1. When changing the ID of a Worker a message should be RETURNED of the form 'Old ID: <old_id>, New ID: <new_id>'.
    Use the change_id() method of the parent class.
"""

class PlantDirector():
    def __init__(self):
        pass

    def increment_salary(self, employee, increment):
        pass

    def calculate_payroll(self):
        pass

class Manager():
    def __init__(self):
        pass

    def area_transfer(self, worker, area):
        pass

class Worker():
    def __init__(self):
        pass

    def change_id():
        pass

class Salesman():
    def __init__(self):
        pass