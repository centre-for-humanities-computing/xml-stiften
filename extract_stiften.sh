python src/intermediary_json.py \
    -d "data/sample_input/" \
    -o "data/processed/json/"

python src/time_binning.py \
    -d "data/processed/json/" \
    -o "data/processed/txt/" \
    -t "M" \
    -p True