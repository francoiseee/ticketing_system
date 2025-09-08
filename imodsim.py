import random
from datetime import datetime

# ANSI color codes for cross-platform compatibility
class Colors:
    # Text colors
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    
    # Background colors
    BG_RED = '\033[101m'
    BG_GREEN = '\033[102m'
    BG_YELLOW = '\033[103m'
    BG_BLUE = '\033[104m'
    BG_MAGENTA = '\033[105m'
    
    # Styles
    BOLD = '\033[1m'
    RESET = '\033[0m'


class Ticket:
    """Represents a concert ticket with unique ID, price, and status."""
    def __init__(self, ticket_id, price):
        self.ticket_id = ticket_id
        self.price = price
        self.status = "AVAILABLE"   # can be AVAILABLE or SOLD

    def __str__(self):
        status_color = Colors.GREEN if self.status == "AVAILABLE" else Colors.RED
        return f"{Colors.CYAN} Ticket #{self.ticket_id}{Colors.RESET} | {status_color}{self.status}{Colors.RESET} | {Colors.YELLOW}₱{self.price}{Colors.RESET}"


class User:
    """Represents a user who wants to buy a ticket."""
    def __init__(self, user_id, name, email):
        self.user_id = user_id
        self.name = name
        self.email = email

    def __str__(self):
        return f"{Colors.MAGENTA}{self.name}{Colors.RESET} ({Colors.BLUE}{self.email}{Colors.RESET})"


class Payment:
    """Represents a payment transaction for a ticket."""
    def __init__(self, amount, method):
        self.amount = amount
        self.method = method
        self.success = False
        self.timestamp = datetime.now()
    
    def process(self, success_rate=0.9):
        """
        Simulates payment processing.
        Success depends on a probability (default: 90%).
        """
        print(f"{Colors.YELLOW} Processing payment of ₱{self.amount} via {self.method}...{Colors.RESET}")
        self.success = random.random() < success_rate
        return self.success

    def __str__(self):
        status_color = Colors.GREEN if self.success else Colors.RED
        status_icon = "✅" if self.success else "❌"
        return f"{status_icon} {status_color}₱{self.amount} via {self.method}{Colors.RESET}"


