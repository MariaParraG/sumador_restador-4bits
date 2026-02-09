# Sumador y Restador de 4 Bits en Python

##  Descripción

Este programa emula un **sumador** y **restador de 4 bits** para números binarios, implementado exclusivamente con compuertas lógicas básicas: **AND**, **OR** y **NOT**. Es una simulación de cómo funcionan los circuitos digitales a nivel de hardware.

##  Objetivo

Demostrar cómo se construyen operaciones aritméticas binarias desde los componentes más básicos de la lógica digital, sin usar operadores aritméticos de Python (+, -), sino únicamente compuertas lógicas.

---

##  Compuertas Lógicas Básicas

### 1. **AND** (Y)
```
A | B | Salida
--|---|-------
0 | 0 |   0
0 | 1 |   0
1 | 0 |   0
1 | 1 |   1
```
Retorna 1 solo si **ambas** entradas son 1.

### 2. **OR** (O)
```
A | B | Salida
--|---|-------
0 | 0 |   0
0 | 1 |   1
1 | 0 |   1
1 | 1 |   1
```
Retorna 1 si **al menos una** entrada es 1.

### 3. **NOT** (NO)
```
A | Salida
--|-------
0 |   1
1 |   0
```
Invierte el valor de entrada.

### 4. **XOR** (O Exclusivo) - Construida
```
A | B | Salida
--|---|-------
0 | 0 |   0
0 | 1 |   1
1 | 0 |   1
1 | 1 |   0
```
**Construcción:** `XOR(A,B) = (A AND NOT B) OR (NOT A AND B)`

Retorna 1 solo si **una y solo una** entrada es 1.

---

##  Componentes del Sistema

### 1. Full Adder (Sumador Completo)

El **sumador completo** es el bloque fundamental. Suma tres bits: dos bits de entrada (A, B) y un acarreo de entrada (Cin).

**Entradas:**
- `A`: primer bit
- `B`: segundo bit  
- `Cin`: acarreo de entrada (carry in)

**Salidas:**
- `S`: suma (resultado)
- `Cout`: acarreo de salida (carry out)

**Ecuaciones lógicas:**
```
S = A XOR B XOR Cin
Cout = (A AND B) OR (Cin AND (A XOR B))
```

**Ejemplo:**
```
A=1, B=1, Cin=1
  1
+ 1
+ 1 (acarreo)
---
= 11 (en binario) → S=1, Cout=1
```

**Tabla de verdad:**
```
A | B | Cin | S | Cout
--|---|-----|---|-----
0 | 0 |  0  | 0 |  0
0 | 0 |  1  | 1 |  0
0 | 1 |  0  | 1 |  0
0 | 1 |  1  | 0 |  1
1 | 0 |  0  | 1 |  0
1 | 0 |  1  | 0 |  1
1 | 1 |  0  | 0 |  1
1 | 1 |  1  | 1 |  1
```

---

### 2. Sumador de 4 Bits (Ripple Carry Adder)

Encadena **4 sumadores completos** donde el acarreo de salida de uno se conecta al acarreo de entrada del siguiente.

**Representación:**
```
A = [A3, A2, A1, A0]  (MSB a LSB)
B = [B3, B2, B1, B0]
      ↓   ↓   ↓   ↓
    [FA][FA][FA][FA]
      ↓   ↓   ↓   ↓
S = [S3, S2, S1, S0]
```

**Proceso:**
1. Bit 0 (LSB): `S0, C1 = FullAdder(A0, B0, 0)`
2. Bit 1: `S1, C2 = FullAdder(A1, B1, C1)`
3. Bit 2: `S2, C3 = FullAdder(A2, B2, C2)`
4. Bit 3 (MSB): `S3, Cout = FullAdder(A3, B3, C3)`

**Ejemplo: 5 + 3**
```
    0101  (5)
  + 0011  (3)
  ------
    1000  (8)
    
Bit por bit:
Bit 0: 1+1+0 = 0, Cout=1
Bit 1: 0+1+1 = 0, Cout=1
Bit 2: 1+0+1 = 0, Cout=1
Bit 3: 0+0+1 = 1, Cout=0
```

**Overflow:**
Si `Cout = 1`, significa que el resultado excede 4 bits (mayor que 15).

---

### 3. Complemento a 2

Para realizar restas, convertimos el problema en una suma usando el **complemento a 2**.

**Complemento a 1:**
Invierte todos los bits usando NOT.
```
Ejemplo: 0101
Comp a 1: 1010
```

**Complemento a 2:**
Complemento a 1 + 1
```
Ejemplo: 0101
Comp a 1: 1010
      +1: 0001
-----------
Comp a 2: 1011
```

**Interpretación:**
En complemento a 2 con 4 bits:
- Si el bit más significativo (MSB) es 0 → número positivo
- Si el MSB es 1 → número negativo

**Rango:** -8 a +7 para 4 bits con signo

---

### 4. Restador de 4 Bits

Implementa la resta como: **A - B = A + complemento_a_2(B)**

**Proceso:**
1. Calcular complemento a 2 de B
2. Sumar A + complemento_a_2(B) usando el sumador de 4 bits
3. El acarreo final indica el signo:
   - `Cout = 1`: resultado positivo o cero
   - `Cout = 0`: resultado negativo (en complemento a 2)

**Ejemplo 1: 7 - 3 = 4**
```
A = 0111 (7)
B = 0011 (3)

Comp a 2 de B:
  0011 → 1100 (comp a 1) → 1101 (comp a 2)

Suma:
    0111
  + 1101
  ------
  1 0100  (Cout=1, Resultado=0100=4)
  
Cout=1 → resultado positivo: 4
```

