import calendar
from rich.console import Console
from rich.table import Table

def display_month_calendar(year, month):
    console = Console()
    months = [calendar.monthcalendar(year, m) for m in range(1,13)]

    for month in range(12):
        month_name = calendar.month_name[month + 1]

        table =  Table(title =f'[bold cyan] {month_name} \n {year} [/bold cyan]', show_lines=True )

        table.add_column('Sun', justify='center', style='white')
        table.add_column('Mon', justify='center', style='white')
        table.add_column('Tue', justify='center', style='white')
        table.add_column('Wed', justify='center', style='white')
        table.add_column('Thu', justify='center', style='white')
        table.add_column('Fri', justify='center', style='white')
        table.add_column('Sat', justify='center', style='Red')

        for week in months[month]:
            table.add_row(*[str(day) if day != 0 else '' for day in week])

        console.print(table)
        console.print('\n')

display_month_calendar(2005,12)

        