class TicketingSystem:
    """Main ticketing system that handles ticket sales and reporting."""
    def __init__(self, total_tickets, price, venue_capacity):
        # Create ticket pool
        self.tickets = [Ticket(i, price) for i in range(1, total_tickets+1)]
        self.venue_capacity = venue_capacity
        self.sales = []       # list of successful sales (user, ticket, payment)
        self.attendance = 0   # track attendance later
        
        # Display system initialization
        print(f"\n{Colors.BG_BLUE}{Colors.WHITE} UDAYS CONCERT TICKETING SYSTEM INITIALIZED {Colors.RESET}")
        print(f"{Colors.CYAN}Total Tickets: {Colors.WHITE}{total_tickets}{Colors.RESET}")
        print(f"{Colors.YELLOW}Price per Ticket: {Colors.WHITE}₱{price}{Colors.RESET}")
        print(f"{Colors.GREEN}Venue Capacity: {Colors.WHITE}{venue_capacity}{Colors.RESET}")
        print(f"{Colors.BLUE}{'='*50}{Colors.RESET}\n")
    
    def buy_ticket(self, user, payment_method):
        """Handles the process of buying a ticket for a given user."""
        
        print(f"\n{Colors.CYAN} Processing purchase for {user.name}...{Colors.RESET}")
        
        # Step 1: Check available tickets
        available_tickets = [t for t in self.tickets if t.status == "AVAILABLE"]
        if not available_tickets:
            print(f"{Colors.BG_RED}{Colors.WHITE} SOLD OUT {Colors.RESET} No tickets left for {user.name}.")
            return None
        
        # Step 2: Choose the first available ticket
        ticket = available_tickets[0]
        print(f"{Colors.GREEN}✓ Found available ticket: {ticket}{Colors.RESET}")
        
        # Step 3: Process payment
        payment = Payment(ticket.price, payment_method)
        
        if payment.process():   # payment success
            ticket.status = "SOLD"
            self.sales.append((user, ticket, payment))
            print(f"{Colors.BG_GREEN}{Colors.WHITE} ✅ SUCCESS {Colors.RESET} {Colors.MAGENTA}{user.name}{Colors.RESET} successfully bought {Colors.CYAN}Ticket #{ticket.ticket_id}{Colors.RESET}!")
            return ticket
        else:                   # payment failure
            print(f"{Colors.BG_RED}{Colors.WHITE} ❌ PAYMENT FAILED {Colors.RESET} Payment failed for {Colors.MAGENTA}{user.name}{Colors.RESET}.")
            return None
    
    def track_attendance(self):
        """
        Updates attendance based on sold tickets,
        limited by the venue capacity.
        """
        sold_tickets = [t for t in self.tickets if t.status == "SOLD"]
        self.attendance = min(len(sold_tickets), self.venue_capacity)
        print(f"\n{Colors.GREEN} Attendance updated: {Colors.WHITE}{self.attendance}{Colors.GREEN}/{Colors.WHITE}{self.venue_capacity}{Colors.RESET}")
    
    def show_available_tickets(self):
        """Display all available tickets in a colorful format."""
        available = [t for t in self.tickets if t.status == "AVAILABLE"]
        print(f"\n{Colors.BG_GREEN}{Colors.WHITE}  AVAILABLE TICKETS ({len(available)}) {Colors.RESET}")
        
        if available:
            for i, ticket in enumerate(available[:10]):  # Show first 10
                print(f"  {ticket}")
            if len(available) > 10:
                print(f"  {Colors.YELLOW}... and {len(available) - 10} more tickets available{Colors.RESET}")
        else:
            print(f"  {Colors.RED}❌ No tickets available{Colors.RESET}")
    
    def report(self):
        """Generates a colorful sales and attendance report."""
        sold = len([t for t in self.tickets if t.status == "SOLD"])
        revenue = sum(t.price for t in self.tickets if t.status == "SOLD")
        sold_percentage = (sold / len(self.tickets)) * 100 if self.tickets else 0
        
        print(f"\n{Colors.BG_BLUE}{Colors.WHITE} SALES & ATTENDANCE REPORT {Colors.RESET}")
        print(f"{Colors.BLUE}{'='*50}{Colors.RESET}")
        
        # Tickets section
        print(f"{Colors.CYAN} Tickets Sold:{Colors.RESET} {Colors.WHITE}{sold}{Colors.RESET}/{Colors.WHITE}{len(self.tickets)}{Colors.RESET} ({Colors.YELLOW}{sold_percentage:.1f}%{Colors.RESET})")
        
        # Revenue section
        revenue_color = Colors.GREEN if revenue > 0 else Colors.RED
        print(f"{Colors.YELLOW} Gross Revenue:{Colors.RESET} {revenue_color}₱{revenue:,.2f}{Colors.RESET}")
        
        # Attendance section
        attendance_percentage = (self.attendance / self.venue_capacity) * 100 if self.venue_capacity else 0
        attendance_color = Colors.GREEN if attendance_percentage >= 80 else Colors.YELLOW if attendance_percentage >= 50 else Colors.RED
        print(f"{Colors.GREEN} Total Attendance:{Colors.RESET} {attendance_color}{self.attendance}{Colors.RESET}/{Colors.WHITE}{self.venue_capacity}{Colors.RESET} ({attendance_color}{attendance_percentage:.1f}%{Colors.RESET})")
        
        # Transactions section
        print(f"{Colors.MAGENTA} Valid Transactions:{Colors.RESET} {Colors.WHITE}{len(self.sales)}{Colors.RESET}")
        
        print(f"{Colors.BLUE}{'='*50}{Colors.RESET}")
        
        # Sales breakdown if there are sales
        if self.sales:
            print(f"\n{Colors.BG_YELLOW}{Colors.WHITE}  RECENT TRANSACTIONS {Colors.RESET}")
            for i, (user, ticket, payment) in enumerate(self.sales[-5:], 1):  # Show last 5 sales
                print(f"  {Colors.CYAN}{i}.{Colors.RESET} {user} → {ticket} | {payment}")


# Example usage with colorful demo
if __name__ == "__main__":
    # Create the ticketing system with peso pricing
    import random
    ticket_price = random.randint(100, 300)  # Random price between 100-300 pesos
    system = TicketingSystem(total_tickets=100, price=ticket_price, venue_capacity=150)
    
    # Create users with the specified names
    users = [
        User(1, "Jasmine Palma", "jasmine.palma@email.com"),
        User(2, "Aldrich Sabando", "aldrich.sabando@email.com"),
        User(3, "Nikko Parungao", "nikko.parungao@email.com"),
        User(4, "Francoise Gurango", "francoise.gurango@email.com"),
        User(5, "Allein Dane Maninang", "allein.maninang@email.com")
    ]
    
    # Show available tickets
    system.show_available_tickets()
    
    # Simulate ticket purchases with Philippine payment methods
    payment_methods = ["GCash", "PayMaya", "BPI Online", "BDO Online", "Credit Card", "Debit Card"]
    
    print(f"\n{Colors.BG_MAGENTA}{Colors.WHITE} SIMULATING UDAY'S CONCERT TICKET PURCHASES {Colors.RESET}")
    
    for user in users:
        method = random.choice(payment_methods)
        system.buy_ticket(user, method)
    
    # Track attendance
    system.track_attendance()
    
    # Generate final report
    system.report()
    
    print(f"\n{Colors.GREEN} Demo completed! Thank you for using Uday's Concert Ticketing System! 🎉{Colors.RESET}")