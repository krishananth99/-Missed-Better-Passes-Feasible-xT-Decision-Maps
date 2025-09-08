# ⚽ Missed Better Passes — Feasible xT Decision Maps

## 📖 Project Overview  
This project explores **missed passing opportunities** in football by focusing on *feasible passes* that could have provided higher Expected Threat (xT) than the actual pass chosen.  

Traditional pass maps only show what happened; this project reframes the question into **what could have happened**. Specifically, it identifies and visualizes situations where a player had better, *realistically feasible* options that were not taken.  

This shifts the analysis from being descriptive → to being improvement-oriented, making it directly actionable for coaches, analysts, and recruiters.

---

## 🎯 Key Achievements
1. **Normalized Pitch Coordinates**  
   - The dataset was preprocessed to normalize all positions (0–1 scale).  
   - Sides were corrected for halftime switches, ensuring consistent attacking direction across halves.

2. **Pass Snapshots (Scalable Design)**  
   - Each pass is stored as a **snapshot** with full contextual data:  
     - Pass ID (unique: H1, H2… for home; A1, A2… for away).  
     - Passer & receiver IDs.  
     - Coordinates of start and end.  
     - Frame/timestamp.  
     - Possession pass index (order of pass in possession).  
     - Pass distance, direction, xT gain.  
     - Full player positions (both teams) at the moment of the pass.  
   - This modular snapshot design makes the dataset reusable for future projects (e.g., pressing, build-up analysis).

3. **Feasibility Model**  
   - Not all higher-xT passes are realistic. To filter options, we defined a **feasibility score** based on:  
     - Passing lane openness (geometry: defender distance to pass line).  
     - Receiver accessibility (nearest defender distance).  
   - Passes are marked feasible if score > threshold.

4. **xT Calculation**  
   - A custom grid-based xT model was built using `numpy` (inspired by Karun Singh’s and `socceraction` methods).  
   - Expected Threat Gain:  
     \[
     xT_{\text{gain}} = xT(\text{destination}) - xT(\text{origin})
     \]

5. **Interactive Pass Maps**  
   - Built with `mplsoccer`, `matplotlib`, and `ipywidgets`.  
   - Features toggle layers for:  
     - Actual pass (highlighted).  
     - Better feasible alternatives (lime green arrows + xT labels).  
     - All feasible passes (white arrows).  
     - Player positions (attackers blue, defenders red).  
   - Direction of play and pass metadata (ID + timestamp) are displayed as plot annotations.

---

## ⚙️ Methodology
1. **Data Source**  
   - Dataset: *Metrica Sports Free Sample Dataset 1*.  
   - Contains both **event data** and **tracking data** (rare in public datasets).  
   - Accessed from [Metrica Sports GitHub](https://github.com/metrica-sports).  
   - Uploaded to Google Drive for Colab processing.

2. **Data Engineering**  
   - Normalize coordinates → consistent analysis.  
   - Event–tracking alignment → link each pass to exact player positions.  
   - Snapshot generation for every pass.

3. **Pass Classification**  
   - Categorized into **Forward, Backward, Sideways** using geometric angles.  
   - Additional tags: line-breaking, possession index.

4. **Feasible Pass Identification**  
   - For each pass: generate all teammates as potential receivers.  
   - Compute feasibility score → filter to realistic passes.  
   - Compute xT gain for feasible passes.  
   - Compare actual choice vs alternatives.

5. **Visualization (Decision Map)**  
   - Layered map for each pass, toggleable by type.  
   - Better alternatives clearly distinguished from all feasible options.  
   - Designed with scalability: works for one pass or full match.

---

## 📦 Tools & Libraries Used
- **Core Analysis**  
  - `pandas`, `numpy` → data wrangling & calculations  
  - Custom xT grid builder  

- **Football-Specific**  
  - `mplsoccer` → pitch plotting & pass maps  

- **Visualization & Interactivity**  
  - `matplotlib` → arrows, annotations  
  - `ipywidgets` → interactive toggles  

- **Notebook Environment**  
  - Google Colab → execution & visualization  

---

## 🔍 Why This Matters
- **Recruitment:** Reveals decision-making tendencies — which players miss progressive options.  
- **Coaching:** Pinpoints timestamps where feasible better options existed → direct video analysis.  
- **Analytics Firms:** Demonstrates ability to reframe standard metrics into actionable, coach-ready outputs.  

This is not just “counting passes” — it’s **measuring decision-making quality.**

---

## 📊 Example Output
- **Pass Snapshot:** A1 (Away Team, Player 19 → 21, Frame 1, Timestamp 0.04s)  
- Actual pass: gold arrow with xT gain label.  
- Better feasible passes: lime arrows with xT gain.  
- All feasible passes: white arrows (background).  
- Players: attackers in blue, defenders in red.  
- Direction of play: annotated arrow.  

---

## 📌 Data Credit
This project uses **Metrica Sports Free Sample Dataset 1**, available on their [GitHub repository](https://github.com/metrica-sports).  
Files were uploaded to Google Drive and accessed in Google Colab.  
No other external datasets or paid sources were used.  
