import string
from typing import Tuple, List
from collections import Counter

def compress_by_common_words(input_text: str) -> str:
    """Takes in some input text and returns the compressed form using the following algorithm:
    
    1. Create a list of the most common english words sorted by length (longest first),
        include the lowercase and capitalized versions
    2. Loop over the list of words and replace each occurance of a word in the input text
        with it's index in the list

    Parameters
    ----------
    input_text : str
        The text to compress

    Returns
    -------
    str
        The compressed text
    """
    
    # 1. Create a list of the most common english words
    common_words = [
    "compression", "efficient","encoding","data",
    "the","at","there","some","my","of","be","use","her","than",
    "and","this","an","would","first","a","have","each","make","water",
    "to","from","which","like","been","in","or","she","him","call",
    "is","one","do","into","who","you","had","how","time","oil",
    "that","by","their","has","its","it","word","if","look","now",
    "he","but","will","two","find","was","not","up","more","long",
    "for","what","other","write","down","on","all","about","go","day",
    "are","were","out","see","did","as","we","many","number","get",
    "with","when","then","no","come","his","your","them","way","made",
    "they","can","these","could","may","I","said","so","people","part",
    ]

    ## 1.2 Add capitalized version of the words
    common_words += [word.capitalize() for word in common_words]

    ## 1.3 Sort by length; Longest word first
    common_words = sorted(common_words, key=len)[::-1]

    # 2. Loop over the list of words
    result = input_text
    for word in common_words:
        ## 2.1 Replace each occurance of a word in the input text with
        ## it's index in the common words list
        result = result.replace(word, f"{str(common_words.index(word))} ")
    return result

def is_word_longer_than_index(word:str, index:int) -> bool:
    """Checks if a word is longer than the number of digits in the index provided

    Parameters
    ----------
    word : str
        The word to check against the index digits

    index : int
        THe index to check the word length against

    Returns
    -------
    bool
        True if word is longer than index, else false
    """
    if len(word) > len(str(index)):
        return True
    else:
        return False

def compress_by_common_words_improved(input_text: str) -> str:
    """Takes in some input text and returns the compressed form using the following algorithm:
    
    1. Create a list of the most common english words sorted by length (longest first), 
        include the lowercase and capitalized versions & remove words that are shorter than their index
    2. Loop over the list of words and replace each occurance of a word in the input text
        with it's index in the list

    Parameters
    ----------
    input_text : str
        The text to compress

    Returns
    -------
    str
        The compressed text
    """
    
    # 1. Create a list of the most common english words
    common_words = [
    "compression", "efficient","encoding","data",
    "the","at","there","some","my","of","be","use","her","than",
    "and","this","an","would","first","a","have","each","make","water",
    "to","from","which","like","been","in","or","she","him","call",
    "is","one","do","into","who","you","had","how","time","oil",
    "that","by","their","has","its","it","word","if","look","now",
    "he","but","will","two","find","was","not","up","more","long",
    "for","what","other","write","down","on","all","about","go","day",
    "are","were","out","see","did","as","we","many","number","get",
    "with","when","then","no","come","his","your","them","way","made",
    "they","can","these","could","may","I","said","so","people","part",
    ]

    ## 1.2 Add capitalized version of the words
    common_words += [word.capitalize() for word in common_words]

    ## 1.3 Sort by length; Shortest word first
    common_words = sorted(common_words, key=len)
    
    ## 1.4 Remove words that are shorter than their index
    for index, word  in enumerate(common_words):
        if not is_word_longer_than_index(word, index):
            common_words.pop(index)
    
    # 2. Loop over the list of words
    result = input_text
    for word in common_words:
        ## 2.1 Replace each occurance of a word in the input text with
        ## it's index in the common words list
        result = result.replace(word, str(common_words.index(word)))
    return result

