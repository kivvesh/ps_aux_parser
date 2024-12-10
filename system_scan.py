import subprocess
import os


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
    return list(users)

def get_count_user_processes(user_process):
    users_count_processes = {}
    for process in user_process:
        if not users_count_processes.get(process.get('user')):
            users_count_processes[process.get('user')] = 1
        else:
            users_count_processes[process.get('user')] += 1
    return users_count_processes


def write_allure(data):



def main():
    user_processes = ps_aux_run()
    users = find_users_system(user_processes)
    count_processes = len(user_processes)
    count_processes_by_user = get_count_user_processes(user_processes)
    sum_cpu = sum([float(process.get('CPU')) for process in user_processes])
    sum_mem = sum([float(process.get('MEM')) for process in user_processes])
    max_cpu = sorted(user_processes, key=lambda x:float(x.get("CPU")), reverse=True)[0]
    max_mem = sorted(user_processes, key=lambda x:float(x.get("MEM")), reverse=True)[0]
    print(max_cpu, max_mem)


if __name__ == '__main__':
    main()



