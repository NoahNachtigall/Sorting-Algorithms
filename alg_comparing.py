import time
import random

# ------------------------
# Bubble Sort
# ------------------------
def bubble_sort(arr):
    n = len(arr)

    for i in range(n):
        swapped = False

        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True

        if not swapped:
            break


# ------------------------
# Selection Sort
# ------------------------
def selection_sort(arr):
    n = len(arr)

    for i in range(n):
        min_idx = i

        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j

        arr[i], arr[min_idx] = arr[min_idx], arr[i]


# ------------------------
# Merge Sort
# ------------------------
def merge_sort(arr):
    if len(arr) > 1:
        left_arr = arr[:len(arr)//2]
        right_arr = arr[len(arr)//2:]

        merge_sort(left_arr)
        merge_sort(right_arr)

        i = 0
        j = 0
        k = 0

        while i < len(left_arr) and j < len(right_arr):
            if left_arr[i] < right_arr[j]:
                arr[k] = left_arr[i]
                i += 1
            else:
                arr[k] = right_arr[j]
                j += 1
            k += 1

        while i < len(left_arr):
            arr[k] = left_arr[i]
            i += 1
            k += 1

        while j < len(right_arr):
            arr[k] = right_arr[j]
            j += 1
            k += 1


# ------------------------
# Benchmark Function
# ------------------------
def benchmark(sort_function, original_arr):
    arr = original_arr.copy()

    start = time.perf_counter()

    sort_function(arr)

    end = time.perf_counter()

    return end - start


# ------------------------
# TEST ARRAY
# ------------------------

# Worst Case
test_arr = list(range(10000, 0, -1))

# Random Array
# test_arr = [random.randint(1, 100000) for _ in range(10000)]


# ------------------------
# BENCHMARKS
# ------------------------
bubble_time = benchmark(bubble_sort, test_arr)
selection_time = benchmark(selection_sort, test_arr)
merge_time = benchmark(merge_sort, test_arr)


# ------------------------
# RESULTS
# ------------------------
print("\n========== SORTING BENCHMARK ==========\n")

print(f"Bubble Sort:     {bubble_time:.6f} seconds")
print(f"Selection Sort:  {selection_time:.6f} seconds")
print(f"Merge Sort:      {merge_time:.6f} seconds")

print("\n=======================================\n")


# ------------------------
# WINNER
# ------------------------
times = {
    "Bubble Sort": bubble_time,
    "Selection Sort": selection_time,
    "Merge Sort": merge_time
}

winner = min(times, key=times.get)

print(f"Fastest Algorithm: {winner}")