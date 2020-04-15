import re, tex2pix, os
from PyPDF2 import PdfFileMerger
from wand.image import Image as WImage

# The idea here is to define regex to remove_control
# Different option indicating what to keep -> based on the paper objective

def beautify(table_number,
remove_control = True,
 constraint = True,
  city_industry = False,
 new_row= False, table_nte = None,
 test_city_industry = False,
 jupyter_preview = True,
 resolution = 150):
    """
    Contrainst -> when all FE: pair and not pair
    remove_control -> remove output, capital, labour (first three row)
    test_city_industry -> test with share SOE computed city indsutry
    """
    table_in = "table_{}.txt".format(table_number)
    table_out = "table_{}.tex".format(table_number)
    #regex = r"^\s\sas\.factor\(year\)200|^\s\sTCZ\\_cTCZ\:as\.factor\(year\)200"

    r_tcz = \
    r"\s\sTCZ\\_cTCZ\:PeriodAfter\:count\\_SOE\s|" \
    r"\s\sTCZ\\_cTCZ\:PeriodAfter\:out\\_share\\_SOE\s|" \
    r"\s\sTCZ\\_cTCZ\:PeriodAfter\:cap\\_share\\_SOE\s|" \
    r"\s\sTCZ\\_cTCZ\:PeriodAfter\:lab\\_share\\_SOE\s|" \
    r"\s\sTCZ\\_cTCZ\:PeriodAfter\:SOESOE\s|" \
    r"\s\spolluted\\_threAbove\:out\\_share\\_SOE|" \
    r"\s\spolluted\\_threAbove\:cap\\_share\\_SOE|" \
    r"\s\spolluted\\_threAbove\:lab\\_share\\_SOE"

    r_spz = \
    r"\s\sPeriodAfter\:count\\_SOE\:SPZ\s|" \
    r"\s\sPeriodAfter\:out\\_share\\_SOE\:SPZ\s|" \
    r"\s\sPeriodAfter\:cap\\_share\\_SOE\:SPZ\s|" \
    r"\s\sPeriodAfter\:lab\\_share\\_SOE\:SPZ\s|" \
    r"\s\spolluted\\_threAbove:out\\_share\\_SOE\:SPZ\s|" \
    r"\s\spolluted\\_threAbove:cap\\_share\\_SOE\:SPZ\s|" \
    r"\s\spolluted\\_threAbove:lab\\_share\\_SOE\:SPZ\s|" \
    r"\s\sPeriodAfter\:SOESOE\:SPZ\s|" \
    r"\s\sPeriodAfter\:SPZ\s|" \
    r"\s\spolluted\\_threAbove\:SPZ\s|" \
    r"\s\sout\\_share\\_SOE\:SPZ\s|" \
    r"\s\scap\\_share\\_SOE\:SPZ\s|" \
    r"\s\slab\\_share\\_SOE\:SPZ\s"

    r_coa = \
    r"\s\sPeriodAfter\:count\\_SOE\:Coastal\s|" \
    r"\s\sPeriodAfter\:out\\_share\\_SOE\:Coastal\s|" \
    r"\s\sPeriodAfter\:cap\\_share\\_SOE\:Coastal\s|" \
    r"\s\sPeriodAfter\:lab\\_share\\_SOE\:Coastal\s|" \
    r"\s\spolluted\\_threAbove:out\\_share\\_SOE\:Coastal\s|" \
    r"\s\spolluted\\_threAbove:cap\\_share\\_SOE\:Coastal\s|" \
    r"\s\spolluted\\_threAbove:lab\\_share\\_SOE\:Coastal\s|" \
    r"\s\sPeriodAfter\:SOESOE\:Coastal\s|" \
    r"\s\sPeriodAfter\:Coastal\s|" \
    r"\s\spolluted\\_threAbove\:Coastal\s|" \
    r"\s\sout\\_share\\_SOE\:Coastal\s|" \
    r"\s\scap\\_share\\_SOE\:Coastal\s|" \
    r"\s\slab\\_share\\_SOE\:Coastal\s"

    r_tfp = r"^\s\spolluted\\_threAbove\:PeriodAfter\:SOESOE\s"

    r_kuznet = \
    r"\s\sdummy\\_SOE\\_c\\_output5Above\s|" \
    r"\s\sdummy\\_SOE\\_c\\_capital5Above\s|" \
    r"\s\sdummy\\_SOE\\_c\\_emp5Above\s"

    r_high_fe = \
        r"\s\sTCZ\\_cTCZ\:polluted\\_threAbove\s|" \
        r"\s\sTCZ\\_cTCZ\:PeriodAfter\s"

    #r_pop_gdp = \
    #r"\s\slog\(gdp\\_cap\)\s|" \
    #r"\s\slog\(population\)\s"


    if city_industry:
        r_concentrated = \
    r"\s\sconcentrated\\_25CONCENTRATED|" \
    r"\s\sconcentrated\\_50CONCENTRATED|" \
    r"\s\sconcentrated\\_75CONCENTRATED|" \
    r"\s\sconcentrated\\_85CONCENTRATED|" \
    r"\s\sTCZ\\_cTCZ\:concentrated\\_25CONCENTRATED|" \
    r"\s\sTCZ\\_cTCZ\:concentrated\\_50CONCENTRATED|" \
    r"\s\sTCZ\\_cTCZ\:concentrated\\_75CONCENTRATED|" \
    r"\s\sTCZ\\_cTCZ\:concentrated\\_85CONCENTRATED|" \
    r"\s\spolluted\\_threAbove\:concentrated\\_25CONCENTRATED|" \
    r"\s\spolluted\\_threAbove\:concentrated\\_50CONCENTRATED|" \
    r"\s\spolluted\\_threAbove\:concentrated\\_75CONCENTRATED|" \
    r"\s\spolluted\\_threAbove\:concentrated\\_85CONCENTRATED|" \
    r"\s\sPeriodAfter\:concentrated\\_25CONCENTRATED|" \
    r"\s\sPeriodAfter\:concentrated\\_50CONCENTRATED|" \
    r"\s\sPeriodAfter\:concentrated\\_75CONCENTRATED|" \
    r"\s\sPeriodAfter\:concentrated\\_85CONCENTRATED|" \
    r"\s\sTCZ\\_cTCZ\:polluted\\_threAbove\:concentrated\\_25CONCENTRATED|" \
    r"\s\sTCZ\\_cTCZ\:polluted\\_threAbove\:concentrated\\_50CONCENTRATED|" \
    r"\s\sTCZ\\_cTCZ\:polluted\\_threAbove\:concentrated\\_75CONCENTRATED|" \
    r"\s\sTCZ\\_cTCZ\:polluted\\_threAbove\:concentrated\\_85CONCENTRATED"

    else:
        r_concentrated = \
    r"\s\sconcentrated\\_25CONCENTRATED|" \
    r"\s\sconcentrated\\_50CONCENTRATED|" \
    r"\s\sconcentrated\\_75CONCENTRATED|" \
    r"\s\sconcentrated\\_85CONCENTRATED|" \
    r"\s\sTCZ\\_cTCZ\:concentrated\\_25CONCENTRATED|" \
    r"\s\sTCZ\\_cTCZ\:concentrated\\_50CONCENTRATED|" \
    r"\s\sTCZ\\_cTCZ\:concentrated\\_75CONCENTRATED|" \
    r"\s\sTCZ\\_cTCZ\:concentrated\\_85CONCENTRATED|" \
    r"\s\spolluted\\_threAbove\:concentrated\\_25CONCENTRATED|" \
    r"\s\spolluted\\_threAbove\:concentrated\\_50CONCENTRATED|" \
    r"\s\spolluted\\_threAbove\:concentrated\\_75CONCENTRATED|" \
    r"\s\spolluted\\_threAbove\:concentrated\\_85CONCENTRATED|" \
    r"\s\sPeriodAfter\:concentrated\\_25CONCENTRATED|" \
    r"\s\sPeriodAfter\:concentrated\\_50CONCENTRATED|" \
    r"\s\sPeriodAfter\:concentrated\\_75CONCENTRATED|" \
    r"\s\sPeriodAfter\:concentrated\\_85CONCENTRATED|" \
    r"\s\sPeriodAfter\:polluted\\_threAbove\:concentrated\\_25CONCENTRATED|" \
    r"\s\sPeriodAfter\:polluted\\_threAbove\:concentrated\\_50CONCENTRATED|" \
    r"\s\sPeriodAfter\:polluted\\_threAbove\:concentrated\\_75CONCENTRATED|" \
    r"\s\sPeriodAfter\:polluted\\_threAbove\:concentrated\\_85CONCENTRATED|" \
    r"\s\sTCZ\\_cTCZ\:polluted\\_threAbove\:concentrated\\_25CONCENTRATED|" \
    r"\s\sTCZ\\_cTCZ\:polluted\\_threAbove\:concentrated\\_50CONCENTRATED|" \
    r"\s\sTCZ\\_cTCZ\:polluted\\_threAbove\:concentrated\\_75CONCENTRATED|" \
    r"\s\sTCZ\\_cTCZ\:polluted\\_threAbove\:concentrated\\_85CONCENTRATED"

    if city_industry:
        r_concentrated_con = \
    r"\s\sHerfindahl|" \
    r"\s\sTCZ\\_cTCZ\:Herfindahl|" \
    r"\s\sPeriodAfter\:Herfindahl|" \
    r"\s\spolluted\\_threAbove\:Herfindahl|" \
    r"\s\sTCZ\\_cTCZ\:polluted\\_threAbove\:Herfindahl"
    else:
        r_concentrated_con = \
    r"\s\sTCZ\\_cTCZ\:Herfindahl\s|" \
    r"\s\sPeriodAfter\:Herfindahl\s|" \
    r"\s\sPeriodAfter\:polluted\\_threAbove\:Herfindahl\s|" \
    r"\s\sTCZ\\_cTCZ\:polluted\\_threAbove\:Herfindahl\s"

    #r"\s\sTCZ\\_cTCZ\:PeriodAfter\:concentrated\\_25CONCENTRATED|" \
    #r"\s\sTCZ\\_cTCZ\:PeriodAfter\:concentrated\\_50CONCENTRATED|" \
    #r"\s\sTCZ\\_cTCZ\:PeriodAfter\:concentrated\\_75CONCENTRATED|" \
    #r"\s\sTCZ\\_cTCZ\:PeriodAfter\:concentrated\\_85CONCENTRATED"

    r_foreign = \
    r"\sTCZ\\_cTCZ\s|" \
    r"\s\sPeriodAfter\s|" \
    r"\s\sout\\_share\\_SOE\s|" \
    r"\s\sout\\_share\\_for\s|" \
    r"\s\scap\\_share\\_SOE\s|" \
    r"\s\scap\\_share\\_for\s|" \
    r"\s\slab\\_share\\_SOE\s|" \
    r"\s\slab\\_share\\_for\s|" \
    r"\s\sTCZ\\_cTCZ\:out\\_share\\_for|" \
    r"\s\sTCZ\\_cTCZ\:out\\_share\\_SOE|" \
    r"\s\sTCZ\\_cTCZ\:out\\_share\\_SOE\\_|" \
    r"\s\sTCZ\\_cTCZ\:cap\\_share\\_for|" \
    r"\s\sTCZ\\_cTCZ\:cap\\_share\\_SOE|" \
    r"\s\sTCZ\\_cTCZ\:cap\\_share\\_SOE\\_|" \
    r"\s\sTCZ\\_cTCZ\:lab\\_share\\_for|" \
    r"\s\sTCZ\\_cTCZ\:lab\\_share\\_SOE|" \
    r"\s\sTCZ\\_cTCZ\:lab\\_share\\_SOE\\_|" \
    r"\s\sPeriodAfter\:polluted\\_threAbove\s|" \
    r"\s\sPeriodAfter\:out\\_share\\_for\s|" \
    r"\s\sPeriodAfter\:out\\_share\\_SOE\s|" \
    r"\s\sPeriodAfter\:out\\_share\\_SOE\\_\s|" \
    r"\s\sPeriodAfter\:cap\\_share\\_for\s|" \
    r"\s\sPeriodAfter\:cap\\_share\\_SOE\s|" \
    r"\s\sPeriodAfter\:cap\\_share\\_SOE\\_\s|" \
    r"\s\sPeriodAfter\:lab\\_share\\_for\s|" \
    r"\s\sPeriodAfter\:lab\\_share\\_SOE\s|" \
    r"\s\sPeriodAfter\:lab\\_share\\_SOE\\_\s|" \
    r"\s\sTCZ\\_cTCZ\:polluted\\_threAbove\:out\\_share\\_for|" \
    r"\s\sTCZ\\_cTCZ\:polluted\\_threAbove\:out\\_share\\_SOE|" \
    r"\s\sTCZ\\_cTCZ\:polluted\\_threAbove\:cap\\_share\\_for|" \
    r"\s\sTCZ\\_cTCZ\:polluted\\_threAbove\:cap\\_share\\_SOE|" \
    r"\s\sTCZ\\_cTCZ\:polluted\\_threAbove\:lab\\_share\\_for|" \
    r"\s\sTCZ\\_cTCZ\:polluted\\_threAbove\:lab\\_share\\_SOE|" \
    r"\s\sPeriodAfter\:polluted\\_threAbove\:out\\_share\\_for\s|" \
    r"\s\sPeriodAfter\:polluted\\_threAbove\:out\\_share\\_SOE\s|" \
    r"\s\sPeriodAfter\:polluted\\_threAbove\:out\\_share\\_SOE\\_\s|" \
    r"\s\sPeriodAfter\:polluted\\_threAbove\:cap\\_share\\_for\s|" \
    r"\s\sPeriodAfter\:polluted\\_threAbove\:cap\\_share\\_SOE\s|" \
    r"\s\sPeriodAfter\:polluted\\_threAbove\:cap\\_share\\_SOE\\_\s|" \
    r"\s\sPeriodAfter\:polluted\\_threAbove\:lab\\_share\\_for\s|" \
    r"\s\sPeriodAfter\:polluted\\_threAbove\:lab\\_share\\_SOE\s|" \
    r"\s\sPeriodAfter\:polluted\\_threAbove\:lab\\_share\\_SOE\\_\s"

    r_decile = \
    r"\s\sdecile\\_so2\\_5Above\s|" \
    r"\s\sdecile\\_so2\\_6Above\s|" \
    r"\s\sdecile\\_so2\\_7Above\s|" \
    r"\s\sdecile\\_so2\\_8Above\s|" \
    r"\s\sdecile\\_so2\\_9Above\s|" \
    r"\s\sTCZ\\_cTCZ:decile\\_so2\\_5Above\s|" \
    r"\s\sPeriodAfter\:decile\\_so2\\_5Above\s|" \
    r"\s\sdecile\\_so2\\_5Above\:out\\_share\\_SOE\s|" \
    r"\s\sdecile\\_so2\\_5Above\:cap\\_share\\_SOE\s|" \
    r"\s\sdecile\\_so2\\_5Above\:lab\\_share\\_SOE\s|" \
    r"\s\sTCZ\\_cTCZ\:decile\\_so2\\_5Above\:out\\_share\\_SOE\s|" \
    r"\s\sTCZ\\_cTCZ\:decile\\_so2\\_5Above\:cap\\_share\\_SOE\s|" \
    r"\s\sTCZ\\_cTCZ\:decile\\_so2\\_5Above\:lab\\_share\\_SOE\s|" \
    r"\s\sPeriodAfter\:decile\\_so2\\_5Above\:out\\_share\\_SOE\s|" \
    r"\s\sPeriodAfter\:decile\\_so2\\_5Above\:cap\\_share\\_SOE\s|" \
    r"\s\sPeriodAfter\:decile\\_so2\\_5Above\:lab\\_share\\_SOE\s|" \
    r"\s\sdecile\\_so2\\_6Above\s|" \
    r"\s\sTCZ\\_cTCZ:decile\\_so2\\_6Above\s|" \
    r"\s\sPeriodAfter\:decile\\_so2\\_6Above\s|" \
    r"\s\sdecile\\_so2\\_6Above\:out\\_share\\_SOE\s|" \
    r"\s\sdecile\\_so2\\_6Above\:cap\\_share\\_SOE\s|" \
    r"\s\sdecile\\_so2\\_6Above\:lab\\_share\\_SOE\s|" \
    r"\s\sTCZ\\_cTCZ\:decile\\_so2\\_6Above\:out\\_share\\_SOE\s|" \
    r"\s\sTCZ\\_cTCZ\:decile\\_so2\\_6Above\:cap\\_share\\_SOE\s|" \
    r"\s\sTCZ\\_cTCZ\:decile\\_so2\\_6Above\:lab\\_share\\_SOE\s|" \
    r"\s\sPeriodAfter\:decile\\_so2\\_6Above\:out\\_share\\_SOE\s|" \
    r"\s\sPeriodAfter\:decile\\_so2\\_6Above\:cap\\_share\\_SOE\s|" \
    r"\s\sPeriodAfter\:decile\\_so2\\_6Above\:lab\\_share\\_SOE\s|" \
    r"\s\sdecile\\_so2\\_7Above\s|" \
    r"\s\sTCZ\\_cTCZ:decile\\_so2\\_7Above\s|" \
    r"\s\sPeriodAfter\:decile\\_so2\\_7Above\s|" \
    r"\s\sdecile\\_so2\\_7Above\:out\\_share\\_SOE\s|" \
    r"\s\sdecile\\_so2\\_7Above\:cap\\_share\\_SOE\s|" \
    r"\s\sdecile\\_so2\\_7Above\:lab\\_share\\_SOE\s|" \
    r"\s\sTCZ\\_cTCZ\:decile\\_so2\\_7Above\:out\\_share\\_SOE\s|" \
    r"\s\sTCZ\\_cTCZ\:decile\\_so2\\_7Above\:cap\\_share\\_SOE\s|" \
    r"\s\sTCZ\\_cTCZ\:decile\\_so2\\_7Above\:lab\\_share\\_SOE\s|" \
    r"\s\sPeriodAfter\:decile\\_so2\\_7Above\:out\\_share\\_SOE\s|" \
    r"\s\sPeriodAfter\:decile\\_so2\\_7Above\:cap\\_share\\_SOE\s|" \
    r"\s\sPeriodAfter\:decile\\_so2\\_7Above\:lab\\_share\\_SOE\s|" \
    r"\s\sdecile\\_so2\\_8Above\s|" \
    r"\s\sTCZ\\_cTCZ:decile\\_so2\\_8Above\s|" \
    r"\s\sPeriodAfter\:decile\\_so2\\_8Above\s|" \
    r"\s\sdecile\\_so2\\_8Above\:out\\_share\\_SOE\s|" \
    r"\s\sdecile\\_so2\\_8Above\:cap\\_share\\_SOE\s|" \
    r"\s\sdecile\\_so2\\_8Above\:lab\\_share\\_SOE\s|" \
    r"\s\sTCZ\\_cTCZ\:decile\\_so2\\_8Above\:out\\_share\\_SOE\s|" \
    r"\s\sTCZ\\_cTCZ\:decile\\_so2\\_8Above\:cap\\_share\\_SOE\s|" \
    r"\s\sTCZ\\_cTCZ\:decile\\_so2\\_8Above\:lab\\_share\\_SOE\s|" \
    r"\s\sPeriodAfter\:decile\\_so2\\_8Above\:out\\_share\\_SOE\s|" \
    r"\s\sPeriodAfter\:decile\\_so2\\_8Above\:cap\\_share\\_SOE\s|" \
    r"\s\sPeriodAfter\:decile\\_so2\\_8Above\:lab\\_share\\_SOE\s|" \
    r"\s\sTCZ\\_cTCZ:decile\\_so2\\_9Above\s|" \
    r"\s\sPeriodAfter\:decile\\_so2\\_9Above\s|" \
    r"\s\sdecile\\_so2\\_9Above\:out\\_share\\_SOE\s|" \
    r"\s\sdecile\\_so2\\_9Above\:cap\\_share\\_SOE\s|" \
    r"\s\sdecile\\_so2\\_9Above\:lab\\_share\\_SOE\s|" \
    r"\s\sTCZ\\_cTCZ\:decile\\_so2\\_9Above\:out\\_share\\_SOE\s|" \
    r"\s\sTCZ\\_cTCZ\:decile\\_so2\\_9Above\:cap\\_share\\_SOE\s|" \
    r"\s\sTCZ\\_cTCZ\:decile\\_so2\\_9Above\:lab\\_share\\_SOE\s|" \
    r"\s\sPeriodAfter\:decile\\_so2\\_9Above\:out\\_share\\_SOE\s|" \
    r"\s\sPeriodAfter\:decile\\_so2\\_9Above\:cap\\_share\\_SOE\s|" \
    r"\s\sPeriodAfter\:decile\\_so2\\_9Above\:lab\\_share\\_SOE\s"

    r_parall = \
    r"^\s\sas\.factor\(year\)|" \
    r"^\s\starget\\_c\:as\.factor\(year\)200|" \
    r"^\s\spolluted\\_threAbove\:as\.factor\(year\)200"


    with open(table_in, "r") as f:
        lines = f.readlines()

        line_to_remove = []

        # Remove empty rows
        # First 13 and last 13 rows are headers and footers
    if constraint:
        #if table_number == 8: ### we have one more line of fixed effect
        #    max_ = 14 ### need to recalculate
        #else:
        #    max_ = 13### need to recalculate
        max_ =  len(lines) - 12
    else:
        max_ =  len(lines) - 9#15
    for x, line in enumerate(lines[13:max_]):
        test = bool(re.search(r'\d', line))
        #test_parallel = bool(re.search(regex, line))
        if test == False:
            line_to_remove.append(x + 13)
            line_to_remove.append((x + 13) + 1)
        # Remove useless rows in Parallel trend
        #if test_parallel == True:
        #    line_to_remove.append(x + 13)
        #    line_to_remove.append((x + 13) + 1)
        # Remove control in Parallel trend
        if remove_control:
            rm_c = bool(re.search(r"output\\_fcit|capital\\_fcit|labour\\_fcit",
                                  line))
            if rm_c == True:
                    line_to_remove.append(x + 13)
                    line_to_remove.append((x + 13) + 1)

        #if constraint == False:
        test_foreign = bool(re.search(r_foreign, line))
        if test_foreign == True:
            line_to_remove.append(x + 13)
            line_to_remove.append((x + 13) + 1)

        test_concentrated_con = bool(re.search(r_concentrated_con, line))
        if test_concentrated_con == True:
            line_to_remove.append(x + 13)
            line_to_remove.append((x + 13) + 1)

        test_concentrated = bool(re.search(r_concentrated, line))
        if test_concentrated == True:
            line_to_remove.append(x + 13)
            line_to_remove.append((x + 13) + 1)

        test_kuznet = bool(re.search(r_kuznet, line))
        if test_kuznet == True:
            line_to_remove.append(x + 13)
            line_to_remove.append((x + 13) + 1)

        test_decile = bool(re.search(r_decile, line))
        if test_decile == True:
            line_to_remove.append(x + 13)
            line_to_remove.append((x + 13) + 1)

        test_parallel = bool(re.search(r_parall, line))
        if test_parallel == True:
            line_to_remove.append(x + 13)
            line_to_remove.append((x + 13) + 1)

        #### Remove useless rows additional controls
        #if table_number == 3 or table_number == 8:
        if constraint:
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
        else:
            test_high_fe = bool(re.search(r_high_fe, line))
            if test_high_fe == True:
                line_to_remove.append(x + 13)
                line_to_remove.append((x + 13) + 1)

            #test_pop_gdp = bool(re.search(r_pop_gdp, line))
            #if test_pop_gdp == True:
            #    line_to_remove.append(x + 13)
            #    line_to_remove.append((x + 13) + 1)



    with open(table_out, "w") as f:
        for x, line in enumerate(lines):
            if x not in line_to_remove:
                f.write(line)

    ### add ajdust box
    with open(table_out, 'r') as f:
        lines = f.readlines()

    if new_row != False:
        temp  = [' & '.join(new_row)]
        temp.append('\n \\\\[-1.8ex]')
        temp.append('\\\\\n ')
        #temp.append('\n \\\\[-1.8ex]\n')
        new_row_ = [temp[1] + temp[0] + temp[2] #+ temp[3]
        ]

    for x, line in enumerate(lines):
        label = bool(re.search(r"label",
                              line))
        tabluar = bool(re.search(r"end{tabular}",
                              line))
        if label:
            lines[x] = lines[x].strip() + '\n\\begin{adjustbox}{width=\\textwidth, totalheight=\\textheight-2\\baselineskip,keepaspectratio}\n'

        if tabluar:
            lines[x] = lines[x].strip() + '\n\\end{adjustbox}\n'

    if new_row != False:
        for x, line in enumerate(lines):
            if x == 11:
                lines[x] = lines[x].strip() + new_row_[0]

    ### Add header
    len_line = len(lines)
    for x, line in enumerate(lines):
        if x ==1:
            if jupyter_preview:
                header= "\documentclass[preview]{standalone} \n\\usepackage[utf8]{inputenc}\n" \
            "\\usepackage{booktabs,caption,threeparttable, siunitx, adjustbox}\n\n" \
            "\\begin{document}"
            else:
                header= "\documentclass[12pt]{article} \n\\usepackage[utf8]{inputenc}\n" \
            "\\usepackage{booktabs,caption,threeparttable, siunitx, adjustbox}\n\n" \
            "\\begin{document}"

            lines[x] =  header

        if x == len_line- 1:
            footer = "\n\n\\end{document}"
            lines[x]  =  lines[x].strip() + footer



    with open(table_out, "w") as f:
        for line in lines:
            f.write(line)

                # Read in the file
    with open(table_out, 'r') as file:
        lines = file.read()

        # Parallel trend
        lines = lines.replace('target\_c:polluted\_threAbove:as.factor(year)2003',
                              '2003')
        lines = lines.replace('target\_c:polluted\_threAbove:as.factor(year)2004',
                              '2004')
        lines = lines.replace('target\_c:polluted\_threAbove:as.factor(year)2005',
                              '2005')
        lines = lines.replace('target\_c:polluted\_threAbove:as.factor(year)2006',
                              '2006')
        lines = lines.replace('target\_c:polluted\_threAbove:as.factor(year)2007',
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

        ### kuznet
        lines = lines.replace('dummy\_SOE\_c\_output5Above:ln\_gdp\_cap\_sqred',
                              'ln\_gdp\_cap\_sqred:dummy\_SOE\_c\_output5Above',
                               1)

        lines = lines.replace('dummy\_SOE\_c\_capital5Above:ln\_gdp\_cap\_sqred',
                              'ln\_gdp\_cap\_sqred:dummy\_SOE\_c\_capital5Above',
                               1)

        lines = lines.replace('dummy\_SOE\_c\_emp5Above:ln\_gdp\_cap\_sqred',
                              'ln\_gdp\_cap\_sqred:dummy\_SOE\_c\_emp5Above',
                               1)


        lines = lines.replace('ln\_gdp\_cap\_sqred',
          ' \\text{(ln gdp per cap) squared}_{ct} ')

        lines = lines.replace('ln\\_pop',
          ' \\text{(ln population)}_{ct} ')

        lines = lines.replace('ln\_gdp\_cap',
         ' \\text{(ln gdp per cap)}_{ct} ')

        lines = lines.replace('dummy\_SOE\_c\_output5Above',
          ' \\text{Output SOE median} ')

        lines = lines.replace('dummy\_SOE\_c\_capital5Above',
          ' \\text{Capital SOE median} ')

        lines = lines.replace('dummy\_SOE\_c\_emp5Above',
          ' \\text{Employment SOE median} ')

        # regex replace
        lines = lines.replace('output\_fcit', 'output_{cit}')
        lines = lines.replace('capital\_fcit', 'capital_{cit}')
        lines = lines.replace('labour\_fcit', 'labour_{cit}')

        # Interaction terms
        lines = lines.replace('TCZ\_cTCZ', ' TCZ_c ')
        lines = lines.replace('polluted\_threAbove', ' \\text{Polluted}_i ')
        lines = lines.replace('PeriodAfter', ' \\text{Period} ')

        # Share SOE
        if test_city_industry:
            lines = lines.replace('out\_share\_SOE',
                                  ' \\text{output share SOE}_{ci} ')
            lines = lines.replace('cap\_share\_SOE',
                                  ' \\text{capital share SOE}_{ci} ')
            lines = lines.replace('lab\_share\_SOE',
                                  ' \\text{labour share SOE}_{ci} ')
        else:
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

        lines = lines.replace('Herfindahl',
        ' \\text{Herfindahl}_{i}')

        lines = lines.replace('decile\_so2\_5Above',
        ' \\text{Polluted decile 5}_{i}')

        lines = lines.replace('decile\_so2\_6Above',
        ' \\text{Polluted decile 6}_{i}')

        lines = lines.replace('decile\_so2\_7Above',
        ' \\text{Polluted decile 7}_{i}')

        lines = lines.replace('decile\_so2\_8Above',
        ' \\text{Polluted decile 8}_{i}')

        lines = lines.replace('decile\_so2\_9Above',
        ' \\text{Polluted decile 9}_{i}')

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
        lines = lines.replace(': ', ' \\times ')




    # Write the file out again
    with open(table_out, 'w') as file:
        file.write(lines)

    ### Add Adjust box

    ### add table #
    if table_nte != None:
        with open(table_out, 'r') as f:
            lines = f.readlines()


        for x, line in enumerate(lines):
            adjusted = bool(re.search(r"end{adjustbox}",
                              line))

            if adjusted:
                lines[x] = lines[x].strip() + "\n\\begin{0} \n \\small \n \\item \\\\ \n{1} \n\\end{2}\n".format(
                "{tablenotes}",
                table_nte,
                "{tablenotes}")

        with open(table_out, "w") as f:
            for line in lines:
                f.write(line)

    if jupyter_preview:
        f = open('table_{}.tex'.format(table_number))
        r = tex2pix.Renderer(f, runbibtex=False)
        r.mkpdf('table_{}.pdf'.format(table_number))
        img = WImage(filename='table_{}.pdf'.format(table_number),
         resolution = resolution)
        return display(img)

def append_pdf(new_row, table_nte,resolution,name, remove_control = True,constraint = False,
city_industry= False,display = True):
    """
    """

    x = [a for a in os.listdir() if a.endswith(".txt")]

    #### Create separated PDF
    for i, val in enumerate(x):
        lb.beautify(table_number = i+1,
            remove_control= remove_control,
            constraint = constraint,
            city_industry = city_industry,
            new_row = new_row,
           table_nte = table_nte,
           jupyter_preview = False,
           resolution = resolution)

    ### Concatenate PDF
    x = [a for a in os.listdir() if a.endswith(".pdf")]
    merger = PdfFileMerger()

    for pdf in x:
        merger.append(open(pdf, 'rb'))

    with open("merge_pdf_{}.pdf".format(name), "wb") as fout:
        merger.write(fout)

    if display:
        with(WImage(filename='merge_pdf.pdf',resolution=200)) as source:
            images=source.sequence
            pages=len(images)
        for i in range(pages):
            display(WImage(images[i]))
