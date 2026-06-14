import tkinter as tk
from tkinter import messagebox, ttk
from weather_client import WeatherClient
from analyzer import ActivityRiskAnalyzer, RecommendationEngine

class WeatherAppGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Risk & Outdoor Activity Planner")
        self.root.geometry("680x640")
        self.root.configure(bg="#f4f6f9")
        
        self.client = WeatherClient()
        self.analyzer = ActivityRiskAnalyzer()
        self.engine = RecommendationEngine()
        
        self.create_widgets()
        
    def create_widgets(self):
        # Header Label Title
        header = tk.Label(self.root, text="🌤️ Weather Risk & Outdoor Activity Planner", font=("Helvetica", 16, "bold"), fg="#1e293b", bg="#f4f6f9", pady=10)
        header.pack()
        
        # User Form Fields Frame
        form_frame = tk.LabelFrame(self.root, text=" Plan Your Outdoor Event ", font=("Helvetica", 10, "bold"), padx=15, pady=15, bg="#ffffff", fg="#475569", relief="solid", bd=1)
        form_frame.pack(fill="x", padx=20, pady=10)
        
        tk.Label(form_frame, text="Enter Target Location:", font=("Helvetica", 10), bg="#ffffff", fg="#334155").grid(row=0, column=0, sticky="w", pady=5)
        self.location_entry = tk.Entry(form_frame, font=("Helvetica", 10), width=28, relief="solid", bd=1)
        self.location_entry.grid(row=0, column=1, padx=10, pady=5)
        self.location_entry.insert(0, "Abuja")
        
        tk.Label(form_frame, text="Select Activity Plan:", font=("Helvetica", 10), bg="#ffffff", fg="#334155").grid(row=1, column=0, sticky="w", pady=5)
        self.activity_box = ttk.Combobox(form_frame, values=["Football", "Jogging", "Farming", "Picnic", "Travelling"], font=("Helvetica", 10), width=26, state="readonly")
        self.activity_box.set("Football")
        self.activity_box.grid(row=1, column=1, padx=10, pady=5)
        
        # Action Buttons Pane
        btn_frame = tk.Frame(form_frame, bg="#ffffff")
        btn_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        run_btn = tk.Button(btn_frame, text="Analyze Safety & Advice", font=("Helvetica", 10, "bold"), bg="#2563eb", fg="#ffffff", padx=10, pady=4, relief="flat", command=self.process_analysis)
        run_btn.pack(side="left", padx=5)
        
        history_btn = tk.Button(btn_frame, text="Show Search History Log", font=("Helvetica", 10), bg="#475569", fg="#ffffff", padx=10, pady=4, relief="flat", command=self.display_history_file)
        history_btn.pack(side="left", padx=5)

        # Output Results Panel Area
        self.results_frame = tk.LabelFrame(self.root, text=" AI Safety Analysis & Summary Report ", font=("Helvetica", 10, "bold"), padx=15, pady=15, bg="#ffffff", fg="#475569", relief="solid", bd=1)
        self.results_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.output_text = tk.Text(self.results_frame, font=("Courier New", 10), bg="#0f172a", fg="#38bdf8", wrap="word")
        self.output_text.pack(fill="both", expand=True)
        self.output_text.insert("1.0", "System Dashboard Ready. Enter parameters above and hit Analyze.")
        
    def process_analysis(self):
        loc = self.location_entry.get().strip()
        act = self.activity_box.get()
        
        if not loc:
            messagebox.showwarning("Input Error", "Please fill in a location name string.")
            return
            
        try:
            # 1. Network API Processing
            forecast = self.client.fetch_forecast(loc)
            
            # 2. Algorithmic Risk Execution
            analysis = self.analyzer.analyze_risk(forecast, act)
            
            # 3. Text Packing Checklist Extraction
            checklist = self.engine.generate_checklist(act, analysis["assessment"])
            
            # Formulate Output Report
            report =  f"================================================\n"
            report += f"📍 TARGET LOCATION: {loc.upper()}\n"
            report += f"🌡️ LIVE METRICS:    {forecast.temperature}°C | {forecast.condition}\n"
            report += f"💨 WIND SPEED:      {forecast.wind_speed} km/h\n"
            report += f"================================================\n"
            report += f"🤖 AI ASSESSMENT:   {analysis['assessment'].upper()}\n"
            report += f"⏰ OPTIMAL TIMING:  {analysis['best_time']}\n"
            report += f"💡 EXPLANATION:     {analysis['advice']}\n"
            report += f"================================================\n"
            report += f"🎒 RECOMMENDATION CHECKLIST INVENTORY:\n"
            for item in checklist:
                report += f"  [ ] {item}\n"
            report += f"================================================\n"
            
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert("1.0", report)
            
            # 4. File Handling Logging
            with open("search_history.txt", "a", encoding="utf-8") as f:
                f.write(f"Location: {loc} | Activity: {act} | Result: {analysis['assessment']} | Temp: {forecast.temperature}°C\n")
                
        except Exception as err:
            messagebox.showerror("System Interruption", str(err))

    def display_history_file(self):
        try:
            with open("search_history.txt", "r", encoding="utf-8") as f:
                data = f.read()
            
            # Launch secondary window displaying local log data store
            history_win = tk.Toplevel(self.root)
            history_win.title("Local Database Archive Log")
            history_win.geometry("540x350")
            
            txt = tk.Text(history_win, font=("Consolas", 10), padx=10, pady=10)
            txt.pack(fill="both", expand=True)
            txt.insert("1.0", data if data.strip() else "No logs discovered in history text database file yet.")
            txt.config(state="disabled")
        except FileNotFoundError:
            messagebox.showinfo("Database Info", "No archive tracking logs discovered yet. Perform an analysis run.")

if __name__ == "__main__":
    app_root = tk.Tk()
    app = WeatherAppGUI(app_root)
    app_root.mainloop()