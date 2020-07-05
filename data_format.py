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

def month2num(date):
    return{
        'Jan' : '01',
        'Feb' : '02',
        'Mar' : '03',
        'Apr' : '04',
        'May' : '05',
        'Jun' : '06',
        'Jul' : '07',
        'Aug' : '08',
        'Sep' : '09',
        'Oct' : '10',
        'Nov' : '11',
        'Dec' : '12'
    }[date]

print('the answer is %s' % size_format(74363130012))  # prints 'the answer is 69.26G'
print(month2num('Sep'))  # prints '09'
