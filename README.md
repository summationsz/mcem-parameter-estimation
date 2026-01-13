# Multi-Organism MCEM Parameter Estimation Framework

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 📋 Overview

A comprehensive framework for kinetic parameter estimation in metabolic pathways using Monte Carlo Expectation-Maximization (MCEM) algorithms. This project validates MCEM parameter estimation across multiple organisms and pathways, demonstrating cross-kingdom applicability of the methodology.

**Thesis Title:** *Enhancing Kinetic Parameter Identifiability in Biochemical Networks via Expectation Maximization*

### Key Features

- ✅ **Multi-organism validation** across bacteria, plants, and fungi
- ✅ **Dual pathway analysis** (Glycolysis + TCA cycle)
- ✅ **Automated visualization** generation (300 DPI publication-ready plots)
- ✅ **Comprehensive data export** (Excel & CSV formats)
- ✅ **Robustness testing** under noise and missing data conditions
- ✅ **Bayesian identifiability analysis** with Fisher Information metrics

---

## 🧬 Organisms Studied

| Kingdom | Organism | Type | Pathways |
|---------|----------|------|----------|
| Bacteria | *E. coli* | Gram-negative prokaryote | Glycolysis + TCA |
| Bacteria | *B. subtilis* | Gram-positive prokaryote | Glycolysis + TCA |
| Plant | *Arabidopsis thaliana* | Model plant | Glycolysis + TCA |
| Fungi | *S. cerevisiae* | Baker's yeast | Glycolysis + TCA |

**Total Parameters Estimated:** ~152 parameters (38 per organism)

---

## 🛠️ Installation

### Prerequisites

- Python 3.9 or higher
- pip package manager

### Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/mcem-parameter-estimation.git
   cd mcem-parameter-estimation
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify installation:**
   ```bash
   python Phase6_2.0_MAIN_WITH_TEST.py
   ```

---

## 🚀 Quick Start

### Running a Test Analysis

```bash
python Phase6_2.0_MAIN_WITH_TEST.py
```

**Select:**
- Analysis: `4` (Complete Analysis)
- Organism: `1` (E. coli)
- Mode: `D` (TEST - ~15-20 minutes)
- Proceed: `Y`

**Output:**
```
results/Session1_CompleteAnalysis_Ecoli_TEST/
  ├── parameter_estimation.npz
  ├── robustness.npz
  ├── bayesian_fispo.npz
  ├── visualizations/
  │   └── E._coli/ [11 high-res PNG plots]
  └── data_exports/
      ├── MASTER_Results.xlsx
      ├── parameter_estimates.csv
      └── summary_statistics.csv
```

---

## 📊 Analysis Modes

### Computation Levels

| Mode | Iterations | Samples | Runtime (per organism) | Use Case |
|------|------------|---------|------------------------|----------|
| **TEST** | 20 | 500 | ~15-20 min | Quick verification |
| **FAST** | 100 | 1000 | ~4-6 hours | Preliminary analysis |
| **BALANCED** | 150 | 1500 | ~8-12 hours | Standard analysis |
| **PRECISE** | 200 | 2000 | ~24+ hours | Final publication |

### Analysis Types

1. **Parameter Estimation** - MCEM-based parameter recovery
2. **Robustness Testing** - Noise sensitivity and missing data analysis
3. **Bayesian + FISPO** - Parameter identifiability analysis
4. **Complete Analysis** - All three analyses in sequence (RECOMMENDED)
5. **Generate Report** - Comparative summary from existing results

---

## 📈 Output Files

### Visualizations (300 DPI, Publication-Ready)

Each organism generates **11 high-resolution plots:**

**Individual Plots (8 files):**
- Parameter estimates vs. true values (per pathway)
- Relative error bar charts (per pathway)
- Error distribution histograms (per pathway)
- Overall pathway performance comparison
- Error boxplot by pathway

**Grouped Plots (2 files):**
- All pathways parameter estimation (2×2 grid)
- All pathways error analysis (2×2 grid)

**Overview Plot (1 file):**
- Complete analysis overview (3×3 grid)

### Data Exports

**Excel Files:**
- `MASTER_Results.xlsx` - Complete dataset in one workbook
- `parameter_estimates.xlsx` - All parameter estimates with errors
- `summary_statistics.xlsx` - Statistical summary by pathway
- `organism_comparison.xlsx` - Cross-organism performance

**CSV Files:**
- `parameter_estimates.csv`
- `summary_statistics.csv`
- `organism_comparison.csv`
- `error_distributions.csv`

---

## 🔬 Methodology

### MCEM Algorithm

The Monte Carlo Expectation-Maximization algorithm iteratively refines parameter estimates by:

1. **E-step:** Sample parameter space using current estimates
2. **M-step:** Maximize likelihood using Monte Carlo integration
3. **Convergence:** Iterate until parameter changes stabilize

### Parameter Recovery Validation

