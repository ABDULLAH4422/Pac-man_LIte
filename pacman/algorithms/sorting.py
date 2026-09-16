"""
Sorting Algorithms (QuickSort & MergeSort)
Syllabus: Sorting Algorithms: quick sort, merge sort
Used for: Ranking scores, leaderboards, and sorting algorithm benchmarking.
"""

def quick_sort(arr: list, key=lambda x: x, reverse: bool = False) -> list:
    """
    In-place recursive QuickSort.
    Divide and Conquer: Partitions array around a pivot element.
    Average Time Complexity: O(N log N), Worst Case: O(N^2).
    Space Complexity: O(log N) recursion stack.
    """
    arr_copy = list(arr)
    _quicksort_helper(arr_copy, 0, len(arr_copy) - 1, key, reverse)
    return arr_copy


def _quicksort_helper(arr: list, low: int, high: int, key, reverse: bool):
    if low < high:
        p_idx = _partition(arr, low, high, key, reverse)
        _quicksort_helper(arr, low, p_idx - 1, key, reverse)
        _quicksort_helper(arr, p_idx + 1, high, key, reverse)


def _partition(arr: list, low: int, high: int, key, reverse: bool) -> int:
    pivot_val = key(arr[high])
    i = low - 1

    for j in range(low, high):
        val = key(arr[j])
        condition = (val > pivot_val) if reverse else (val < pivot_val)
        if condition:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


def merge_sort(arr: list, key=lambda x: x, reverse: bool = False) -> list:
    """
    MergeSort (Divide and Conquer).
    Stable sorting algorithm.
    Time Complexity: O(N log N) in all cases (best, average, worst).
    Space Complexity: O(N).
    """
    if len(arr) <= 1:
        return list(arr)

    mid = len(arr) // 2
    left = merge_sort(arr[:mid], key, reverse)
    right = merge_sort(arr[mid:], key, reverse)

    return _merge(left, right, key, reverse)


def _merge(left: list, right: list, key, reverse: bool) -> list:
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        val_l = key(left[i])
        val_r = key(right[j])
        condition = (val_l >= val_r) if reverse else (val_l <= val_r)
        if condition:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    while i < len(left):
        result.append(left[i])
        i += 1
    while j < len(right):
        result.append(right[j])
        j += 1

    return result
