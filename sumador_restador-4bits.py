"""
Sumador y Restador de 4 bits
Implementación usando exclusivamente compuertas AND, OR y NOT
"""

# ============================================================================
# COMPUERTAS LÓGICAS BÁSICAS
# ============================================================================

def AND(a, b):
    """Compuerta AND: retorna 1 solo si ambos inputs son 1"""
    return 1 if (a == 1 and b == 1) else 0

def OR(a, b):
    """Compuerta OR: retorna 1 si al menos uno de los inputs es 1"""
    return 1 if (a == 1 or b == 1) else 0

def NOT(a):
    """Compuerta NOT: invierte el valor del input"""
    return 1 if a == 0 else 0


# ============================================================================
# COMPUERTAS DERIVADAS (construidas con AND, OR, NOT)
# ============================================================================

def XOR(a, b):
    """
    Compuerta XOR construida con AND, OR y NOT
    XOR = (A AND NOT B) OR (NOT A AND B)
    """
    return OR(AND(a, NOT(b)), AND(NOT(a), b))

def NAND(a, b):
    """Compuerta NAND: NOT(AND(a, b))"""
    return NOT(AND(a, b))


# ============================================================================
# SUMADOR COMPLETO (FULL ADDER)
# ============================================================================

def full_adder(a, b, cin):
    """
    Sumador completo de 1 bit
    Entradas: a, b (bits a sumar), cin (acarreo de entrada)
    Salidas: (suma, cout) donde cout es el acarreo de salida
    
    Suma = A XOR B XOR Cin
    Cout = (A AND B) OR (Cin AND (A XOR B))
    """
    # Calcular la suma
    sum_ab = XOR(a, b)
    sum_total = XOR(sum_ab, cin)
    
    # Calcular el acarreo de salida
    carry1 = AND(a, b)
    carry2 = AND(cin, sum_ab)
    cout = OR(carry1, carry2)
    
    return sum_total, cout


# ============================================================================
# SUMADOR DE 4 BITS
# ============================================================================

def sumador_4bits(A, B, cin=0):
    """
    Sumador de 4 bits usando encadenamiento de sumadores completos
    
    Entradas:
        A: lista de 4 bits [A3, A2, A1, A0] (de MSB a LSB)
        B: lista de 4 bits [B3, B2, B1, B0]
        cin: acarreo de entrada (por defecto 0)
    
    Salidas:
        S: lista de 4 bits con el resultado [S3, S2, S1, S0]
        cout: acarreo de salida (overflow)
    """
    S = [0, 0, 0, 0]
    
    # Sumador bit 0 (LSB)
    S[3], c1 = full_adder(A[3], B[3], cin)
    
    # Sumador bit 1
    S[2], c2 = full_adder(A[2], B[2], c1)
    
    # Sumador bit 2
    S[1], c3 = full_adder(A[1], B[1], c2)
    
    # Sumador bit 3 (MSB)
    S[0], cout = full_adder(A[0], B[0], c3)
    
    return S, cout


# ============================================================================
# COMPLEMENTO A 2 (para implementar la resta)
# ============================================================================

def complemento_a_1(A):
    """
    Calcula el complemento a 1 de un número de 4 bits
    Simplemente invierte todos los bits usando NOT
    """
    return [NOT(A[0]), NOT(A[1]), NOT(A[2]), NOT(A[3])]

def complemento_a_2(A):
    """
    Calcula el complemento a 2 de un número de 4 bits
    Complemento a 2 = Complemento a 1 + 1
    """
    comp1 = complemento_a_1(A)
    # Sumar 1 al complemento a 1
    uno = [0, 0, 0, 1]
    comp2, _ = sumador_4bits(comp1, uno)
    return comp2


# ============================================================================
# RESTADOR DE 4 BITS
# ============================================================================

def restador_4bits(A, B):
    """
    Restador de 4 bits: A - B
    Implementado como: A + complemento_a_2(B)
    
    Entradas:
        A: lista de 4 bits (minuendo)
        B: lista de 4 bits (sustraendo)
    
    Salidas:
        R: lista de 4 bits con el resultado
        borrow: indicador de préstamo (si es 0, hubo préstamo)
    """
    # Calcular complemento a 2 de B
    comp2_B = complemento_a_2(B)
    
    # Sumar A + complemento_a_2(B)
    R, cout = sumador_4bits(A, comp2_B)
    
    # El acarreo de salida indica si hubo préstamo
    # Si cout = 1, no hubo préstamo (resultado positivo)
    # Si cout = 0, hubo préstamo (resultado negativo en complemento a 2)
    
    return R, cout


# ============================================================================
# FUNCIONES AUXILIARES
# ============================================================================

