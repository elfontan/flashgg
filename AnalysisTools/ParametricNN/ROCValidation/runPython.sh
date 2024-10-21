mkdir -p output
python3 plotMVA.py
python3 plotMVA_Data.py
python3 plotMVA_DataMassWindows.py
python3 plotMVA_Sig.py
python3 plotROC.py
python3 plotAsimov.py > output/outputAsimov.log
python3 plotAsimovOverlay.py
