# Algorithm: Shortest Job First (SJF) - Non-Preemptive

def calculate_sjf(processes):
    n = len(processes)
    # Sort by Arrival Time first to help with initial logic
    processes.sort(key=lambda x: x['arrival_time'])
    
    completed = 0
    current_time = 0
    visited = [False] * n
    results = []

    print("--- SJF Execution Log ---")
    
    while completed < n:
        # 1. Find all processes that have arrived by current_time and are not done
        candidates = []
        for i in range(n):
            if processes[i]['arrival_time'] <= current_time and not visited[i]:
                candidates.append((processes[i], i)) # Store process and its original index
        
        if not candidates:
            # If no process has arrived, move time forward
            current_time += 1
            continue

        # 2. Select the one with Minimum Burst Time
        # The key for min() is the burst_time of the process
        best_candidate = min(candidates, key=lambda x: x[0]['burst_time'])
        proc = best_candidate[0]
        idx = best_candidate[1]

        # 3. Execute the process (Non-preemptive: it runs fully)
        start_time = current_time
        completion_time = start_time + proc['burst_time']
        
        # Calculate Metrics
        turnaround_time = completion_time - proc['arrival_time']
        waiting_time = turnaround_time - proc['burst_time']
        
        # Save results
        proc['completion_time'] = completion_time
        proc['turnaround_time'] = turnaround_time
        proc['waiting_time'] = waiting_time
        
        results.append(proc)
        visited[idx] = True
        completed += 1
        current_time = completion_time
        
        print(f"Time {start_time} -> {completion_time}: Process {proc['id']} executed.")

    return results

def print_table(results):
    print("\n{:<5} {:<5} {:<5} {:<5} {:<5} {:<5}".format(
        "PID", "AT", "BT", "CT", "TAT", "WT"))
    print("-" * 40)
    
    total_wt = 0
    total_tat = 0
    
    for p in results:
        print("{:<5} {:<5} {:<5} {:<5} {:<5} {:<5}".format(
            p['id'], p['arrival_time'], p['burst_time'], 
            p['completion_time'], p['turnaround_time'], p['waiting_time']
        ))
        total_wt += p['waiting_time']
        total_tat += p['turnaround_time']
        
    print("-" * 40)
    print(f"Average Waiting Time: {total_wt / len(results):.2f}")
    print(f"Average Turnaround Time: {total_tat / len(results):.2f}")

# --- Main Execution ---
if __name__ == "__main__":
  
    input_processes = [
        {'id': 'P1', 'arrival_time': 0, 'burst_time': 7},
        {'id': 'P2', 'arrival_time': 2, 'burst_time': 4},
        {'id': 'P3', 'arrival_time': 4, 'burst_time': 1},
        {'id': 'P4', 'arrival_time': 5, 'burst_time': 4}
    ]
    
    final_data = calculate_sjf(input_processes)

    print_table(final_data)
