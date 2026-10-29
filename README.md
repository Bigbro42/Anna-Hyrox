# Anna HYROX · HYROX 2

Eigenständige Progressive Web App mit einem **vollständig vorbefüllten Trainingsplan** aus `HYROX_Neustart_13_Wochen_bis_19-01-2027.xlsx`.

## Enthalten

- **13 Wochen, 52 Workout-Termine**, direkt im Kalender verankert (Mo A Lauf, Mi B Kraft, Fr D Kraft/HYROX, So C Kombination).
- 3 zusätzliche Race-Week-Termine (17., 18. und 19. Januar 2027).
- Alle Wochenfoki, Phasen, Übungsblöcke, Ziel-RPE, Pausen, Sled-, Carry-, Lunge- und Wall-Ball-Progressionen aus dem Excel-Plan.
- Vollständig editierbare Trainingstermine (Datum, Titel, Übungen, Umfang, tatsächliche Werte, Status, Notizen), neue Termine, Verschieben, Wiederherstellen, Auslassen.
- Partnerstrategie für Mixed Doubles mit editierbaren Anteilen.
- Fortschrittsansicht und Wochen-Check-ins (Energie, Handgelenk, Laufgefühl).
- Eigenständiges App-Icon, offline-fähige PWA, lokaler IndexedDB-Speicher und JSON-/CSV-Export.

## Termindifferenz unbedingt beachten

**Die Excel-Datei nennt das Renn-Datum 19.01.2027 und den Trainingsbeginn 19.10.2026.** Das unterscheidet sich vom im Gespräch genannten HYROX Wien im Februar 2027. Die App übernimmt absichtlich das Excel-Datum, **ohne** es stillschweigend zu verändern. In den App-Einstellungen können Start und Race Date angepasst werden. Der Planbeginn verschiebt alle Termine gemeinsam; das Renndatum wird separat bearbeitet.

Das Blatt nennt **vier** Einheiten/Woche, während die frühere allgemeine Trainingsplanung drei Einheiten plus Fußball vorsah. In der App gilt der beigefügte Plan; bei Zeitmangel priorisiert die Datei A + B + C.

Die Datei enthält Hinweise zum **Handgelenk**. Sie enthält keine individuelle Diagnose. Stationen, Gewichte, Belastung und Renntermin vor der Nutzung mit realer Belastbarkeit und aktuellem offiziellen Regelwerk abgleichen.

## Als dritte App auf GitHub Pages veröffentlichen

1. Neues **öffentliches** GitHub-Repository anlegen, zum Beispiel `Bigbro42/Anna-Hyrox`.
2. Alle Dateien **aus dem ZIP-Ordner direkt in den Root** des Repositories hochladen: `index.html`, `app.js`, `styles.css`, `plan.json`, `sw.js`, `manifest.webmanifest`, die Icons und diese README. Nicht nur das ZIP hochladen.
3. GitHub → Repository **Settings → Pages → Deploy from a branch → main → /(root)** aktivieren.
4. Die Adresse lautet dann bei diesem Repo-Namen: `https://bigbro42.github.io/Anna-Hyrox/`.
5. Auf dem iPhone: Safari → Teilen → Zum Home-Bildschirm. Auf Android: Chrome → App installieren.

GitHub Pages nutzt HTTPS. **Lokales Öffnen via `file://` funktioniert nicht zuverlässig**, weil `plan.json` mit `fetch()` geladen wird. Für lokale Entwicklung: `python -m http.server 8000` im Projektordner, dann `http://localhost:8000` öffnen.

## Datensicherheit

Die Trainingsdaten werden lokal in **IndexedDB** unter dem Namen `anna-hyrox2` gespeichert; als Fallback wird ein eigener `localStorage`-Eintrag verwendet. Die App ist unabhängig von FORM. und der anderen HYROX-App. Sie überträgt deine Trainingswerte nicht an GitHub.

Exportiere regelmäßig dein JSON-Backup. Browserdaten löschen, Browser wechseln oder deinstallieren kann die Daten entfernen. Die App enthält einen Import für exportierte Anna-HYROX-Backups.

## Quelle

Die `plan.json` wurde direkt aus den Blättern Übersicht, Kraft-Progression, Partnerstrategie, Hinweise sowie allen 13 Wochen und der Race Week der angehängten Excel-Datei erzeugt. Der Originalplan liegt bei dir weiterhin als Excel-Datei vor.

## Kein Medizinprodukt

Keine Diagnose, Therapieanweisung oder automatische Belastungsfreigabe. Schmerzhafte Übungen und relevante Beschwerden sollten individuell abgeklärt werden. Die vollständige Rennbelastung ist kein Versprechen, sondern ein aus der Datei übernommener Zielplan.
