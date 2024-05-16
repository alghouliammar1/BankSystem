import role

plant_director = role.PlantDirector(9999, 'John', 1000, 5000)
manager = role.Manager(8888, 'Camila', 800)
worker_1 = role.Worker(3456, 'Bryan', 25, 13, "Paint")
worker_2 = role.Worker(9044, 'James', 35, 34, "Repair")
salesman = role.Salesman(8390, 'Liu', 500, 300)

# Check the bonus of the plant director
assert plant_director.calculate_payroll() == plant_director.weekly_salary + plant_director.bonus

# Increment salary of manager
old_salary = manager.weekly_salary
increment = 50
plant_director.increment_salary(manager, increment)
new_salary = manager.weekly_salary
assert new_salary == (old_salary + increment)

# Change area of worker
old_area = worker_1.area
manager.area_transfer(worker_1, "Assembly")
assert worker_1.area == "Assembly"

# Wrongly try to transfer salesman
try:
    manager.area_transfer(salesman, "Assembly")
    raise Exception("Chaos a salesman was transferred!")
except ValueError as e:
    print(e)