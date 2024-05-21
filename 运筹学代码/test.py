import numpy as np
from collections import deque

def greedy_algorithm(requests, server_specs):
    num_requests = len(requests)
    num_servers = len(server_specs)
    # 服务器资源利用情况
    server_utilization = np.zeros((num_servers, 2))
    buffer_size = 1
    buffer = deque()
    num_used_servers = 0
    max_used_servers = 0
    for req_idx, (req_cpu, req_memory) in enumerate(requests):
        # 寻找可用的服务器
        selected_server = None
        max_utilization = -1
        for server_idx in range(num_servers):
            if server_utilization[server_idx][0] + req_cpu <= server_specs[server_idx][0] and \
                    server_utilization[server_idx][1] + req_memory <= server_specs[server_idx][1]:
                # 计算服务器利用率
                cpu_utilization = server_utilization[server_idx][0] / server_specs[server_idx][0]
                memory_utilization = server_utilization[server_idx][1] / server_specs[server_idx][1]
                server_utilization_ratio = cpu_utilization * memory_utilization
                if server_utilization_ratio > max_utilization:
                    selected_server = server_idx
                    max_utilization = server_utilization_ratio
        # 如果找到可用的服务器，则将请求加入缓冲区
        if selected_server is not None:
            buffer.append((req_idx, selected_server))
            print(buffer)
        # 处理队列中的请求
        req_idx, server_idx = buffer.popleft()
        req_cpu, req_memory = requests[req_idx]
        server_utilization[server_idx][0] += req_cpu
        server_utilization[server_idx][1] += req_memory
        num_used_servers = server_idx
        max_used_servers=max(max_used_servers,server_idx)
    return max_used_servers

# 导入示例数据
requests = []
with open('requests.txt', 'r') as file:
    for line in file:
        cpu, memory = line.strip().split('\t')
        requests.append((int(cpu), int(memory)))
server_specs = []
with open('server_info.txt') as file:
    for line in file:
        cpu, memory = line.strip().split('\t')
        server_specs.append((int(cpu), int(memory)))
# 使用贪心算法求解
num_servers = greedy_algorithm(requests, server_specs)
print("所需服务器的最小数目:", num_servers+1)
