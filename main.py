# IMPORTS
import os
import tkinter as tk
from tkcalendar import Calendar, DateEntry
import pandas as pd
from pycoingecko import CoinGeckoAPI
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datetime as dt
import time
import seaborn as sns

class CryptocurrencyInfoViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Cryptocurrency Info Viewer")
        self.root.geometry("800x550")

        # PART 1: CRYPTO INFO VIEWER

        # Header
        self.info_viewer_label = tk.Label(root, text="--------------------------------------------------- CRYPTO INFO VIEWER ---------------------------------------------------")
        self.info_viewer_label.pack(pady=2)

        # Crypto options label
        self.crypto_label = tk.Label(root, text="Select the cryptocurrencies")
        self.crypto_label.pack(pady=2)

        # Crypto options
        self.crypto_entry = tk.Listbox(root, width=10, height=4, selectmode="multiple")
        self.crypto_entry.pack(padx=10, pady=5, expand=False, fill="both")
        x = ["bitcoin", "ethereum", "usd-coin", "axie-infinity"]
        self.crypto_entry.pack(pady=5)
        for each_item in range(len(x)):
            self.crypto_entry.insert(tk.END, x[each_item])

        # Frame for info viewer buttons
        self.info_buttons = tk.Frame(root)
        self.info_buttons.pack(pady=5)

        # Get Info button
        self.get_info_button = tk.Button(self.info_buttons, text="Get Info", command=self.get_info)
        self.get_info_button.pack(side=tk.LEFT, anchor='e')

        # Plot Correlation Graph button
        self.plot_correlation_button = tk.Button(self.info_buttons, text="Plot Correlation Graph for past 30 days", command=self.plot_correlation_graph)
        self.plot_correlation_button.pack(side=tk.LEFT, anchor='w')

        # Info Viewer Table Display
        self.table_label = tk.Text(root, width=115, height=5, wrap=tk.NONE)
        self.table_label.tag_configure("center", justify='center')
        self.table_label.insert("1.0", " ")
        self.table_label.tag_add("center", "1.0", "end")
        self.table_label.pack(pady=5)
        self.table_label.insert(tk.END, 'No crypto currency selected yet.')
        self.table_label.config(state=tk.DISABLED)

        # Export Dataframe button
        self.export_button = tk.Button(root, text="Export Info in excel format", command=self.export)
        self.export_button.pack()
        
        # PART TWO: GRAPH PLOTTER

        # Header
        self.graph_plotter_label = tk.Label(root, text="------------------------------------------------------- PLOT GRAPHS --------------------------------------------------------")
        self.graph_plotter_label.pack(pady=(50, 0))

        # Input Dates Instructions Label
        self.date_label = tk.Label(root, text="Double-click to enter start and end dates (DD/MM/YYYY)")
        self.date_label.pack(pady=2)

        # Frame for date inputs labels
        self.date_entries_labels = tk.Frame(root)
        self.date_entries_labels.pack(pady=(10,2))

        # Start and End Date entry labels
        self.start_label = tk.Label(self.date_entries_labels, text="--------Start Date---------")
        self.start_label.pack(side=tk.LEFT, anchor='e')
        self.end_label = tk.Label(self.date_entries_labels, text="---------End Date--------")
        self.end_label.pack(side=tk.LEFT, anchor='w')

        # Frame for date inputs dropdown
        self.date_entries = tk.Frame(root)
        self.date_entries.pack(pady=(5,0))

        # Start and End Date entries
        self.start_entry = DateEntry(self.date_entries, height=5, width=16, background="magenta3", foreground="white", bd=2, date_pattern='dd/MM/yyyy')
        self.start_entry.set_date(dt.date.today() - dt.timedelta(days=8)) # set a week before yesterday as start date
        self.start_entry.pack(side=tk.LEFT, anchor='e')
        self.end_entry = DateEntry(self.date_entries, height=5, width=16, background="magenta3", foreground="white", bd=2, date_pattern='dd/MM/yyyy')
        self.end_entry.set_date(dt.date.today() - dt.timedelta(days=1)) # set yesterday's date as end date
        self.end_entry.pack(side=tk.LEFT, anchor='w')

        # Frame for graph plotting buttons
        self.plot_buttons = tk.Frame(root)
        self.plot_buttons.pack()

        # Subplots button
        self.plot_button_altogether = tk.Button(root, text="Plot Graph On Same Plot", command=self.graph_altogether)
        self.plot_button_altogether.pack(side=tk.LEFT, anchor='e', expand=True)

        # Individual plots button
        self.plot_button_separate = tk.Button(root, text="Plot Graph On Different Plots", command=self.graph_separate)
        self.plot_button_separate.pack(side=tk.LEFT, anchor='w', expand=True)

    # Function to get cryptocurrency info using coingecko API
    def get_info(self):

        # Validate that we won't display an empty dataframe
        if len(self.crypto_entry.curselection()) == 0:
            tk.messagebox.showerror('Error', 'Please select at least one crypto currency.')
        
        else:
            self.table_label.config(state=tk.NORMAL)  # Enable editing state
            self.table_label.delete("1.0", tk.END)    # Clear previous content

            cg = CoinGeckoAPI()

            full_df = pd.DataFrame()
            for i in self.crypto_entry.curselection():
                crypto = self.crypto_entry.get(i)
                data = cg.get_price(ids=crypto, vs_currencies='sgd', include_market_cap=True, include_24hr_vol=True, include_24hr_change=True, include_last_updated_at=True)
                curr_data = data[crypto]
                df = pd.DataFrame(curr_data, index=[0])
                df.insert(0, 'Crypto Currency', crypto)
                full_df = pd.concat([full_df, df])

            new_column_names = {
            'sgd': 'Price (SGD)',
            'sgd_market_cap': 'Market Cap (SGD)',
            'sgd_24h_vol': '24h Volume (SGD)',
            'sgd_24h_change': '24h Change (SGD)',
            'last_updated_at': 'Last Updated At'
            }

            full_df = full_df.rename(columns=new_column_names)
            self.full_df = full_df
            self.table_label.insert(tk.END, full_df.to_string(index=False))  # Display the DataFrame
            self.table_label.tag_add("center", "1.0", "end")
            self.table_label.config(state=tk.DISABLED)
            return self.full_df

    # Function to export pandas DF
    def export(self):
        try:
            fp = os.getcwd() + "/Crypto_currency_info"
            self.full_df.to_excel("Crypto_currency_info.xlsx")
            tk.messagebox.showinfo(title="Export Successful", message=f"Data exported to {fp}")
        except AttributeError:
            tk.messagebox.showerror("No info displayed", "Please select at least one crypto currency and click 'Get Info' before exporting.")

    # Function to validate start and end dates input by user
    def validate_dates(self, start, end):
        if start > end:
            return False
        elif start > time.time():
            return False
        elif end > time.time():
            return False
        else:
            return True

    # Function to plot line charts for each cryptocurrency using Matplotlib
    def plot_indiv_line_charts(self, df_list, title):
        fig, ax = plt.subplots()
        for df in df_list:
            ax.plot(df["timestamp"], df[f"{df.columns[2]}"], label=df.columns[2])

        ax.set(xlabel="Date", ylabel="SGD", title=title)
        ax.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    # Function to plot subplots (single graph) using Matplotlib
    def plot_subplots(self, dataframes):
        num_plots = len(dataframes)
        num_cols = min(2, num_plots)  # Limit to 2 columns for better display
        num_rows = (num_plots + 1) // 2

        fig, axes = plt.subplots(num_rows, num_cols, figsize=(12, 5 * num_rows), sharex=True)

        for i, df in enumerate(dataframes):
            row = i // num_cols
            col = i % num_cols

            ax = axes[row, col] if num_rows > 1 else axes[col]
            crypto = self.crypto_entry.get(i)

            ax.plot(df["timestamp"], df.iloc[:, 2], label=crypto)

            ax.set_ylabel("Price (SGD)")
            ax.set_title(f"{crypto} Price Over Time")
            ax.legend()

            # Rotate x-axis labels for each subplot
            for tick in ax.get_xticklabels():
                tick.set_rotation(30)

        # Remove empty subplots if there are an odd number of cryptocurrencies
        if num_plots % 2 != 0:
            axes[-1, -1].axis("off")

        plt.tight_layout()
        plt.show()

    # Function to plot all the line graphs on one plot
    def graph_altogether(self):
        cg = CoinGeckoAPI()
        start = dt.datetime.combine(self.start_entry.get_date(), dt.datetime.min.time()).timestamp()
        end = dt.datetime.combine(self.end_entry.get_date(), dt.datetime.max.time()).timestamp()

        if self.validate_dates(start, end) == False:
            tk.messagebox.showerror('Error', 'Please select valid start and end dates.')

        else:
            dataframes = []
            for i in self.crypto_entry.curselection():
                crypto = self.crypto_entry.get(i)
                data = cg.get_coin_market_chart_range_by_id(id=crypto, vs_currency='sgd', from_timestamp=start, to_timestamp=end)
                df = pd.DataFrame(data['prices'], columns=["timestamp", f"{crypto}"])
                df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
                df.insert(0, 'Crypto Currency', crypto)
                dataframes.append(df)

            if len(self.crypto_entry.curselection()) == 0:
                tk.messagebox.showerror('Error', 'Please select at least one crypto currency.')
            elif len(self.crypto_entry.curselection()) == 1:
                self.graph_separate()
            else:
                num_plots = len(dataframes)
                num_cols = min(2, num_plots)  # Limit to 2 columns for better display
                num_rows = (num_plots + 1) // 2

                fig, axes = plt.subplots(num_rows, num_cols, figsize=(12, 5 * num_rows), sharex=True)

                for i, df in enumerate(dataframes):
                    row = i // num_cols
                    col = i % num_cols

                    ax = axes[row, col] if num_rows > 1 else axes[col]
                    crypto = self.crypto_entry.get(i)

                    ax.plot(df["timestamp"], df.iloc[:, 2], label=crypto)

                    ax.set_ylabel("Price (SGD)")
                    ax.set_title(f"{crypto} Price Over Time")
                    ax.legend()

                    # Rotate x-axis labels for each subplot
                    for tick in ax.get_xticklabels():
                        tick.set_rotation(30)

                # Remove empty subplots if there are an odd number of cryptocurrencies
                if num_plots % 2 != 0:
                    axes[-1, -1].axis("off")

                plt.tight_layout()
                plt.show()

    # Function to plot separate graphs on their respective plots
    def graph_separate(self):
        if len(self.crypto_entry.curselection()) == 0:
            tk.messagebox.showerror('Error', 'Please select at least one crypto currency.')

        else:
            start = dt.datetime.combine(self.start_entry.get_date(), dt.datetime.min.time()).timestamp()
            end = dt.datetime.combine(self.end_entry.get_date(), dt.datetime.max.time()).timestamp()

            if self.validate_dates(start, end) == False:
                tk.messagebox.showerror('Error', 'Please select valid start and end dates.')
            
            else:
                cg = CoinGeckoAPI()
                dataframes = []
                for i in self.crypto_entry.curselection():
                    dataframes = []
                    crypto = self.crypto_entry.get(i)
                    data = cg.get_coin_market_chart_range_by_id(id=crypto, vs_currency='sgd', from_timestamp=start, to_timestamp=end)
                    df = pd.DataFrame(data['prices'], columns=["timestamp", f"{crypto}"])
                    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
                    df.insert(0, 'Crypto Currency', crypto)
                    dataframes.append(df)
                    self.plot_indiv_line_charts(dataframes, "Price Over Time")

    # Function to plot correlation graph
    def plot_correlation_graph(self):
        cg = CoinGeckoAPI()
    
        dataframes = []
        for i in self.crypto_entry.curselection():
            crypto = self.crypto_entry.get(i)
            data = cg.get_coin_market_chart_by_id(id=crypto, vs_currency='sgd', days='30', interval='daily')
            df = pd.DataFrame(data['prices'], columns=["timestamp", f"{crypto}"])
            df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms").dt.date
            df.set_index("timestamp", inplace=True)
            df = df.loc[~df.index.duplicated(keep='first')]
            dataframes.append(df)

        if len(dataframes) > 1:
            # Concatenate the resulting DataFrames
            merged_df = pd.concat(dataframes, axis=1, join="inner")

            # Calculate the correlation matrix
            correlation_matrix = merged_df.corr()
            # Create a correlation heatmap using Seaborn
            plt.figure(figsize=(10, 8))
            sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
            plt.title(f"Correlation Heatmap of Cryptocurrencies (SGD)")
            plt.show()
        else:
            tk.messagebox.showerror('Error', 'Please select at least two crypto currencies.')

if __name__ == "__main__":
    root = tk.Tk()
    app = CryptocurrencyInfoViewer(root)
    root.mainloop()
