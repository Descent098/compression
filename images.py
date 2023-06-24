import random
from typing import List, Tuple
from collections import Counter

def round_pixels(image_values: List[List[List[int]]]) -> List[List[Tuple[int]]]:
    """Takes in a representation of image values, rounds the pixels to nearest number divisible 
    by 5 and then returns the new representation with tuples instead of lists

    Parameters
    ----------
    image_values : List[List[List[int]]]
        A representation of values of an image where the list contains
        rows of pixels of 3 RGB values i.e. a 2x2 image would be [[[255,255,255],[0,0,0]],[[0,0,0],[255,255,255]]]

    Returns
    -------
    List[List[Tuple[int]]]
        A representation of values of an image where the list contains
        rows of pixels of 3 RGB values. The innermost dimension is converted to 
    
    Examples
    --------
    ```
    image_values = [ 
    [[101,125,0],[255,115,83],[96,17,25],[255,255,255],[255,255,255]],
    [[255,255,255],      [0,0,0],[0,0,0],[0,0,0],      [255,255,255]],
    ]
    
    round_pixels(image_values)
    # Resulting list
    #  [
    #    [(105, 125, 0), (255, 115, 85), (100, 20, 25), (255, 255, 255), (255, 255, 255)],
    #    [(255, 255, 255), (0, 0, 0), (0, 0, 0), (0, 0, 0), (255, 255, 255)]
    #  ]
    ```
    """
    for row in image_values:
        for pixel in row:
            for index, value in enumerate(pixel):
                if value % 5 == 0: # Value is divisible by 5
                    continue
                else:
                    if len(str(value)) ==3: # 3 digit number
                        if int(str(value)[-1]) > 5:
                            pixel[index] = int(f"{str(value)[0]}{int(str(value)[1])+1}0")
                        else:
                            pixel[index]= int(f"{str(value)[0]}{str(value)[1]}5")
                    elif len(str(value)) ==2: # 2 digit number
                        if int(str(value)[-1]) > 5:
                            pixel[index] = int(f"{int(str(value)[0])+1}0")
                        else:
                            pixel[index]= int(f"{str(value)[0]}5")
                    elif len(str(value)) ==1: # single digit number
                        if value > 5:
                            pixel[index] = 10 
                        else:
                            pixel[index] = 0

    # Convert lists to tuples since  lists can't be used with Counter
    image_values = [[tuple(pixel) for pixel in row] for row in image_values]
    return image_values
    
def compress_image(image_values: List[List[List[int]]]) -> Tuple[List[List[Tuple[int]]], List[Tuple[int]]]:
    """Compresses images using the following algorithm:
    
    1. Round each number up to the next multiple of 5 (except 255, which stays 255). 
        So if we had the tuple `(120, 253, 119)` we would get `(125, 255, 120)` and if we
        had `(255, 0, 1)` we would get `(255, 5, 5)`
    2. Count the occurence of each tupple and make a list mapping each tuple to an index
    3. Replace each tupple with the index of where it would appear in the list of occurences

    Parameters
    ----------
    image_values : List[List[List[int]]]
        The initial representation of the image to be compressed

    Returns
    -------
    List[List[Tuple[int]]], List[Tuple[int]]
        The first argument is the compressed result, the second is the list used to compress the result

    Raises
    ------
    ValueError
        If there are more than 10 billion unique pixels
        
    Examples
    --------
    ```
    image_values = [ 
        [[101,125,0],[255,115,83],[96,17,25],[255,255,255],[255,255,255]],
        [[255,255,255],      [0,0,0],[0,0,0],[0,0,0],      [255,255,255]],
    ]
    
    result, compression_mapping = compress_image(image_values)
    print(f"{result=} | {compression_mapping=}")
    # result=[[(0,), (1,), (2,), (3,), (3,)], [(3,), (4,), (4,), (4,), (3,)]] | compression_mapping=[(105, 125, 0), (255, 115, 85), (100, 20, 25), (255, 255, 255), (0, 0, 0)]
    ```
    """
    # 1. "Round" pixel values to nearest multiple of 5
    image_values = round_pixels(image_values)

    # 2. Count tuple occurances
    counter = Counter()

    for row in image_values:
        for pixel in row:
            counter[pixel] += 1

    # 2.1 Convert to dictionary to make it easier to work with
    terms = dict(counter)

    ## 2.2 Make a list of the terms
    common_pixels = list(terms.keys())
    
    ## 2.3 Raise an error if the compression would result in larger files
    if len(common_pixels) > 10_000_000_000:
        raise ValueError("Image has too many unique values to be compressed")

    # 3. Replace occurences of tuples with their index in the list of common pixels
    result = image_values
    for index, row in enumerate(result):
        for inner_list_index, pixel in enumerate(row):
            result[index][inner_list_index] = tuple([common_pixels.index(pixel) if pixel in common_pixels else pixel])
    return result, common_pixels