def compress_with_counter(input_text:str) -> Tuple[str, List[str]]:
    """Compression using the counter method:
    
    1. Create a dictionary of every word in the text with their number of
        occurences in the text
    2. Filter the dictionary so that only items with 2 or more occurences
        are in the resulting list, then sort by length (longest first)
    3. Remove any term where the index is the same size, or has more digits
        than the length of text
    4. Loop over the list of words and replace each occurance of a word in the
        input text with it's index in the common words list

    Parameters
    ----------
    input_text : str
        The text to compress

    Returns
    -------
    str, List[str]
        The first return value is the compressed text, the second is the terms used to compress
        
    """
    # 1. Create dictionary of word occurences
    ## 1.1 Remove punctuation from input text
    counter_text = input_text.translate(str.maketrans('','',string.punctuation,))

    ## 1.2 Split input text into a list of words so they can be counted
    counter_text = counter_text.split(" ")
    for word in counter_text:
        if "\n" in word:
            terms = word.split("\n")
            counter_text.remove(word)
            for term in terms:
                counter_text.append(term)

    ## 1.3 Count occurances of words in the text
    counter = Counter(counter_text)

    # 2. Filter to only terms with 2 or more items
    terms = {x: count for x, count in counter.items() if count >= 2}

    ## 2.1 Sort words by length; longest first
    words = sorted(list(terms.keys()), key=len)[::-1]
    
    # 3. Remove words that are shorter than their index
    for index, word in enumerate(words):
        if not is_word_longer_than_index(word, index):
            words.remove(word)
    
    # 4. Loop over the list of words
    result = input_text

    for word in words:
        ## 4.1 Replace each occurance of a word in the input text with
        ## it's index in the words list
        result = result.replace(word, str(words.index(word)))

    return result, words

def decompress(compressed_text: str, terms:List[str]) -> str:
    """Decompresses text based on index-replaced compression

    Parameters
    ----------
    compressed_text : str
        The text that has been compressed

    terms : List[str]
        The list of terms used to compress the text

    Returns
    -------
    str
        The decompressed text
    """
    result = compressed_text
    
    # Start from last element
    index = len(terms)-1
    while index >=0:
        # Replace each element from end to beginning 
        result = result.replace(str(index), terms[index])
        index -=1
    
    return result

if __name__ == "__main__":
    input_text = """"
    Compression is a fundamental technique used in various fields to reduce the size of data while preserving its essential information. In computer science and information technology, data compression plays a crucial role in storage, transmission, and processing of large amounts of information. By eliminating redundancy and exploiting patterns in data, compression algorithms can significantly reduce file sizes, resulting in more efficient use of storage space and faster data transfer over networks. From simple algorithms like run-length encoding to sophisticated methods like Huffman coding and Lempel-Ziv-Welch (LZW) algorithm, compression enables us to store and transmit data more effectively.

    Compression algorithms employ different strategies to achieve efficient data compression. Lossless compression techniques ensure that the compressed data can be fully reconstructed back to its original form without any loss of information. These techniques are commonly used in applications where preserving the integrity of data is critical, such as archiving files, databases, and text documents. On the other hand, lossy compression methods trade off some degree of data fidelity for higher compression ratios. Such techniques are commonly used in multimedia applications like image, audio, and video compression, where the removal of non-essential information or imperceptible details can lead to significant reduction in file sizes while maintaining acceptable perceptual quality.

    The benefits of compression extend beyond just saving storage space and reducing transmission time. Compressed data also reduces the demand for computational resources and improves system performance. When processing large datasets, compressed files can be read and decompressed faster than their uncompressed counterparts, allowing for quicker access and analysis. Moreover, compression enables efficient streaming of multimedia content, making it possible to deliver high-quality videos and audio over bandwidth-constrained networks. By minimizing the amount of data that needs to be transmitted, compression contributes to a smoother and more efficient digital experience, whether it's browsing the web, downloading files, or streaming media.

    In summary, compression is a vital technique that enables efficient storage, transmission, and processing of data. It utilizes various algorithms and strategies to reduce file sizes while preserving data integrity or achieving perceptual quality. By minimizing storage requirements, improving data transfer speeds, and enhancing system performance, compression plays a central role in modern computing and communication systems, benefiting users across a wide range of applications.
    """


    # Testing original algorithm
    print(f"Original Length of text = {len(input_text)}")
    result = compress_by_common_words(input_text)
    print(f"Length of compressed text = {len(result)}")

    # Testing improved compression system
    print(f"Original Length of text = {len(input_text)}")
    result = compress_by_common_words_improved(input_text)
    print(f"Length of compressed text = {len(result)}")

    # Testing with counter
    print(f"Original Length of text = {len(input_text)}")
    result, terms = compress_with_counter(input_text)
    print(f"Length of compressed text = {len(result)}")
    print(f"Decompressed text is: {decompress(result, terms)}")

    print(f"Resulting text is: \n{result}")

