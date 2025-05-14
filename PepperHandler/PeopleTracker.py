# coding=utf-8
import threading
import time


class PeopleTracker:
    def __init__(self, session):
        """Inizializza il tracker con una sessione Qi esistente."""
        self.session = session
        self.people_service = self.session.service("ALPeoplePerception")
        self.memory_service = self.session.service("ALMemory")
        self.tracker_service = self.session.service("ALTracker")

        self.target_id = None
        self.tracking_active = False
        self.tracking_thread = None

    def tracking_loop(self):
        """Loop di tracking che gira in un thread separato."""
        self.people_service.subscribe("PeopleTracking")
        # self.tracker_service.setMode("Move")  # Permette a Pepper di muoversi per inseguire
        self.tracker_service.setMode("Head")  # Solo la testa si muove

        while self.tracking_active:
            people_list = self.memory_service.getData("PeoplePerception/PeopleList")

            if people_list:
                if self.target_id not in people_list:  # Se il target è perso o cambiato
                    self.target_id = people_list[0]
                    print("Nuovo target:", self.target_id)

                    self.tracker_service.unregisterAllTargets()
                    self.tracker_service.registerTarget("People", self.target_id)
                    self.tracker_service.track("People")
            else:
                print("Nessuna persona visibile, continuo a cercare...")

            time.sleep(5)  # Aspetta 5 secondi prima di controllare di nuovo

    def start_tracking(self):
        """Avvia il tracking in un thread separato."""
        if not self.tracking_active:
            self.tracking_active = True
            self.tracking_thread = threading.Thread(target=self.tracking_loop)
            self.tracking_thread.daemon = True  # Il thread si chiuderà automaticamente con il programma
            self.tracking_thread.start()
            print("Tracking avviato.")

    def stop_tracking(self):
        """Ferma il tracking."""
        if self.tracking_active:
            self.tracking_active = False
            if self.tracking_thread:
                self.tracking_thread.join()  # Attende la chiusura del thread
            self.tracker_service.stopTracker()
            self.tracker_service.unregisterAllTargets()
            print("Tracking fermato.")
