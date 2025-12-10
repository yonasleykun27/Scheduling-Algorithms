# Algorithm: Round Robin (RR)

def calculate_round_robin(processes, time_quantum):
    n = len(processes)
    # Sort by arrival time initially
    processes.sort(key=lambda x: x['arrival_time'])
    
    # Create a copy of burst times to track remaining time
    remaining_burst = {p['id']: p['burst_time'] for p in processes}
    
    current_time = 0
    queue = []
    
    # Track which processes are currently in the queue
    in_queue = {p['id']: False for p in processes}
    
    # Add first process(es) that arrived at time 0
    for p in processes:
        if p['arrival_time'] <= current_time and not in_queue[p['id']]:
            queue.append(p)
            in_queue[p['id']] = True

    completed_list = []
    
    print(f"--- Round Robin Execution Log (Quantum: {time_quantum}) ---")

    while queue:
        # Get next process
        p = queue.pop(0)
        pid = p['id']
        
        # Execute
        if remaining_burst[pid] > time_quantum:
            # Process runs for full quantum
            current_time += time_quantum
            remaining_burst[pid] -= time_quantum
            print(f"Time {current_time}: {pid} ran (Remaining: {remaining_burst[pid]})")
        else:
            # Process finishes
            current_time += remaining_burst[pid]
            remaining_burst[pid] = 0
            
            # Calculate stats
            p['completion_time'] = current_time
            p['turnaround_time'] = p['completion_time'] - p['arrival_time']
            p['waiting_time'] = p['turnaround_time'] - p['burst_time']
            completed_list.append(p)
            print(f"Time {current_time}: {pid} Finished!")

        # IMPORTANT: Check for new arrivals BEFORE re-adding current process
        for new_p in processes:
            if (new_p['arrival_time'] <= current_time and 
                remaining_burst[new_p['id']] > 0 and 
                not in_queue[new_p['id']]):
                
                queue.append(new_p)
                in_queue[new_p['id']] = True

        # If current process is not done, add it back to the END of queue
        if remaining_burst[pid] > 0:
            queue.append(p)

    return completed_list

def print_table(results):
    # Sort results by ID just for cleaner printing
    results.sort(key=lambda x: x['id'])
    
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
        {'id': 'P1', 'arrival_time': 0, 'burst_time': 5},
        {'id': 'P2', 'arrival_time': 1, 'burst_time': 3},
        {'id': 'P3', 'arrival_time': 2, 'burst_time': 1},
        {'id': 'P4', 'arrival_time': 3, 'burst_time': 2}
    ]
    
    quantum = 2
    final_data = calculate_round_robin(input_processes, quantum)
    print_table(final_data)