import random
import math

import numpy as np
from tqdm import tqdm

num_request = 1008 #请求数量
initial_t = 100000 #初始温度
lowest_t = 0.03 #最低温度
iteration = 5000 #迭代次数
M = 1500 #最多不发生改变的次数
alpha = 0.99 #退火率

#导入数据
requests = []
with open('运筹学代码/requests.txt', 'r') as file:
    for line in file:
        cpu, memory = line.strip().split('\t')
        requests.append((int(cpu), int(memory)))
server_specs = []
with open('运筹学代码/requests.txt') as file:
    for line in file:
        cpu, memory = line.strip().split('\t')
        server_specs.append((int(cpu), int(memory)))


#初始解
def calculate_server_idx(server_specs, requests):
    server_idx = 0
    #服务器资源使用情况
    num_servers = len(server_specs)
    server_utilization = np.zeros((num_servers, 2))
    for req_idx, (req_cpu, req_memory) in enumerate(requests):
        if server_utilization[server_idx][0] + req_cpu <= server_specs[server_idx][0] and \
            server_utilization[server_idx][1] + req_memory <= server_specs[server_idx][1]:
            server_utilization[server_idx][0] = server_utilization[server_idx][0] + req_cpu
            server_utilization[server_idx][1] = server_utilization[server_idx][1] + req_memory
            continue
        else:
            server_idx += 1
    end_idx = server_idx + 1
    return end_idx

end_idx_1 = calculate_server_idx(server_specs, requests)
print("最初的服务器数量", end_idx_1)

#内外循环
pbar = tqdm(total=iteration)
current_t = initial_t
while (current_t > lowest_t):
    count_m = 0
    count_iteration = 0
    while (count_m < M and count_iteration < iteration):
        i=0
        j=0
        while(i==j):#防止随机了同一个资源
            i=random.randint(0,1007)
            j=random.randint(0,1007)
        #随机互换两个资源的位置
        requests[i], requests[j] = requests[j], requests[i]
        end_idx = calculate_server_idx(server_specs, requests)
        idx_delta = end_idx - end_idx_1
        rand=random.random()
        exp_d=math.exp(-idx_delta/current_t)
        if idx_delta<0:
            end_idx_1 = end_idx
        elif exp_d>rand:
            end_idx_1 = end_idx
        else:
            count_m=count_m+1
        count_iteration=count_iteration+1
        pbar.update(1)
    current_t=alpha*current_t#改变温度
print("所需服务器的最小数目：",end_idx_1)



