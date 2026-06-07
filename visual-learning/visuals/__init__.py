# Visual Learning Games Package

This package contains interactive visual learning games built with Streamlit.

## Package Structure

```
visuals/
├── k8s_finops_mystery/    # FinOps K8s Mystery game
│   ├── app.py
│   ├── components/
│   ├── assets/
│   ├── README.md
│   └── requirements.txt
└── [other games...]
```

## Installation

```bash
# Install the package using uv
cd visual-learning
uv pip install -e .
```

## Usage

```bash
# Run a specific game
cd visuals/k8s_finops_mystery/
uv run streamlit run app.py
```

## Development

See individual game READMEs for development instructions.
