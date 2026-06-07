# Visual Learning Games

Interactive visual learning games built with Streamlit to demonstrate complex concepts through interactive narratives.

## 🎮 Games

### The K8s Mystery: FinOps Learning Game
**Location:** `visuals/k8s_finops_mystery/`

An interactive narrative-driven simulation that demonstrates the real-world impact of poor FinOps practices on Kubernetes operations.

**Learn:**
- Why proper Kubernetes labeling is critical for incident response
- The true cost of "untagged" resources
- How FinOps practices impact operational efficiency

**Run:**
```bash
cd visuals/k8s_finops_mystery/
uv run streamlit run app.py
```

**See:** `visuals/k8s_finops_mystery/README.md` for detailed instructions.

## 🚀 Quick Start

1. **Navigate to the game:**
   ```bash
   cd visual-learning/visuals/k8s_finops_mystery/
   ```

2. **Install dependencies:**
   ```bash
   uv pip install -r requirements.txt
   ```

3. **Run the game:**
   ```bash
   uv run streamlit run app.py
   ```

## 📚 Documentation

- **Game Design:** See `visuals/k8s_finops_mystery/GAME_DESIGN.md` for detailed game concept and narrative arc.
- **Game Instructions:** See `visuals/k8s_finops_mystery/README.md` for how to play and customize.

## 🛠️ Development

### Using uv (Recommended)
```bash
# Install dependencies
uv pip install -r requirements.txt

# Run the app
uv run streamlit run app.py
```

### Using pip
```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

## 📊 Project Structure

```
visual-learning/
├── pyproject.toml              # Package configuration
├── README.md                   # This file
└── visuals/
    ├── __init__.py
    └── k8s_finops_mystery/
        ├── app.py              # Main application
        ├── components/         # Game components
        │   ├── __init__.py
        │   ├── state_manager.py
        │   ├── act1_incident.py
        │   ├── act2_investigation.py
        │   ├── act3_revelation.py
        │   └── act4_solution.py
        ├── assets/             # Icons, images
        ├── README.md           # Game instructions
        └── GAME_DESIGN.md      # Game design document
```

## 🎯 Key Features

- **Interactive narratives** with branching choices
- **Real-time metrics** showing MTTR and revenue impact
- **Visual feedback** with color-coded resources
- **Educational moments** explaining FinOps concepts
- **Side-by-side comparisons** showing Before vs After

## 📝 Adding New Games

1. Create a new folder in `visuals/`
2. Set up `pyproject.toml` for the game
3. Create game components and app entry point
4. Add instructions to this README

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
- Designed to demonstrate operational impact of proper resource management
