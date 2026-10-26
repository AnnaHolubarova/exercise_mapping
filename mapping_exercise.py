# Task 1

def brute_force(text, p):
    """
    A brute-force approach to find all occurrences of the pattern p in the text.
    
    Parameters:
    text (str): The text in which to search for the pattern.
    p (str): The pattern to search for in the text.
    
    Returns:
    list: A list of starting indices where the pattern is found in the text.
    """
    occurrences = []
    n = len(text)
    m = len(p)
    
    for i in range(n - m + 1):
        if text[i:i + m] == p:
            occurrences.append(i)
    
    #print(f"Occurrences of pattern '{p}' in text '{text}': {occurrences}")
    return occurrences

#brute_force("AAAA", "AA")

def suffix_array(text):
    """
    Constructs the suffix array of the given text.
    
    Parameters:
    text (str): The text for which to construct the suffix array.
    
    Returns:
    list: A list of starting indices of the sorted suffixes of the text.
    """
    suffixes = [(text[i:], i) for i in range(len(text))]
    suffixes.sort()
    return [suffix[1] for suffix in suffixes]

#print(suffix_array("AAGGCGGCTTCA$"))

def find_block(text, sa, p):
    """
    Finds the block of suffixes in the suffix array that match the pattern p.
    
    Parameters:
    text (str): The text in which to search for the pattern.
    sa (list): The suffix array of the text.
    p (str): The pattern to search for in the text.
    
    Returns:
    tuple: A tuple containing the starting and ending indices of the block of matching suffixes.
           If no matches are found, returns (-1, -1).
    """
    n = len(sa)
    m = len(p)
    
    # Binary search for the left boundary
    left, right = 0, n - 1
    start = -1
    while left <= right:
        mid = (left + right) // 2
        suffix = text[sa[mid]:sa[mid] + m]
        if suffix < p:
            left = mid + 1
        elif suffix > p:
            right = mid - 1
        else:
            start = mid
            right = mid - 1
    
    if start == -1:
        return (-1, -1)
    
    # Binary search for the right boundary
    left, right = start, n - 1
    end = start
    while left <= right:
        mid = (left + right) // 2
        suffix = text[sa[mid]:sa[mid] + m]
        if suffix == p:
            end = mid
            left = mid + 1
        else:
            right = mid - 1
    
    #print(f"Block of suffixes matching pattern '{p}' in text '{text}': Start index: {start}, End index: {end}")
    return (start, end)

find_block("AAGGCGGCTTCA$", suffix_array("AAGGCGGCTTCA$"), "GGC")

# Task 2