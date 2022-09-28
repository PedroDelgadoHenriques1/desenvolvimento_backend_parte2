
# VAE Dogs

## Atividades executadas:
- Leitura do capítulo sobre Variotional AutoEncoders
- Análise do problema
- Análise do código do Variotional AutoEncoder da documentação do Keras
    - Execução do código no Colab correspondente (estimativa de 52 minutos de treinamento) com o exemplo do dataset do MNIST Digits
- Estimativa de que só para rodar o treinamento desse conjunto no meu notebook demoraria bastante (sendo que o do MNIST que é bem menor e no próprio ambiente do Google Colab já demoraria quase 1 hora)
- Download dos dados do Kaggle + tentativa de rodar alguns dos códigos com modelos pré-treinados (sem sucesso) (e instalação das dependências)

### Variational AutoEncoders
Eu já havia estudado um pouco sobre os AutoEncoders (AE) mas sem aplicar nada prático. Sua variante Variotinal (VAE) já havia ouvido falar mas só fui entender (conceitualmente, em alto nível) com a leitura do capítulo indicado no desafio. Eu entendi que o VAE armazena uma distribuição de probabilidade (através da média e desvio padrão, uma distribuição normal) para a representação do dado no espaço latente, ao contrário do AE original que armazena diretamente uma representação. Dessa forma, no processo de decodificação é incluída uma etapa extra, onde é necessário realizar uma amostragem da distribuição (dentro do espaço latente) para realizar a reconstrução. Como há essa variação o erro decodificação-codificação será maior (pois há o componente aleatório) porém isso, junto com outras operações de regularização, garantem que as amostras se mantenham dentro de um determinado range, sem criar dados irrelevantes que não representam o conjunto de entrada.

### Proposta do desafio
Pelo o que eu entendi, a ideia para o desafio seria construir um VAE, semelhante ao do exemplo do MNIST da documentação, com o conjunto de dados das raças dos cachorros. Dessa forma, o VAE aprenderia a representar imagens de cachorros em um espaço dimensional menor (o chamado espaço latente). Sua característica Variotional permitiria, teoricamente, que qualquer sample obtida do espaço latente fosse uma representação "válida" de um possível cachorro, pois após todo o treinamento de todo o conjunto de dados, a rede aprendeu como lidar com a representação de diferentes cachorros. Ou seja, o output do decodificador do VAE para qualquer amostra obtida no espaço latente representaria o que o VAE "entendeu como um cachorro", com um range de variação entre todas as raças aprendidas, podendo gerar "raças novas e intermediárias" que estariam entre as outras 120 possíveis raças já treinadas, podendo variar graças à amostragem aleatória da distribuição normal.

### Análise sobre o viralata caramelo e o pythinho
Em relação às questões em relação a raça do viralata caramelo e o pythinho não tenho certeza se entendi como o VAE se encaixaria na situação. Um modelo de aprendizado supervisionado padrão aprenderia quais características classificam cada cachorro em uma das 120 raças, então se as imagens dos dois fossem passadas como input para um modelo já treinado ele responderia com a raça mais próxima (que tem as features mais parecidas). Dessa forma, obtendo um top-k seria possível descobrir quais são as raças mais parecidas com os dois e o QUÃO parecidas são ou não com essas k raças.

Agora, descobrir qual a miscigenação que gerou o viralata caramelo seria um problema completamente diferente e mais complexo, dependendo de combinatória (quantas raças diferentes envolvidas? quais?) e da biologia (quais características são herdadas dos ancestrais? como é o processo de mistura? (qual porcentagem/características são herdadas de cada ancestral)). Enfim, computacionalmente teria que ser definido um critério para simplicar o problema (exemplo: definir que o viralata caramelo é uma mistura das 4 raças que o VAE classificou como tendo as features mais próximas).