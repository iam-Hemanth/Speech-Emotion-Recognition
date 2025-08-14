# 🏗️ Project Restructuring Plan

## Current State Analysis
The project has already been partially restructured with some files in `src/ser/`, but there are still many files in the root directory that need to be organized.

## Files to Move to Target Structure

### 1. Core Python Files (Already in src/ser/)
✅ `src/ser/config.py` - Already moved
✅ `src/ser/features.py` - Already moved  
✅ `src/ser/model.py` - Already moved
✅ `src/ser/inference.py` - Already moved
✅ `src/ser/app.py` - Already moved
✅ `src/ser/datasets/tess.py` - Already moved

### 2. Data Organization
- Move `examples/` → `data/examples/` (already done)
- Move `dataset_features/` → `data/processed/dataset_features/` (already done)
- Move `TESS_Toronto_emotional_speech_set_data/` → `data/raw/tess/` (already done)
- Move `features/` → `data/processed/features/` (if exists)

### 3. Models
- Move `Deep Learning/SER_model.h5` → `models/SER_model.h5` (already done)
- Move `Deep Learning/SER(Deep_Learning).ipynb` → `notebooks/SER_Deep_Learning.ipynb`
- Move `Deep Learning/TestingLive.ipynb` → `notebooks/TestingLive.ipynb`

### 4. Notebooks
- Move `MLP.ipynb` → `notebooks/MLP.ipynb`
- Move `Machine Learning Algorithm - SVM/` contents → `notebooks/`

### 5. Documentation
- Move `PROJECT_GUIDE.txt` → `docs/PROJECT_GUIDE.md`
- Move `Docs/` contents → `docs/` (if not already done)

### 6. Assets
- Move `media/` → `assets/` (if not already done)

## Files to Quarantine (to_be_deleted/)
- `__pycache__/` directories
- `.DS_Store` files
- `downloads/` directory
- Any duplicate or legacy files
- Stray files that don't fit the structure

## Root Files to Keep
- `README.md`
- `requirements.txt`
- `.gitignore`
- `.gitattributes`
- `app.py` (entry point)
- `scripts/` directory

## Target Structure
```
.
├── src/
│   └── ser/
│       ├── __init__.py
│       ├── config.py
│       ├── features.py
│       ├── model.py
│       ├── inference.py
│       ├── datasets/
│       │   └── tess.py
│       └── app.py
├── scripts/
│   ├── predict.sh
│   └── rebuild_features.sh
├── models/
│   └── SER_model.h5
├── data/
│   ├── raw/
│   │   └── tess/
│   ├── processed/
│   │   └── dataset_features/
│   └── examples/
├── notebooks/
├── docs/
├── assets/
├── .github/
├── .gitattributes
├── .gitignore
├── requirements.txt
└── README.md
```

## Execution Steps
1. ✅ Create quarantine directory
2. ✅ Move files to target structure
3. ✅ Update imports and paths
4. ✅ Create helper scripts
5. ✅ Update .gitignore and .gitattributes
6. ✅ Update README.md
7. ✅ Run smoke tests
8. ✅ Create cleanup logs
9. ✅ Fix import issues for direct execution

## What Was Actually Moved

### Files Moved to Quarantine (to_be_deleted/)
- `__pycache__/` directories (Python cache)
- `.DS_Store` (macOS system file)
- `downloads/` (temporary downloads)
- `run_inference.py` (duplicate of src/ser/inference.py)
- `ser_model.py` (duplicate of src/ser/model.py)
- `tess_pipeline.py` (duplicate of src/ser/datasets/tess.py)
- `create_features.py` (duplicate of src/ser/features.py)
- `config.py` (duplicate of src/ser/config.py)
- `Deep Learning/` (legacy directory, notebooks moved)
- `Machine Learning Algorithm - SVM/` (legacy directory, notebooks moved)
- `MLP classifier/` (legacy directory, notebooks moved)
- `Docs/` (legacy documentation directory)
- `TESS_Toronto_emotional_speech_set_data/` (legacy data directory)
- `features/` (legacy features directory)
- `examples/` (legacy examples directory)
- `dataset_features/` (legacy dataset directory)
- `media/` (contents moved to assets/)

### Files Reorganized
- `MLP.ipynb` → `notebooks/MLP.ipynb`
- `Deep Learning/SER(Deep_Learning).ipynb` → `notebooks/SER_Deep_Learning.ipynb`
- `Deep Learning/TestingLive.ipynb` → `notebooks/TestingLive.ipynb`
- `Machine Learning Algorithm - SVM/SER - SVM - Feature Extraction-.ipynb` → `notebooks/SER - SVM - Feature Extraction-.ipynb`
- `Machine Learning Algorithm - SVM/SER_SVM.ipynb` → `notebooks/SER_SVM.ipynb`
- `PROJECT_GUIDE.txt` → `docs/PROJECT_GUIDE.md`
- `media/*` → `assets/`

### New Files Created
- `.gitattributes` (Git LFS configuration)
- `scripts/predict.sh` (prediction helper script)
- `scripts/rebuild_features.sh` (feature rebuild script)
- `scripts/restore_from_quarantine.py` (file restore tool)
- `cleanup_log.txt` (cleanup log)
- `cleanup_map.json` (cleanup mapping)
- `models/.gitkeep` (preserve empty models directory)
- `data/processed/.gitkeep` (preserve empty processed directory)