def decompress_image(image_values:List[List[Tuple[int]]], common_pixels:List[Tuple[int]]) -> List[List[Tuple[int]]]:
    """Takes in an image compressed using the algorithm in compress_image(), and it's mapping and decompresses it

    Parameters
    ----------
    image_values : List[List[Tuple[int]]]
        The compressed representation of the image

    common_pixels : List[Tuple[int]]
        The list used to compress the image values

    Returns
    -------
    List[List[Tuple[int]]]
        The decompressed version of the image
        
    Examples
    --------
    ```
    image_values = [ 
        [[101,125,0],[255,115,83],[96,17,25],[255,255,255],[255,255,255]],
        [[255,255,255],      [0,0,0],[0,0,0],[0,0,0],      [255,255,255]],
    ]

    result, common_pixels = compress_image(image_values)

    print(decompress_image(result, common_pixels)) 
    # [
    #   [((105, 125, 0),), ((255, 115, 85),), ((100, 20, 25),), ((255, 255, 255),), ((255, 255, 255),)],
    #   [((255, 255, 255),), ((0, 0, 0),), ((0, 0, 0),), ((0, 0, 0),), ((255, 255, 255),)]
    # ]
    ```
    """
    # Takes in a compressed image, and the mapping used to compress it, and decompresses back to original form
    result = image_values
    for index, row in enumerate(result):
        for j_index, pixel in enumerate(row):
            if len(pixel) == 1: # Was compressed, convert back to original value
                result[index][j_index] = tuple([common_pixels[pixel[0]]])
    return result

def create_test_data(width:int, height:int) -> List[List[List[int]]]:
    """Generates test data to be used with compress_image()

    Parameters
    ----------
    width : int
        The width of the "image" to generate

    height : int
        The height of the "image" to generate

    Returns
    -------
    List[List[List[int]]]
        An "image" of size width x height
    """
    result = []
    for row in range(width):
        current_row = []
        for column in range(height):
            current_row.append([random.randint(0,255), random.randint(0,255), random.randint(0,255)])
        result.append(current_row)
    
    return result

if __name__ == "__main__": # Testing, only runs when file is run
    # Run with example in readme
    image_values = [ 
        # Start with third dimension being a list so the values can be rounded (tuples are immutable)
        [[255,255,255],[255,255,255],[255,255,255],[255,255,255],[255,255,255]],
        [[255,255,255],      [0,0,0],[0,0,0],[0,0,0],      [255,255,255]],
        [[255,255,255],[255,255,255],[0,0,0],[255,255,255],[255,255,255]],
        [[255,255,255],[255,255,255],[0,0,0],[255,255,255],[255,255,255]],
        [[255,255,255],[255,255,255],[0,0,0],[255,255,255],[255,255,255]],
    ]
    
    print(f"Original Length of text = {len(str(image_values))}")
    result, common_pixels = compress_image(image_values)
    print(f"Length of compressed text = {len(str(result))}")
    print(f"Compression ratio is ~%{((len(str(result))/len(str(image_values))))*100}")

    # Run with 50x50 randomly generated image
    image_values = create_test_data(50,50)

    print(f"Original Length of text = {len(str(image_values))}")
    result, common_pixels = compress_image(image_values)
    print(f"Length of compressed text = {len(str(result))}")
    print(f"Compression ratio is ~%{((len(str(result))/len(str(image_values))))*100}")

    print(decompress_image(result, common_pixels))

    # Run with example from docstrings
    image_values = [ 
        [[101,125,0],[255,115,83],[96,17,25],[255,255,255],[255,255,255]],
        [[255,255,255],      [0,0,0],[0,0,0],[0,0,0],      [255,255,255]],
    ]
    # result, compression_mapping = compress_image(image_values)
    # print(f"{result=}\n{compression_mapping=}")

