def _one_round(A, otus, count, group, node_dict):
    div = []  # sum of each row
    for f in A:
        div.append(sum(f))
    n = len(A)  # number of otus

    # two nodes only:  we're done
    if n == 2:
        dist = A[1][0]
        if dist < 0:
            node_dict[otus[0] + 1] = [(otus[0], abs(dist)), (otus[1], 0)]
        else:
            node_dict[otus[0] + 1] = [(otus[0], 0), (otus[1], dist)]
        return None, otus

    # find the i,j to work on using divergence
    i, j = 1, 0
    low_value = A[1][0]
    for r, row in enumerate(A):
        if r == 0:
            continue
        for c, col in enumerate(row):
            if c >= r:
                continue
            dist = A[r][c]
            first = div[c]
            second = div[r]
            correction = (first + second) / float(n - 2)
            value = dist - correction
            if value <= low_value:
                i, j, low_value = r, c, value

    # merge i and j entries
    # calculate distance of new node from tips
    #
    # dist from node[i]
    dist = A[i][j]
    diff = div[i] - div[j]
    dist_i = dist / 2.0 + diff / (2.0 * (n - 2))
    dist_j = dist - dist_i
    if dist_i < 0:
        dist_j += abs(dist_i)
        dist_i = 0.0
    elif dist_j < 0:
        dist_i += abs(dist_j)
        dist_j = 0.0
    else:
        if dist_i < dist_j:
            dist_j += abs(dist_i)
            dist_i = 0.0
        else:
            dist_i += abs(dist_j)
            dist_j = 0.0
    node = [(otus[i], dist_i), (otus[j], dist_j)]
    node_dict[group] = node

    # calculate distances to new node
    # i,j assigned above
    tL = list()
    ij_dist = A[i][j]
    for k in range(len(A[0])):
        if k == i or k == j:
            continue
        dist = (A[i][k] + A[j][k] - ij_dist) / 2.0
        tL.append(dist)

    # remove columns and rows involving i or j
    if i < j:
        i, j = j, i
    assert j < i
    for k in [i, j]:    # larger first
        A.pop(k)
        for tmp in A:
            tmp.pop(k)
    # correct the otu names:
    otus = [group] + otus[:j] + otus[j + 1:i] + otus[i + 1:]

    new_rol = [0] + tL
    A.insert(0, new_rol)

    for pos in range(1, len(A)):
        A[pos].insert(0, tL[pos - 1])

    return A, otus


def nj_matrix(orig_A, orig_otus):
    otus = orig_otus[:]
    A = []
    for i in range(len(orig_A)):
        A.append([])
        for j in range(len(orig_A[i])):
            A[i].append(float(orig_A[i][j]))
    count = 0
    group = 0
    node_dict = dict()
    while True:
        A, otus = _one_round(A, otus, count, group, node_dict)
        group += 1
        if A is None:
            break
        count += 1
    return node_dict


def nj(docs, conn):
    A = _create_matrix(docs, conn)
    otus = [x.name for x in docs]
    return nj_matrix(A, otus)


def _create_matrix(docs, conn):
    matrix = [[0] * len(docs) for x in xrange(len(docs))]
    h = dict(zip(docs, range(len(docs))))
    for doc1, doc2, value in conn:
        matrix[h[doc1]][h[doc2]] = 1 - value
        matrix[h[doc2]][h[doc1]] = 1 - value
    for i in xrange(len(docs)):
        matrix[i][i] = 0
    return matrix


def merge(node_dict, diff=0.0):
    merge = []
    for node in sorted(node_dict):
        if not [x[1] for x in node_dict[node] if x[1] > diff]:
            merge.append(node)
    for node in sorted(node_dict):
        final_child = []
        for child in node_dict[node]:
            if isinstance(child[0], int) and (child[0] in merge or node in merge):
                for c_child in node_dict[child[0]]:
                    final_child.append((c_child[0], c_child[1] + child[1]))
                del node_dict[child[0]]
            else:
                final_child.append(child)
        node_dict[node] = final_child
