
def ValidarDNI(dni):
    if len(str(dni)) != 9:
        raise Exception("El DNI debe tener 9 digitos")
    LETRAS_DNI = 'TRWAGMYFPDXBNJZSQVHLCKE'
    if dni[-1] == LETRAS_DNI[int(dni[0:-1]) % 23]:
        return True
    else:
        return False
    
