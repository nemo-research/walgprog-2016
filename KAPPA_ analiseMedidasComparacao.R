
#carregando dados
dir <- "/home/danilo/workspace/R/medidasComparacao/"

especialistas <- read.csv(file.path(paste(dir,"especialistas.csv", sep="")))
Jaccard_ref1 <- read.csv(file.path(paste(dir,"Jaccard_ref1.csv", sep="")))
Jaccard_ref4 <- read.csv(file.path(paste(dir,"Jaccard_ref4.csv", sep="")))
Text_ref1 <- read.csv(file.path(paste(dir,"Text_ref1.csv", sep="")))
Text_ref4 <- read.csv(file.path(paste(dir,"Text_ref4.csv", sep="")))
Tree_ref1 <- read.csv(file.path(paste(dir,"Tree_ref1.csv", sep="")))
Tree_ref4 <- read.csv(file.path(paste(dir,"Tree_ref4.csv", sep="")))
TFIDF_ref1 <- read.csv(file.path(paste(dir,"TFIDF_ref1.csv", sep="")))
TFIDF_ref4 <- read.csv(file.path(paste(dir,"TFIDF_ref4.csv", sep="")))


#Para Kappa
kappa.especialistas <- c(especialistas$K, especialistas$K.1, especialistas$K.2, especialistas$K.3)
kappa.Jaccard_ref1 <- c(Jaccard_ref1$K, Jaccard_ref1$K.1, Jaccard_ref1$K.2, Jaccard_ref1$K.3)
kappa.Jaccard_ref4 <- c(Jaccard_ref4$K, Jaccard_ref4$K.1, Jaccard_ref4$K.2, Jaccard_ref4$K.3)
kappa.Text_ref1 <- c(Text_ref1$K, Text_ref1$K.1, Text_ref1$K.2, Text_ref1$K.3)
kappa.Text_ref4 <- c(Text_ref4$K, Text_ref4$K.1, Text_ref4$K.2, Text_ref4$K.3)
kappa.Tree_ref1 <- c(Tree_ref1$K, Tree_ref1$K.1, Tree_ref1$K.2, Tree_ref1$K.3)
kappa.Tree_ref4 <- c(Tree_ref4$K, Tree_ref4$K.1, Tree_ref4$K.2, Tree_ref4$K.3)
kappa.TFIDF_ref1 <- c(TFIDF_ref1$K, TFIDF_ref1$K.1, TFIDF_ref1$K.2, TFIDF_ref1$K.3)
kappa.TFIDF_ref4 <- c(TFIDF_ref4$K, TFIDF_ref4$K.1, TFIDF_ref4$K.2, TFIDF_ref4$K.3)



#Boxplot com todos os Kappa
tabelaKappa <- data.frame(
  Especialistas = kappa.especialistas, 
  Jaccard_ref1 = kappa.Jaccard_ref1, 
  Jaccard_ref4 = kappa.Jaccard_ref4,
  Text_ref1 = kappa.Text_ref1,
  Text_ref4 = kappa.Text_ref4,
  Tree_ref1 = kappa.Tree_ref1,
  Tree_ref4 = kappa.Tree_ref4,
  TFIDF_ref1 = kappa.TFIDF_ref1,
  TFIDF_ref4 = kappa.TFIDF_ref4)
boxplot(tabelaKappa)



























