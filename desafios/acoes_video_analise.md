
# Reconhecimento de Ações em Vídeo

## Atividades executadas:
- Leitura do github do Mediapipe e Openpose
- Leitura do Mediapipe Holistic
    - Inclusive o exemplo de código, entendendo sua estrutura básica para marcação das landmarks
- Análise do problema
- Pesquisa por reconhecimento de ações em vídeo
    - Encontrado no site PapersWithCode a tarefa e juntamente associada a ela diversas propostas de solução, com comparativos entre abordagens diferentes, descritas nos papers e divulgadas com código aberto
    - Leitura sobre um dos maiores datasets que lidam com essa problemática: Kinetics-600, que contém cerca de 500k de vídeos com 600 classes de ações diferentes como labels e, no mínimo, 600 amostras de cada classe
    - Leitura "skimming" do artigo que descreve a solução atualmente nº 1 de acordo com o site: MerlotReserve. Nesse trabalho eles usaram uma quantidade imensa de vídeos (20 milhões) para treinar uma rede neural com capacidade de resolver o problema de identificação dos conteúdos dos vídeos, utilizando diferentes datasets (o Kinetics incluso). Para isso eles usam, além das informações das imagens, informações textuais e o áudio do vídeo!

### Análise do desafio
Se entendi bem o problema e a solução esperada por vocês nesse caso seria o seguinte:
- Encontrar um dataset na web que possua os vídeos e as ações, selecionando 20 ações (para reduzir o tamanho do problema, facilitando o treinamento). Nesse caso poderia selecionar então 20 categorias das 600 disponíveis no Kinetics-600
- Processar os vídeos utilizando o Mediapipe Holistic, para incluir como features, além das imagens em si, as landmarks correspondentes das poses, para auxiliar na identificação da ação (como um processo de Feature Engineering)
- Com as imagens já anotadas com as landamarks das poses a partir do Holistic, treinar o modelo com todas as features

### Requisitos adicionais
- O requisito do reconhecimento por webcam não entendi se seria a utilização de alguma biblioteca que acesse a webcam do computador que está executando o código ou simplesmente para deixar claro que poderiam ser colocadas quaisquer novas amostras para o teste
- O desafio bônus para a predição em tempo real envolve a utilização de um algoritmo de baixa latência, com talvez até um pouco menos de acurácia, mas que seja rápido (já que esse é um trade-off comum em aprendizado de máquina, ainda mais para tarefas complexas como visão computacional ou natural language understanding)