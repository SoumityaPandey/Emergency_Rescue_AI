# 🚑 ResQ AI — Intelligent Emergency Response & Rescue System

> **AI-powered emergency response, pathfinding, traffic management, and rescue dispatch system for Dehradun, Uttarakhand.**

[![Live Demo](https://img.shields.io/badge/Live-Demo-00A8E8?style=for-the-badge)](https://resq-ai-dehradun.streamlit.app)
[![GitHub](https://img.shields.io/badge/Source-GitHub-181717?style=for-the-badge&logo=github)](https://github.com/SoumityaPandey/Emergency_Rescue_AI)
[![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?style=for-the-badge&logo=streamlit)](https://streamlit.io/)

---

## 🌐 Live Demo

### 🚨 [Open ResQ AI — Live Application](https://resq-ai-dehradun.streamlit.app)

### 💻 [View Source Code on GitHub](https://github.com/SoumityaPandey/Emergency_Rescue_AI)

The application is deployed using **Streamlit Community Cloud** and can be accessed directly from a web browser without installing Python or running the project locally.

---

# 📌 Project Overview

**ResQ AI** is an intelligent emergency response and rescue management system designed around the geographical environment of **Dehradun, Uttarakhand**.

The system combines:

- Artificial Intelligence pathfinding
- Graph-based route planning
- Emergency management
- Traffic simulation
- Road-block management
- Real geographic map visualization
- Satellite imagery
- Road-following rescue route visualization
- Interactive Streamlit frontend

The primary objective is to determine an efficient rescue route from a selected rescue location to an emergency location while considering the project's road network, traffic conditions, and blocked roads.

The system provides a visual command-center interface where emergency situations can be reported, rescue routes can be calculated, traffic conditions can be modified, and emergency records can be monitored.

---

# 🎯 Objectives

The major objectives of ResQ AI are:

1. To develop an intelligent emergency response system.
2. To model Dehradun locations as a graph.
3. To implement multiple pathfinding algorithms.
4. To compare different approaches to route finding.
5. To consider distance and simulated traffic conditions.
6. To support blocked-road scenarios.
7. To visualize emergency locations on a real geographic map.
8. To display calculated rescue routes clearly.
9. To provide an interactive web-based dashboard.
10. To create a deployable emergency-response prototype.

---

# 🧠 Core Concept

The project uses a **graph-based representation of the city**.

Each important location is represented as a **node**, while roads between locations are represented as **edges**.

### Example

```text
              Pacific Mall
                    │
                    │
             Rajpur Road
                    │
                    │
              Dalanwala
                    │
                    │
              Clock Tower
               /        \
              /          \
     Paltan Bazaar      Hospital
            │
            │
      Railway Station
            │
            │
           ISBT
```

Each road contains information such as:

- Distance
- Traffic factor
- Blocked/open status

The pathfinding algorithm then searches this graph to determine a route between the rescue vehicle and emergency location.

---

# 🗺️ Locations Covered

The current system includes important Dehradun locations such as:

### Major Locations

- ISBT
- Railway Station
- Prem Nagar
- Ballupur
- Clock Tower
- Paltan Bazaar
- Dalanwala
- Rajpur Road
- Pacific Mall

### Emergency / Rescue Locations

- Hospital
- Fire Station
- Police Station

### Additional Locations

- DIT University
- Golden Manor
- Imperial Heights

These locations are represented both in the project graph and on the geographic map where applicable.

---

# 🤖 Pathfinding Algorithms

ResQ AI supports four pathfinding algorithms.

## 1. A* Search

A* combines the actual path cost with a heuristic estimate of the remaining distance.

```text
f(n) = g(n) + h(n)
```

Where:

- `g(n)` = cost from the starting node
- `h(n)` = estimated cost to the destination
- `f(n)` = total estimated cost

A* is useful when an efficient route needs to be found using additional information about the destination.

---

## 2. Dijkstra's Algorithm

Dijkstra's algorithm finds the minimum-cost path from the starting location to the destination.

In this project, the cost can be based on:

- Distance
- Simulated travel time

For time optimization:

```text
Travel Cost = Distance × Traffic Factor
```

---

## 3. Breadth-First Search (BFS)

BFS explores the graph level by level.

It is useful for demonstrating an unweighted graph traversal approach.

---

## 4. Depth-First Search (DFS)

DFS explores one branch of the graph as deeply as possible before backtracking.

It is included primarily for algorithm comparison and demonstration.

---

# 🚦 Traffic & Road Management

The system includes a simulated traffic-management module.

Each road can have:

```text
Distance
Traffic Factor
Blocked / Open
```

### Traffic Factor

A higher traffic factor represents greater travel difficulty/time.

For example:

```text
Traffic = 1.0
```

represents normal conditions.

While:

```text
Traffic = 4.0
```

represents significantly heavier traffic.

The user can modify traffic conditions directly from the dashboard.

---

# 🚧 Road Blocking

Roads can also be manually blocked or reopened.

Example:

```text
Road A → Road B
        ↓
     BLOCKED
```

When a road is blocked, the pathfinding algorithms exclude that edge from their search.

This allows the system to demonstrate how an emergency route can change when a road becomes unavailable.

---

# 🚨 Emergency Management

The application allows users to report emergencies using:

### Emergency Type

- Medical
- Fire
- Accident
- Flood
- Other

### Severity

- Critical
- High
- Medium
- Low

### Location

Any supported location in the Dehradun project map.

Each emergency receives an identifier and can progress through the rescue workflow.

---

# 🚑 Rescue Dispatch

The rescue workflow is:

```text
Report Emergency
        ↓
Select Emergency
        ↓
Select Rescue Vehicle Location
        ↓
Select Algorithm
        ↓
Select Optimization Mode
        ↓
Calculate Route
        ↓
Assign Rescue Route
        ↓
Visualize Route
        ↓
Complete Emergency
```

The application displays:

- Selected algorithm
- Route cost
- Nodes explored
- Complete route
- Rescue vehicle location
- Emergency location
- Route steps

---

# 🛰️ Real Geographic Map

The frontend uses a real geographic map of Dehradun rather than a purely schematic map.

The map provides:

- Geographic positioning
- Satellite imagery
- Location markers
- Emergency markers
- Rescue vehicle markers
- Route visualization
- Optional 3D visualization

The project locations are plotted using longitude and latitude coordinates.

---

# 🛣️ Road-Following Route Visualization

A key feature of the frontend is the separation between **AI route selection** and **map visualization**.

The project's pathfinding algorithm determines the sequence of locations.

For example:

```text
DIT University
       ↓
Golden Manor
       ↓
Imperial Heights
```

The route is then visualized using real road geometry when routing data is available.

Therefore, instead of displaying a simple straight line:

```text
DIT ───────────── Imperial Heights
```

the map can display a route that follows the actual road network.

### Architecture

```text
             ResQ AI Graph
                   │
                   ▼
        A* / Dijkstra / BFS / DFS
                   │
                   ▼
          Selected route sequence
                   │
                   ▼
            Road geometry
                   │
                   ▼
        Real geographic map
                   │
                   ▼
       🛣️ Visual rescue route
```

The road-following visualization is therefore separate from the project's core graph-based pathfinding logic.

---

# 🎨 Interactive Frontend

The application is developed using **Streamlit** and provides a modern emergency command-center interface.

### Main sections

```text
🚑 ResQ AI
│
├── 3D City Dashboard
│
├── Report Emergency
│
├── Rescue Operations
│
├── Traffic & Roads
│
└── Emergency Records
```

The dashboard includes:

- Emergency statistics
- Interactive map
- Location overview
- Emergency history
- Rescue route visualization
- Map style controls
- Optional subtle 3D buildings

---

# 🏙️ Optional 3D Visualization

The dashboard includes an optional subtle 3D mode.

It can display simplified building structures while maintaining the geographic map underneath.

The 3D visualization is primarily intended to improve presentation and visual understanding rather than represent exact architectural building models.

---

# 🧩 System Architecture

```text
                         ┌─────────────────────┐
                         │     Streamlit UI    │
                         └──────────┬──────────┘
                                    │
                  ┌─────────────────┼─────────────────┐
                  │                 │                 │
                  ▼                 ▼                 ▼
          Emergency Manager   Traffic Manager    Map Interface
                  │                 │                 │
                  └─────────────────┼─────────────────┘
                                    │
                                    ▼
                           City Graph / Network
                                    │
                                    ▼
                         Pathfinding Algorithms
                                    │
                 ┌──────────────────┼──────────────────┐
                 │                  │                  │
                 ▼                  ▼                  ▼
                A*              Dijkstra             BFS / DFS
                 │                  │                  │
                 └──────────────────┼──────────────────┘
                                    │
                                    ▼
                           Selected Rescue Route
                                    │
                                    ▼
                         Geographic Map Layer
                                    │
                                    ▼
                         🛰️ Dehradun Visualization
```

---

# 📁 Project Structure

```text
Emergency_Rescue_AI/
│
├── app.py
│   └── Main Streamlit application and frontend
│
├── algorithms.py
│   └── BFS, DFS, Dijkstra and A* implementations
│
├── city_graph.py
│   └── Dehradun graph and road definitions
│
├── emergency.py
│   └── Emergency management and status handling
│
├── traffic.py
│   └── Traffic and road-block management
│
├── compare_algorithms.py
│   └── Algorithm comparison utilities
│
├── test_algorithms.py
│   └── Algorithm testing
│
├── requirements.txt
│   └── Python dependencies
│
├── README.md
│   └── Project documentation
│
└── .gitignore
    └── Files excluded from Git
```

---

# 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Web application and frontend |
| NetworkX | Graph representation |
| PyDeck | Interactive map visualization |
| Requests | Road-routing communication |
| Git | Version control |
| GitHub | Source-code hosting |
| Streamlit Community Cloud | Application deployment |
| Satellite Map Tiles | Geographic visualization |

---

# ⚙️ Installation

## 1. Clone the repository

```bash
git clone https://github.com/SoumityaPandey/Emergency_Rescue_AI.git
```

## 2. Enter the project directory

```bash
cd Emergency_Rescue_AI
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 4. Run the application

```bash
streamlit run app.py
```

The application will normally be available at:

```text
http://localhost:8501
```

---

# 📦 Requirements

The project requires the following main packages:

```text
streamlit
pydeck
requests
networkx
```

They are listed in `requirements.txt`.

---

# 🧪 Testing the System

The project includes algorithm testing through:

```text
test_algorithms.py
```

Run:

```bash
python test_algorithms.py
```

Algorithm comparison can be performed using:

```bash
python compare_algorithms.py
```

---

# 🚀 Deployment

The application is deployed using **Streamlit Community Cloud**.

### Live Application

🔗 **https://resq-ai-dehradun.streamlit.app**

### GitHub Repository

🔗 **https://github.com/SoumityaPandey/Emergency_Rescue_AI**

---

# 🔄 Updating the Deployed Application

After making changes locally:

```bash
git add .
```

```bash
git commit -m "Update ResQ AI"
```

```bash
git push
```

The GitHub repository remains the source for the deployed application, allowing the Streamlit deployment to be updated without changing the application's public URL.

---

# 🔐 Project Safety

The repository uses `.gitignore` to avoid committing unnecessary local files such as:

```text
__pycache__/
*.pyc
.venv/
venv/
.env
.streamlit/secrets.toml
tempCodeRunnerFile.py
```

Sensitive credentials, passwords, API keys, or secrets should never be committed to the repository.

---

# 📊 Example Rescue Scenario

### Scenario

A fire emergency is reported at:

```text
Imperial Heights
```

A rescue vehicle starts from:

```text
DIT University
```

The operator selects:

```text
Algorithm:
A*

Optimization:
Distance
```

The system calculates a graph-based route:

```text
DIT University
        ↓
Golden Manor
        ↓
Imperial Heights
```

The frontend then displays:

```text
🟢 Rescue Vehicle
        │
        │ 🛣️ Rescue Route
        │
        🟠 Golden Manor
        │
        │
        🔴 Emergency
        Imperial Heights
```

The dashboard provides the calculated route, cost, explored nodes, and emergency status.

---

# 🎓 Academic Relevance

ResQ AI demonstrates practical applications of several computer science concepts:

### Artificial Intelligence

- A* Search
- Heuristic Search
- State-space exploration
- Pathfinding

### Data Structures & Algorithms

- Graphs
- BFS
- DFS
- Priority Queues
- Dijkstra's Algorithm

### Software Engineering

- Modular Python architecture
- Separation of concerns
- Testing
- Version control

### Web Development

- Interactive dashboards
- Streamlit
- Geographic visualization

### Real-World Application

- Emergency response
- Rescue dispatch
- Traffic-aware routing
- Road-block scenarios
- Geographic decision support

---

# 🔮 Future Enhancements

The current system is a functional prototype. Future versions could include:

- Real-time traffic data
- Live GPS tracking of rescue vehicles
- Multiple rescue vehicles
- Automatic nearest emergency-service selection
- Real hospital availability
- Live emergency notifications
- Weather and flood information
- Ambulance fleet management
- Real road-network graph generation
- Estimated arrival time
- Historical emergency analytics
- Machine-learning-based traffic prediction
- Real-time multi-agent dispatch
- Mobile application integration

---

# ⚠️ Current Limitations

The project is designed as an academic prototype and therefore has some limitations:

1. Traffic values are simulated rather than obtained from a live traffic provider.
2. Road blocking is controlled manually through the application.
3. The project graph represents selected important locations rather than every road in Dehradun.
4. The 3D buildings are simplified visual representations.
5. Road-following visualization depends on availability of the external routing service.
6. Emergency data is maintained within the application's runtime rather than a persistent production database.

These limitations provide clear directions for future development.

---

# 👨‍💻 Project Information

**Project:** ResQ AI — Intelligent Emergency Response & Rescue System

**Location:** Dehradun, Uttarakhand, India

**Platform:** Streamlit

**Language:** Python

**Repository:**  
https://github.com/SoumityaPandey/Emergency_Rescue_AI

**Live Demo:**  
https://resq-ai-dehradun.streamlit.app

---

# ⭐ If You Like the Project

If this project is useful or interesting, consider giving the repository a ⭐ on GitHub.

---

## 🚑 ResQ AI

> **Think faster. Find the route. Respond smarter.**
