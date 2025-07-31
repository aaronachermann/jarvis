"""Vision analysis plugin using OpenCV if available."""
from . import Plugin, register

class Vision(Plugin):
    def setup(self) -> None:
        pass

    def capture(self) -> str:
        try:
            import cv2  # type: ignore
            cap = cv2.VideoCapture(0)
            ret, _ = cap.read()
            cap.release()
            if not ret:
                return "Impossibile acquisire immagine."
            return "Immagine catturata."  # placeholder
        except Exception as e:
            return f"Errore camera: {e}"

vision = Vision()
register(vision)
