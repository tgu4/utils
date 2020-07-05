def size_format(num):
    """convert bytes size unit"""

    magnitude = 0
    if abs(num) < 1024:
        return '%.f%s' % (num, ['B'][magnitude])
    while abs(num) >= 1024:
        magnitude += 1
        num /= 1024.0
        
    # add more suffixes if you need them
    return '%.2f%s' % (num, ['B', 'K', 'M', 'G', 'T', 'P'][magnitude])

print('the answer is %s' % size_format(74363130012))  # prints 'the answer is 69.26G'
