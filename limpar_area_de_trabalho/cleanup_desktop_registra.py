import os
import time
import shutil  # Para lidar com pastas

# Caminhos possíveis para a área de trabalho
possible_paths = [
    os.path.join(os.path.expanduser("~"), "OneDrive", "Área de Trabalho"),  # OneDrive
    os.path.join(os.path.expanduser("~"), "Desktop"),  # Desktop padrão
]

# Caminho relativo para o arquivo de log (assumindo que está no mesmo diretório que o script)
log_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lixeira.txt")

# Tempo limite em segundos (1 hora)
time_limit = 1 * 3600

# Tempo atual
now = time.time()

# Função para verificar se a área de trabalho existe em qualquer um dos caminhos
desktop_path = None
for path in possible_paths:
    if os.path.exists(path):
        desktop_path = path
        break

if desktop_path is None:
    print(f"Erro: Nenhum dos caminhos possíveis para a Área de Trabalho foi encontrado.")
else:
    print(f"Caminho encontrado para a Área de Trabalho: {desktop_path}")

    # Verifica se o diretório do log existe
    log_dir = os.path.dirname(log_file_path)
    if not os.path.exists(log_dir):
        print(f"Erro: O diretório do arquivo de log não existe: {log_dir}")
    else:
        # Abre o arquivo de log no modo de adição (append)
        try:
            with open(log_file_path, "a") as log_file:
                # Verifica cada item na área de trabalho
                for item_name in os.listdir(desktop_path):
                    item_path = os.path.join(desktop_path, item_name)

                    # Verifica se o item é um arquivo ou uma pasta
                    if (os.path.isfile(item_path) or os.path.isdir(item_path)) and not item_name.endswith('.lnk'):
                        # Verifica a data de modificação do item
                        item_mod_time = os.path.getmtime(item_path)

                        # Se o item tem mais de 1 hora, exclui
                        if now - item_mod_time > time_limit:
                            try:
                                # Registra informações no log
                                if os.path.isfile(item_path):
                                    item_size = os.path.getsize(item_path)
                                    log_entry = f"Arquivo: {item_name} | Caminho: {item_path} | Tamanho: {item_size} bytes | Removido em: {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
                                else:  # Se for uma pasta
                                    log_entry = f"Pasta: {item_name} | Caminho: {item_path} | Removido em: {time.strftime('%Y-%m-%d %H:%M:%S')}\n"

                                log_file.write(log_entry)

                                # Remove o item (arquivo ou pasta)
                                if os.path.isfile(item_path):
                                    os.remove(item_path)
                                else:
                                    shutil.rmtree(item_path)  # Remove a pasta e seu conteúdo

                                print(f"{item_name} excluído.")
                            except Exception as e:
                                print(f"Erro ao excluir {item_name}: {e}")
        except Exception as e:
            print(f"Erro ao abrir o arquivo de log para escrita: {e}")
