'''
    average line strategy is:
    1. first BELLOW_LAST_DAY day, 80% percent time bellow ma20
    2. the BELLOW_LAST_DAY + 1 day break through the ma5
    3. the BELLOW_LAST_DAY + CHECK_LAST_DAY + 1 day still upon the ma5
    4. cal the 40th day result: (V40 - V25)/V25

    return list(21day, result)

    none match move to next day
    matched move to next 5 day
'''
def averageLineStratey(data):
    # low last day
    BELLOW_LAST_DAY = 5
    CHECK_LAST_DAY = 4
    AT_LEAST_BELLOW_DAY = int(BELLOW_LAST_DAY * 0.8)

    totalLen = len(data)
    index = 0
    result = []
    while totalLen - index > BELLOW_LAST_DAY + CHECK_LAST_DAY + 5:
        bellowMa5Day = 0
        for i in range(BELLOW_LAST_DAY):
            if data[index + i][0] < data[index + i][2]:
                bellowMa5Day += 1
        if bellowMa5Day >= AT_LEAST_BELLOW_DAY:
            if data[index + BELLOW_LAST_DAY + 1][0] > data[index + BELLOW_LAST_DAY + 1][1]:
                if data[index + BELLOW_LAST_DAY + CHECK_LAST_DAY + 1][0] > data[index + BELLOW_LAST_DAY + CHECK_LAST_DAY + 1][1]:
                    # find sell point, bellow 21 average line
                    startDay = find = index + BELLOW_LAST_DAY + CHECK_LAST_DAY + 2
                    for j in range(totalLen - startDay):
                        find = startDay + j
                        if data[startDay + j][0] < data[startDay + j][2] \
                                and data[startDay + j - 1][0] > data[startDay + j - 1][2]:
                            break
                    getData = []
                    getData.append(data[index + BELLOW_LAST_DAY + CHECK_LAST_DAY + 1][3])
                    getData.append(data[find][3])
                    getData.append((data[find][0] - data[index + BELLOW_LAST_DAY + CHECK_LAST_DAY + 1][0]) / data[index + BELLOW_LAST_DAY + CHECK_LAST_DAY + 1][0])
                    result.append(getData)
                    index = find + 1
                    continue
        index += 1
        continue
    return result