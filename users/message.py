class message:
    def __init__(self, type: str, message: str, code: int, img: str = None, details: object = None):
        self.type = type
        self.message = message
        self.code = code
        self.img = img
        self.details = details

    def __str__(self):
        return f"[{self.type.upper()}] Código {self.code}: {self.message} (Imagen: {self.img}) (Detalles: {self.details})"

    def to_dict(self):
        return {
            "tipo": self.type,
            "mensaje": self.message,
            "codigo": self.code,
            "imagen": self.img,
            "details": self.details
        }