import math


def knapsack__(weights, values, capacity, max_items):
    n = len(weights)
    # Create a table to store the maximum values at each capacity and number of items
    capacity = math.ceil(capacity)
    max_items = math.ceil(max_items)
    dp = [
        [[0 for _ in range(capacity + 1)] for _ in range(max_items + 1)]
        for _ in range(n + 1)
    ]

    for i in range(1, n + 1):
        for j in range(1, max_items + 1):
            for w in range(1, capacity + 1):
                if weights[i - 1][0] <= w:
                    dp[i][j][w] = max(
                        values[i - 1] + dp[i - 1][j - 1][w - weights[i - 1][0]],
                        dp[i - 1][j][w],
                    )
                else:
                    dp[i][j][w] = dp[i - 1][j][w]

    # Find the selected items
    selected_items = []
    w = capacity
    for i in range(n, 0, -1):
        if dp[i][max_items][w] != dp[i - 1][max_items][w]:
            selected_items.append(weights[i - 1])
            w -= weights[i - 1][0]
            max_items -= 1

    return selected_items


def knapsack(weights, values, capacity):
    n = len(weights)
    capacity = math.ceil(capacity)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    selected = [[False] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(1, capacity + 1):
            if weights[i - 1][0] <= w:
                if values[i - 1] + dp[i - 1][w - weights[i - 1][0]] > dp[i - 1][w]:
                    dp[i][w] = values[i - 1] + dp[i - 1][w - weights[i - 1][0]]
                    selected[i][w] = True
                else:
                    dp[i][w] = dp[i - 1][w]
            else:
                dp[i][w] = dp[i - 1][w]

    selected_weights = []
    i, w = n, capacity
    while i > 0 and w > 0:
        if selected[i][w]:
            selected_weights.append(weights[i - 1])
            w -= weights[i - 1][0]
        i -= 1

    return selected_weights


def knapsack_with_tolerance(weights, values, capacity):
    n = len(weights)
    capacity = math.ceil(capacity)

    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    selected = [[False] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(1, capacity + 1):
            if weights[i - 1][0] <= w:
                if values[i - 1] + dp[i - 1][w - weights[i - 1][0]] > dp[i - 1][w]:
                    dp[i][w] = values[i - 1] + dp[i - 1][w - weights[i - 1][0]]
                    selected[i][w] = True
                else:
                    dp[i][w] = dp[i - 1][w]
            else:
                dp[i][w] = dp[i - 1][w]

    selected_weights = []
    i, w = n, capacity
    while i > 0 and w > 0:
        if selected[i][w]:
            selected_weights.append(weights[i - 1])
            w -= weights[i - 1][0]
        i -= 1

    # Check if the total weight exceeds the maximum capacity by only 10%
    total_weight = sum([sw[0] for sw in selected_weights])
    if total_weight > 1.1 * capacity:
        # Remove the last item until the weight is within the permitted range
        while total_weight >= 1.1 * capacity:
            last_weight = selected_weights.pop()
            total_weight -= last_weight[0]

    return selected_weights
