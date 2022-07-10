from bs4 import BeautifulSoup
import pandas as pd

result_list = []


# procedure to get html item text, providing BS object and css selector
def soup_get(soup, selector):
    result = soup.select_one(selector)
    if result:
        result = result.get_text().strip()
    else:
        result = ''
    return result


# Creating Soup from HTML file
with open('rptTicketsByDate.html') as f:
    soup = BeautifulSoup(f, 'html5lib')

# Converting all table rows into a list of tickets, by iterating all <tr>
tbody = soup.select('body > table:nth-child(2) > tbody > tr')

all_tickets = []
new_ticket = False

for tr in tbody:

    if tr.get('title') == '[Right Click for Options]':
        if new_ticket:
            all_tickets.append(new_ticket)
        new_ticket = soup.new_tag('table')
        new_ticket.append(tr)

    if new_ticket and tr.get('title') != '[Right Click for Options]':
        new_ticket.append(tr)

if new_ticket:
    all_tickets.append(new_ticket)

# Parsing the List of tickets
for ticket in all_tickets:
    # Wrap data into body tag, 'notes' selector wont work properly without it
    body = soup.new_tag('body')
    body.append(ticket)
    ticket = body
    # Creating Soup from the Ticket, 'notes' selector wont work properly without it
    ticket = BeautifulSoup(str(ticket), 'html5lib')

    ticket_name = soup_get(ticket, '#tblOutlineBox > tbody > tr > td:nth-child(1)')
    ticket_status = soup_get(ticket, '#tblOutlineBox > tbody > tr:nth-child(1) > td:nth-child(2)')
    account_name = soup_get(ticket, '#tblOutlineBox > tbody > tr:nth-child(1) > td:nth-child(1) > span')
    work_type = soup_get(ticket, '#tblOutlineBox > tbody > tr:nth-child(2) > td:nth-child(1) > span')
    entered_by = soup_get(ticket, '#tblOutlineBox > tbody > tr:nth-child(1) > td:nth-child(2).fieldLabels')
    assigned_to = soup_get(ticket, '#tblOutlineBox > tbody > tr:nth-child(2) > td:nth-child(2)')
    issue_type = soup_get(ticket, '#tblOutlineBox > tbody > tr:nth-child(3) > td:nth-child(2)')
    sub_issue_type = soup_get(ticket, '#tblOutlineBox > tbody > tr:nth-child(4) > td:nth-child(2)')
    description = soup_get(ticket, '#tblOutlineBox > tbody > tr:nth-child(6) > td')

    # Parsing Ticket Notes
    notes = ticket.select('body > table > tbody > tr > td > table:NOT(body > table > tbody > tr:nth-child(1) > td > table):NOT(body > table > tbody > tr:nth-child(2) > td > table)')

    notes_content = ''

    for note in notes:
        note_time = soup_get(note, 'table > tbody > tr:nth-child(2) > td:nth-child(3)')
        note_owner = soup_get(note, 'table > tbody > tr:nth-child(2) > td:nth-child(4)')
        note_status = soup_get(note, 'table > tbody > tr:nth-child(2) > td:nth-child(5)')
        # note_description = soup_get(note, 'table > tbody > tr:nth-child(3) > td:nth-child(2) > table > tbody > tr:nth-child(1) > td:nth-child(2) > span')
        note_description = soup_get(note, 'table > tbody  span')
        note_content = f'{note_time}, Owner: {note_owner}, Status: {note_status}, \n\n {note_description} \n\n'
        notes_content += note_content

    # Compiling Ticket Row
    result_row = {
        'Ticket Name': ticket_name,
        'Status': ticket_status[9:],
        'Account Name': account_name,
        'Work Type': work_type,
        'Enter Time': entered_by[-10:],
        'Entered By': entered_by[11:-13],
        'Assigned To': assigned_to[22:],
        'Issue Type': issue_type,
        'Sub Issue Type': sub_issue_type,
        'Description': description,
        'Notes': notes_content
    }

    # Adding Ticket to the Result DataFrame
    result_list.append(result_row)

# Saving to file
result_df = pd.DataFrame(result_list)
result_df.to_csv('result.csv', index=False)

print('Done!')

