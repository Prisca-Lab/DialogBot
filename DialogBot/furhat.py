from furhat_remote_api import FurhatRemoteAPI
import time


class FurhatController:
    def __init__(self, ip, voice):
        self.furhat = None
        self.ip = ip
        self.voice = voice
        self.gestures = [
            "BigSmile", "Blink", "BrowFrown", "BrowRaise", "CloseEyes",
            "ExpressAnger", "ExpressDisgust", "ExpressFear", "ExpressSad",
            "GazeAway", "Nod", "Oh", "OpenEyes", "Roll", "Shake",
            "Smile", "Surprise", "Thoughtful", "Wink"
        ]

    def connect(self):
        """Connette Furhat utilizzando l'indirizzo IP fornito."""
        if not self.furhat:
            self.furhat = FurhatRemoteAPI(self.ip)
            if self.voice is not None:
                self.furhat.set_voice(name=self.voice)
            print("Connesso a Furhat con la voce ", self.voice)

    def say_something(self, text, blocking=True):
        if not self.furhat:
            raise Exception("Furhat not connected. Call connect() first.")

        # Use the following instructions when using the physical robot. Virtualenv has no camera option
        # Wait for the closest human user
        # users = self.furhat.get_users()
        # print("List of users:", users)
        # self.furhat.attend(user="CLOSEST")

        # Note: furhat can only block execution for 60 seconds
        self.furhat.say(text=text, blocking=blocking)  # use abort=True to abort current speaking

    def listen(self, language="it-IT"):
        """Furhat ascolta e restituisce il risultato del parlato riconosciuto."""
        if not self.furhat:
            raise Exception("Furhat non connesso. Chiama connect() prima.")
        result = self.furhat.listen(language=language)
        return result

    def perform_gesture(self, gesture_name, blocking=True):
        """Esegue un gesto specifico."""
        if not self.furhat:
            raise Exception("Furhat non connesso. Chiama connect() prima.")
        self.furhat.gesture(name=gesture_name, blocking=blocking)
        print("Eseguito gesto: ", gesture_name)

    def blink_light(self, red=255, green=255, blue=255, duration=1.0):
        """
        Blink the robot's light with a specified color and duration.
        :param red: Intensity of red (0-255)
        :param green: Intensity of green (0-255)
        :param blue: Intensity of blue (0-255)
        :param duration: Duration of the blink in seconds
        """
        if not self.furhat:
            raise Exception("Furhat not connected. Call connect() first.")

        self.furhat.furhat_led_post(red=red, green=green, blue=blue)
        time.sleep(duration)
        self.furhat.furhat_led_post(red=0, green=0, blue=0)


# Esempio di utilizzo
if __name__ == "__main__":
    controller = FurhatController("100.101.0.172", "Adriano-Neural")
    controller.connect()

    controller.perform_gesture(controller.gestures[0])  # BigSmile example

    controller.blink_light(red=255, green=0, blue=0, duration=2.0)
