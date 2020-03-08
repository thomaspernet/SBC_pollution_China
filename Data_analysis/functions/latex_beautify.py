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
                    line_to_remove.append(x + 13)
                    line_to_remove.append((x + 13) + 1)


    with open(table_out, "w") as f:
        for x, line in enumerate(lines):
            if x not in line_to_remove:
                f.write(line)

                # Read in the file
    with open(table_out, 'r') as file:
        lines = file.read()

        # Parallel trend
        lines = lines.replace('polluted\_threAbove:as.factor(year)2003',
                              '2003')
        lines = lines.replace('polluted\_threAbove:as.factor(year)2004',
                              '2004')
        lines = lines.replace('polluted\_threAbove:as.factor(year)2005',
                              '2005')
        lines = lines.replace('polluted\_threAbove:as.factor(year)2006',
                              '2006')
        lines = lines.replace('polluted\_threAbove:as.factor(year)2007',
                              '2007')

        # Reorder additional controls
        lines = lines.replace('PeriodAfter:polluted\_threAbove:SPZ',
                              'SPZ:PeriodAfter:polluted\_threAbove', 1)

        lines = lines.replace('PeriodAfter:polluted\_threAbove:count\_SOE:SPZ',
                              'SPZ:PeriodAfter:polluted\_threAbove:count\_SOE', 1)

        lines = lines.replace('PeriodAfter:polluted\_threAbove:out\_share\_SOE:SPZ',
                              'SPZ:PeriodAfter:polluted\_threAbove:out\_share\_SOE', 1)

        lines = lines.replace('PeriodAfter:polluted\_threAbove:cap\_share\_SOE:SPZ',
                              'SPZ:PeriodAfter:polluted\_threAbove:cap\_share\_SOE', 1)

        lines = lines.replace('PeriodAfter:polluted\_threAbove:lab\_share\_SOE:SPZ',
                              'SPZ:PeriodAfter:polluted\_threAbove:lab\_share\_SOE', 1)



        lines = lines.replace('PeriodAfter:polluted\_threAbove:Coastal',
                              'Coastal:PeriodAfter:polluted\_threAbove', 1)

        lines = lines.replace('PeriodAfter:polluted\_threAbove:count\_SOE:Coastal',
                              'Coastal:PeriodAfter:polluted\_threAbove:count\_SOE', 1)

        lines = lines.replace('PeriodAfter:polluted\_threAbove:out\_share\_SOE:Coastal',
                              'Coastal:PeriodAfter:polluted\_threAbove:out\_share\_SOE', 1)

        lines = lines.replace('PeriodAfter:polluted\_threAbove:cap\_share\_SOE:Coastal',
                              'Coastal:PeriodAfter:polluted\_threAbove:cap\_share\_SOE', 1)

        lines = lines.replace('PeriodAfter:polluted\_threAbove:lab\_share\_SOE:Coastal',
                              'Coastal:PeriodAfter:polluted\_threAbove:lab\_share\_SOE', 1)

        # Reorder TFP

        lines = lines.replace('polluted\_threAbove:PeriodAfter:SPZ',
                              'SPZ:polluted\_threAbove:PeriodAfter', 1)

        lines = lines.replace('polluted\_threAbove:PeriodAfter:Coastal',
                              'Coastal:polluted\_threAbove:PeriodAfter', 1)

        lines = lines.replace('PeriodAfter:SOESOE:SPZ',
                              'SPZ:PeriodAfter:SOESOE', 1)

        lines = lines.replace('PeriodAfter:SOESOE:Coastal',
                              'Coastal:PeriodAfter:SOESOE', 1)

        lines = lines.replace('polluted\_threAbove:PeriodAfter:SOESOE:SPZ',
                              'SPZ:polluted\_threAbove:PeriodAfter:SOESOE')

        lines = lines.replace('polluted\_threAbove:PeriodAfter:SOESOE:Coastal',
                              'Coastal:polluted\_threAbove:PeriodAfter:SOESOE')

        ### in case it fails because first matches
        lines = lines.replace('polluted\_threAbove:SPZ:PeriodAfter:SOESOE',
                              'SPZ:polluted\_threAbove:PeriodAfter:SOESOE',
                               1)

        lines = lines.replace('polluted\_threAbove:Coastal:PeriodAfter:SOESOE',
                              'Coastal:polluted\_threAbove:PeriodAfter:SOESOE',
                               1)


        # regex replace
        lines = lines.replace('output\_fcit', 'output_{cit}')
        lines = lines.replace('capital\_fcit', 'capital_{cit}')
        lines = lines.replace('labour\_fcit', 'labour_{cit}')

        # Interaction terms
        lines = lines.replace('TCZ\_cTCZ', ' TCZ_c ')
        lines = lines.replace('polluted\_threAbove', ' \\text{Polluted}_i ')
        lines = lines.replace('PeriodAfter', ' \\text{Period} ')

        # Share SOE
        lines = lines.replace('count\_SOE', ' \\text{count share SOE}_{i} ')
        lines = lines.replace('out\_share\_SOE',
                              ' \\text{output share SOE}_{i} ')
        lines = lines.replace('cap\_share\_SOE',
                              ' \\text{capital share SOE}_{i} ')
        lines = lines.replace('lab\_share\_SOE',
                              ' \\text{labour share SOE}_{i} ')

        ### foreing
        lines = lines.replace('out\_share\_for',
        ' \\text{output share Foreign}_{i}')

        lines = lines.replace('cap\_share\_for',
                              ' \\text{capital share Foreign}_{i} ')

        lines = lines.replace('lab\_share\_for',
                              ' \\text{labour share Foreign}_{i} ')

        lines = lines.replace('concentratedCONCENTRATED',
        ' \\text{Concencentrated}_{i}')

        lines = lines.replace('concentrated\_25CONCENTRATED',
        ' \\text{Concencentrated 25}_{i}')

        lines = lines.replace('concentrated\_50CONCENTRATED',
        ' \\text{Concencentrated 50}_{i}')

        lines = lines.replace('concentrated\_75CONCENTRATED',
        ' \\text{Concencentrated 75}_{i}')

        lines = lines.replace('concentrated\_85CONCENTRATED',
        ' \\text{Concencentrated 85}_{i}')

        # Additional controls
        lines = lines.replace('Coastal', ' Coastal_c ')
        lines = lines.replace('SPZ', ' SPZ_c ')
        lines = lines.replace('log(gdp\_cap)',
                              ' \\text{ln gdp per cap)}_{ct} ')
        lines = lines.replace('log(population)',
                              ' \\text{ln population)}_{ct} ')

        # Policy
        lines = lines.replace('target\_c', ' target_c ')



        # TFP
        lines = lines.replace('SOESOE', ' SOE ')
        lines = lines.replace('Coastal_c TRUE', ' Coastal_c ')
        lines = lines.replace(' : ', ' \\times ')



    # Write the file out again
    with open(table_out, 'w') as file:
        file.write(lines)

    # return lines