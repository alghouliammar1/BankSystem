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

class PlantDirector(SalaryEmployee):
    def __init__(self, id, name, weekly_salary, bonus):
        super().__init__(id, name, weekly_salary)
        self.bonus = bonus

    def increment_salary(self, employee, increment):
        if isinstance(employee, SalaryEmployee):
            employee.weekly_salary += increment
        elif isinstance(employee, HourlyEmployee):
            employee.hourly_rate += increment
        elif isinstance(employee, CommissionEmployee):
            employee.weekly_salary += increment
            employee.commission += increment

    def calculate_payroll(self):
        return self.weekly_salary + self.bonus

class Worker(HourlyEmployee):
    def __init__(self, id, name, hours_worked, hourly_rate, area):
        super().__init__(id, name, hours_worked, hourly_rate)
        self.area = area

    def change_id(self, id):
        old_id = self.id
        super.change_id(id)
        return f'Old ID: {old_id}, New ID: {self.id}'
class Manager(SalaryEmployee):
    def __init__(self, id, name, weekly_salary):
        super().__init__(id, name, weekly_salary)

    def area_transfer(self, worker, new_area):
        if isinstance(worker, Salesman):
            raise ValueError('Only workers can get transferred.')
        worker.area = new_area

class Salesman(CommissionEmployee):
    def __init__(self, id, name, weekly_salary, commission, sales_good):
        super().__init__(id, name, weekly_salary, commission)