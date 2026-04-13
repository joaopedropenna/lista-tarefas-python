import sqlite3

# -- CRIAR O BANCO --
# Preferi usar SQLite porque é mais simples para um projeto sozinho.
conexao = sqlite3.connect('lista_tarefas.db')
cursor = conexao.cursor()

# -- Criando a tabela --
cursor.execute('''
    CREATE TABLE IF NOT EXISTS tarefas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        descricao TEXT,
        data_entrega TEXT,
        hora_entrega TEXT,
        prioridade TEXT,
        status TEXT DEFAULT 'Pendente'
    )
''')
conexao.commit()
print("Banco de dados criado.")

# --- ETAPA 1: FUNÇÃO PARA LISTAR TAREFAS ---
def listar_tarefas():
    print("\n--- Lista de Tarefas Atual ---")
    cursor.execute('SELECT id, titulo, hora_entrega, status FROM tarefas')
    tarefas = cursor.fetchall()

    if not tarefas:
        print("O seu Backlog está vazio.")
    else:
        for t in tarefas:
            print(f"ID: {t[0]} | Tarefa: {t[1]} | Hora: {t[2]} | Status: {t[3]}")

# --- ETAPA 2: FUNÇÃO PARA CADASTRAR ---
def cadastrar():
    
    listar_tarefas() 
    print("\n--- Cadastro de Nova Tarefa ---")
    titulo = input("Nome da tarefa: ")
    descricao = input("Descrição: ")
    data = input("Data (ex: 20/05): ")
    hora = input("Horas: (ex: 18:30) ")
    prioridade = input("Prioridade (Alta - Média - Baixa): ")
    cursor.execute('''
        INSERT INTO tarefas (titulo, descricao, data_entrega, hora_entrega, prioridade)
        VALUES (?, ?, ?, ?, ?)
    ''', (titulo, descricao, data, hora, prioridade))
    
    conexao.commit()
    print("Tarefa salva no banco!")

 # -- ETAPA 3: FUNÇÃO PARA CONCLUIR TAREFA ---
def marcar_concluida():
    print("\n--- Marcar como Concluída ---")
    id_tarefa = input("Digite o ID da tarefa que deseja finalizar: ")
    
    cursor.execute('''
        UPDATE tarefas 
        SET status = 'Concluída' 
        WHERE id = ?
    ''', (id_tarefa,))
    conexao.commit()
    print(f" Tarefa {id_tarefa} foi marcada como concluída.")

 # -- ETAPA 4: EDITAR TAREFA ---
def editar_tarefa():
    listar_tarefas()
    id_tarefa = input("\nDigite o ID da tarefa que deseja editar: ")
    novo_titulo = input("Novo Título (deixe vazio para não alterar): ")
    nova_prioridade = input("Nova Prioridade (deixe vazio para não alterar): ")

    if novo_titulo:
        cursor.execute('UPDATE tarefas SET titulo = ? WHERE id = ?', (novo_titulo, id_tarefa))
    if nova_prioridade:
        cursor.execute('UPDATE tarefas SET prioridade = ? WHERE id = ?', (nova_prioridade, id_tarefa))
    
    conexao.commit()
    print(f"Tarefa {id_tarefa} atualizada com sucesso!")

# --- ETAPA 5: EXCLUIR TAREFA ---
def excluir_tarefa():
    listar_tarefas()
    id_tarefa = input("\nDigite o ID da tarefa que deseja EXCLUIR: ")
    confirmar = input(f"Tem certeza que deseja excluir a tarefa {id_tarefa}? (s/n): ")

    if confirmar.lower() == 's':
        cursor.execute('DELETE FROM tarefas WHERE id = ?', (id_tarefa,))
        conexao.commit()
        print("Tarefa excluída com sucesso!")
    else:
        print("Operação cancelada.")
# -- MENU --
def menu():
    while True:
        print("\n--- Painel de Atividades ---")
        print("1. Ver tarefas")
        print("2. Nova tarefa")
        print("3. Concluir tarefa")
        print("4. Excluir tarefa")
        print("0. Sair")
        
        opcao = input("\nO que deseja fazer? ")

        if opcao == '1':
            listar_tarefas()
        elif opcao == '2':
            cadastrar()
        elif opcao == '3':
            marcar_concluida()
        elif opcao == '4':
            excluir_tarefa()
        elif opcao == '0':
            print("Encerrando...")
            break
        else:
            print("Opção inválida!")
   
# # --- PONTO DE ENTRADA DO SISTEMA ---

if __name__ == "__main__":
    menu()
    conexao.close()
    print("Conexão encerrada. Até breve.")