import os


def file_count(directory):
    # Zähle die Dateien im angegebenen Verzeichnis
    try:
        files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        file_counter = len(files)  # Speichere die Anzahl in einer normalen Python-Variablen
        print(f"Anzahl der Dateien: {file_counter}")  # Drucke die Anzahl der Dateien in der Konsole
        return file_counter
    except Exception as e:
        print("Fehler beim Lesen des Verzeichnisses:", e)
        return 0