Performance metrics:
- **Relative Error:** `|estimated - true| / true × 100%`
- **Average Error:** Mean across all parameters
- **Identifiability Score:** Based on Fisher Information

### Robustness Testing

- **Noise Sensitivity:** 5%, 10%, 15%, 20% noise levels
- **Missing Data:** 10%, 20%, 30% random removal
- **Success Rate:** Algorithm convergence percentage

---

## 📁 Project Structure

```
MCEM-Parameter-Estimation/
├── Phase6_2.0_MAIN_WITH_TEST.py       # Main entry point
├── phase6_parameter_estimation.py     # Parameter estimation module
├── phase6_robustness.py               # Robustness testing module
├── phase6_bayesian_fispo.py           # Identifiability analysis
├── phase6_complete_analysis.py        # Complete analysis workflow
├── phase6_generate_report.py          # Report generation
├── generate_thesis_visualizations.py  # Visualization generator
├── export_data_tables.py              # Excel/CSV export module
├── glycolysis_model.py                # Glycolysis pathway ODE model
├── tca_model.py                       # TCA cycle ODE model
├── my_mcem_fixed.py                   # MCEM implementation
├── kinetic_parameters.py              # Parameter definitions
├── add_true_params.py                 # Data preparation utility
├── Bio-Database/                      # Organism data (SBML models)
│   ├── BACTERIA/
│   │   ├── Escherichia_coli/
│   │   └── Bacillus_subtilis/
│   ├── PLANTS/
│   │   └── Arabidopsis_thaliana/
│   └── FUNGI/
│       └── Saccharomyces_cerevisiae/
├── results/                           # Generated results (git-ignored)
├── requirements.txt                   # Python dependencies
├── README.md                          # This file
└── .gitignore                         # Git ignore rules
```

---

## 💻 Advanced Usage

### Standalone Visualization

Generate visualizations for existing results:

```bash
# Interactive mode (shows session selector)
python generate_thesis_visualizations.py

# Direct mode
python generate_thesis_visualizations.py results/Session1_CompleteAnalysis_Ecoli_TEST
```

### Standalone Data Export

Export Excel/CSV files from existing results:

```bash
python export_data_tables.py results/Session1_CompleteAnalysis_Ecoli_TEST
```

### Generate Comparative Report

Create text-based summary report:

```bash
python phase6_generate_report.py
```

---

## 📊 Example Results

### Parameter Estimation Performance

| Organism | Parameters | Average Error | Runtime (TEST) |
|----------|------------|---------------|----------------|
| *E. coli* | 38 | 14.37% | 11.4 min |
| *B. subtilis* | 38 | 14.37% | 65.7 min |
| *Arabidopsis* | 38 | 14.37% | 55.4 min |
| *S. cerevisiae* | 38 | 7.48% | 8.8 min |

### Robustness Results

- **Noise Sensitivity:** <2% error increase up to 20% noise
- **Missing Data:** 89% success rate with 30% missing data
- **Identifiability:** 4 highly identifiable parameters per organism

---

## 🤝 Contributing

This is a thesis research project. For questions or collaboration inquiries, please contact the author.

---

## 📄 Citation

If you use this work in your research, please cite:

```bibtex
@thesis{yourname2026,
  author = {Your Name},
  title = {Enhancing Kinetic Parameter Identifiability in Biochemical Networks via Expectation Maximization},
  school = {Your University},
  year = {2026},
  type = {Bachelor's Thesis}
}
```

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙏 Acknowledgments

- **BioModels Database** for SBML model data
- **BRENDA** and **MetaCyc** for kinetic parameter references
- **Anthropic** for computational assistance during development

---

## 📧 Contact

**Author:** John Gabriel M. Gali
**Email:** johngabrielmgali@iskolarngbayan.pup.edu.ph  
**Thesis Advisor:** Dr. Erickson Fajikulay  
**Institution:** Polytechnic University of the Philippines Sta. Mesa Manila

---

## 🔧 Troubleshooting

### Common Issues

**Issue:** `ModuleNotFoundError: No module named 'pandas'`
```bash
pip install pandas openpyxl
```

**Issue:** MCEM takes too long
- Solution: Use TEST mode (D) for quick verification
- For production: Use FAST mode (A) overnight

**Issue:** Visualizations fail
```bash
# Run manually
python generate_thesis_visualizations.py results/SessionN
```

**Issue:** Excel files not created
```bash
# Run manually
python export_data_tables.py results/SessionN
```

---

## 🎯 Future Work

- [ ] Extended pathway coverage (pentose phosphate, fatty acid metabolism)
- [ ] Additional organism validation (mammalian systems)
- [ ] GPU acceleration for MCEM
- [ ] Web-based visualization dashboard
- [ ] Real-time parameter estimation monitoring

---

**⭐ If you find this work useful, please star the repository!**

---

*Last Updated: January 2026*
