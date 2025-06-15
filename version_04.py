from tkinter import Tk, Label, Entry, Button, StringVar, OptionMenu, messagebox
import matplotlib.pyplot as plt

class EmptyInputError(Exception):
    """Custom exception for empty input fields."""
    pass

class GraphPlotter(Tk):
    def __init__(self):
        super().__init__()
        self.title('Graph Plotter')
        self.geometry('500x600')
        self.configure(bg='#F5F5F5')  # Light gray background

        # Title
        Label(self, text='Graph Plotter', font=('Segoe UI', 20, 'bold'),
              fg='#333333', bg='#F5F5F5').pack(pady=10)

        # Input fields
        self.create_label_entry('X values (comma-separated):', 'e1')
        self.create_label_entry('X-axis label:', 'e2')
        self.create_label_entry('Y values (comma-separated):', 'e3')
        self.create_label_entry('Y-axis label:', 'e4')

        # Graph style selection
        Label(self, text='Select graph style:', font=('Segoe UI', 10),
              fg='#333333', bg='#F5F5F5').pack(pady=5)
        self.graph_type = StringVar(self)
        self.graph_type.set('Line')
        OptionMenu(self, self.graph_type, 'Line', 'Scatter', 'Bar').pack()

        # Plot button
        Button(self, text='Plot Graph', font=('Segoe UI', 11),
               fg='white', bg='#2E8B57', activebackground='#3CB371',
               command=self.draw_graph).pack(pady=20)

        # Status label
        self.status = Label(self, text='', font=('Segoe UI', 9),
                            fg='gray', bg='#F5F5F5')
        self.status.pack()

        self.save_ui_created = False  # Track if save UI was already created

        self.mainloop()

    def create_label_entry(self, label_text, attr_name):
        Label(self, text=label_text, font=('Segoe UI', 10),
              fg='#333333', bg='#F5F5F5').pack()
        entry = Entry(self, font=('Segoe UI', 10), bg='white')
        entry.pack(pady=5, ipadx=5, ipady=3, fill='x', padx=30)
        setattr(self, attr_name, entry)

    def draw_graph(self):
        try:
            x = list(map(float, self.e1.get().split(',')))
            y = list(map(float, self.e3.get().split(',')))

            if len(x) != len(y):
                raise ValueError("X and Y must have the same number of values.")

            plt.style.use('default') 
            graph_type = self.graph_type.get()

            if graph_type == 'Line':
                plt.plot(x, y, marker='o', color='#007acc')
            elif graph_type == 'Scatter':
                plt.scatter(x, y, color='#dc3912')
            elif graph_type == 'Bar':
                plt.bar(x, y, color='#3366cc')
            
            a = self.e2.get()
            b = self.e4.get()
            if not a or not b:
                raise EmptyInputError

            plt.xlabel(a, fontsize=12)
            plt.ylabel(b, fontsize=12)
            plt.title('Data Visualization', fontsize=14)
            plt.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)
            plt.tight_layout()

            self.current_figure = plt.gcf()
            plt.show()

            self.status.config(text='Graph plotted successfully.')

            # Create Save UI once
            if not self.save_ui_created:
                self.create_label_entry('File name:', 'e5')
                Button(self, text='Save Graph', font=('Segoe UI', 11),
                       fg='white', bg='#2E8B57', activebackground='#3CB371',
                       command=self.save_graph).pack(pady=10)
                self.save_ui_created = True
            
        except ValueError as ve:
            messagebox.showerror("Input Error", str(ve))
            self.status.config(text='Error: Invalid input.')
        except EmptyInputError:
            messagebox.showerror("Input Error", "Please fill in all fields.")
            self.status.config(text='Error: Empty input.')
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.status.config(text='Error occurred.')

    def save_graph(self):
        try:
            if hasattr(self, 'current_figure'):
                f = self.e5.get().strip()
                if not f:
                    raise EmptyInputError
                file_path = f + '.png'
                self.current_figure.savefig(file_path)
                messagebox.showinfo("Success", f"Graph saved as {file_path}")
            else:
                messagebox.showwarning("Warning", "No graph to save.")
        except EmptyInputError:
            messagebox.showerror("Input Error", "Please enter a file name.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

g = GraphPlotter()


