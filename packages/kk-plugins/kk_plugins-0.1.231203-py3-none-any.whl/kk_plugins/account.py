def format_accounting(number):
    # 将数字转换为字符串，并去除小数部分
    str_number = str(int(number))

    # 检查数字的正负性
    if number < 0:
        sign = '-'
        str_number = str_number[1:]  # 去除负号
    else:
        sign = ''

    # 添加千位分隔符
    parts = []
    while str_number:
        parts.append(str_number[-3:])
        str_number = str_number[:-3]
    formatted_number = ','.join(reversed(parts))

    # 添加货币符号和负号（如果有）
    formatted_number = f'{sign} {formatted_number}'

    return formatted_number