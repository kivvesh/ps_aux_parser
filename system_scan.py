import subprocess
import os

from datetime import datetime


ROOT_DIR = os.getcwd()


def ps_aux_run():
    exe_results = subprocess.run(['ps','aux'], stdout=subprocess.PIPE, text=True)

    output = exe_results.stdout
    lines = output.splitlines()
    processes = lines[1:]
    user_processes = []
    for process in processes:
        values = process.split()
        user_process = {
            'user': values[0],
            'PID': values[1],
            'CPU': values[2],
            'MEM': values[3],
            'COMMAND': ' '.join(values[10:]),
        }
        user_processes.append(user_process)
    return user_processes


def find_users_system(user_processes):
    users = set([process.get('user') for process in user_processes])
    return ', '.join(list(users))

def get_count_user_processes(user_process):
    users_count_processes = {}
    for process in user_process:
        if not users_count_processes.get(process.get('user')):
            users_count_processes[process.get('user')] = 1
        else:
            users_count_processes[process.get('user')] += 1
    users_count_processes = dict(sorted(users_count_processes.items(), key=lambda x:x[1],reverse=True))
    return '\n'.join([f'{key}: {value}' for key, value in users_count_processes.items()])


def write_allure(data):
    name_file = f'{datetime.now().strftime("%d-%m-%Y-%H:%M")}-scan.txt'

    with open(os.path.join(ROOT_DIR,name_file),'w', encoding='utf-8') as file:
        file.write(
f'''Отчёт о состоянии системы:
Пользователи системы: {data.get("users")}
Процессов запущено: {data.get("count_processes")}

Пользовательских процессов:
{data.get("count_processes_by_user")}

Всего памяти используется: {data.get("sum_mem")}%
Всего CPU используется: {data.get("sum_cpu")}%
Больше всего памяти использует: {data.get("name_max_mem")}
Больше всего CPU использует: {data.get("name_max_cpu")}''')


def main():
    user_processes = ps_aux_run()
    users = find_users_system(user_processes)
    count_processes = len(user_processes)
    count_processes_by_user = get_count_user_processes(user_processes)
    sum_cpu = sum([float(process.get('CPU')) for process in user_processes])
    sum_mem = sum([float(process.get('MEM')) for process in user_processes])
    max_cpu = sorted(user_processes, key=lambda x:float(x.get("CPU")), reverse=True)[0]
    max_mem = sorted(user_processes, key=lambda x: float(x.get("MEM")), reverse=True)[0]
    name_max_cpu = max_cpu.get('COMMAND') if len(max_cpu.get('COMMAND')) <= 20 else max_cpu.get('COMMAND')[:20]
    name_max_mem = max_mem.get('COMMAND') if len(max_mem.get('COMMAND')) <= 20 else max_mem.get('COMMAND')[:20]
    write_allure(
        {
            'users':users,
            'count_processes':count_processes,
            'count_processes_by_user': count_processes_by_user,
            'sum_cpu':sum_cpu,
            'sum_mem':sum_mem,
            'name_max_cpu':name_max_cpu,
            'name_max_mem':name_max_mem,
        }
    )




if __name__ == '__main__':
    main()



