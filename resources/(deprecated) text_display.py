'''Deprecated'''

def tablizeData(heading_data, field_widths, data_lists, selection_id=None, id_row=0):
    '''
    Take lists of headings and data with the same index length and convert them into a human-
    readable table format.  Field widths determine the string length of each column.
    heading_data -> list of strings
    field_widths -> list of integers
    data_lists   -> list or tuple of lists containing data
    selection_id -> ID or name of selected object
    id_row       -> Column that the ID or name will be found in
    '''

    # Loop through the given lists of data and convert everything to a string if possible
    for data_list in data_lists:
        for i in range(len(data_list)):
            if data_list[i] is None:
                data_list[i] = ''
            else:
                try:
                    data_list[i] = str(data_list[i])
                except ValueError:
                    raise Exception(f'Could not convert data of type {type(data_list[i])} into a string')

    sl = '>'
    sr = '<'
    p = ' '
    h = '-'
    u = '|'
    row_str = ''
    rows = []

    # Loop through the heading data and make sure the headings fit in the defined limits in field_widths
    # Add dividers and any extra spacing needed to keep the rows uniform and easy to read string format
    begin_flag = True
    # For each index in heading data
    for i in range(len(heading_data)):

        # Check for the begin flag and set data_str to appropriate string
        if begin_flag is True:
            data_str = p + u
            begin_flag = False
        else:
            data_str = ''

        # If heading data is the same as the field width..
        if len(heading_data[i]) == field_widths[i]:
            data_str += h + heading_data[i] + h + u

        # If heading data is longer than the field width..
        elif len(heading_data[i]) > field_widths[i]:
            # Get the i'th item in data_list.  Splice it starting from the first character [0].
            # Continue the splice until the end string position MINUS field_widths[i] - len(data_list[i])
            # + 2.  Example:
            # s = 'Hello my name is Bob'
            # print(s[0:-10])
            # 'Hello my n'
            edited_head_str = heading_data[i][0:field_widths[i] - len(heading_data[i]) - 2]
            data_str += h + edited_head_str + '..' + h + u

        # If heading data is shorter than the field width..
        elif len(heading_data[i]) < field_widths[i]:
            data_str += h + heading_data[i] + (h * (field_widths[i] - len(heading_data[i]))) + h + u

        # Add the new data to the row
        row_str += data_str

    # Append the row string to the list of rows and reset its value to an empty string
    rows.append(row_str)
    row_str = ''

    # Loop thru the data in each data list and make sure the data fits in the defined limits in field_widths
    # Add dividers and any extra spacing needed to keep the rows uniform and easy to read string format
    selected = False
    # For each provided list in data_lists
    for data_list in data_lists:
        if selection_id is not None:
            if selection_id == int(data_list[id_row]):
                selected = True
            else:
                selected = False

        begin_flag = True

        # For each index in data list
        for i in range(len(data_list)):
            data_str = ''
            if selected is True and begin_flag is True:
                data_str += sl + u
                begin_flag = False
            elif begin_flag is True:
                data_str += p + u
                begin_flag = False
            else:
                data_str = ''

            # If length of the string is equal to limit...
            if len(data_list[i]) == field_widths[i]:
                data_str += p + data_list[i] + p + u

            # If length of the string is greater than the limit...
            elif len(data_list[i]) > field_widths[i]:
                # Get the i'th item in data_list.  Splice it starting from the first character [0].
                # Continue the splice until the end string position MINUS field_widths[i] - len(data_list[i])
                # + 2.  Example:
                # s = 'Hello my name is Bob'
                # print(s[0:-10])
                # 'Hello my n'
                edited_attr_str = data_list[i][0:field_widths[i] - len(data_list[i]) - 2]

                # Add the beginning and ending padding (p), dots to indicate continuation and
                # the union divider (u)
                data_str += p + edited_attr_str + '..' + p + u

                # data_str += p + data_list[i] + (p * (field_widths[i] - len(data_list[i]))) + p + u

            # If length of the string is less than the limit...
            elif len(data_list[i]) < field_widths[i]:
                data_str += p + data_list[i] + (p * (field_widths[i] - len(data_list[i]))) + p + u

            # Add the data string to the row string
            row_str += data_str

        # Add the ending selection marker if the row item is selected
        if selected is True:
            row_str += sr

        # Add the row string to the list of rows and reset the row string to an empty string
        rows.append(row_str)
        row_str = ''

    for r in rows:
        print(r)
    print()


def presentHeadings(head_list, width):
    '''
    Take strings to be presented to the user in a more uniform way
    '''

    pass
