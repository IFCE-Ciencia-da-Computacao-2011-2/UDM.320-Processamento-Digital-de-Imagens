# PILL - Trabalho Processamento Digital de Imagem - Pílulas

## Índice

 * **[0. Trabalho.ipynb](0. Trabalho.ipynb)** - Descrição do trabalho
 * **[1. Informações gerais do banco de imagens.ipynb](1. Informações gerais do banco de imagens.ipynb)**
   * 1.1 Todas as imagens possuem o mesmo tamanho?
   * 1.2 O cinza de fundo de todas as imagens é a mesma cor?
   * 1.3 O quanto de cinza cada imagem possui?
   * 1.4 Existe uma área em comum para todas as pílulas?
 * **[2. Análise de histograma das imagens.ipynb](2. Análise de histograma das imagens.ipynb)** (esboço)
   * 2.1 Análise do ruido do cinza
   * 2.2 Comparador de histograma
 * **[3. Separador de pílulas pelo formato.ipynb](3. Separador de pílulas pelo formato.ipynb)**
   * 3.1 Classe identificadora da posição das bordas
   * 3.2 Processamento do banco de imagens
   * 3.3 Resultados
     * 3.3.1 0.8 < razão - Possivelmente redondas
     * 3.3.2 0.7 < razão < 0.8 - Possivelmente losangulares
     * 3.3.3 razão < 0.7 - Possivelmente ovais
 * **[4. Comparação por cor.ipynb](4. Comparação por cor.ipynb)**
   * 4.1 Introdução
     * 4.1.1 Algoritmo - Pseudo código
     * 4.1.2 Tipos de comparação de cores
   * 4.2 Comparação RGB
   * 4.3 Comparação H (SV são desconsiderados)
   * 4.4 Comparação L\*a\*b\*
     
## Base de dados

A base de dados deve estar em `PILL/`. Não coloquei por ser pesada
