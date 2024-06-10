import csv

#file_route = "lagos_arg.csv"
file_route = "./lagos_arg.csv"
def my_function(data, *args):
    sub_data = filter(lambda x: x[1] in args and x[3]=='', data)
    return list(sub_data)

with open(file_route, "r") as data_set:
    reader = csv.reader(data_set,delimiter=',')
    header, data = next(reader), list(reader)

result1 = my_function(data, "Chubut", "Río Negro")
result2 = my_function(data, "Neuquén")

print(len(result1), result1)
print(f"\n****\n{len(result2), result2}") 