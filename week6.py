import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime

# Constants for ticket prices
PRICES = {
    'adult': {'1_day': 20.00, '2_day': 30.00},
    'child': {'1_day': 12.00, '2_day': 18.00},
    'senior': {'1_day': 16.00, '2_day': 24.00},
    'family': {'1_day': 60.00, '2_day': 90.00},
    'group': {'1_day': 15.00, '2_day': 22.00}
}

# Constants for extra attractions
EXTRAS = {
    'lion_feeding': 2.50,
    'penguin_feeding': 2.00,
    'bbq': 5.00
}

# Function to calculate the total cost of the booking
def calculate_total(tickets, days, extras):
    total = 0
    day_price = f'{days}_day'
    for ticket_type, quantity in tickets.items():
        total += PRICES[ticket_type][day_price] * quantity
    for extra, included in extras.items():
        if included:
            total += EXTRAS[extra] * sum(tickets.values())
    return total

# Function to generate a unique booking number
def generate_booking_number():
    return datetime.now().strftime('%Y%m%d%H%M%S')

# Function to suggest a better package if available
def suggest_better_package(tickets, days, total_cost):
    suggestions = []
    # Check if family package is a better deal
    num_people = tickets['adult'] + tickets['child'] + tickets['senior']
    family_cost = PRICES['family'][f'{days}_day']
    if num_people >= 3 and num_people <= 5 and total_cost > family_cost:
        savings = total_cost - family_cost
        suggestions.append(f"Consider the family package for better value. You could save ${savings:.2f}!")

    # Check if group package is a better deal
    group_cost_per_person = PRICES['group'][f'{days}_day']
    if num_people >= 6 and total_cost > (num_people * group_cost_per_person):
        savings = total_cost - (num_people * group_cost_per_person)
        suggestions.append(f"Consider the group package for better value. You could save ${savings:.2f} per person!")

    return suggestions

# GUI Application
class WildlifeParkBookingApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Wildlife Park Ticket Booking')

        # Variables for ticket quantities
        self.adult_tickets_var = tk.IntVar(value=0)
        self.child_tickets_var = tk.IntVar(value=0)
        self.senior_tickets_var = tk.IntVar(value=0)

        # Variables for day selection
        self.day_var = tk.StringVar(value='1')

        # Variables for extra attractions
        self.lion_feeding_var = tk.BooleanVar(value=False)
        self.penguin_feeding_var = tk.BooleanVar(value=False)
        self.bbq_var = tk.BooleanVar(value=False)

        # Setup the UI
        self.setup_ui()

    def setup_ui(self):
        # Ticket entry fields
        ttk.Label(self.root, text='Adult Tickets:').grid(row=0, column=0)
        ttk.Entry(self.root, textvariable=self.adult_tickets_var).grid(row=0, column=1)

        ttk.Label(self.root, text='Child Tickets:').grid(row=1, column=0)
        ttk.Entry(self.root, textvariable=self.child_tickets_var).grid(row=1, column=1)

        ttk.Label(self.root, text='Senior Tickets:').grid(row=2, column=0)
        ttk.Entry(self.root, textvariable=self.senior_tickets_var).grid(row=2, column=1)


        # Day selection radio buttons
        ttk.Radiobutton(self.root, text='1 Day', variable=self.day_var, value='1').grid(row=3, column=0)
        ttk.Radiobutton(self.root, text='2 Days', variable=self.day_var, value='2').grid(row=3, column=1)

        # Extra attractions checkboxes
        ttk.Checkbutton(self.root, text='Lion Feeding', variable=self.lion_feeding_var).grid(row=4, column=0)
        ttk.Checkbutton(self.root, text='Penguin Feeding', variable=self.penguin_feeding_var).grid(row=4, column=1)
        ttk.Checkbutton(self.root, text='BBQ (2-day ticket only)', variable=self.bbq_var).grid(row=4, column=2)

        # Calculate button
        ttk.Button(self.root, text='Calculate Total', command=self.calculate).grid(row=5, column=0, columnspan=3)

    def calculate(self):
        # Get ticket quantities
        tickets = {
            'adult': self.adult_tickets_var.get(),
            'child': self.child_tickets_var.get(),
            'senior': self.senior_tickets_var.get()
        }

        # Get selected day
        days = self.day_var.get()

        # Get extras
        extras = {
            'lion_feeding': self.lion_feeding_var.get(),
            'penguin_feeding': self.penguin_feeding_var.get(),
            'bbq': self.bbq_var.get() and days == '2'
        }

        # Calculate total cost
        total_cost = calculate_total(tickets, days, extras)

        # Generate booking number
        booking_number = generate_booking_number()

        # Suggest a better package if available
        suggestions = suggest_better_package(tickets, days, total_cost)

        # Display booking details and suggestions in a message box
        booking_details = f'Total Cost: ${total_cost:.2f}\nBooking Number: {booking_number}'
        if suggestions:
            booking_details += '\n\n' + '\n'.join(suggestions)
        messagebox.showinfo('Booking Details', booking_details)

if __name__ == '__main__':
    root = tk.Tk()
    app = WildlifeParkBookingApp(root)
    root.mainloop()
