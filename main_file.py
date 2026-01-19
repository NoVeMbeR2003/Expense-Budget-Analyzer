import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
import json
import os
import csv
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
matplotlib.use('TkAgg')

class ExpenseBudgetAnalyzerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("💰 Expense & Budget Analyzer")
        self.root.geometry("1200x700")
        self.root.configure(bg='#f0f2f5')
        
        # Set style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.configure_styles()
        
        # Data storage
        self.data_file = "budget_data.json"
        self.users_file = "users.json"
        self.current_user = None
        self.budgets = {}
        self.expenses = {}
        self.categories = ["Food", "Travel", "Rent", "Entertainment", "Others"]
        self.months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                      'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        self.budget_types = ['Personal', 'Travel', 'Emergency', 'Shopping', 'Custom']
        
        # Load data
        self.load_users()
        
        # Show login screen
        self.show_login_screen()
    
    def configure_styles(self):
        """Configure custom styles for widgets"""
        self.style.configure('Title.TLabel', font=('Arial', 24, 'bold'), background='#f0f2f5')
        self.style.configure('Heading.TLabel', font=('Arial', 16, 'bold'), background='#f0f2f5')
        self.style.configure('Normal.TLabel', font=('Arial', 11), background='#f0f2f5')
        
        self.style.configure('Primary.TButton', font=('Arial', 11, 'bold'))
        self.style.map('Primary.TButton',
                      foreground=[('active', 'white'), ('!disabled', 'white')],
                      background=[('active', '#0056b3'), ('!disabled', '#007bff')])
        
        self.style.configure('Success.TButton', font=('Arial', 11, 'bold'))
        self.style.map('Success.TButton',
                      foreground=[('active', 'white'), ('!disabled', 'white')],
                      background=[('active', '#1e7e34'), ('!disabled', '#28a745')])
        
        self.style.configure('Danger.TButton', font=('Arial', 11, 'bold'))
        self.style.map('Danger.TButton',
                      foreground=[('active', 'white'), ('!disabled', 'white')],
                      background=[('active', '#c82333'), ('!disabled', '#dc3545')])
        
        self.style.configure('Warning.TButton', font=('Arial', 11, 'bold'))
        self.style.map('Warning.TButton',
                      foreground=[('active', 'black'), ('!disabled', 'black')],
                      background=[('active', '#e0a800'), ('!disabled', '#ffc107')])
        
        self.style.configure('Treeview', font=('Arial', 10))
        self.style.configure('Treeview.Heading', font=('Arial', 11, 'bold'))
    
    def clear_window(self):
        """Clear all widgets from the window"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def show_login_screen(self):
        """Display login/register screen"""
        self.clear_window()
        
        # Main container
        main_frame = tk.Frame(self.root, bg='#f0f2f5', padx=20, pady=20)
        main_frame.pack(expand=True, fill='both')
        
        # Title
        title_label = ttk.Label(main_frame, text="💰 Expense & Budget Analyzer", 
                               style='Title.TLabel')
        title_label.pack(pady=(0, 30))
        
        # Login Frame
        login_frame = tk.Frame(main_frame, bg='white', padx=30, pady=30, 
                              relief='groove', borderwidth=2)
        login_frame.pack(pady=20)
        
        ttk.Label(login_frame, text="🔐 User Authentication", 
                 style='Heading.TLabel', background='white').pack(pady=(0, 20))
        
        # Username
        tk.Label(login_frame, text="Username:", font=('Arial', 11), 
                bg='white').pack(anchor='w', pady=(0, 5))
        self.username_entry = ttk.Entry(login_frame, font=('Arial', 11), width=30)
        self.username_entry.pack(pady=(0, 15))
        
        # Password
        tk.Label(login_frame, text="Password:", font=('Arial', 11), 
                bg='white').pack(anchor='w', pady=(0, 5))
        self.password_entry = ttk.Entry(login_frame, font=('Arial', 11), 
                                       width=30, show="•")
        self.password_entry.pack(pady=(0, 25))
        
        # Buttons Frame
        button_frame = tk.Frame(login_frame, bg='white')
        button_frame.pack()
        
        ttk.Button(button_frame, text="Login", style='Primary.TButton',
                  command=self.login).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Register", style='Success.TButton',
                  command=self.register).pack(side='left', padx=5)
        
        # Bind Enter key to login
        self.root.bind('<Return>', lambda e: self.login())
    
    def login(self):
        """Handle user login"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return
        
        if username in self.users and self.users[username]["password"] == password:
            self.current_user = username
            self.load_data()
            messagebox.showinfo("Success", f"Welcome back, {username}!")
            self.show_main_dashboard()
        else:
            messagebox.showerror("Error", "Invalid username or password")
    
    def register(self):
        """Handle user registration"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username:
            messagebox.showerror("Error", "Username cannot be empty")
            return
        
        if not password:
            messagebox.showerror("Error", "Password cannot be empty")
            return
        
        if username in self.users:
            messagebox.showerror("Error", "Username already exists")
            return
        
        self.users[username] = {
            "password": password,
            "created_at": datetime.now().isoformat()
        }
        self.current_user = username
        self.save_users()
        self.budgets = {}
        self.expenses = {}
        messagebox.showinfo("Success", f"Account created successfully!\nWelcome, {username}!")
        self.show_main_dashboard()
    
    def load_users(self):
        """Load users from file"""
        if os.path.exists(self.users_file):
            try:
                with open(self.users_file, 'r') as f:
                    self.users = json.load(f)
            except:
                self.users = {}
        else:
            self.users = {}
    
    def save_users(self):
        """Save users to file"""
        with open(self.users_file, 'w') as f:
            json.dump(self.users, f, indent=2)
    
    def load_data(self):
        """Load data from JSON file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    if self.current_user in data:
                        user_data = data[self.current_user]
                        self.budgets = user_data.get('budgets', {})
                        self.expenses = user_data.get('expenses', {})
            except:
                self.budgets = {}
                self.expenses = {}
        else:
            self.budgets = {}
            self.expenses = {}
    
    def save_data(self):
        """Save data to JSON file"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    all_data = json.load(f)
            else:
                all_data = {}
            
            all_data[self.current_user] = {
                'budgets': self.budgets,
                'expenses': self.expenses,
                'last_updated': datetime.now().isoformat()
            }
            
            with open(self.data_file, 'w') as f:
                json.dump(all_data, f, indent=2)
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Error saving data: {e}")
            return False
    
    def show_main_dashboard(self):
        """Display main dashboard"""
        self.clear_window()
        
        # Create menu bar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Save Data", command=self.save_data)
        file_menu.add_command(label="Export Report", command=self.export_report_dialog)
        file_menu.add_separator()
        file_menu.add_command(label="Logout", command=self.logout)
        file_menu.add_command(label="Exit", command=self.exit_app)
        
        # Budget menu
        budget_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Budget", menu=budget_menu)
        budget_menu.add_command(label="Create New Budget", command=self.create_budget_dialog)
        budget_menu.add_command(label="View All Budgets", command=self.view_all_budgets)
        budget_menu.add_command(label="Delete Budget", command=self.delete_budget_dialog)
        
        # Expense menu
        expense_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Expense", menu=expense_menu)
        expense_menu.add_command(label="Add Expense", command=self.add_expense_dialog)
        expense_menu.add_command(label="View Expenses", command=self.view_expenses)
        expense_menu.add_command(label="Edit/Delete Expense", command=self.edit_expense_dialog)
        
        # Report menu
        report_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Reports", menu=report_menu)
        report_menu.add_command(label="Budget Analysis", command=self.analyze_budget_dialog)
        report_menu.add_command(label="Expense Summary", command=self.expense_summary)
        report_menu.add_command(label="Budget Warnings", command=self.check_budget_warnings)
        report_menu.add_separator()
        report_menu.add_command(label="Pie Chart", command=self.show_pie_chart)
        report_menu.add_command(label="Bar Chart", command=self.show_bar_chart)
        report_menu.add_command(label="Line Chart", command=self.show_line_chart)
        
        # Main content area
        main_frame = tk.Frame(self.root, bg='#f0f2f5')
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Welcome message
        welcome_label = ttk.Label(main_frame, 
                                 text=f"👋 Welcome, {self.current_user}!",
                                 style='Title.TLabel')
        welcome_label.pack(pady=(0, 30))
        
        # Dashboard widgets in a grid
        dashboard_frame = tk.Frame(main_frame, bg='#f0f2f5')
        dashboard_frame.pack(expand=True, fill='both')
        
        # Row 1: Quick Stats
        stats_frame = tk.Frame(dashboard_frame, bg='#f0f2f5')
        stats_frame.grid(row=0, column=0, columnspan=3, pady=(0, 20), sticky='ew')
        
        total_budgets = len(self.budgets)
        total_expenses = sum(len(exp_list) for exp_list in self.expenses.values())
        
        # Create stat cards
        stat_cards = [
            ("📊 Budgets", str(total_budgets), "#007bff"),
            ("💰 Expenses", str(total_expenses), "#28a745"),
            ("📈 Active", f"{len([b for b in self.budgets.values() if b['total_budget'] > 0])}", "#ffc107")
        ]
        
        for i, (title, value, color) in enumerate(stat_cards):
            card = tk.Frame(stats_frame, bg=color, padx=20, pady=15, relief='raised', borderwidth=1)
            card.grid(row=0, column=i, padx=10, sticky='nsew')
            
            tk.Label(card, text=title, font=('Arial', 12, 'bold'), 
                    bg=color, fg='white').pack()
            tk.Label(card, text=value, font=('Arial', 24, 'bold'), 
                    bg=color, fg='white').pack()
        
        # Configure grid columns
        for i in range(3):
            stats_frame.grid_columnconfigure(i, weight=1)
        
        # Row 2: Quick Actions
        actions_frame = tk.Frame(dashboard_frame, bg='#f0f2f5')
        actions_frame.grid(row=1, column=0, columnspan=3, pady=(0, 20))
        
        tk.Label(actions_frame, text="Quick Actions", font=('Arial', 14, 'bold'),
                bg='#f0f2f5').pack(pady=(0, 10))
        
        action_buttons = [
            ("📝 Create Budget", self.create_budget_dialog, 'Primary.TButton'),
            ("➕ Add Expense", self.add_expense_dialog, 'Success.TButton'),
            ("📊 View Analysis", self.analyze_budget_dialog, 'Warning.TButton'),
            ("📋 View Expenses", self.view_expenses, 'Normal.TButton'),
            ("⚠️ Check Warnings", self.check_budget_warnings, 'Danger.TButton'),
            ("📈 View Charts", self.show_pie_chart, 'Primary.TButton')
        ]
        
        button_frame = tk.Frame(actions_frame, bg='#f0f2f5')
        button_frame.pack()
        
        for i, (text, command, style) in enumerate(action_buttons):
            btn = ttk.Button(button_frame, text=text, style=style, command=command)
            btn.grid(row=i//3, column=i%3, padx=5, pady=5, ipadx=10, ipady=5)
        
        # Row 3: Recent Budgets
        recent_frame = tk.Frame(dashboard_frame, bg='white', relief='groove', borderwidth=1)
        recent_frame.grid(row=2, column=0, columnspan=3, pady=(0, 20), sticky='ew', padx=10)
        
        tk.Label(recent_frame, text="Recent Budgets", font=('Arial', 14, 'bold'),
                bg='white').pack(pady=10)
        
        if self.budgets:
            # Create a treeview for budgets
            tree_frame = tk.Frame(recent_frame, bg='white')
            tree_frame.pack(fill='both', expand=True, padx=10, pady=(0, 10))
            
            tree = ttk.Treeview(tree_frame, columns=('Type', 'Month', 'Budget', 'Spent', 'Remaining'), 
                               show='headings', height=min(5, len(self.budgets)))
            
            # Define headings
            tree.heading('Type', text='Type')
            tree.heading('Month', text='Month')
            tree.heading('Budget', text='Total Budget')
            tree.heading('Spent', text='Total Spent')
            tree.heading('Remaining', text='Remaining')
            
            tree.column('Type', width=100)
            tree.column('Month', width=80)
            tree.column('Budget', width=120)
            tree.column('Spent', width=120)
            tree.column('Remaining', width=120)
            
            # Add scrollbar
            scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)
            scrollbar.pack(side='right', fill='y')
            tree.pack(side='left', fill='both', expand=True)
            
            # Insert data
            for budget_name, budget in list(self.budgets.items())[-5:]:
                expenses = self.expenses.get(budget_name, [])
                total_spent = sum(exp['amount'] for exp in expenses)
                remaining = budget['total_budget'] - total_spent
                
                tree.insert('', 'end', values=(
                    budget['type'],
                    budget['month'],
                    f"₹{budget['total_budget']:,.2f}",
                    f"₹{total_spent:,.2f}",
                    f"₹{remaining:,.2f}"
                ))
        else:
            tk.Label(recent_frame, text="No budgets created yet. Create your first budget!",
                    font=('Arial', 11), bg='white', fg='gray').pack(pady=20)
        
        # Configure grid weights
        for i in range(3):
            dashboard_frame.grid_columnconfigure(i, weight=1)
        dashboard_frame.grid_rowconfigure(2, weight=1)
    
    def logout(self):
        """Logout current user"""
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.save_data()
            self.current_user = None
            self.budgets = {}
            self.expenses = {}
            self.show_login_screen()
    
    def exit_app(self):
        """Exit the application"""
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            self.save_data()
            self.root.quit()
    
    def create_budget_dialog(self):
        """Dialog for creating a new budget"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Create New Budget")
        dialog.geometry("500x600")
        dialog.configure(bg='#f0f2f5')
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Title
        ttk.Label(dialog, text="📊 Create New Budget", 
                 style='Heading.TLabel', background='#f0f2f5').pack(pady=20)
        
        # Main form frame
        form_frame = tk.Frame(dialog, bg='white', padx=30, pady=30)
        form_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        # Budget Name
        tk.Label(form_frame, text="Budget Name:", font=('Arial', 11), 
                bg='white').grid(row=0, column=0, sticky='w', pady=(0, 5))
        name_entry = ttk.Entry(form_frame, font=('Arial', 11), width=30)
        name_entry.grid(row=0, column=1, pady=(0, 15), padx=(10, 0))
        
        # Budget Type
        tk.Label(form_frame, text="Budget Type:", font=('Arial', 11), 
                bg='white').grid(row=1, column=0, sticky='w', pady=(0, 5))
        type_var = tk.StringVar(value=self.budget_types[0])
        type_combo = ttk.Combobox(form_frame, textvariable=type_var, 
                                 values=self.budget_types, font=('Arial', 11),
                                 width=27, state='readonly')
        type_combo.grid(row=1, column=1, pady=(0, 15), padx=(10, 0))
        
        # Custom Type Frame (hidden initially)
        custom_frame = tk.Frame(form_frame, bg='white')
        custom_frame.grid(row=2, column=0, columnspan=2, sticky='ew', pady=(0, 15))
        custom_frame.grid_remove()
        
        tk.Label(custom_frame, text="Custom Type:", font=('Arial', 11), 
                bg='white').pack(side='left')
        custom_entry = ttk.Entry(custom_frame, font=('Arial', 11), width=25)
        custom_entry.pack(side='left', padx=(10, 0))
        
        def on_type_change(event):
            if type_var.get() == 'Custom':
                custom_frame.grid()
            else:
                custom_frame.grid_remove()
        
        type_combo.bind('<<ComboboxSelected>>', on_type_change)
        
        # Month
        tk.Label(form_frame, text="Month:", font=('Arial', 11), 
                bg='white').grid(row=3, column=0, sticky='w', pady=(0, 5))
        month_var = tk.StringVar(value=self.months[datetime.now().month - 1])
        month_combo = ttk.Combobox(form_frame, textvariable=month_var, 
                                  values=self.months, font=('Arial', 11),
                                  width=27, state='readonly')
        month_combo.grid(row=3, column=1, pady=(0, 15), padx=(10, 0))
        
        # Total Budget
        tk.Label(form_frame, text="Total Budget (₹):", font=('Arial', 11), 
                bg='white').grid(row=4, column=0, sticky='w', pady=(0, 5))
        budget_entry = ttk.Entry(form_frame, font=('Arial', 11), width=30)
        budget_entry.grid(row=4, column=1, pady=(0, 15), padx=(10, 0))
        
        # Configure grid columns
        form_frame.grid_columnconfigure(0, weight=1)
        form_frame.grid_columnconfigure(1, weight=2)
        
        # Buttons
        button_frame = tk.Frame(dialog, bg='#f0f2f5')
        button_frame.pack(pady=(0, 20))
        
        def create_budget():
            name = name_entry.get().strip()
            budget_type = type_var.get()
            month = month_var.get()
            
            if not name:
                messagebox.showerror("Error", "Budget name cannot be empty")
                return
            
            if budget_type == 'Custom':
                custom_type = custom_entry.get().strip()
                if not custom_type:
                    messagebox.showerror("Error", "Custom type cannot be empty")
                    return
                budget_type = custom_type
            
            try:
                total_budget = float(budget_entry.get())
                if total_budget <= 0:
                    messagebox.showerror("Error", "Budget must be positive")
                    return
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number for budget")
                return
            
            # Check for existing budget
            if name in self.budgets:
                if not messagebox.askyesno("Confirm", f"Budget '{name}' already exists. Overwrite?"):
                    return
            
            # Create budget
            self.budgets[name] = {
                'type': budget_type,
                'month': month,
                'total_budget': total_budget,
                'created_at': datetime.now().isoformat(),
                'expenses': {}
            }
            
            messagebox.showinfo("Success", f"Budget '{name}' created successfully!")
            dialog.destroy()
            self.show_main_dashboard()
        
        ttk.Button(button_frame, text="Create Budget", style='Success.TButton',
                  command=create_budget).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Cancel", style='Danger.TButton',
                  command=dialog.destroy).pack(side='left', padx=5)
    
    def add_expense_dialog(self):
        """Dialog for adding expenses"""
        if not self.budgets:
            messagebox.showerror("Error", "No budgets available. Please create a budget first.")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Expense")
        dialog.geometry("500x700")
        dialog.configure(bg='#f0f2f5')
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Title
        ttk.Label(dialog, text="💸 Add Expense", 
                 style='Heading.TLabel', background='#f0f2f5').pack(pady=20)
        
        # Main form frame
        form_frame = tk.Frame(dialog, bg='white', padx=30, pady=30)
        form_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        # Select Budget
        tk.Label(form_frame, text="Select Budget:", font=('Arial', 11), 
                bg='white').grid(row=0, column=0, sticky='w', pady=(0, 5))
        budget_var = tk.StringVar()
        budget_combo = ttk.Combobox(form_frame, textvariable=budget_var, 
                                   values=list(self.budgets.keys()), 
                                   font=('Arial', 11), width=27, state='readonly')
        budget_combo.grid(row=0, column=1, pady=(0, 15), padx=(10, 0))
        
        # Budget info label
        budget_info_label = tk.Label(form_frame, text="", font=('Arial', 10), 
                                    bg='white', fg='blue')
        budget_info_label.grid(row=1, column=0, columnspan=2, pady=(0, 15))
        
        def update_budget_info(event=None):
            budget_name = budget_var.get()
            if budget_name in self.budgets:
                budget = self.budgets[budget_name]
                expenses = self.expenses.get(budget_name, [])
                total_spent = sum(exp['amount'] for exp in expenses)
                remaining = budget['total_budget'] - total_spent
                budget_info_label.config(
                    text=f"Total: ₹{budget['total_budget']:,.2f} | "
                         f"Spent: ₹{total_spent:,.2f} | "
                         f"Remaining: ₹{remaining:,.2f}"
                )
        
        budget_combo.bind('<<ComboboxSelected>>', update_budget_info)
        
        # Category
        tk.Label(form_frame, text="Category:", font=('Arial', 11), 
                bg='white').grid(row=2, column=0, sticky='w', pady=(0, 5))
        category_var = tk.StringVar(value=self.categories[0])
        category_combo = ttk.Combobox(form_frame, textvariable=category_var, 
                                     values=self.categories, font=('Arial', 11),
                                     width=27, state='readonly')
        category_combo.grid(row=2, column=1, pady=(0, 15), padx=(10, 0))
        
        # Description
        tk.Label(form_frame, text="Description:", font=('Arial', 11), 
                bg='white').grid(row=3, column=0, sticky='w', pady=(0, 5))
        desc_entry = ttk.Entry(form_frame, font=('Arial', 11), width=30)
        desc_entry.grid(row=3, column=1, pady=(0, 15), padx=(10, 0))
        
        # Amount
        tk.Label(form_frame, text="Amount (₹):", font=('Arial', 11), 
                bg='white').grid(row=4, column=0, sticky='w', pady=(0, 5))
        amount_entry = ttk.Entry(form_frame, font=('Arial', 11), width=30)
        amount_entry.grid(row=4, column=1, pady=(0, 15), padx=(10, 0))
        
        # Date
        tk.Label(form_frame, text="Date (DD-MM-YYYY):", font=('Arial', 11), 
                bg='white').grid(row=5, column=0, sticky='w', pady=(0, 5))
        date_entry = ttk.Entry(form_frame, font=('Arial', 11), width=30)
        date_entry.insert(0, datetime.now().strftime("%d-%m-%Y"))
        date_entry.grid(row=5, column=1, pady=(0, 15), padx=(10, 0))
        
        # Configure grid columns
        form_frame.grid_columnconfigure(0, weight=1)
        form_frame.grid_columnconfigure(1, weight=2)
        
        # Buttons
        button_frame = tk.Frame(dialog, bg='#f0f2f5')
        button_frame.pack(pady=(0, 20))
        
        def add_expense():
            budget_name = budget_var.get()
            if not budget_name:
                messagebox.showerror("Error", "Please select a budget")
                return
            
            description = desc_entry.get().strip()
            if not description:
                messagebox.showerror("Error", "Description cannot be empty")
                return
            
            try:
                amount = float(amount_entry.get())
                if amount <= 0:
                    messagebox.showerror("Error", "Amount must be positive")
                    return
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number for amount")
                return
            
            date_str = date_entry.get().strip()
            try:
                expense_date = datetime.strptime(date_str, "%d-%m-%Y")
            except ValueError:
                messagebox.showerror("Error", "Invalid date format. Use DD-MM-YYYY")
                return
            
            # Add expense
            expense_id = f"exp_{datetime.now().timestamp()}"
            if budget_name not in self.expenses:
                self.expenses[budget_name] = []
            
            self.expenses[budget_name].append({
                'id': expense_id,
                'name': description,
                'category': category_var.get(),
                'amount': amount,
                'date': date_str,
                'added_at': datetime.now().isoformat()
            })
            
            messagebox.showinfo("Success", f"Expense added successfully!")
            
            # Check for budget warning
            self.check_single_budget_warning(budget_name)
            
            dialog.destroy()
            self.show_main_dashboard()
        
        ttk.Button(button_frame, text="Add Expense", style='Success.TButton',
                  command=add_expense).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Cancel", style='Danger.TButton',
                  command=dialog.destroy).pack(side='left', padx=5)
    
    def view_all_budgets(self):
        """Display all budgets in a new window"""
        if not self.budgets:
            messagebox.showinfo("Info", "No budgets available.")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("All Budgets")
        dialog.geometry("900x500")
        dialog.configure(bg='#f0f2f5')
        
        # Title
        ttk.Label(dialog, text="📁 All Budgets", 
                 style='Heading.TLabel', background='#f0f2f5').pack(pady=20)
        
        # Create treeview with scrollbar
        tree_frame = tk.Frame(dialog, bg='#f0f2f5')
        tree_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        # Create Treeview
        columns = ('Name', 'Type', 'Month', 'Total Budget', 'Total Spent', 'Remaining', '% Used')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        # Define headings
        for col in columns:
            tree.heading(col, text=col)
            if col == 'Name':
                tree.column(col, width=150)
            elif col in ['Total Budget', 'Total Spent', 'Remaining']:
                tree.column(col, width=120)
            else:
                tree.column(col, width=100)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        tree.pack(side='left', fill='both', expand=True)
        
        # Insert data
        for budget_name, budget in self.budgets.items():
            expenses = self.expenses.get(budget_name, [])
            total_spent = sum(exp['amount'] for exp in expenses)
            remaining = budget['total_budget'] - total_spent
            percent_used = (total_spent / budget['total_budget'] * 100) if budget['total_budget'] > 0 else 0
            
            tree.insert('', 'end', values=(
                budget_name,
                budget['type'],
                budget['month'],
                f"₹{budget['total_budget']:,.2f}",
                f"₹{total_spent:,.2f}",
                f"₹{remaining:,.2f}",
                f"{percent_used:.1f}%"
            ))
        
        # Buttons
        button_frame = tk.Frame(dialog, bg='#f0f2f5')
        button_frame.pack(pady=(0, 20))
        
        ttk.Button(button_frame, text="Close", style='Primary.TButton',
                  command=dialog.destroy).pack(side='left', padx=5)
    
    def view_expenses(self):
        """Display all expenses in a new window"""
        if not self.expenses:
            messagebox.showinfo("Info", "No expenses available.")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("All Expenses")
        dialog.geometry("1000x500")
        dialog.configure(bg='#f0f2f5')
        
        # Title
        ttk.Label(dialog, text="📋 All Expenses", 
                 style='Heading.TLabel', background='#f0f2f5').pack(pady=20)
        
        # Create notebook for different budgets
        notebook = ttk.Notebook(dialog)
        notebook.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        for budget_name in self.budgets.keys():
            expenses = self.expenses.get(budget_name, [])
            if not expenses:
                continue
            
            # Create tab for this budget
            tab = ttk.Frame(notebook)
            notebook.add(tab, text=f"{budget_name} ({len(expenses)})")
            
            # Create treeview for this budget's expenses
            tree_frame = tk.Frame(tab)
            tree_frame.pack(fill='both', expand=True, padx=10, pady=10)
            
            columns = ('Date', 'Description', 'Category', 'Amount')
            tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=10)
            
            # Define headings
            for col in columns:
                tree.heading(col, text=col)
                if col == 'Description':
                    tree.column(col, width=300)
                else:
                    tree.column(col, width=150)
            
            # Add scrollbar
            scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)
            scrollbar.pack(side='right', fill='y')
            tree.pack(side='left', fill='both', expand=True)
            
            # Insert expenses sorted by date
            sorted_expenses = sorted(expenses, 
                                   key=lambda x: datetime.strptime(x['date'], "%d-%m-%Y"), 
                                   reverse=True)
            
            total_amount = 0
            for exp in sorted_expenses:
                tree.insert('', 'end', values=(
                    exp['date'],
                    exp['name'],
                    exp['category'],
                    f"₹{exp['amount']:,.2f}"
                ))
                total_amount += exp['amount']
            
            # Add total label
            total_label = tk.Label(tab, text=f"Total: ₹{total_amount:,.2f}", 
                                  font=('Arial', 12, 'bold'))
            total_label.pack(pady=10)
        
        # Close button
        button_frame = tk.Frame(dialog, bg='#f0f2f5')
        button_frame.pack(pady=(0, 20))
        
        ttk.Button(button_frame, text="Close", style='Primary.TButton',
                  command=dialog.destroy).pack()
    
    def analyze_budget_dialog(self):
        """Dialog for analyzing a specific budget"""
        if not self.budgets:
            messagebox.showerror("Error", "No budgets available.")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Analyze Budget")
        dialog.geometry("600x500")
        dialog.configure(bg='#f0f2f5')
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Title
        ttk.Label(dialog, text="📈 Analyze Budget", 
                 style='Heading.TLabel', background='#f0f2f5').pack(pady=20)
        
        # Budget selection
        select_frame = tk.Frame(dialog, bg='white', padx=20, pady=20)
        select_frame.pack(fill='x', padx=20, pady=(0, 20))
        
        tk.Label(select_frame, text="Select Budget:", font=('Arial', 11), 
                bg='white').pack(anchor='w')
        
        budget_var = tk.StringVar(value=list(self.budgets.keys())[0])
        budget_combo = ttk.Combobox(select_frame, textvariable=budget_var, 
                                   values=list(self.budgets.keys()), 
                                   font=('Arial', 11), state='readonly')
        budget_combo.pack(fill='x', pady=10)
        
        # Analysis display area
        analysis_frame = tk.Frame(dialog, bg='white', padx=20, pady=20)
        analysis_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        # Analysis text widget
        analysis_text = tk.Text(analysis_frame, height=15, width=50, 
                               font=('Courier', 10), wrap='word')
        scrollbar = tk.Scrollbar(analysis_frame, command=analysis_text.yview)
        analysis_text.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side='right', fill='y')
        analysis_text.pack(side='left', fill='both', expand=True)
        
        def analyze_budget():
            budget_name = budget_var.get()
            budget = self.budgets[budget_name]
            expenses = self.expenses.get(budget_name, [])
            
            total_expenses = sum(exp['amount'] for exp in expenses)
            remaining = budget['total_budget'] - total_expenses
            percentage_used = (total_expenses / budget['total_budget'] * 100) if budget['total_budget'] > 0 else 0
            
            # Clear and update analysis text
            analysis_text.delete(1.0, tk.END)
            
            analysis_text.insert(tk.END, "="*50 + "\n")
            analysis_text.insert(tk.END, f"ANALYSIS: {budget_name}\n")
            analysis_text.insert(tk.END, "="*50 + "\n\n")
            
            analysis_text.insert(tk.END, f"Type: {budget['type']}\n")
            analysis_text.insert(tk.END, f"Month: {budget['month']}\n")
            analysis_text.insert(tk.END, f"Total Budget: ₹{budget['total_budget']:,.2f}\n")
            analysis_text.insert(tk.END, f"Total Expenses: ₹{total_expenses:,.2f}\n")
            analysis_text.insert(tk.END, f"Remaining Budget: ₹{remaining:,.2f}\n")
            analysis_text.insert(tk.END, f"Percentage Used: {percentage_used:.1f}%\n\n")
            
            # Category breakdown
            analysis_text.insert(tk.END, "Category Breakdown:\n")
            analysis_text.insert(tk.END, "-"*30 + "\n")
            
            category_totals = {cat: 0 for cat in self.categories}
            for exp in expenses:
                category_totals[exp['category']] += exp['amount']
            
            for category in self.categories:
                amount = category_totals[category]
                if amount > 0:
                    percentage = (amount / total_expenses * 100) if total_expenses > 0 else 0
                    analysis_text.insert(tk.END, f"{category:<15}: ₹{amount:>10,.2f} ({percentage:.1f}%)\n")
            
            # Warning
            analysis_text.insert(tk.END, "\n" + "="*50 + "\n")
            if percentage_used >= 90:
                analysis_text.insert(tk.END, "🔴 CRITICAL: 90%+ of budget used!\n")
            elif percentage_used >= 75:
                analysis_text.insert(tk.END, "🟠 WARNING: 75%+ of budget used\n")
            else:
                analysis_text.insert(tk.END, "✅ Within budget limits\n")
            analysis_text.insert(tk.END, "="*50 + "\n")
            
            # Make text read-only
            analysis_text.config(state='disabled')
        
        # Analyze button
        button_frame = tk.Frame(dialog, bg='#f0f2f5')
        button_frame.pack(pady=(0, 20))
        
        ttk.Button(button_frame, text="Analyze", style='Primary.TButton',
                  command=analyze_budget).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Close", style='Danger.TButton',
                  command=dialog.destroy).pack(side='left', padx=5)
        
        # Run initial analysis
        analyze_budget()
    
    def expense_summary(self):
        """Display expense summary by category"""
        if not self.expenses:
            messagebox.showinfo("Info", "No expenses available.")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Expense Summary")
        dialog.geometry("800x600")
        dialog.configure(bg='#f0f2f5')
        
        # Title
        ttk.Label(dialog, text="📊 Expense Summary by Category", 
                 style='Heading.TLabel', background='#f0f2f5').pack(pady=20)
        
        # Create notebook for different views
        notebook = ttk.Notebook(dialog)
        notebook.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        # Tab 1: Overall Summary
        overall_tab = ttk.Frame(notebook)
        notebook.add(overall_tab, text="Overall")
        
        # Calculate overall totals
        all_expenses = []
        for exp_list in self.expenses.values():
            all_expenses.extend(exp_list)
        
        total_all = sum(exp['amount'] for exp in all_expenses)
        
        # Treeview for overall summary
        tree_frame = tk.Frame(overall_tab)
        tree_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        tree = ttk.Treeview(tree_frame, columns=('Category', 'Amount', 'Percentage'), 
                           show='headings', height=len(self.categories))
        
        tree.heading('Category', text='Category')
        tree.heading('Amount', text='Amount (₹)')
        tree.heading('Percentage', text='Percentage')
        
        tree.column('Category', width=150)
        tree.column('Amount', width=150)
        tree.column('Percentage', width=100)
        
        # Insert data
        category_totals = {cat: 0 for cat in self.categories}
        for exp in all_expenses:
            category_totals[exp['category']] += exp['amount']
        
        for category in self.categories:
            amount = category_totals[category]
            if amount > 0:
                percentage = (amount / total_all * 100) if total_all > 0 else 0
                tree.insert('', 'end', values=(
                    category,
                    f"₹{amount:,.2f}",
                    f"{percentage:.1f}%"
                ))
        
        tree.pack(fill='both', expand=True)
        
        # Total label
        tk.Label(overall_tab, text=f"Total Expenses: ₹{total_all:,.2f}", 
                font=('Arial', 12, 'bold')).pack(pady=10)
        
        # Tab 2: By Budget
        by_budget_tab = ttk.Frame(notebook)
        notebook.add(by_budget_tab, text="By Budget")
        
        # Treeview for budget-wise summary
        budget_tree_frame = tk.Frame(by_budget_tab)
        budget_tree_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        budget_tree = ttk.Treeview(budget_tree_frame, 
                                  columns=('Budget', 'Category', 'Amount'), 
                                  show='headings', height=20)
        
        budget_tree.heading('Budget', text='Budget')
        budget_tree.heading('Category', text='Category')
        budget_tree.heading('Amount', text='Amount (₹)')
        
        budget_tree.column('Budget', width=150)
        budget_tree.column('Category', width=150)
        budget_tree.column('Amount', width=150)
        
        # Insert data
        for budget_name, exp_list in self.expenses.items():
            if exp_list:
                # Group by category
                cat_totals = {cat: 0 for cat in self.categories}
                for exp in exp_list:
                    cat_totals[exp['category']] += exp['amount']
                
                for category in self.categories:
                    amount = cat_totals[category]
                    if amount > 0:
                        budget_tree.insert('', 'end', values=(
                            budget_name,
                            category,
                            f"₹{amount:,.2f}"
                        ))
        
        scrollbar = ttk.Scrollbar(budget_tree_frame, orient='vertical', 
                                 command=budget_tree.yview)
        budget_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        budget_tree.pack(side='left', fill='both', expand=True)
        
        # Close button
        button_frame = tk.Frame(dialog, bg='#f0f2f5')
        button_frame.pack(pady=(0, 20))
        
        ttk.Button(button_frame, text="Close", style='Primary.TButton',
                  command=dialog.destroy).pack()
    
    def edit_expense_dialog(self):
        """Dialog for editing/deleting expenses"""
        if not self.expenses:
            messagebox.showinfo("Info", "No expenses available to edit.")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit/Delete Expenses")
        dialog.geometry("1000x600")
        dialog.configure(bg='#f0f2f5')
        
        # Title
        ttk.Label(dialog, text="✏️ Edit/Delete Expenses", 
                 style='Heading.TLabel', background='#f0f2f5').pack(pady=20)
        
        # Create treeview with all expenses
        tree_frame = tk.Frame(dialog, bg='#f0f2f5')
        tree_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        # Create Treeview
        columns = ('Budget', 'Date', 'Description', 'Category', 'Amount', 'ID')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=20)
        
        # Define headings
        tree.heading('Budget', text='Budget')
        tree.heading('Date', text='Date')
        tree.heading('Description', text='Description')
        tree.heading('Category', text='Category')
        tree.heading('Amount', text='Amount')
        tree.heading('ID', text='ID')
        
        tree.column('Budget', width=120)
        tree.column('Date', width=100)
        tree.column('Description', width=250)
        tree.column('Category', width=100)
        tree.column('Amount', width=100)
        tree.column('ID', width=0, stretch=False)  # Hide ID column
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        tree.pack(side='left', fill='both', expand=True)
        
        # Insert all expenses
        for budget_name, exp_list in self.expenses.items():
            for exp in exp_list:
                tree.insert('', 'end', values=(
                    budget_name,
                    exp['date'],
                    exp['name'],
                    exp['category'],
                    f"₹{exp['amount']:,.2f}",
                    exp['id']
                ))
        
        # Buttons frame
        button_frame = tk.Frame(dialog, bg='#f0f2f5')
        button_frame.pack(pady=(0, 20))
        
        def edit_selected():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Warning", "Please select an expense to edit.")
                return
            
            item = tree.item(selected[0])
            values = item['values']
            expense_id = values[5]
            budget_name = values[0]
            
            # Find the expense
            expense = None
            for exp in self.expenses[budget_name]:
                if exp['id'] == expense_id:
                    expense = exp
                    break
            
            if expense:
                self.show_edit_expense_dialog(budget_name, expense, dialog)
        
        def delete_selected():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Warning", "Please select an expense to delete.")
                return
            
            item = tree.item(selected[0])
            values = item['values']
            expense_id = values[5]
            budget_name = values[0]
            description = values[2]
            amount = values[4]
            
            confirm = messagebox.askyesno("Confirm Delete", 
                                         f"Are you sure you want to delete:\n"
                                         f"{description} - {amount}?")
            
            if confirm:
                # Remove expense
                self.expenses[budget_name] = [exp for exp in self.expenses[budget_name] 
                                            if exp['id'] != expense_id]
                # Update tree
                tree.delete(selected[0])
                messagebox.showinfo("Success", "Expense deleted successfully!")
        
        ttk.Button(button_frame, text="Edit Selected", style='Primary.TButton',
                  command=edit_selected).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Delete Selected", style='Danger.TButton',
                  command=delete_selected).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Close", style='Warning.TButton',
                  command=dialog.destroy).pack(side='left', padx=5)
    
    def show_edit_expense_dialog(self, budget_name, expense, parent_dialog=None):
        """Dialog for editing an expense"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Expense")
        dialog.geometry("500x500")
        dialog.configure(bg='#f0f2f5')
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Title
        ttk.Label(dialog, text="✏️ Edit Expense", 
                 style='Heading.TLabel', background='#f0f2f5').pack(pady=20)
        
        # Main form frame
        form_frame = tk.Frame(dialog, bg='white', padx=30, pady=30)
        form_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        # Budget (read-only)
        tk.Label(form_frame, text="Budget:", font=('Arial', 11), 
                bg='white').grid(row=0, column=0, sticky='w', pady=(0, 5))
        tk.Label(form_frame, text=budget_name, font=('Arial', 11), 
                bg='white', fg='blue').grid(row=0, column=1, sticky='w', pady=(0, 15), padx=(10, 0))
        
        # Category
        tk.Label(form_frame, text="Category:", font=('Arial', 11), 
                bg='white').grid(row=1, column=0, sticky='w', pady=(0, 5))
        category_var = tk.StringVar(value=expense['category'])
        category_combo = ttk.Combobox(form_frame, textvariable=category_var, 
                                     values=self.categories, font=('Arial', 11),
                                     width=27, state='readonly')
        category_combo.grid(row=1, column=1, pady=(0, 15), padx=(10, 0))
        
        # Description
        tk.Label(form_frame, text="Description:", font=('Arial', 11), 
                bg='white').grid(row=2, column=0, sticky='w', pady=(0, 5))
        desc_entry = ttk.Entry(form_frame, font=('Arial', 11), width=30)
        desc_entry.insert(0, expense['name'])
        desc_entry.grid(row=2, column=1, pady=(0, 15), padx=(10, 0))
        
        # Amount
        tk.Label(form_frame, text="Amount (₹):", font=('Arial', 11), 
                bg='white').grid(row=3, column=0, sticky='w', pady=(0, 5))
        amount_entry = ttk.Entry(form_frame, font=('Arial', 11), width=30)
        amount_entry.insert(0, str(expense['amount']))
        amount_entry.grid(row=3, column=1, pady=(0, 15), padx=(10, 0))
        
        # Date
        tk.Label(form_frame, text="Date (DD-MM-YYYY):", font=('Arial', 11), 
                bg='white').grid(row=4, column=0, sticky='w', pady=(0, 5))
        date_entry = ttk.Entry(form_frame, font=('Arial', 11), width=30)
        date_entry.insert(0, expense['date'])
        date_entry.grid(row=4, column=1, pady=(0, 15), padx=(10, 0))
        
        # Configure grid columns
        form_frame.grid_columnconfigure(0, weight=1)
        form_frame.grid_columnconfigure(1, weight=2)
        
        # Buttons
        button_frame = tk.Frame(dialog, bg='#f0f2f5')
        button_frame.pack(pady=(0, 20))
        
        def update_expense():
            description = desc_entry.get().strip()
            if not description:
                messagebox.showerror("Error", "Description cannot be empty")
                return
            
            try:
                amount = float(amount_entry.get())
                if amount <= 0:
                    messagebox.showerror("Error", "Amount must be positive")
                    return
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number for amount")
                return
            
            date_str = date_entry.get().strip()
            try:
                datetime.strptime(date_str, "%d-%m-%Y")
            except ValueError:
                messagebox.showerror("Error", "Invalid date format. Use DD-MM-YYYY")
                return
            
            # Update expense
            for exp in self.expenses[budget_name]:
                if exp['id'] == expense['id']:
                    exp['name'] = description
                    exp['category'] = category_var.get()
                    exp['amount'] = amount
                    exp['date'] = date_str
                    exp['updated_at'] = datetime.now().isoformat()
                    break
            
            messagebox.showinfo("Success", "Expense updated successfully!")
            dialog.destroy()
            if parent_dialog:
                parent_dialog.destroy()
            self.edit_expense_dialog()  # Refresh the list
        
        ttk.Button(button_frame, text="Update", style='Success.TButton',
                  command=update_expense).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Cancel", style='Danger.TButton',
                  command=dialog.destroy).pack(side='left', padx=5)
    
    def delete_budget_dialog(self):
        """Dialog for deleting a budget"""
        if not self.budgets:
            messagebox.showinfo("Info", "No budgets available to delete.")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Delete Budget")
        dialog.geometry("500x400")
        dialog.configure(bg='#f0f2f5')
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Title
        ttk.Label(dialog, text="🗑️ Delete Budget", 
                 style='Heading.TLabel', background='#f0f2f5').pack(pady=20)
        
        # Budget selection
        select_frame = tk.Frame(dialog, bg='white', padx=20, pady=20)
        select_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        tk.Label(select_frame, text="Select Budget to Delete:", 
                font=('Arial', 11), bg='white').pack(anchor='w', pady=(0, 10))
        
        # Create listbox with scrollbar
        listbox_frame = tk.Frame(select_frame, bg='white')
        listbox_frame.pack(fill='both', expand=True)
        
        listbox = tk.Listbox(listbox_frame, font=('Arial', 11), height=10)
        scrollbar = tk.Scrollbar(listbox_frame, command=listbox.yview)
        listbox.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side='right', fill='y')
        listbox.pack(side='left', fill='both', expand=True)
        
        # Populate listbox
        for budget_name in self.budgets.keys():
            budget = self.budgets[budget_name]
            expenses_count = len(self.expenses.get(budget_name, []))
            listbox.insert('end', f"{budget_name} ({budget['type']} - {budget['month']}) - {expenses_count} expenses")
        
        # Info label
        info_label = tk.Label(select_frame, text="", font=('Arial', 10), 
                             bg='white', fg='red')
        info_label.pack(pady=10)
        
        def update_info(event):
            selection = listbox.curselection()
            if selection:
                index = selection[0]
                budget_name = list(self.budgets.keys())[index]
                budget = self.budgets[budget_name]
                expenses_count = len(self.expenses.get(budget_name, []))
                info_label.config(
                    text=f"This will delete '{budget_name}' and all {expenses_count} expenses!"
                )
        
        listbox.bind('<<ListboxSelect>>', update_info)
        
        # Buttons
        button_frame = tk.Frame(dialog, bg='#f0f2f5')
        button_frame.pack(pady=(0, 20))
        
        def delete_budget():
            selection = listbox.curselection()
            if not selection:
                messagebox.showwarning("Warning", "Please select a budget to delete.")
                return
            
            index = selection[0]
            budget_name = list(self.budgets.keys())[index]
            expenses_count = len(self.expenses.get(budget_name, []))
            
            confirm = messagebox.askyesno("Confirm Delete", 
                                         f"Are you sure you want to delete:\n"
                                         f"'{budget_name}' with {expenses_count} expenses?\n\n"
                                         f"This action cannot be undone!")
            
            if confirm:
                del self.budgets[budget_name]
                if budget_name in self.expenses:
                    del self.expenses[budget_name]
                messagebox.showinfo("Success", f"Budget '{budget_name}' deleted successfully!")
                dialog.destroy()
                self.show_main_dashboard()
        
        ttk.Button(button_frame, text="Delete Selected", style='Danger.TButton',
                  command=delete_budget).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Cancel", style='Primary.TButton',
                  command=dialog.destroy).pack(side='left', padx=5)
    
    def check_budget_warnings(self):
        """Check and display budget warnings"""
        if not self.budgets:
            messagebox.showinfo("Info", "No budgets available.")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Budget Warnings")
        dialog.geometry("600x500")
        dialog.configure(bg='#f0f2f5')
        
        # Title
        ttk.Label(dialog, text="⚠️ Budget Warning System", 
                 style='Heading.TLabel', background='#f0f2f5').pack(pady=20)
        
        # Create text widget for warnings
        text_frame = tk.Frame(dialog, bg='#f0f2f5')
        text_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        warning_text = tk.Text(text_frame, height=20, width=60, 
                              font=('Courier', 10), wrap='word')
        scrollbar = tk.Scrollbar(text_frame, command=warning_text.yview)
        warning_text.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side='right', fill='y')
        warning_text.pack(side='left', fill='both', expand=True)
        
        # Check for warnings
        warnings_found = False
        critical_warnings = []
        normal_warnings = []
        
        for budget_name, budget in self.budgets.items():
            expenses = self.expenses.get(budget_name, [])
            total_expenses = sum(exp['amount'] for exp in expenses)
            
            if budget['total_budget'] > 0:
                percentage_used = (total_expenses / budget['total_budget']) * 100
                
                if percentage_used >= 90:
                    critical_warnings.append((budget_name, budget, total_expenses, percentage_used))
                    warnings_found = True
                elif percentage_used >= 75:
                    normal_warnings.append((budget_name, budget, total_expenses, percentage_used))
                    warnings_found = True
        
        # Display warnings
        warning_text.insert(tk.END, "="*60 + "\n")
        warning_text.insert(tk.END, "BUDGET WARNINGS CHECK\n")
        warning_text.insert(tk.END, "="*60 + "\n\n")
        
        if not warnings_found:
            warning_text.insert(tk.END, "✅ No budget warnings found.\n")
            warning_text.insert(tk.END, "All budgets are within safe limits.\n")
        else:
            # Show critical warnings
            if critical_warnings:
                warning_text.insert(tk.END, "🔴 CRITICAL WARNINGS:\n")
                warning_text.insert(tk.END, "-"*40 + "\n")
                for budget_name, budget, spent, percent in critical_warnings:
                    warning_text.insert(tk.END, f"\n{budget_name}:\n")
                    warning_text.insert(tk.END, f"  Type: {budget['type']}\n")
                    warning_text.insert(tk.END, f"  Month: {budget['month']}\n")
                    warning_text.insert(tk.END, f"  Budget: ₹{budget['total_budget']:,.2f}\n")
                    warning_text.insert(tk.END, f"  Spent: ₹{spent:,.2f}\n")
                    warning_text.insert(tk.END, f"  Used: {percent:.1f}%\n")
                warning_text.insert(tk.END, "\n")
            
            # Show normal warnings
            if normal_warnings:
                warning_text.insert(tk.END, "🟠 WARNINGS:\n")
                warning_text.insert(tk.END, "-"*40 + "\n")
                for budget_name, budget, spent, percent in normal_warnings:
                    warning_text.insert(tk.END, f"\n{budget_name}:\n")
                    warning_text.insert(tk.END, f"  Type: {budget['type']}\n")
                    warning_text.insert(tk.END, f"  Month: {budget['month']}\n")
                    warning_text.insert(tk.END, f"  Budget: ₹{budget['total_budget']:,.2f}\n")
                    warning_text.insert(tk.END, f"  Spent: ₹{spent:,.2f}\n")
                    warning_text.insert(tk.END, f"  Used: {percent:.1f}%\n")
        
        # Daily budget calculation
        warning_text.insert(tk.END, "\n" + "="*60 + "\n")
        warning_text.insert(tk.END, "DAILY BUDGET CALCULATION\n")
        warning_text.insert(tk.END, "="*60 + "\n\n")
        
        today = datetime.now()
        
        for budget_name, budget in self.budgets.items():
            try:
                month = budget['month']
                if month:
                    current_year = today.year
                    month_num = datetime.strptime(month, "%b").month
                    
                    # Days in month
                    if month_num == 12:
                        next_month = datetime(current_year + 1, 1, 1)
                    else:
                        next_month = datetime(current_year, month_num + 1, 1)
                    
                    month_start = datetime(current_year, month_num, 1)
                    days_in_month = (next_month - month_start).days
                    
                    # Days left
                    if today.month == month_num and today.year == current_year:
                        days_left = days_in_month - today.day + 1
                        
                        if days_left > 0:
                            expenses = self.expenses.get(budget_name, [])
                            total_expenses = sum(exp['amount'] for exp in expenses)
                            remaining = budget['total_budget'] - total_expenses
                            daily_budget = remaining / days_left
                            
                            warning_text.insert(tk.END, f"{budget_name}:\n")
                            warning_text.insert(tk.END, f"  Days left in {month}: {days_left}\n")
                            warning_text.insert(tk.END, f"  Remaining: ₹{remaining:,.2f}\n")
                            warning_text.insert(tk.END, f"  Daily budget: ₹{daily_budget:,.2f}/day\n\n")
            except:
                continue
        
        # Make text read-only
        warning_text.config(state='disabled')
        
        # Close button
        button_frame = tk.Frame(dialog, bg='#f0f2f5')
        button_frame.pack(pady=(0, 20))
        
        ttk.Button(button_frame, text="Close", style='Primary.TButton',
                  command=dialog.destroy).pack()
    
    def check_single_budget_warning(self, budget_name):
        """Check warning for a single budget"""
        if budget_name in self.budgets:
            budget = self.budgets[budget_name]
            expenses = self.expenses.get(budget_name, [])
            total_expenses = sum(exp['amount'] for exp in expenses)
            
            if budget['total_budget'] > 0:
                percentage_used = (total_expenses / budget['total_budget']) * 100
                
                if percentage_used >= 90:
                    messagebox.showwarning("Critical Warning", 
                                         f"CRITICAL: {budget_name} has used {percentage_used:.1f}% of budget!")
                elif percentage_used >= 75:
                    messagebox.showwarning("Warning", 
                                         f"WARNING: {budget_name} has used {percentage_used:.1f}% of budget")
    
    def export_report_dialog(self):
        """Dialog for exporting reports"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Export Report")
        dialog.geometry("400x300")
        dialog.configure(bg='#f0f2f5')
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Title
        ttk.Label(dialog, text="💾 Export Report", 
                 style='Heading.TLabel', background='#f0f2f5').pack(pady=20)
        
        # Options frame
        options_frame = tk.Frame(dialog, bg='white', padx=30, pady=30)
        options_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        # Format selection
        tk.Label(options_frame, text="Export Format:", font=('Arial', 11), 
                bg='white').pack(anchor='w', pady=(0, 10))
        
        format_var = tk.StringVar(value='CSV')
        ttk.Radiobutton(options_frame, text="CSV (Excel compatible)", 
                       variable=format_var, value='CSV', style='TRadiobutton').pack(anchor='w', pady=5)
        ttk.Radiobutton(options_frame, text="TXT (Text file)", 
                       variable=format_var, value='TXT', style='TRadiobutton').pack(anchor='w', pady=5)
        
        # Include data selection
        tk.Label(options_frame, text="Include:", font=('Arial', 11), 
                bg='white').pack(anchor='w', pady=(20, 10))
        
        include_budgets_var = tk.BooleanVar(value=True)
        include_expenses_var = tk.BooleanVar(value=True)
        
        ttk.Checkbutton(options_frame, text="Budget Summary", 
                       variable=include_budgets_var, style='TCheckbutton').pack(anchor='w', pady=2)
        ttk.Checkbutton(options_frame, text="Expense Details", 
                       variable=include_expenses_var, style='TCheckbutton').pack(anchor='w', pady=2)
        
        # Buttons
        button_frame = tk.Frame(dialog, bg='#f0f2f5')
        button_frame.pack(pady=(0, 20))
        
        def export_report():
            # Ask for file location
            filename = filedialog.asksaveasfilename(
                defaultextension='.csv' if format_var.get() == 'CSV' else '.txt',
                filetypes=[
                    ("CSV files", "*.csv"),
                    ("Text files", "*.txt"),
                    ("All files", "*.*")
                ]
            )
            
            if not filename:
                return
            
            # Export based on format
            if format_var.get() == 'CSV':
                self.export_to_csv(filename, include_budgets_var.get(), include_expenses_var.get())
            else:
                self.export_to_txt(filename, include_budgets_var.get(), include_expenses_var.get())
            
            messagebox.showinfo("Success", f"Report exported to:\n{filename}")
            dialog.destroy()
        
        ttk.Button(button_frame, text="Export", style='Success.TButton',
                  command=export_report).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Cancel", style='Danger.TButton',
                  command=dialog.destroy).pack(side='left', padx=5)
    
    def export_to_csv(self, filename, include_budgets=True, include_expenses=True):
        """Export data to CSV file"""
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                
                # Write header
                writer.writerow(['Budget Analyzer Report', 'Generated', datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
                writer.writerow(['User:', self.current_user])
                writer.writerow([])
                
                if include_budgets and self.budgets:
                    # Write budgets summary
                    writer.writerow(['BUDGETS SUMMARY'])
                    writer.writerow(['Name', 'Type', 'Month', 'Total Budget', 'Total Spent', 'Remaining', '% Used'])
                    
                    for name, budget in self.budgets.items():
                        expenses = self.expenses.get(name, [])
                        total_spent = sum(exp['amount'] for exp in expenses)
                        remaining = budget['total_budget'] - total_spent
                        percent_used = (total_spent / budget['total_budget'] * 100) if budget['total_budget'] > 0 else 0
                        
                        writer.writerow([
                            name,
                            budget['type'],
                            budget['month'],
                            f"₹{budget['total_budget']:,.2f}",
                            f"₹{total_spent:,.2f}",
                            f"₹{remaining:,.2f}",
                            f"{percent_used:.1f}%"
                        ])
                    
                    writer.writerow([])
                
                if include_expenses and self.expenses:
                    # Write expenses detail
                    writer.writerow(['EXPENSES DETAIL'])
                    writer.writerow(['Budget', 'Date', 'Description', 'Category', 'Amount'])
                    
                    for budget_name, exp_list in self.expenses.items():
                        for exp in exp_list:
                            writer.writerow([
                                budget_name,
                                exp['date'],
                                exp['name'],
                                exp['category'],
                                f"₹{exp['amount']:,.2f}"
                            ])
        except Exception as e:
            messagebox.showerror("Error", f"Error exporting to CSV: {e}")
    
    def export_to_txt(self, filename, include_budgets=True, include_expenses=True):
        """Export data to text file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("="*60 + "\n")
                f.write(f"{'BUDGET ANALYZER REPORT':^60}\n")
                f.write("="*60 + "\n\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"User: {self.current_user}\n\n")
                
                if include_budgets and self.budgets:
                    f.write("BUDGETS SUMMARY\n")
                    f.write("-"*60 + "\n")
                    
                    for name, budget in self.budgets.items():
                        expenses = self.expenses.get(name, [])
                        total_spent = sum(exp['amount'] for exp in expenses)
                        remaining = budget['total_budget'] - total_spent
                        percent_used = (total_spent / budget['total_budget'] * 100) if budget['total_budget'] > 0 else 0
                        
                        f.write(f"\nBudget: {name}\n")
                        f.write(f"  Type: {budget['type']}\n")
                        f.write(f"  Month: {budget['month']}\n")
                        f.write(f"  Total Budget: ₹{budget['total_budget']:,.2f}\n")
                        f.write(f"  Total Spent: ₹{total_spent:,.2f}\n")
                        f.write(f"  Remaining: ₹{remaining:,.2f}\n")
                        f.write(f"  Percentage Used: {percent_used:.1f}%\n")
                    
                    f.write("\n" + "="*60 + "\n\n")
                
                if include_expenses and self.expenses:
                    f.write("EXPENSES DETAIL\n")
                    f.write("-"*60 + "\n")
                    
                    for budget_name, exp_list in self.expenses.items():
                        f.write(f"\n[{budget_name}]\n")
                        
                        for exp in exp_list:
                            f.write(f"  {exp['date']} - {exp['name']} ({exp['category']}): ₹{exp['amount']:,.2f}\n")
        except Exception as e:
            messagebox.showerror("Error", f"Error exporting to TXT: {e}")
    
    def show_pie_chart(self):
        """Show pie chart of expenses by category"""
        if not self.expenses:
            messagebox.showinfo("Info", "No expenses available for chart.")
            return
        
        # Gather all expenses
        all_expenses = []
        for exp_list in self.expenses.values():
            all_expenses.extend(exp_list)
        
        if not all_expenses:
            messagebox.showinfo("Info", "No expense data to display.")
            return
        
        # Calculate category totals
        category_totals = {cat: 0 for cat in self.categories}
        for exp in all_expenses:
            category_totals[exp['category']] += exp['amount']
        
        # Filter out zero categories
        labels = []
        sizes = []
        colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#c2c2f0']
        
        for cat in self.categories:
            if category_totals[cat] > 0:
                labels.append(cat)
                sizes.append(category_totals[cat])
        
        if not sizes:
            messagebox.showinfo("Info", "No expense data to display.")
            return
        
        # Create chart window
        chart_window = tk.Toplevel(self.root)
        chart_window.title("Expense Distribution by Category")
        chart_window.geometry("800x600")
        
        # Create matplotlib figure
        fig, ax = plt.subplots(figsize=(8, 6))
        wedges, texts, autotexts = ax.pie(sizes, labels=labels, colors=colors[:len(labels)], 
                                         autopct='%1.1f%%', startangle=90)
        
        # Equal aspect ratio ensures that pie is drawn as a circle
        ax.axis('equal')
        ax.set_title('Expense Distribution by Category', fontsize=16, fontweight='bold')
        
        # Create canvas
        canvas = FigureCanvasTkAgg(fig, master=chart_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
    
    def show_bar_chart(self):
        """Show bar chart comparing budget vs expenses"""
        if not self.budgets:
            messagebox.showinfo("Info", "No budgets available for chart.")
            return
        
        # Prepare data
        budgets_list = list(self.budgets.keys())
        budget_amounts = []
        expense_amounts = []
        
        for name in budgets_list:
            budget = self.budgets[name]
            expenses = self.expenses.get(name, [])
            total_expenses = sum(exp['amount'] for exp in expenses)
            
            budget_amounts.append(budget['total_budget'])
            expense_amounts.append(total_expenses)
        
        # Create chart window
        chart_window = tk.Toplevel(self.root)
        chart_window.title("Budget vs Actual Expenses")
        chart_window.geometry("900x600")
        
        # Create matplotlib figure
        fig, ax = plt.subplots(figsize=(10, 6))
        
        x = range(len(budgets_list))
        width = 0.35
        
        bars1 = ax.bar(x, budget_amounts, width, label='Budget', color='green', alpha=0.7)
        bars2 = ax.bar([i + width for i in x], expense_amounts, width, label='Actual Expenses', color='red', alpha=0.7)
        
        ax.set_xlabel('Budgets')
        ax.set_ylabel('Amount (₹)')
        ax.set_title('Budget vs Actual Expenses', fontsize=16, fontweight='bold')
        ax.set_xticks([i + width/2 for i in x])
        ax.set_xticklabels(budgets_list, rotation=45, ha='right')
        ax.legend()
        
        # Add value labels
        def autolabel(bars):
            for bar in bars:
                height = bar.get_height()
                ax.annotate(f'₹{height:,.0f}',
                           xy=(bar.get_x() + bar.get_width() / 2, height),
                           xytext=(0, 3),
                           textcoords="offset points",
                           ha='center', va='bottom', fontsize=8)
        
        autolabel(bars1)
        autolabel(bars2)
        
        plt.tight_layout()
        
        # Create canvas
        canvas = FigureCanvasTkAgg(fig, master=chart_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
    
    def show_line_chart(self):
        """Show line chart of spending trend"""
        # Group expenses by date
        date_totals = {}
        for exp_list in self.expenses.values():
            for exp in exp_list:
                date = exp['date']
                if date not in date_totals:
                    date_totals[date] = 0
                date_totals[date] += exp['amount']
        
        if len(date_totals) < 2:
            messagebox.showinfo("Info", "Need at least 2 days of data for trend analysis.")
            return
        
        # Sort dates
        sorted_dates = sorted(date_totals.keys(), 
                             key=lambda x: datetime.strptime(x, "%d-%m-%Y"))
        sorted_amounts = [date_totals[date] for date in sorted_dates]
        
        # Create chart window
        chart_window = tk.Toplevel(self.root)
        chart_window.title("Spending Trend Over Time")
        chart_window.geometry("900x600")
        
        # Create matplotlib figure
        fig, ax = plt.subplots(figsize=(10, 6))
        
        ax.plot(sorted_dates, sorted_amounts, marker='o', linewidth=2, color='blue')
        ax.set_xlabel('Date')
        ax.set_ylabel('Daily Spending (₹)')
        ax.set_title('Spending Trend Over Time', fontsize=16, fontweight='bold')
        ax.grid(True, alpha=0.3)
        
        # Rotate date labels for better readability
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
        
        plt.tight_layout()
        
        # Create canvas
        canvas = FigureCanvasTkAgg(fig, master=chart_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)


# Main application
def main():
    root = tk.Tk()
    app = ExpenseBudgetAnalyzerGUI(root)
    
    # Handle window close
    def on_closing():
        if messagebox.askyesno("Exit", "Are you sure you want to exit?\n\nUnsaved changes will be lost."):
            try:
                app.save_data()
            except:
                pass
            root.quit()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()