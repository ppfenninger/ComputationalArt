""" 
Creates randomly generated art using pre-defined functions
"""

import random
from PIL import Image
import math


def build_random_function(min_depth, max_depth):
    """ Builds a random function of depth at least min_depth and depth
        at most max_depth (see assignment writeup for definition of depth
        in this context)

        min_depth: the minimum depth of the random function
        max_depth: the maximum depth of the random function
        returns: the randomly generated function represented as a nested list
                 (see assignment writeup for details on the representation of
                 these functions)
    """
    # define lamda functions
    xEval = lambda x,y: x
    yEval = lambda x,y: y
    sin_pi = lambda x: math.sin(math.pi*x)
    cos_pi = lambda x: math.cos(math.pi*x)
    neg = lambda x: -1*x
    cube = lambda x: x**3
    prod = lambda x,y: x*y 
    avg = lambda x,y: (x + y) / 2 

    ran = random.randint(min_depth, max_depth) # picks an integer between the max and min depth

    func_list0 = [xEval, yEval] #zero input arguments
    func_list1 = [sin_pi, cos_pi, neg, cube]
    func_list2 = [prod, avg]
    total_func_list = func_list1 + func_list2 

    if ran <= 0:
        fun = random.choice(func_list0)
        return fun
    else:
        fun = random.choice(total_func_list)
        if fun in func_list2: #takes 2 input variables
            func1 = build_random_function(min_depth - 1, max_depth - 1) # completed one interation, so we have to subtract 1 from min and max depth
            func2 = build_random_function(min_depth - 1, max_depth - 1)
            new_func = lambda x,y: fun(func1(x, y), func2(x, y))
        else: #takes one input variable
            func1 = build_random_function(min_depth - 1, max_depth - 1)
            new_func = lambda x,y: fun(func1(x, y))

        return new_func


def remap_interval(val,
                   input_interval_start,
                   input_interval_end,
                   output_interval_start,
                   output_interval_end):
    """ Given an input value in the interval [input_interval_start,
        input_interval_end], return an output value scaled to fall within
        the output interval [output_interval_start, output_interval_end].

        val: the value to remap
        input_interval_start: the start of the interval that contains all
                              possible values for val
        input_interval_end: the end of the interval that contains all possible
                            values for val
        output_interval_start: the start of the interval that contains all
                               possible output values
        output_inteval_end: the end of the interval that contains all possible
                            output values
        returns: the value remapped from the input to the output interval

        >>> remap_interval(0.5, 0, 1, 0, 10)
        5.0
        >>> remap_interval(5, 4, 6, 0, 2)
        1.0
        >>> remap_interval(5, 4, 6, 1, 2)
        1.5
    """
    var = (val - input_interval_start)*(output_interval_end - output_interval_start)
    var /= float(input_interval_end - input_interval_start)
    var += output_interval_start
    return var



def color_map(val):
    """ Maps input value between -1 and 1 to an integer 0-255, suitable for
        use as an RGB color code.

        val: value to remap, must be a float in the interval [-1, 1]
        returns: integer in the interval [0,255]

        >>> color_map(-1.0)
        0
        >>> color_map(1.0)
        255
        >>> color_map(0.0)
        127
        >>> color_map(0.5)
        191
    """
    # NOTE: This relies on remap_interval, which you must provide
    color_code = remap_interval(val, -1, 1, 0, 255)
    return int(color_code)


def test_image(filename, x_size=350, y_size=350):
    """ Generate test image with random pixels and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (random.randint(0, 255),  # Red channel
                            random.randint(0, 255),  # Green channel
                            random.randint(0, 255))  # Blue channel

    im.save(filename)


def generate_art(filename, x_size=350, y_size=350):
    """ Generate computational art and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Functions for red, green, and blue channels - where the magic happens!
    red_function = build_random_function(6, 10)
    green_function = build_random_function(6, 10)
    blue_function = build_random_function(6, 10)

    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (
                    color_map(red_function(x,y)),
                    color_map(green_function(x,y)),
                    color_map(blue_function(x,y))
                    )

    im.save(filename)


# if __name__ == '__main__':
#     import doctest
#     doctest.testmod()
# if __name__ == "__main__":
#     import doctest
#     doctest.run_docstring_examples(evaluate_random_function, globals())
#     doctest.run_docstring_examples(remap_interval, globals())




    # Create some computational art!
    # TODO: Un-comment the generate_art function call after you
    #       implement remap_interval and evaluate_random_function
generate_art("myart.png")

    # Test that PIL is installed correctly
    # TODO: Comment or remove this function call after testing PIL install
    # test_image("noise.png")
