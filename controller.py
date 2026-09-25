import time
import requests

class RoverController:
    def __init__(self, ip, username="admin", password=""):
        self.base_url = f"http://{ip}"
        self.auth = (username, password) if password else None
        # Timeout für schnelle Abbruchreaktionszeiten
        self.timeout = 2.0 

    def _send_cmd(self, command_path):
        """Sendet einen CGI-Steuerbefehl an den Rover."""
        url = f"{self.base_url}/{command_path}"
        try:
            response = requests.get(url, auth=self.auth, timeout=self.timeout)
            if response.status_code == 200:
                print(f"[OK] Befehl gesendet: {command_path}")
            else:
                print(f"[Fehler] Status-Code {response.status_code} bei {command_path}")
        except requests.exceptions.RequestException as e:
            print(f"[Verbindungsfehler] {e}")

    # --- Bewegungsbefehle ---
    def vorwaerts(self, dauer=1.0):
        print("Fahre vorwärts...")
        self._send_cmd("cgi-bin/decoder_control.cgi?command=0") # 0 = Vorwärts
        time.sleep(dauer)
        self.stopp()

    def rueckwaerts(self, dauer=1.0):
        print("Fahre rückwärts...")
        self._send_cmd("cgi-bin/decoder_control.cgi?command=1") # 1 = Rückwärts
        time.sleep(dauer)
        self.stopp()

    def links(self, dauer=0.5):
        print("Drehe links...")
        self._send_cmd("cgi-bin/decoder_control.cgi?command=2") # 2 = Links
        time.sleep(dauer)
        self.stopp()

    def rechts(self, dauer=0.5):
        print("Drehe rechts...")
        self._send_cmd("cgi-bin/decoder_control.cgi?command=3") # 3 = Rechts
        time.sleep(dauer)
        self.stopp()

    def stopp(self):
        print("Stopp.")
        self._send_cmd("cgi-bin/decoder_control.cgi?command=4") # 4 = Stopp

    # --- Kamerasteuerung / Tilt ---
    def kamera_hoch(self):
        self._send_cmd("cgi-bin/decoder_control.cgi?command=5")

    def kamera_runter(self):
        self._send_cmd("cgi-bin/decoder_control.cgi?command=6")

    # --- Patrouillen-Routine ---
    def patrouille(self):
        """Eine einfache automatische Kontrollrunde."""
        print("=== Starte Patrouille ===")
        
        # 1. Stück nach vorne fahren
        self.vorwaerts(dauer=2.0)
        
        # 2. Umsehen (Kamera hoch/runter + Drehung)
        self.kamera_hoch()
        time.sleep(1)
        self.links(dauer=1.5)
        self.kamera_runter()
        
        # 3. Weiterfahren
        self.vorwaerts(dauer=2.0)
        
        # 4. Umkehren
        self.rechts(dauer=3.0) # ca. 180 Grad Drehung
        self.vorwaerts(dauer=4.0)
        
        print("=== Patrouille beendet ===")


if __name__ == "__main__":
    # ERSETZEN: IP-Adresse des Rovers in deinem WLAN
    ROVER_IP = "192.168.0.75" 
    
    rover = RoverController(ip=ROVER_IP, username="admin", password="")

    # Beispiel-Ablauf:
    rover.patrouille()
