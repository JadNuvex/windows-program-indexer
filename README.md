# windows-program-indexer
A Python utility that scans C:\Program Files and C:\Program Files (x86) to index installed applications by locating .exe files. It automatically skips setup/install/uninstall executables, avoids duplicates, and saves a clean JSON map of discovered programs. Includes a progress bar via tqdm for real-time feedback.
