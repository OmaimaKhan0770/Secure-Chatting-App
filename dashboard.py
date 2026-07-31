import matplotlib.pyplot as plt
from tkinter import *
from tkinter import ttk

# =========================================================
# DASHBOARD WINDOW
# =========================================================
def show_dashboard(times, cpu_usage):

    dashboard = Tk()

    dashboard.title("Encryption Dashboard 📊")

    dashboard.geometry("900x600")

    dashboard.configure(bg="#E6E6FA")

    # =====================================================
    # TITLE
    # =====================================================
    title = Label(
        dashboard,
        text="📊 Algorithm Performance Dashboard",
        font=("Segoe UI", 20, "bold"),
        bg="#E6E6FA",
        fg="#6A0DAD"
    )

    title.pack(pady=10)

    # =====================================================
    # TABLE
    # =====================================================
    table = ttk.Treeview(
        dashboard,
        columns=("Algorithm", "Time", "CPU"),
        show="headings",
        height=5
    )

    table.heading("Algorithm", text="Algorithm")
    table.heading("Time", text="Avg Encryption Time")
    table.heading("CPU", text="Avg CPU Usage")

    table.column("Algorithm", width=200)
    table.column("Time", width=250)
    table.column("CPU", width=250)

    table.pack(pady=20)

    algorithms = ["AES", "DES", "HYBRID"]

    avg_times = []
    avg_cpu = []

    # =====================================================
    # CALCULATIONS
    # =====================================================
    for algo in algorithms:

        # TIME
        if len(times[algo]) > 0:

            avg_time = sum(times[algo]) / len(times[algo])

        else:
            avg_time = 0

        # CPU
        if len(cpu_usage[algo]) > 0:

            avg_cpu_use = (
                sum(cpu_usage[algo]) /
                len(cpu_usage[algo])
            )

        else:
            avg_cpu_use = 0

        avg_times.append(avg_time)
        avg_cpu.append(avg_cpu_use)

        # INSERT ROW
        table.insert(
            "",
            END,
            values=(
                algo,
                f"{avg_time:.6f} sec",
                f"{avg_cpu_use:.2f} %"
            )
        )

    # =====================================================
    # BAR GRAPH FUNCTION
    # =====================================================
    def show_time_graph():

        plt.figure(figsize=(7, 5))

        plt.bar(
            algorithms,
            avg_times
        )

        plt.title("Encryption Time Comparison")

        plt.xlabel("Algorithms")

        plt.ylabel("Time (Seconds)")

        plt.show()

    # =====================================================
    # CPU GRAPH FUNCTION
    # =====================================================
    def show_cpu_graph():

        plt.figure(figsize=(7, 5))

        plt.bar(
            algorithms,
            avg_cpu
        )

        plt.title("CPU Usage Comparison")

        plt.xlabel("Algorithms")

        plt.ylabel("CPU Usage %")

        plt.show()

    # =====================================================
    # REAL TIME LINE GRAPH
    # =====================================================
    def show_live_graph():

        plt.figure(figsize=(8, 5))

        for algo in algorithms:

            if len(times[algo]) > 0:

                plt.plot(
                    times[algo],
                    label=algo
                )

        plt.title("Real-Time Encryption Performance")

        plt.xlabel("Messages")

        plt.ylabel("Time")

        plt.legend()

        plt.show()

    # =====================================================
    # BUTTONS
    # =====================================================
    btn_frame = Frame(
        dashboard,
        bg="#E6E6FA"
    )

    btn_frame.pack(pady=20)

    time_btn = Button(
        btn_frame,
        text="Encryption Time Graph",
        bg="#B57EDC",
        fg="white",
        font=("Segoe UI", 11, "bold"),
        padx=15,
        command=show_time_graph
    )

    time_btn.grid(row=0, column=0, padx=10)

    cpu_btn = Button(
        btn_frame,
        text="CPU Usage Graph",
        bg="#C8A2C8",
        font=("Segoe UI", 11, "bold"),
        padx=15,
        command=show_cpu_graph
    )

    cpu_btn.grid(row=0, column=1, padx=10)

    live_btn = Button(
        btn_frame,
        text="Live Performance Graph",
        bg="#D8BFD8",
        font=("Segoe UI", 11, "bold"),
        padx=15,
        command=show_live_graph
    )

    live_btn.grid(row=0, column=2, padx=10)

    # =====================================================
    # INFO TEXT
    # =====================================================
    info = Label(
        dashboard,
        text=(
            "AES → Fastest\\n"
            "DES → Older algorithm\\n"
            "Hybrid RSA+AES → Most Secure but Slowest"
        ),
        font=("Segoe UI", 11),
        bg="#E6E6FA",
        fg="#4B0082",
        justify=LEFT
    )

    info.pack(pady=20)

    dashboard.mainloop()