# TODO: Implementa el código del ejercicio aquí
from abc import ABC, abstractmethod
from modelo.errores import NoCumpleLongitudMinimaError, NoTieneLetraMayusculaError, NoTieneLetraMinusculaError, NoTieneNumeroError, NoTieneCaracterEspecialError, NoTienePalabraSecretaError

class ReglaValidacion(ABC):

    def __init__(self, _longitud_esperada: int):
        self._longitud_esperada = _longitud_esperada

    def _validar_longitud(self, clave: str)-> bool:
        if len(clave) >= self._longitud_esperada:
            return True
        return False

    def _contiene_mayuscula(self, clave: str) -> bool:
        return any(caracter.isupper() for caracter in clave)

    def _contiene_minuscula(self, clave: str) -> bool:
        return any(caracter.islower() for caracter in clave)
    
    def _contiene_numero(self, clave: str) -> bool:
        return any(caracter.isdigit() for caracter in clave)
    
    @abstractmethod
    def es_valida(self, clave)->bool:
        pass
    

class ReglaValidacionGanimedes(ReglaValidacion):
    def contiene_caracter_especial(self, clave)-> bool:
        c_especiales = {'@', '_', '#', '$', '%'}
        return any(c in c_especiales for c in clave)
    
    def es_valida(self, clave: str)-> bool:
        if not self._validar_longitud(clave):
            raise NoCumpleLongitudMinimaError
        if not self._contiene_mayuscula(clave):
            raise NoTieneLetraMayusculaError
        if not self._contiene_minuscula(clave):
            raise NoTieneLetraMinusculaError
        if not self._contiene_numero(clave):
            raise NoTieneNumeroError
        if not self.contiene_caracter_especial(clave):
            raise NoTieneCaracterEspecialError
        return True
    

class ReglaValidacionCalisto(ReglaValidacion):
    def contiene_calisto(self, clave: str) -> bool:
        letras_mayusculas = sum(1 for c in clave if c.isupper())
        return 'calisto' in clave.lower() and letras_mayusculas >= 2 and not clave.isupper()
    
    def es_valida(self, clave: str) -> bool:
        if not self._validar_longitud(clave):
            raise NoCumpleLongitudMinimaError
        if not self._contiene_numero(clave):
            raise NoTieneNumeroError
        if not self.contiene_calisto(clave):
            raise NoTienePalabraSecretaError
        return True
    

class Validador(ReglaValidacion):
    def __init__(self, regla: ReglaValidacion):
        self.regla = regla

    def es_valida(self, clave: str) -> bool:
        return self.regla.es_valida(clave)