import time
import numpy as np
import sys
from parser import parseDolphin, parseLesmis, parseNCAA

def page_rank(nodes, inlinks, outlinks, d =0.85, epsilon=1e-8):
    node_list = list(nodes)
    num_nodes = len(node_list)
    idx = {node: i for i, node in enumerate(node_list)}

    M = np.zeros((num_nodes, num_nodes))
    for j, node in enumerate(node_list):
        out = outlinks.get(node, set())
        if out:
            for target in out:
                i = idx[target]
                M[i, j] = 1.0 / len(out)
    # dangling nodes (no out-links)
    dangling = np.array([1.0 if len(outlinks.get(node, set())) == 0 else 0.0 
                         for node in node_list])
    
    pr = np.full(num_nodes, 1.0 / num_nodes)
    iterations = 0
    while True:
        dangling_sum = np.dot(dangling, pr)
        
        new_pr = (1-d) / num_nodes + d * (M @ pr + dangling_sum / num_nodes)
        if np.sum(np.abs(new_pr - pr)) < epsilon:
            break
        pr = new_pr
        iterations += 1
    return pr, node_list, iterations

if __name__ == "__main__":
    filename = sys.argv[1]

    # Timed
    start_read = time.time()

    if "dolphin" in filename.lower():
        nodes, inlinks, outlinks = parseDolphin(filename)
    elif "lesmis" in filename.lower():
        nodes, inlinks, outlinks = parseLesmis(filename)
    else:
        nodes, inlinks, outlinks = parseNCAA(filename)

    end_read = time.time()

    read_time = time.time() - start_read

    start_proc = time.time()
    pr, node_list, iterations = page_rank(nodes, inlinks, outlinks)
    end_proc = time.time()
    proc_time = end_proc - start_proc

    ranked = sorted(zip(node_list, pr), key=lambda x: x[1], reverse=True)
    for rank, (node, score) in enumerate(ranked, 1):
        print(f"{rank} {node} with pagerank: {score}")

    print(f"\nRead time: {read_time:.4f} seconds")
    print(f"Processing time: {proc_time:.4f} seconds")
    print(f"Iterations: {iterations}")
    print(f"Sum of PageRank scores: {sum(pr):.6f}")