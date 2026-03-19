def get_next_matricula_num(alunos, curso):
    numeros = []
    for aluno in alunos:
        if aluno['curso'] == curso:
            # Extrai a parte numérica após a sigla do curso
            num_str = aluno['matricula'][len(curso):]
            if num_str.isdigit():
                numeros.append(int(num_str))
    return max(numeros) + 1 if numeros else 1


def criar_aluno(alunos):
    nome = input("Nome: ").strip()
    email = input("Email: ").strip()
    curso = input("Curso (GES, GEC, GET, GEP): ").strip().upper()
    cursos_validos = ['GES', 'GEC', 'GET', 'GEP']

    if curso not in cursos_validos:
        print("Curso inválido. Use um dos: GES, GEC, GET, GEP.")
        return

    proximo_num = get_next_matricula_num(alunos, curso)
    matricula = curso + str(proximo_num)

    aluno = {
        'nome': nome,
        'email': email,
        'curso': curso,
        'matricula': matricula
    }
    alunos.append(aluno)
    print(f"Aluno criado com matrícula {matricula}")


def listar_alunos(alunos):
    if not alunos:
        print("Nenhum aluno cadastrado.")
        return

    print("\n--- Lista de Alunos ---")
    for aluno in alunos:
        print(f"{aluno['matricula']}: {aluno['nome']} - {aluno['email']} - {aluno['curso']}")


def buscar_matricula(alunos, matricula):
    for aluno in alunos:
        if aluno['matricula'] == matricula:
            return aluno
    return None


def atualizar_aluno(alunos):
    matricula = input("Digite a matrícula do aluno a ser atualizado: ").strip()
    aluno = buscar_matricula(alunos, matricula)

    if not aluno:
        print("Aluno não encontrado.")
        return

    print("Deixe em branco para manter o valor atual.")
    novo_nome = input(f"Nome ({aluno['nome']}): ").strip()
    if novo_nome:
        aluno['nome'] = novo_nome

    novo_email = input(f"Email ({aluno['email']}): ").strip()
    if novo_email:
        aluno['email'] = novo_email

    print("Aluno atualizado com sucesso.")


def excluir_aluno(alunos):
    matricula = input("Digite a matrícula do aluno a ser excluído: ").strip()
    aluno = buscar_matricula(alunos, matricula)

    if not aluno:
        print("Aluno não encontrado.")
        return

    alunos.remove(aluno)
    print("Aluno excluído com sucesso.")


def main():
    alunos = []  # Lista que armazena alunos

    while True:
        print()  # Linha em branco para melhor formatação
        print("\n===== Menu =====")
        print("1. Criar aluno")
        print("2. Listar alunos")
        print("3. Atualizar aluno")
        print("4. Excluir aluno")
        print("5. Sair")
        opcao = input("Escolha uma opção:").strip()
        print()  # Linha em branco para melhor formatação

        if opcao == '1':
            criar_aluno(alunos)
        elif opcao == '2':
            listar_alunos(alunos)
        elif opcao == '3':
            atualizar_aluno(alunos)
        elif opcao == '4':
            excluir_aluno(alunos)
        elif opcao == '5':
            print("Encerrando programa...")
            break
        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    main()