import time
import random

arr_size = 10000
bubble_comparisons = 0
selection_comparisons = 0
merge_comparisons = 0
quick_comparisons = 0
insertion_comparisons = 0


# ------------------------
# Bubble Sort
# ------------------------
def bubble_sort(arr):
    global bubble_comparisons
    n = len(arr)

    for i in range(n):
        swapped = False

        for j in range(n - i - 1):
            bubble_comparisons += 1
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True

        if not swapped:
            break


# ------------------------
# Selection Sort
# ------------------------
def selection_sort(arr):
    global selection_comparisons
    n = len(arr)

    for i in range(n):
        min_idx = i

        for j in range(i + 1, n):
            selection_comparisons += 1
            if arr[j] < arr[min_idx]:
                min_idx = j

        arr[i], arr[min_idx] = arr[min_idx], arr[i]


# ------------------------
# Merge Sort
# ------------------------
def merge_sort(arr):
    global merge_comparisons
    if len(arr) > 1:
        left_arr = arr[:len(arr)//2]
        right_arr = arr[len(arr)//2:]

        merge_sort(left_arr)
        merge_sort(right_arr)

        i = 0
        j = 0
        k = 0

        while i < len(left_arr) and j < len(right_arr):
            merge_comparisons += 1
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


# Quick Sort
def quick_sort(arr):
    global quick_comparisons

    def partition(a, low, high):
        global quick_comparisons
        pivot_index = random.randint(low, high)
        a[pivot_index], a[high] = a[high], a[pivot_index]
        pivot = a[high]
        i = low - 1

        for j in range(low, high):
            quick_comparisons += 1
            if a[j] <= pivot:
                i += 1
                a[i], a[j] = a[j], a[i]

        a[i + 1], a[high] = a[high], a[i + 1]
        return i + 1

    def _quick_sort(a, low, high):
        while low < high:
            pi = partition(a, low, high)
            left_size = pi - 1 - low
            right_size = high - (pi + 1)

            if left_size < right_size:
                _quick_sort(a, low, pi - 1)
                low = pi + 1
            else:
                _quick_sort(a, pi + 1, high)
                high = pi - 1

    _quick_sort(arr, 0, len(arr) - 1)
    return arr


# Insertion Sort
def insertion_sort(arr):
    global insertion_comparisons
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1

        while True:
            if j < 0:
                insertion_comparisons += 1
                break

            insertion_comparisons += 1
            if arr[j] > key:
                arr[j + 1] = arr[j]
                j -= 1
            else:
                break

        arr[j + 1] = key

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
test_arr = list(range(arr_size, 0, -1))

# Random Array
# test_arr = [random.randint(1, 100000) for _ in range(arr_size)]


# ------------------------
# BENCHMARKS
# ------------------------
bubble_time = benchmark(bubble_sort, test_arr)
selection_time = benchmark(selection_sort, test_arr)
merge_time = benchmark(merge_sort, test_arr)
quick_time = benchmark(quick_sort, test_arr)
insertion_time = benchmark(insertion_sort, test_arr)

# ------------------------
# RESULTS
# ------------------------
print("\n========== SORTING BENCHMARK ==========\n")

print(f"Array Size: {len(test_arr)}")

print(f"Bubble Sort:     {bubble_time:.6f} seconds", f"({bubble_comparisons} comparisons)")
print(f"Selection Sort:  {selection_time:.6f} seconds", f"({selection_comparisons} comparisons)")
print(f"Merge Sort:      {merge_time:.6f} seconds", f"({merge_comparisons} comparisons)")
print(f"Quick Sort:      {quick_time:.6f} seconds", f"({quick_comparisons} comparisons)")
print(f"Insertion Sort:  {insertion_time:.6f} seconds", f"({insertion_comparisons} comparisons)")

print("\n=======================================\n")


# ------------------------
# WINNER
# ------------------------
times = {
    "Bubble Sort": bubble_time,
    "Selection Sort": selection_time,
    "Merge Sort": merge_time,
    "Quick Sort": quick_time,
    "Insertion Sort": insertion_time
}

winner = min(times, key=times.get)

print(f"Fastest Algorithm: {winner}")