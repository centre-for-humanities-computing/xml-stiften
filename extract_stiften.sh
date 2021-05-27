python src/intermediary_json.py \
    -d "/media/jan/Seagate Expansion Drive/stiftstidende/1932-46/" \
    -o "data/processed/json"

python src/time_binning.py \
    -d "data/processed/json/" \
    -o "data/processed/monthly_txt/" \
    -f "txt" \
    -t "M"