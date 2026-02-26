def potencia(base, potencia):
    return base ** potencia

def potencia_superior(potencia):
    def aux(base):
        return base ** potencia
    return aux

elevar_al_cuadrado = potencia_superior(2)
print(elevar_al_cuadrado(5))
print(potencia_superior(3)(6))
