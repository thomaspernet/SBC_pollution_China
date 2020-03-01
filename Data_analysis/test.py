import re


def beautify(table_number):
    """
    """
    table_in = "table_{}.txt".format(table_number)
    table_out = "table_{}.tex".format(table_number)
    regex = r"^\s\sas\.factor\(year\)200|^\s\sTCZ\\_cTCZ\:as\.factor\(year\)200"

    r_tcz = r"\s\sTCZ\\_cTCZ\:PeriodAfter\:count\\_SOE|\s\sTCZ\\_cTCZ\:PeriodAfter\:out\\_share\\_SOE|\s\sTCZ\\_cTCZ\:PeriodAfter\:cap\\_share\\_SOE|\s\sTCZ\\_cTCZ\:PeriodAfter\:lab\\_share\\_SOE|\s\sTCZ\\_cTCZ\:PeriodAfter\:SOESOE"

    r_spz = r"\s\sPeriodAfter\:count\\_SOE\:SPZ|\s\sPeriodAfter\:out\\_share\\_SOE\:SPZ|\s\sPeriodAfter\:cap\\_share\\_SOE\:SPZ|\s\sPeriodAfter\:lab\\_share\\_SOE\:SPZ|\s\sPeriodAfter\:SOESOE\:SPZ"

    r_coa = r"\s\sPeriodAfter\:count\\_SOE\:Coastal|\s\sPeriodAfter\:out\\_share\\_SOE\:Coastal|\s\sPeriodAfter\:cap\\_share\\_SOE\:Coastal|\s\sPeriodAfter\:lab\\_share\\_SOE\:Coastal|\s\sPeriodAfter\:SOESOE\:Coastal"

    r_tfp = r"^\s\spolluted\\_threAbove\:PeriodAfter\:SOESOE\s"

    with open(table_in, "r") as f:
        lines = f.readlines()

        line_to_remove = []

        # Remove empty rows
        # First 13 and last 13 rows are headers and footers

    if table_number == 8: ### we have one more line of fixed effect
        max_ = 14
    else:
        max_ = 13
    for x, line in enumerate(lines[13:-max_]):
        print(line)
        test = bool(re.search(r'\d', line))
        test_parallel = bool(re.search(regex, line))
        if test == False:
            line_to_remove.append(x + 13)
            line_to_remove.append((x + 13) + 1)
        # Remove useless rows in Parallel trend
        if test_parallel == True:
            line_to_remove.append(x + 13)
            line_to_remove.append((x + 13) + 1)
        # Remove control in Parallel trend
        if table_number == 2 or table_number == 3 or table_number == 4 \
        or table_number == 5 or table_number == 6 or table_number == 7:
            rm_c = bool(re.search(r"output\\_fcit|capital\\_fcit|labour\\_fcit",
                                  line))
            if rm_c == True:
                    line_to_remove.append(x + 13)
                    line_to_remove.append((x + 13) + 1)

        #### Remove useless rows additional controls
        if table_number == 3 or table_number == 8:
            test_tcz = bool(re.search(r_tcz, line))
            if test_tcz == True:
                    line_to_remove.append(x + 13)
                    line_to_remove.append((x + 13) + 1)

            test_spz = bool(re.search(r_spz, line))
            if test_spz == True:
                    line_to_remove.append(x + 13)
                    line_to_remove.append((x + 13) + 1)

            test_coa = bool(re.search(r_coa, line))
            if test_coa == True:
                    line_to_remove.append(x + 13)
                    line_to_remove.append((x + 13) + 1)

            test_tfp = bool(re.search(r_tfp, line))
            if test_tfp == True:
                    line_to_remove.append(x + 13) ## coef
                    line_to_remove.append((x + 13)+1) ## standard error


    print(line_to_remove)

    with open(table_out, "w") as f:
        for x, line in enumerate(lines):
            if x not in line_to_remove:
                f.write(line)

    return table_out

beautify(table_number = 8)
