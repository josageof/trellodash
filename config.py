# %% Trello configs

current_storage_file = "data/current.pkl"
history_storage_file = "data/history.pkl"
processed_storage_file = "data/processed.pkl"


## Considering the kanban diagram (todo, doing, done), insert
## keywords that can differentiate the lists by the headers
stage_list = {"todo": "|".join(['a fazer', 'revisar', 'vencida']),
                  "doing": "|".join(['backlog', 'andamento', 'preparação']),
                  "done": "|".join(['concluído', 'concluido', 'calibrado'])}


## Use keywords to identify different lists for different types of tasks
task_type = ['Atividades',
              'Calibração',
              'Manutenção',
              'Documentos',
              'Treinamento']
