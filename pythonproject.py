import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt

class MarketingApp:
    def __init__(self, root, username):
        self.root = root
        self.root.title("MARKET TREND FORECASTING")

        self.tree = ttk.Treeview(root, columns=("Product", "Quantity", "Sold"), show="headings")
        self.tree.heading("Product", text="Product")
        self.tree.heading("Quantity", text="Quantity")
        self.tree.heading("Sold", text="Sold")
        self.tree.pack(pady=10)

        tk.Button(root, text="Load Excel or CSV File", command=self.load_file).pack(pady=10)
        tk.Button(root, text="Analyze Data", command=self.analyze_data).pack(pady=10)
        tk.Button(root, text="Plot Graph", command=self.plot_graph).pack()

        self.username = username
        tk.Label(root, text=f"Welcome, {self.username}").pack()

    def load_file(self):
        try:
            file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx;*.xls"), ("CSV files", "*.csv")])
            if file_path:
                if file_path.lower().endswith('.csv'):
                    self.products = pd.read_csv(file_path)
                else:
                    self.products = pd.read_excel(file_path)

                print("File loaded successfully:")
                print(self.products)
                self.update_treeview()
            else:
                print("No file selected.")
        except Exception as e:
            messagebox.showerror("Error", f"Error loading file: {e}")

    def analyze_data(self):
        if hasattr(self, 'products') and not self.products.empty:
            numerical_columns = self.products.select_dtypes(include=['number']).columns

            if not numerical_columns.empty:
                for column in numerical_columns:
                    max_value = self.products[column].max()
                    min_value = self.products[column].min()
                    print(f"Maximum {column}: {max_value}")
                    print(f"Minimum {column}: {min_value}")
            else:
                print("No numerical columns found in the loaded data.")
        else:
            print("No data to analyze. Please load a file first.")

    def update_treeview(self):
        self.tree.delete(*self.tree.get_children())
        for index, row in self.products.iterrows():
            self.tree.insert("", index, values=(row["Product"], row["Quantity"], row["Sold"]))

    def plot_graph(self):
        try:
            if hasattr(self, 'products') and not self.products.empty:
                plt.figure(figsize=(10, 6))

                if 'Product' in self.products.columns:
                    for column in self.products.columns[1:]:
                        if pd.to_numeric(self.products[column], errors='coerce').notnull().all():
                            plt.plot(self.products['Product'], self.products[column], label=column)
                        else:
                            plt.bar(self.products['Product'], self.products[column], label=column)

                            max_value = self.products[column].max()
                            min_value = self.products[column].min()
                            plt.scatter(self.products.loc[self.products[column] == max_value, 'Product'],
                                        [max_value] * len(self.products[self.products[column] == max_value]),
                                        color='purple', marker='o', label=f'Max {column}')
                            plt.scatter(self.products.loc[self.products[column] == min_value, 'Product'],
                                        [min_value] * len(self.products[self.products[column] == min_value]),
                                        color='orange', marker='o', label=f'Min {column}')

                plt.xlabel('Product' if 'Product' in self.products.columns else 'Index')
                plt.ylabel('Value')
                plt.title('Data Visualization')
                plt.legend()
                plt.show()
            else:
                print("No data to plot. Please load a file first.")
        except Exception as e:
            messagebox.showerror("Error", f"Error plotting graph: {e}")

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Login System")

        self.username_entry = tk.Entry(root)
        self.password_entry = tk.Entry(root, show="*")

        tk.Label(root, text="Username:").pack(pady=10)
        self.username_entry.pack(pady=10)
        tk.Label(root, text="Password:").pack(pady=10)
        self.password_entry.pack(pady=10)

        self.login_button = tk.Button(root, text="Login", command=self.validate_login)
        self.login_button.pack(pady=20)

        self.users = {"Sahithi": "12345"}

    def validate_login(self):
        entered_username = self.username_entry.get()
        entered_password = self.password_entry.get()

        if entered_username in self.users and self.users[entered_username] == entered_password:
            messagebox.showinfo("Login Successful", "Welcome, {}".format(entered_username))
            self.show_main_app(entered_username)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def show_main_app(self, username):
        self.root.withdraw()  # Hide the login window
        main_app_root = tk.Toplevel()  # Create a new top-level window for the main app
        main_app = MarketingApp(main_app_root, username)

if __name__ == "__main__":
    root = tk.Tk()
    login_app = LoginApp(root)
    root.mainloop()
