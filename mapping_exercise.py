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

#find_block("AAGGCGGCTTCA$", suffix_array("AAGGCGGCTTCA$"), "GGC")

# Task 2
def bwt(text, sa):
    """
    Computes the Burrows-Wheeler Transform (BWT) of the given text using its suffix array.
    
    Parameters:
    text (str): The text for which to compute the BWT.
    sa (list): The suffix array of the text.
    
    Returns:
    str: The BWT of the text.
    """
    bwt_result = []
    n = len(text)
    
    for i in range(n):
        if sa[i] == 0:
            bwt_result.append(text[-1])  # Last character of the text
        else:
            bwt_result.append(text[sa[i] - 1])  # Character before the suffix
    
    #print(f"BWT of text '{text}' using suffix array {sa}: {''.join(bwt_result)}")
    return ''.join(bwt_result)

#bwt("AAGGCGGCTTCA$", [12, 11, 0, 1, 10, 4, 7, 3, 6, 2, 5, 9, 8])

def first_occurrence(letters):
    """
    Computes the first occurrence of each character in the sorted list of letters.
    
    Parameters:
    letters (list): A list of characters (letters) from the BWT.
    
    Returns:
    dict: A dictionary mapping each character to its first occurrence index in the sorted list.
    """
    first_occ = {}
    sorted_letters = sorted(letters)
    
    for i, char in enumerate(sorted_letters):
        if char not in first_occ:
            first_occ[char] = i
    
    #print(f"First occurrence of letters {letters}: {first_occ}")
    return first_occ

#first_occurrence("$AAACCCGGGGTT")

def inverse_bwt(bwt):
    """
    Computes the inverse of the Burrows-Wheeler Transform (BWT) to reconstruct the original text.
    
    Parameters:
    bwt (str): The BWT of the text.
    
    Returns:
    str: The original text reconstructed from the BWT.
    """
    n = len(bwt)
    first_col = sorted(bwt)
    
    # Create a mapping from characters in the BWT to their positions in the first column
    first_occ = first_occurrence(bwt)
    
    # Create a list to hold the next indices for each character in the BWT
    next_indices = [0] * n
    count = {}
    
    for i, char in enumerate(bwt):
        if char not in count:
            count[char] = 0
        next_indices[i] = first_occ[char] + count[char]
        count[char] += 1
    
    # Reconstruct the original text using the next indices
    original_text = []
    index = bwt.index('$')  # Start from the end-of-string character
    
    for _ in range(n):
        original_text.append(bwt[index])
        index = next_indices[index]
    
    # The original text is constructed in reverse order, so we need to reverse it
    return''.join(reversed(original_text))

#print(inverse_bwt(bwt("AAGGCGGCTTCA$", [12, 11, 0, 1, 10, 4, 7, 3, 6, 2, 5, 9, 8])))

# Task 3