def decimal_a_binario_4bits(n):
    """Convierte un número decimal (0-15) a binario de 4 bits"""
    if n < 0 or n > 15:
        raise ValueError("El número debe estar entre 0 y 15")
    
    binario = []
    for i in range(3, -1, -1):
        bit = (n >> i) & 1
        binario.append(bit)
    
    return binario

def binario_a_decimal(bits):
    """Convierte un número binario de 4 bits a decimal"""
    return bits[0]*8 + bits[1]*4 + bits[2]*2 + bits[3]*1

def binario_a_decimal_con_signo(bits):
    """
    Convierte un número binario de 4 bits con signo (complemento a 2) a decimal
    """
    if bits[0] == 1:  # Número negativo
        # Calcular complemento a 2 para obtener el valor absoluto
        comp1 = complemento_a_1(bits)
        valor_abs_bits, _ = sumador_4bits(comp1, [0, 0, 0, 1])
        valor_abs = binario_a_decimal(valor_abs_bits)
        return -valor_abs
    else:  # Número positivo
        return binario_a_decimal(bits)

def imprimir_bits(bits, etiqueta=""):
    """Imprime un número binario de forma legible"""
    bits_str = ''.join(map(str, bits))
    decimal = binario_a_decimal(bits)
    if etiqueta:
        print(f"{etiqueta}: {bits_str} (decimal: {decimal})")
    else:
        print(f"{bits_str} (decimal: {decimal})")


# ============================================================================
# PROGRAMA PRINCIPAL
# ============================================================================

def main():
    print("=" * 60)
    print("SUMADOR Y RESTADOR DE 4 BITS")
    print("Usando exclusivamente compuertas AND, OR y NOT")
    print("=" * 60)
    
    while True:
        print("\n" + "=" * 60)
        print("MENÚ PRINCIPAL")
        print("=" * 60)
        print("1. Suma de 4 bits")
        print("2. Resta de 4 bits")
        print("3. Salir")
        print("=" * 60)
        
        opcion = input("\nSeleccione una opción (1-3): ")
        
        if opcion == "3":
            print("\n¡Hasta luego!")
            break
        
        if opcion not in ["1", "2"]:
            print("Opción inválida. Intente nuevamente.")
            continue
        
        # Solicitar números
        print("\nIngrese números entre 0 y 15:")
        try:
            num1 = int(input("Primer número: "))
            num2 = int(input("Segundo número: "))
            
            if num1 < 0 or num1 > 15 or num2 < 0 or num2 > 15:
                print("Error: Los números deben estar entre 0 y 15")
                continue
            
            # Convertir a binario
            A = decimal_a_binario_4bits(num1)
            B = decimal_a_binario_4bits(num2)
            
            print("\n" + "-" * 60)
            print("REPRESENTACIÓN BINARIA:")
            print("-" * 60)
            imprimir_bits(A, f"A = {num1}")
            imprimir_bits(B, f"B = {num2}")
            
            if opcion == "1":
                # SUMA
                print("\n" + "-" * 60)
                print("OPERACIÓN: SUMA")
                print("-" * 60)
                S, cout = sumador_4bits(A, B)
                
                resultado_decimal = binario_a_decimal(S)
                
                print(f"\nA + B = {num1} + {num2}")
                imprimir_bits(S, "Resultado")
                print(f"Acarreo de salida (overflow): {cout}")
                
                if cout == 1:
                    print(f"\n⚠️  OVERFLOW: El resultado real es {resultado_decimal + 16}")
                    print(f"   (excede el rango de 4 bits: 0-15)")
                
            else:
                # RESTA
                print("\n" + "-" * 60)
                print("OPERACIÓN: RESTA")
                print("-" * 60)
                R, borrow = restador_4bits(A, B)
                
                print(f"\nA - B = {num1} - {num2}")
                imprimir_bits(R, "Resultado")
                print(f"Indicador de préstamo: {borrow}")
                
                if borrow == 1:
                    # Resultado positivo
                    resultado_decimal = binario_a_decimal(R)
                    print(f"\n✓ Resultado positivo: {resultado_decimal}")
                else:
                    # Resultado negativo (en complemento a 2)
                    resultado_decimal = binario_a_decimal_con_signo(R)
                    print(f"\n✓ Resultado negativo (en complemento a 2): {resultado_decimal}")
            
            # Mostrar tabla de verdad del proceso
            print("\n" + "-" * 60)
            print("PROCESO BIT POR BIT:")
            print("-" * 60)
            print("Bit | A | B | Resultado | Acarreo")
            print("-" * 40)
            
            if opcion == "1":
                c = 0
                for i in range(3, -1, -1):
                    s, c = full_adder(A[i], B[i], c)
                    print(f" {3-i}  | {A[i]} | {B[i]} |     {s}     |    {c}")
            
        except ValueError as e:
            print(f"Error: {e}")
            continue

if __name__ == "__main__":
    main()