**Ejemplo 2: 3 - 7 = -4**
```
A = 0011 (3)
B = 0111 (7)

Comp a 2 de B:
  0111 → 1000 (comp a 1) → 1001 (comp a 2)

Suma:
    0011
  + 1001
  ------
  0 1100  (Cout=0, Resultado=1100)
  
Cout=0 → resultado negativo
1100 en comp a 2 = -4
```

---

##  Uso del Programa

### Requisitos
- Python 3.x

### Ejecución
```bash
python sumador_restador_4bits.py
```

### Menú Interactivo
```
============================================================
MENÚ PRINCIPAL
============================================================
1. Suma de 4 bits
2. Resta de 4 bits
3. Salir
============================================================
```

### Ejemplo de Suma
```
Seleccione una opción (1-3): 1

Ingrese números entre 0 y 15:
Primer número: 12
Segundo número: 5

------------------------------------------------------------
REPRESENTACIÓN BINARIA:
------------------------------------------------------------
A = 12: 1100 (decimal: 12)
B = 5: 0101 (decimal: 5)

------------------------------------------------------------
OPERACIÓN: SUMA
------------------------------------------------------------

A + B = 12 + 5
Resultado: 0001 (decimal: 1)
Acarreo de salida (overflow): 1

  OVERFLOW: El resultado real es 17
   (excede el rango de 4 bits: 0-15)
```

### Ejemplo de Resta
```
Seleccione una opción (1-3): 2

Ingrese números entre 0 y 15:
Primer número: 8
Segundo número: 3

------------------------------------------------------------
REPRESENTACIÓN BINARIA:
------------------------------------------------------------
A = 8: 1000 (decimal: 8)
B = 3: 0011 (decimal: 3)

------------------------------------------------------------
OPERACIÓN: RESTA
------------------------------------------------------------

A - B = 8 - 3
Resultado: 0101 (decimal: 5)
Indicador de préstamo: 1

✓ Resultado positivo: 5
```

---

##  Conceptos Clave

### Números Binarios de 4 Bits

**Sin signo (0-15):**
```
0000 = 0    1000 = 8
0001 = 1    1001 = 9
0010 = 2    1010 = 10
0011 = 3    1011 = 11
0100 = 4    1100 = 12
0101 = 5    1101 = 13
0110 = 6    1110 = 14
0111 = 7    1111 = 15
```

**Con signo en complemento a 2 (-8 a 7):**
```
0000 = 0     1000 = -8
0001 = 1     1001 = -7
0010 = 2     1010 = -6
0011 = 3     1011 = -5
0100 = 4     1100 = -4
0101 = 5     1101 = -3
0110 = 6     1110 = -2
0111 = 7     1111 = -1
```

### Acarreo (Carry)
El bit adicional que se genera cuando la suma de dos bits excede 1.
```
  1 1 0   (acarreos)
    1 1 0
  + 0 1 1
  -------
    1 0 0 1
```

### Overflow
Ocurre cuando el resultado de una operación no puede representarse con el número de bits disponible.

**En suma de 4 bits sin signo:**
- Si Cout = 1, hubo overflow (resultado > 15)

---

##  Pruebas Recomendadas

### Sumas
1. `5 + 3 = 8` (sin overflow)
2. `12 + 5 = 17` (con overflow)
3. `15 + 15 = 30` (con overflow)
4. `0 + 0 = 0` (caso límite)

### Restas
1. `8 - 3 = 5` (resultado positivo)
2. `3 - 8 = -5` (resultado negativo)
3. `7 - 7 = 0` (resultado cero)
4. `0 - 5 = -5` (resultado negativo)

---

##  Aplicaciones Educativas

Este programa es útil para:

1. **Entender circuitos digitales:** Cómo se construyen sumadores en hardware
2. **Lógica digital:** Construcción de funciones complejas con compuertas simples
3. **Aritmética binaria:** Suma, resta y complemento a 2
4. **Arquitectura de computadores:** Base de la ALU (Unidad Aritmético-Lógica)
5. **Propagación de acarreo:** Concepto de ripple carry adder

---

##  Estructura del Código

```
sumador_restador_4bits.py
│
├── Compuertas básicas
│   ├── AND(a, b)
│   ├── OR(a, b)
│   └── NOT(a)
│
├── Compuertas derivadas
│   ├── XOR(a, b)
│   └── NAND(a, b)
│
├── Bloques funcionales
│   ├── full_adder(a, b, cin)
│   ├── sumador_4bits(A, B, cin)
│   ├── complemento_a_1(A)
│   ├── complemento_a_2(A)
│   └── restador_4bits(A, B)
│
├── Funciones auxiliares
│   ├── decimal_a_binario_4bits(n)
│   ├── binario_a_decimal(bits)
│   ├── binario_a_decimal_con_signo(bits)
│   └── imprimir_bits(bits, etiqueta)
│
└── main()
    └── Interfaz interactiva
```

---

##  Mejoras Futuras

- Implementar sumador de 8, 16 o 32 bits
- Agregar multiplicación y división binaria
- Implementar carry lookahead adder (más rápido)
- Visualización gráfica de compuertas
- Animación del flujo de datos
- Exportar circuito a formato HDL (Verilog/VHDL)

---

##  Referencias

- **Lógica Digital:** Fundamentos de diseño de circuitos digitales
- **Complemento a 2:** Representación de números negativos en binario
- **Full Adder:** Componente básico de la ALU
- **Ripple Carry Adder:** Sumador con propagación de acarreo

---

##  Autor

María Parra
