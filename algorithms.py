import math
import random
import numpy as np

def floyd_warshall_modified(P, n):
    R = np.copy(P)
    for i in range(n):
        R[i][i] = 1
    for k in range(n):
        for i in range(n):
            for j in range(n):
                R[i][j] = R[i][j] or (R[i][k] and R[k][j])
    return R

def compute_distances(a, b, c, d, n):
    lengths = []
    for i in range(n):
        length = math.sqrt((c[i] - a[i]) ** 2 + (d[i] - b[i]) ** 2)
        lengths.append(length)
    return lengths

def do_segments_intersect(a1, b1, c1, d1, a2, b2, c2, d2):
    def cross_product(x1, y1, x2, y2):
        return x1 * y2 - y1 * x2

    def is_point_on_segment(x, y, a, b, c, d):
        return (x >= min(a, c) and x <= max(a, c) and
                y >= min(b, d) and y <= max(b, d))

    dx1 = c1 - a1
    dy1 = d1 - b1
    dx2 = c2 - a2
    dy2 = d2 - b2

    cross_product_val = cross_product(dx1, dy1, dx2, dy2)

    if cross_product_val == 0:
        return (is_point_on_segment(a2, b2, a1, b1, c1, d1) or
                is_point_on_segment(c2, d2, a1, b1, c1, d1) or
                is_point_on_segment(a1, b1, a2, b2, c2, d2) or
                is_point_on_segment(c1, d1, a2, b2, c2, d2))
    else:
        t = cross_product(a2 - a1, b2 - b1, dx2, dy2) / cross_product_val
        u = cross_product(a2 - a1, b2 - b1, dx1, dy1) / cross_product_val
        return t >= 0 and t <= 1 and u >= 0 and u <= 1

def create_adjacency_matrix(a, b, c, d, n):
    P = np.zeros((n, n), dtype=int)
    for i in range(n):
        for j in range(n):
            if i != j:
                if do_segments_intersect(a[i], b[i], c[i], d[i], a[j], b[j], c[j], d[j]):
                    P[i][j] = 1
    return P

def greedy_algorithm(n, a, b, c, d):
    lengths = compute_distances(a, b, c, d, n)
    P = create_adjacency_matrix(a, b, c, d, n)
    R = floyd_warshall_modified(P, n)
    
    max_reachable = -1
    best_tunnel = 0
    best_length = -1
    
    for i in range(n):
        reachable_count = sum(R[i])
        if reachable_count > max_reachable:
            max_reachable = reachable_count
            best_tunnel = i
            best_length = lengths[i]
        elif reachable_count == max_reachable and lengths[i] > best_length:
            best_tunnel = i
            best_length = lengths[i]
    
    x = [0] * n
    total_length = 0
    
    x[best_tunnel] = 1
    total_length += lengths[best_tunnel]
    
    for j in range(n):
        if j != best_tunnel and R[best_tunnel][j] == 1:
            x[j] = 1
            total_length += lengths[j]
    
    return x, total_length

def probabilistic_algorithm(n, a, b, c, d, m):
    lengths = compute_distances(a, b, c, d, n)
    P = create_adjacency_matrix(a, b, c, d, n)
    R = floyd_warshall_modified(P, n)
    
    total_length_sum = sum(lengths)
    probabilities = [l / total_length_sum for l in lengths]
    
    best_x = [0] * n
    best_L = 0
    
    for _ in range(m):
        xm = [0] * n
        Lm = 0
        t = random.choices(range(n), weights=probabilities, k=1)[0]
        xm[t] = 1
        Lm += lengths[t]
        
        for j in range(n):
            if j != t and R[t][j] == 1:
                xm[j] = 1
                Lm += lengths[j]
        
        if Lm > best_L:
            best_L = Lm
            best_x = xm[:]
    
    return best_x, best_L