import datetime as dt

Year = int(input('Year: '))

first_day = dt.datetime.strptime(f'{Year}-01-01','%Y-%m-%d').date()

for d in range(0,7):
    x = first_day + dt.timedelta(d)

    if x.weekday() == 6:
        first_Sunday = x

All_Sundays = [first_Sunday]

print(All_Sundays)
while All_Sundays[-1].year < Year+1:
    All_Sundays.append(All_Sundays[-1]+dt.timedelta(7))

for i in All_Sundays:
    print(i,i.weekday())
