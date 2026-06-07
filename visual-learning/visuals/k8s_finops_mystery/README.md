# FinOps K8s Mystery — Visual Learning Game

An interactive narrative-driven simulation that demonstrates the real-world impact of poor FinOps practices on Kubernetes operations.

## 🎮 Game Overview

**"The K8s Mystery: Who Owns the Broken Service?"**

Experience the frustration of on-call engineering without proper FinOps practices. Watch how a 3-minute technical fix turns into a 4+ hour investigation nightmare when ownership information is missing or outdated.

## 📚 What You'll Learn

- Why proper Kubernetes labeling is critical for incident response
- The true cost of "untagged" resources in terms of MTTR, revenue, and team morale
- How FinOps practices directly impact operational efficiency
- The compound effect of poor resource attribution during critical incidents

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- pip or uv package manager

### Installation

1. **Navigate to the project directory:**
   ```bash
   cd visual-learning/visuals/k8s_finops_mystery/
   ```

2. **Install dependencies using uv:**
   ```bash
   uv pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   uv run streamlit run app.py
   ```

## 📖 How to Play

The game consists of 4 Acts:

### Act 1: The Incident Begins (2 AM)
- Receive a critical PagerDuty alert
- Investigate a cascading failure in payment-api
- Try to find ownership via Kubernetes labels (the pain begins)

### Act 2: The Investigation Deepens
- Slack chaos — ping multiple teams with no success
- Navigate an outdated org chart
- Check cost reports (60% untagged resources)
- Escalation roulette through 4 levels of management

### Act 3: The Revelation
- Finally find the owner by accident
- See the full impact: $127K revenue lost, 4h 23m MTTR
- Understand why the fix took 3 minutes but finding the owner took 4+ hours

### Act 4: The FinOps Solution
- Rewind and replay with proper FinOps practices
- See how the same incident takes 30 seconds to resolve
- Compare side-by-side: Before vs After
- Explore the FinOps dashboard

## 🎯 Key Features

- **Interactive narrative**: Make choices that affect the story
- **Real-time metrics**: Watch MTTR and revenue impact grow
- **Visual feedback**: Color-coded resources (red=bad, green=good)
- **Educational moments**: "What if FinOps had fixed this?" explanations
- **Side-by-side comparison**: See the difference FinOps makes

## 📊 Technical Details

### Project Structure
```
k8s_finops_mystery/
├── app.py                    # Main application entry point
├── components/
│   ├── __init__.py
│   ├── state_manager.py      # Game state and data
│   ├── act1_incident.py      # Act 1 scenes
│   ├── act2_investigation.py # Act 2 scenes
│   ├── act3_revelation.py    # Act 3 scenes
│   └── act4_solution.py      # Act 4 scenes
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

### Dependencies
- **streamlit**: Web application framework
- **plotly**: Data visualization
- **pandas**: Data manipulation

## 🛠️ Development

### Running with uv (Recommended)

```bash
# Install dependencies
uv pip install -r requirements.txt

# Run the app
uv run streamlit run app.py

# Or run directly with uv
uv run streamlit run app.py
```

### Running with pip

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

## 📝 Customization

### Adding New Scenes

1. Create a new function in the appropriate `actX_*.py` file
2. Add scene logic to check `st.session_state.current_scene`
3. Use `advance_scene()` to move to the next scene
4. Use `advance_act()` to move to the next act

### Modifying Game Data

Edit the data in `components/state_manager.py`:

```python
BROKEN_SERVICES = [
    {
        "name": "your-service",
        "namespace": "your-namespace",
        "error_rate": "xx%",
        "latency": "xx seconds",
        "owner_label": "your-label",
        "cost_center": "your-cost-center",
        "actual_owner": "your-team",
        "severity": "critical"
    },
    # ... more services
]
```

### Changing Metrics

Modify the MTTR and revenue calculation in `state_manager.py`:

```python
def add_mttr(minutes):
    st.session_state.mttr_minutes += minutes
    # Customize revenue calculation
    st.session_state.revenue_lost = st.session_state.mttr_minutes * 500
```

## 🎨 Styling

Custom CSS is embedded in `app.py` for the dark mode theme. You can modify:

- Background colors
- Metric card styles
- Button colors
- Text colors
- Sidebar styling

## 📚 Game Design Document

For detailed information about the game concept, narrative arc, and learning objectives, see:
- `GAME_DESIGN.md` — Complete game design document

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is part of the k8-finops-agent repository. See main repository license for details.

## 🙏 Acknowledgments

- Built with Streamlit
- Inspired by real-world FinOps challenges
- Designed to demonstrate operational impact of proper resource management

## 📞 Support

For questions or issues:
- Open an issue in the repository
- Contact the development team

---

**Ready to experience the K8s Mystery? Run `uv run streamlit run app.py` and start playing!** 🚀
