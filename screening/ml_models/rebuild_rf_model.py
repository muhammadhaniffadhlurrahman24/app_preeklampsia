"""
Utility to (re)build `rf_preeclampsia.joblib`.

Usage (recommended): create a Python 3.8 venv and install NumPy 1.24.3
so the binary will be compatible with your Django environment.

Example commands (PowerShell):

# create a Python 3.8 virtualenv (make sure python3.8 is installed)
python3.8 -m venv .venv-py38
.\.venv-py38\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install numpy==1.24.3 scikit-learn==1.2.2 joblib

# run the rebuild script (it will save rf_preeclampsia.joblib in the same folder)
python rebuild_rf_model.py --out rf_preeclampsia.joblib

If you have training data, place a CSV at `training_data.csv` (same folder)
with the last column as the label (0/1) and the first 29 columns as features.
If no training data exists the script will generate a small synthetic dataset
and train a RandomForestClassifier with a deterministic seed.

"""
import argparse
import os
import sys
import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report


def load_csv(path):
    import csv

    """
    Load training data from CSV.

    Disesuaikan agar bisa membaca `ALL_FINAL.csv`:
    - Separator: titik koma `;`
    - Kolom terakhir: label string "NonPreeklampsia" / "Preeklampsia"

    Juga tetap bisa membaca CSV sederhana dengan label 0/1.
    """

    X = []
    y = []
    with open(path, newline="", encoding="utf-8") as fh:
        # `ALL_FINAL.csv` memakai delimiter ';'
        reader = csv.reader(fh, delimiter=";")
        rows = list(reader)

    if not rows:
        raise ValueError(f"No data in CSV: {path}")

    # Skip header jika baris pertama berisi nama kolom (mis. 'Kabupaten/Kota')
    start_idx = 1 if rows[0] and "Kabupaten" in rows[0][0] else 0

    for row in rows[start_idx:]:
        if not row:
            continue

        # asumsi kolom terakhir adalah label
        *features, label = row

        # Ambil 29 fitur pertama dan ubah ke float (non‑numeric -> 0.0)
        raw_feats = features[:29]
        feats = []
        for x in raw_feats:
            s = (x or "").strip().strip('"').strip("'")
            try:
                feats.append(float(s) if s != "" else 0.0)
            except Exception:
                feats.append(0.0)
        X.append(feats)

        # Label:
        # - kalau sudah "NonPreeklampsia"/"Preeklampsia": biarkan string
        # - kalau 0/1: simpan sebagai int
        lab = (label or "").strip().strip('"').strip("'")
        if lab in ("NonPreeklampsia", "Preeklampsia"):
            y.append(lab)
        else:
            try:
                y.append(int(lab))
            except Exception:
                # fallback: pakai string mentah
                y.append(lab)

    X_arr = np.array(X, dtype=float)
    y_arr = np.array(y)
    return X_arr, y_arr


def generate_synthetic(n_samples=500, n_features=29, random_state=42):
    rng = np.random.RandomState(random_state)
    X = rng.normal(loc=0.0, scale=1.0, size=(n_samples, n_features))
    # create a simple rule to assign labels so model is not random:
    # sum of a few feature columns > threshold = positive
    weights = rng.uniform(-1, 1, size=(n_features,))
    scores = X.dot(weights)
    y = (scores > np.median(scores)).astype(int)
    return X, y


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--train', help='Path to CSV training data (optional)')
    parser.add_argument('--out', default='rf_preeclampsia.joblib', help='Output joblib filename')
    parser.add_argument('--n-estimators', type=int, default=100, help='RandomForest n_estimators')
    parser.add_argument('--seed', type=int, default=42, help='Random seed')
    parser.add_argument('--string-labels', action='store_true', help='Save model with string labels (NonPreeklampsia/Preeklampsia)')
    args = parser.parse_args()

    if args.train and os.path.exists(args.train):
        print('Loading training data from', args.train)
        X, y = load_csv(args.train)
        if X.shape[1] < 29:
            # pad columns to 29
            pad = np.zeros((X.shape[0], 29 - X.shape[1]))
            X = np.hstack([X, pad])
    else:
        print('No training CSV provided or not found; generating synthetic data')
        X, y = generate_synthetic(n_samples=800, n_features=29, random_state=args.seed)

    print('X shape:', X.shape, 'y shape:', y.shape)

    # Optionally convert numeric labels (0/1) to string labels for compatibility
    # with the application which previously expected 'Preeklampsia' strings.
    if args.string_labels:
        # If y is numeric, map 0->NonPreeklampsia, 1->Preeklampsia
        try:
            # Determine if all labels are ints 0/1
            uniq = set(int(v) for v in np.unique(y))
            if uniq.issubset({0, 1}):
                mapping = {0: 'NonPreeklampsia', 1: 'Preeklampsia'}
                y = np.array([mapping[int(v)] for v in y])
                print('Converted numeric labels to string labels:', mapping)
            else:
                # If labels are already strings or other ints, leave as-is
                print('Labels are not plain 0/1 integers; leaving labels as-is')
        except Exception:
            print('Could not convert labels to strings; leaving as-is')

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=args.seed)

    clf = RandomForestClassifier(n_estimators=args.n_estimators, random_state=args.seed)
    clf.fit(X_train, y_train)

    preds = clf.predict(X_test)
    print('Classification report on test set:')
    print(classification_report(y_test, preds))

    joblib.dump(clf, args.out)
    print('Saved model to', args.out)


if __name__ == '__main__':
    main()
