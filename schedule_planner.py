import os
import random

def getNextLine(f):
    next_line = f.readline()
    while next_line[0] == '#':
        next_line = f.readline()
    new_next_line = ''
    for i in range(len(next_line)):
        if(i <= len(next_line)-2):
            new_next_line += next_line[i]
    return new_next_line


user_option = ''
while user_option != 'c' and user_option != 'b':
    staff = []
    schedule = [['monday', ['morning', [], 4],['afternoon', [], 4.5],['evening', [], 4.5]],['tuesday', ['morning', [], 4],['afternoon', [], 4.5],['evening', [], 4.5]],['wednesday', ['morning', [], 4],['afternoon', [], 4.5],['evening', [], 4.5]],['thursday', ['morning', [], 4],['afternoon', [], 4.5],['evening', [], 4.5]],['friday', ['morning', [], 4],['afternoon', [], 4.5],['evening', [], 4.5]],['saturday', ['morning', [], 6.5],['evening', [], 6.5]],['sunday', ['morning', [], 5.5],['evening', [], 6.5]]]

    f = open("staff.txt", 'r')

    number_of_staff = getNextLine(f)
    for i in range(int(number_of_staff)):
        new_staff = {}
        staff_times = []
        new_staff['hours'] = 0
        name = getNextLine(f)
        new_staff["name"] = name
        boss = getNextLine(f)
        new_staff["boss"] = True if boss == 'y' else False
        sig_other = getNextLine(f)
        if sig_other == 'y':
            other_employee = getNextLine(f)
            new_staff["significant-other"] = other_employee
        else:
            new_staff["significant-other"] = "NOBODY"
        hour_cap = getNextLine(f)
        if hour_cap == "y":
            hours = getNextLine(f)
            new_staff['hour_cap'] = int(hours)
        else:
            new_staff['hour_cap'] = 20
        for j in range(len(schedule)):
            day = [schedule[j][0]]
            for a in range(len(schedule[j])-1):
                available = getNextLine(f)
                day.append([schedule[j][a+1][0], available])
            staff_times.append(day)
        new_staff['availability'] = staff_times
        


        staff.append(new_staff)


    random.shuffle(staff)

    for run in range(2):
        if run == 0:
            for i in range(len(schedule)): #each day
                for j in range(len(schedule[i])-1): #each shift
                    if schedule[i][0] == 'saturday' or schedule[i][0] == 'sunday' or schedule[i][j+1][0] != 'morning' and run == 0: 
                        for person in staff:
                            if person['boss'] == True and person['availability'][i][j+1][1] == 'a' and person['hours'] <= person['hour_cap'] - 6.5:
                                schedule[i][j+1][1].append(person['name'])
                                person['hours'] += schedule[i][j+1][2]
                                break
                        if len(schedule[i][j+1][1]) == 0:
                            for person2 in staff:
                                if person2['boss'] == True and (person2['availability'][i][j+1][1] == 'a' or person2['availability'][i][j+1][1] == 'm') and person2['hours'] <= person['hour_cap'] - 6.5:
                                    schedule[i][j+1][1].append(person2['name'])
                                    person2['hours'] += schedule[i][j+1][2]
                                    break
                            if len(schedule[i][j+1][1]) == 0:
                                print('could not fill boss position')
                    if schedule[i][0] != 'saturday' and schedule[i][0] != 'sunday' and schedule[i][j+1][0] == 'morning' and len(schedule[i][j+1][1]) < 1:
                        added = False
                        for person in staff:
                            if person['availability'][i][j+1][1] == 'a' and person['hours'] <= person['hour_cap'] - 6.5 and person['name'] not in schedule[i][j+1][1] and person['significant-other'] not in schedule[i][j+1][1]:
                                schedule[i][j+1][1].append(person['name'])
                                person['hours'] += schedule[i][j+1][2]
                                added = True
                                break
                        if added == False:
                            for person in staff:
                                if (person['availability'][i][j+1][1] == 'a' or person['availability'][i][j+1][1] == 'm') and person['hours'] <= person['hour_cap'] - 6.5 and person['name'] not in schedule[i][j+1][1] and person['significant-other'] not in schedule[i][j+1][1]:
                                    schedule[i][j+1][1].append(person['name'])
                                    person['hours'] += schedule[i][j+1][2]
                                    added = True
                                    break
                            if added == False:
                                print('cant fill id position')
                    if schedule[i][0] == 'saturday' or schedule[i][0] == 'sunday' or schedule[i][j+1][0] != 'morning': 
                        threshold = 3 + run
                        for person in staff:
                            if person['availability'][i][j+1][1] == 'a' and person['hours'] <= person['hour_cap'] - 6.5 and person['name'] not in schedule[i][j+1][1] and person['significant-other'] not in schedule[i][j+1][1]:
                                schedule[i][j+1][1].append(person['name'])
                                person['hours'] += schedule[i][j+1][2]
                                added = True
                                if len(schedule[i][j+1][1]) >= threshold:
                                    break
                        if len(schedule[i][j+1][1]) < 1:
                            for person in staff:
                                if (person['availability'][i][j+1][1] == 'a' or person['availability'][i][j+1][1] == 'm') and person['hours'] <= person['hour_cap'] - 6.5 and person['name'] not in schedule[i][j+1][1] and person['significant-other'] not in schedule[i][j+1][1]:
                                    schedule[i][j+1][1].append(person['name'])
                                    person['hours'] += schedule[i][j+1][2]
                                    added = True
                                    if len(schedule[i][j+1][1]) >= threshold:
                                        break
                random.shuffle(staff)
        else:
            for i in range(len(schedule)-1, -1, -1): #each day
                for j in range(len(schedule[i])-1): #each shift
                    if schedule[i][0] == 'saturday' or schedule[i][0] == 'sunday' or schedule[i][j+1][0] != 'morning': 
                        threshold = 3 + run
                        for person in staff:
                            if person['availability'][i][j+1][1] == 'a' and person['hours'] <= person['hour_cap'] - 6.5 and person['name'] not in schedule[i][j+1][1] and person['significant-other'] not in schedule[i][j+1][1]:
                                schedule[i][j+1][1].append(person['name'])
                                person['hours'] += schedule[i][j+1][2]
                                if len(schedule[i][j+1][1]) >= threshold:
                                    break
                        if len(schedule[i][j+1][1]) < 1:
                            for person in staff:
                                if (person['availability'][i][j+1][1] == 'a' or person['availability'][i][j+1][1] == 'm') and person['hours'] <= person['hour_cap'] - 6.5 and person['name'] not in schedule[i][j+1][1] and person['significant-other'] not in schedule[i][j+1][1]:
                                    schedule[i][j+1][1].append(person['name'])
                                    person['hours'] += schedule[i][j+1][2]
                                    if len(schedule[i][j+1][1]) >= threshold:
                                        break
                random.shuffle(staff)



    with open('schedule.txt', 'w+') as f:
        f.write('----------------------schedule------------------------\n')
        print('----------------------schedule------------------------')
        for i in range(len(schedule)): #day
            f.write('------' + schedule[i][0] + '------\n')
            print('------' + schedule[i][0] + '------')
            for j in range(len(schedule[i])-1): #shift
                f.write(' ' + schedule[i][j+1][0] + '\n')
                print(' ' + schedule[i][j+1][0])
                for a in range(len(schedule[i][j+1][1])):
                    if schedule[i][0] == 'saturday' or schedule[i][0] == 'sunday' or schedule[i][j+1][0] != 'morning':
                        if a == 0:
                            f.write('    BOS: ' + schedule[i][j+1][1][a] + '\n')
                            print('    BOS: ' + schedule[i][j+1][1][a])
                        elif a == 1:
                            f.write('    ID: ' + schedule[i][j+1][1][a] + '\n')
                            print('    ID: ' + schedule[i][j+1][1][a])
                        else:
                            f.write('    OA: ' + schedule[i][j+1][1][a] + '\n')
                            print('    OA: ' + schedule[i][j+1][1][a])
                    else:
                        f.write('    ID: ' + schedule[i][j+1][1][a] + '\n')
                        print('    ID: ' + schedule[i][j+1][1][a])
        f.write('\n')                
        print('')
        f.write('----------------------staff hours------------------------\n')
        print('----------------------staff hours------------------------')
        average = 0
        for person in staff:
            average += person['hours']
            f.write(person['name'] + ': ' + str(person['hours']) + '\n')
            print(person['name'] + ': ' + str(person['hours']))
        f.write('\n')
        print('')
        f.write('average staff hours: ' + str((average / len(staff))) + '\n')
        print('average staff hours: ' + str((average / len(staff))))
    print('')
    print('please choose an option:')
    print('a) regenerate')
    print('b) save schedule to file')
    print('c) exit')
    user_option = input('')
if user_option == 'c':
    os.remove('schedule.txt')



        



