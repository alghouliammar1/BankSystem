# Slide 6
class Employee:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __str__(self):
        return f'Employee: {self.id} - {self.name}'

    def change_id(self, id):
        self.id = id

# Create employee
employee_1 = Employee(1234, "Max")
print(employee_1)

# Change id
employee_1.change_id(1000)
print(employee_1)


# Slide 7
import hr_redundant as hr_red

# Create employees
salary_employee = hr_red.SalaryEmployee(5253, 'Debby', 400)
hourly_employee = hr_red.HourlyEmployee(1890, 'Jane', 20, 15)
commission_employee = hr_red.CommissionEmployee(5678, 'Tom', 400, 100)

## List with employees
all_employees = [salary_employee, hourly_employee, commission_employee]

## Calculate Payroll
payroll_system = hr_red.PayrollSystem()
payroll_system.calculate_payroll(all_employees)

"""
Problems:
1. Redundant code -> Inheritance!
2. Class explosion problem -> Modularize!
"""
# Slide 9

## Inherit everything
class SalaryEmployee(Employee):
    pass

salary_employee = SalaryEmployee(5253, 'Debby')
print(salary_employee)

## Option 1
class SalaryEmployee(Employee):
    def __init__(self, id, name, weekly_salary):
        Employee.__init__(self, id, name)
        self.weekly_salary = weekly_salary

    def calculate_payroll(self):
        return self.weekly_salary

salary_employee = SalaryEmployee(5253, 'Debby', 400)
print(f'Salary: {salary_employee.calculate_payroll()}')

## Option 2
class SalaryEmployee(Employee):
    def __init__(self, id, name, weekly_salary):
        super().__init__(id, name)
        self.weekly_salary = weekly_salary

    def calculate_payroll(self):
        return self.weekly_salary

salary_employee = SalaryEmployee(5253, 'Debby', 400)
print(f'Salary: {salary_employee.calculate_payroll()}')

import employee
import hr

## Create employees
base_employee = employee.Employee(1234, 'Anna')
salary_employee = employee.SalaryEmployee(5253, 'Debby', 400)
hourly_employee = employee.HourlyEmployee(1890, 'Jane', 20, 15)
commission_employee = employee.CommissionEmployee(5678, 'Tom', 400, 100)

## List with employees
all_employees = [salary_employee, hourly_employee, commission_employee]

## Calculate Payroll
payroll_system = hr.PayrollSystem()
payroll_system.calculate_payroll(all_employees)

# Slide 12
import employee
import hr

class BoardMember(Employee):
    def __init__(self, id, name, votes):
        super().__init__(id, name)
        self.votes = votes

    def __str__(self):
        s = super().__str__()
        s += f'\nNumber of votes: {self.votes}'
        return s

board_member = BoardMember(7878, 'Farida', 3)
print(board_member)