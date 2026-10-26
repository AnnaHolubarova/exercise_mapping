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

class FMIndex:
    """A sampled FM-index for a text terminated by ``$``."""

    def __init__(self, text, s):
        if not text.endswith("$"):
            raise ValueError("text must end with '$'")
        if not isinstance(s, int) or isinstance(s, bool) or s <= 0:
            raise ValueError("s must be a positive integer")

        sa = suffix_array(text)
        self.bwt = bwt(text, sa)
        #print(self.bwt)
        self.first_occurrence = first_occurrence(self.bwt)
        self.s = s
        self.sampled = {
            row: position
            for row, position in enumerate(sa)
            if position % s == 0
        }
        #print(self.sampled)

        self.counts = {letter: [0] for letter in self.bwt}
        for letter in self.bwt:
            for indexed_letter, prefix_counts in self.counts.items():
                prefix_counts.append(
                    prefix_counts[-1] + (indexed_letter == letter)
                )
        #print(self.counts["T"])

    def lf(self, row):
        """Return the row for the suffix starting one position earlier."""
        if not 0 <= row < len(self.bwt):
            raise IndexError("row is outside the BWT")
        letter = self.bwt[row]
        #print(f"LF mapping for row {row} with letter '{letter}': First occurrence: {self.first_occurrence[letter]}, Count: {self.counts[letter][row]}")
        return self.first_occurrence[letter] + self.counts[letter][row]

    def count(self, p):
        """Return the half-open suffix-array interval matching ``p``."""
        if not p:
            raise ValueError("p must be non-empty")
        if p.count("$") > 1 or ("$" in p and not p.endswith("$")):
            return 0, 0

        top, bottom = 0, len(self.bwt)
        for letter in reversed(p):
            if letter not in self.first_occurrence:
                return top, top
            top = self.first_occurrence[letter] + self.counts[letter][top]
            bottom = (
                self.first_occurrence[letter] + self.counts[letter][bottom]
            )
            if top == bottom:
                break
        #print(f"Count for pattern '{p}': Top index: {top}, Bottom index: {bottom}")
        return top, bottom

    def locate(self, p):
        """Return the text positions of all occurrences of ``p``."""
        top, bottom = self.count(p)
        positions = []
        for row in range(top, bottom):
            steps = 0
            while row not in self.sampled:
                row = self.lf(row)
                steps += 1
            positions.append(self.sampled[row] + steps)
        return positions

#FMIndex("CAT$", 2)
#FMIndex.lf(FMIndex("CAT$", 2), 1)
#FMIndex.count(FMIndex("AAGGCGGCTTCA$", 2), "GGC")
