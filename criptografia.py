# ===== Definição das Cores ANSI ===============================================================================================================
class Cores:
    RESET = '\033[0m'
    VERMELHO = '\033[91m'
    VERDE = '\033[92m'
    AMARELO = '\033[93m'
    AZUL = '\033[94m'
    MAGENTA = '\033[95m'
    CIANO = '\033[96m'
    NEGRITO = '\033[1m'

# ===== Utilitários ============================================================================================================================
def euclides_extendido(a: int, b: int) -> tuple[int, int, int]:
    if a == 0:                                                      
        return (b, 0, 1)

    mdc, x1, y1 = euclides_extendido(b % a, a)                      
    x = y1 - (b // a) * x1                                          
    y = x1                                                          
    return (mdc, x, y) # ax + by = mdc(a, b)                                             

def inverso_modular(a: int, m: int) -> int:
    mdc, x, _ = euclides_extendido(a, m)                            
    if mdc != 1:                                                    
        raise ValueError(f"{Cores.VERMELHO}O inverso modular não existe!{Cores.RESET}")
    return x % m # [0, m-1]                                                

def checagem_de_primos(n: int) -> bool:
    if n == 0:
        return False
    if n == 1:
        return False
    if n == 2:
        return True
    for i in range(2, n):
        if i * i > n:
            return True
        if n % i == 0:
            return False

def exp_modular_rapida(base: int, expoente: int, modulo: int) -> int:
    resultado = 1
    base = base % modulo

    while expoente > 0:
        if expoente % 2 == 1: # Se é impar, o último digito binário é 1         
            resultado = (resultado * base) % modulo 
        expoente = expoente // 2 # >>       
        base = (base * base) % modulo

    return resultado


# ===== Conversão texto ↔ números ==================================================================================================================

# {A = 2, ' ' = 28}
def texto_para_numeros(mensagem: str) -> list[int]:
    numeros = []
    for char in mensagem:
        if (char == ' '):
            numeros.append(28)
        elif "A" <= char <= "Z":
            numeros.append(ord(char) - 63) # Ex.: Código ASCII (A) = 65 --> 65 - 63 = [2]                                                                                        
        else:
            print(f"{Cores.VERMELHO}Caracter inválido na mensagem. Use apenas A-Z e espaço.{Cores.RESET}")
            continue
    return numeros


def numeros_para_texto(numeros: list[int]) -> str:
    mensagem = ""
    for num in numeros:
        if num == 28:
            mensagem += " "
        elif 2 <= num <= 27:
            mensagem += chr(num + 63)   # Inverso de ord(char) - 63
        else:
            print(f"{Cores.VERMELHO}Número inválido ({num}). Use apenas valores entre 2 e 28.{Cores.RESET}")
            continue
    return mensagem


# ===== Chave pública ================================================================================================================================
def gerar_chave_publica() -> tuple[int, int]:
    _, _, e, n, _ = ler_p_q_e()
    chave_publica = (n, e)
    with open("chave_publica.txt", "w", encoding="utf-8") as file:
        file.write(f"{n} {e}")

    print(f"\n{Cores.VERDE}Chave pública gerada com sucesso!{Cores.RESET}")
    print(f"O arquivo {Cores.CIANO}'chave_publica.txt'{Cores.RESET} foi criado no diretório atual.\n")

    return chave_publica


# ===== Criptografia e Descriptografia ==============================================================================================================
def criptografar() -> None:
    mensagem = input(f"{Cores.AMARELO}Digite a mensagem a ser criptografada: {Cores.RESET}").upper()
    chave_publica = input(f"{Cores.AMARELO}Digite a chave pública (n e e separados por espaço): {Cores.RESET}")
    n, e = map(int, chave_publica.split())

    numeros_mensagem = texto_para_numeros(mensagem)

    # Criptografar cada número: C = M^e mod n
    mensagem_criptografada = [exp_modular_rapida(M, e, n) for M in numeros_mensagem] 
    with open("mensagem_criptografada.txt", "w", encoding="utf-8") as file:
        file.write(f"{' '.join(map(str, mensagem_criptografada))}")

    print(f"\n{Cores.VERDE}Mensagem criptografada com sucesso!{Cores.RESET}\n\"{Cores.CIANO}{' '.join(map(str, mensagem_criptografada))}{Cores.RESET}\"")
    print(f"O arquivo {Cores.CIANO}'mensagem_criptografada.txt'{Cores.RESET} foi criado no diretório atual.\n")


def descriptografar() -> None:
    criptografia = input(f"{Cores.AMARELO}Digite a mensagem a ser descriptografada: {Cores.RESET}")
    _, _, e, n, phi = ler_p_q_e()
    d = inverso_modular(e, phi)
    try:
        numeros_alf = [int(x) for x in criptografia.split()]
    except ValueError:
        print(f"{Cores.VERMELHO}Formato inválido. Digite somente números inteiros separados por espaço.{Cores.RESET}")
        return

    # Descriptografar cada número: M = C^d mod n
    numeros_decifrados = [exp_modular_rapida(C, d, n) for C in numeros_alf]

    # Agora temos os numeros e vamos converter para texto
    mensagem = numeros_para_texto(numeros_decifrados)
    with open("mensagem_descriptografada.txt", "w", encoding="utf-8") as file:
        file.write(f"{mensagem}")

    print(f"\n{Cores.VERDE}Mensagem descriptografada com sucesso!{Cores.RESET}\n\"{Cores.CIANO}{mensagem}{Cores.RESET}\"")
    print(f"O arquivo {Cores.CIANO}'mensagem_descriptografada.txt'{Cores.RESET} foi criado no diretório atual.\n")


# ===== Leitura de p, q e e ====================================================================================================================
def ler_p_q_e() -> tuple[int, int, int, int, int]:
    
    while True:
        try:
            p = int(input(f"{Cores.AMARELO}Digite um número primo p: {Cores.RESET}"))
            if checagem_de_primos(p) == False:
                print(f"{Cores.VERMELHO}Número inválido. Digite um número primo.{Cores.RESET}")
            else:
                break
        except ValueError:
            print(f"{Cores.VERMELHO}Número inválido. Digite um número inteiro.{Cores.RESET}")
            continue

    while True:
        try:
            q = int(input(f"{Cores.AMARELO}Digite um número primo q: {Cores.RESET}"))
            if checagem_de_primos(q) == False:
                print(f"{Cores.VERMELHO}Número inválido. Digite um número primo.{Cores.RESET}")
            elif q == p:
                print(f"{Cores.VERMELHO}Número inválido. O número q deve ser diferente de p.{Cores.RESET}")
            elif p * q <= 28:
                print(f"{Cores.VERMELHO}Número inválido. A multiplicação de p*q deve ser maior que 28{Cores.RESET}")
            else:
                break
        except ValueError:
            print(f"{Cores.VERMELHO}Número inválido. Digite um número inteiro.{Cores.RESET}")
            continue

    n = p * q
    phi = (p - 1) * (q - 1)

    # Gerar candidatos a e
    candidatos = []
    for possivel_e in range(2, phi):
        mdc, _, _ = euclides_extendido(phi, possivel_e)
        if mdc == 1:
            candidatos.append(possivel_e)
        if len(candidatos) == 3:
            break

    print(f"\n{Cores.CIANO}Sugestões de expoentes possíveis (coprimos de {phi}): {candidatos[0]} , {candidatos[1]} e {candidatos[2]}{Cores.RESET}\n")

    while True:
        try:
            e = int(input(f"{Cores.AMARELO}Digite um expoente (relativamente primo a (p-1)(q-1), ou seja, coprimo de {phi}): {Cores.RESET}")) 
        except ValueError:
            print(f"{Cores.VERMELHO}Entrada inválida. Digite um número inteiro.{Cores.RESET}")
            continue
        if not (1 < e < phi):
            print(f"{Cores.VERMELHO}O número precisa estar entre 1 e {phi}.{Cores.RESET}")
            continue
        mdc, _, _ = euclides_extendido(e, phi)

        if mdc == 1:
            return(p, q, e, n, phi)
        else:
            print(f"{Cores.VERMELHO}O número não é relativamente primo. Digite um número primo.{Cores.RESET}") 


def main() -> None:
    while True:
        print(f"{Cores.NEGRITO}{Cores.MAGENTA}===== Projeto de Criptografia RSA ====={Cores.RESET}\n")
        print(f"{Cores.AZUL}1 - Gerar chave pública{Cores.RESET}")
        print(f"{Cores.AZUL}2 - Criptografar{Cores.RESET}")
        print(f"{Cores.AZUL}3 - Descriptografar{Cores.RESET}")
        print(f"{Cores.AZUL}4 - Sair{Cores.RESET}\n")

        escolha = input(f"{Cores.NEGRITO}{Cores.AMARELO}Opção: {Cores.RESET}").strip()

        if escolha == '1':
            gerar_chave_publica()
        elif escolha == '2':
            criptografar()
        elif escolha == '3':
            descriptografar()
        elif escolha == '4':
            print(f"{Cores.CIANO}Saindo do programa...{Cores.RESET}")
            break
        else:
            print(f"{Cores.VERMELHO}Opção inválida. Escolha um número de 1 a 4.{Cores.RESET}")

if __name__ == "__main__":
    main()

'''
Mapeamento de caracteres para números:

A: 2, B: 3, C: 4, D: 5, E: 6, F: 7, 
G: 8, H: 9, I: 10, J: 11, K: 12, 
L: 13, M: 14, N: 15, O: 16, P: 17, 
Q: 18, R: 19, S: 20, T: 21, U: 22, 
V: 23, W: 24, X: 25, Y: 26, Z: 27, 
' ': 28

Exemplo: "AB C" -> [2, 3, 28, 4]
'''