# http://www.cookbook-r.com/Statistical_analysis/Inter-rater_reliability/

#carregando bibliotecas para kappa e kappa2
library(irr)
library(fmsb)

# carregando csv =========================================================
dados = read.csv(file.path("/home/danilo/TCC/Kappa/dados4.csv"))

# separando colunas =======================================================
dados.p1 <- dados$P1
dados.p2 <- dados$P2
dados.t <- dados$T
dados.token <- dados$Token
dados.tokenw <- dados$Tokenw
dados.text <-dados$Text
dados.tree <-dados$Tree
dados.tfn <- dados$TFIDFANC
dados.tft <- dados$TFIDFATC

# Kappas ==================================================================

# If kappa is less than 0, "No agreement", 
# if 0-0.2, "Slignt agreement", 
# if 0.2-0.4, "Fair agreement",
# if 0.4-0.6, "Moderate agreement",
# if 0.6-0.8, "Substantial agreement",
# if 0.8-1.0, "Almost perfect agreement".

# Kappa para dados ordinais
# equal or squared
# entre pessoas
kappa2(dados[,c(1,2)], "squared")
kappa2(dados[,c(1,3)], "squared")
kappa2(dados[,c(2,3)], "squared")

# entre p1 x algoritmos
kappa2(dados[,c(1,4)], "squared") # dados.token
kappa2(dados[,c(1,5)], "squared") # dados.tokenw
kappa2(dados[,c(1,6)], "squared") # dados.text
kappa2(dados[,c(1,7)], "squared") # dados.tree
kappa2(dados[,c(1,8)], "squared") # dados.tfn = TFIDFANC
kappa2(dados[,c(1,9)], "squared") # dados.tft = TFIDFATC

# entre p2 x algoritmos
kappa2(dados[,c(2,4)], "squared") # dados.token
kappa2(dados[,c(2,5)], "squared") # dados.tokenw
kappa2(dados[,c(2,6)], "squared") # dados.text
kappa2(dados[,c(2,7)], "squared") # dados.tree
kappa2(dados[,c(2,8)], "squared") # dados.tfn = TFIDFANC
kappa2(dados[,c(2,9)], "squared") # dados.tft = TFIDFATC

# entre t x algoritmos
kappa2(dados[,c(3,4)], "squared") # dados.token
kappa2(dados[,c(3,5)], "squared") # dados.tokenw
kappa2(dados[,c(3,6)], "squared") # dados.text
kappa2(dados[,c(3,7)], "squared") # dados.tree
kappa2(dados[,c(3,8)], "squared") # dados.tfn = TFIDFANC
kappa2(dados[,c(3,9)], "squared") # dados.tft = TFIDFATC

# Single Score Intraclass Correlation
# twoway - subjects and raters randomly chosen 
# oneway - subjects be considered as random effects

# entre pessoas
#icc(dados[,c(1,2)], model="oneway", type="agreement")
#icc(dados[,c(1,3)], model="oneway", type="agreement")
#icc(dados[,c(2,3)], model="oneway", type="agreement")

# entre p1 e algoritmos
#icc(dados[,c(1,4)], model="oneway", type="agreement") # dados.token
#icc(dados[,c(1,5)], model="oneway", type="agreement") # dados.tokenw
#icc(dados[,c(1,6)], model="oneway", type="agreement") # dados.text
#icc(dados[,c(1,7)], model="oneway", type="agreement") # dados.tree
#icc(dados[,c(1,8)], model="oneway", type="agreement") # dados.tfn = TFIDFANC
#icc(dados[,c(1,9)], model="oneway", type="agreement") # dados.tft = TFIDFATC

# entre p2 e algoritmos
#icc(dados[,c(2,4)], model="oneway", type="agreement") # dados.token
#icc(dados[,c(2,5)], model="oneway", type="agreement") # dados.tokenw
#icc(dados[,c(2,6)], model="oneway", type="agreement") # dados.text
#icc(dados[,c(2,7)], model="oneway", type="agreement") # dados.tree
#icc(dados[,c(2,8)], model="oneway", type="agreement") # dados.tfn = TFIDFANC
#icc(dados[,c(2,9)], model="oneway", type="agreement") # dados.tft = TFIDFATC

# entre t e algoritmos
#icc(dados[,c(3,4)], model="oneway", type="agreement") # dados.token
#icc(dados[,c(3,5)], model="oneway", type="agreement") # dados.tokenw
#icc(dados[,c(3,6)], model="oneway", type="agreement") # dados.text
#icc(dados[,c(3,7)], model="oneway", type="agreement") # dados.tree
#icc(dados[,c(3,8)], model="oneway", type="agreement") # dados.tfn = TFIDFANC
#icc(dados[,c(3,9)], model="oneway", type="agreement") # dados.tft = TFIDFATC

# =========================================================================
#Kappa.test(dados.p1, dados.p2, conf.level=0.95)
#Kappa.test(dados.p1, dados.t, conf.level=0.95)
#Kappa.test(dados.p2, dados.t, conf.level=0.95)

# Kappa para dados categoricos
#kappa2(dados[,c(1,2)], "unweighted")
#kappa2(dados[,c(1,3)], "unweighted")
#kappa2(dados[,c(2,3)], "unweighted")

# Kappa para dados de mais de um par de avaliadores
#kappam.fleiss(dados)
#kappam.fleiss(dados, exact=TRUE)

# testando normalidade ====================================================
shapiro.test(dados.p1)
shapiro.test(dados.p2)
shapiro.test(dados.t)
shapiro.test(dados.token)
shapiro.test(dados.tokenw)
shapiro.test(dados.text)
shapiro.test(dados.tree)
shapiro.test(dados.tfn)
shapiro.test(dados.tft)

# correlação entre pessoas ================================================
cor.test(dados.p1, dados.p2, method="kendall")
cor.test(dados.p1, dados.t, method="kendall")
cor.test(dados.p2, dados.t, method="kendall")

# correlação p1 vs. algoritmos
cor.test(dados.p1, dados.token, method="kendall")
cor.test(dados.p1, dados.tokenw, method="kendall")
cor.test(dados.p1, dados.text, method="kendall")
cor.test(dados.p1, dados.tree, method="kendall")
cor.test(dados.p1, dados.tfn, method="kendall")
cor.test(dados.p1, dados.tft, method="kendall")

# correlação p2 vs. algoritmos
cor.test(dados.p2, dados.token, method="kendall")
cor.test(dados.p2, dados.tokenw, method="kendall")
cor.test(dados.p2, dados.text, method="kendall")
cor.test(dados.p2, dados.tree, method="kendall")
cor.test(dados.p2, dados.tfn, method="kendall")
cor.test(dados.p2, dados.tft, method="kendall")

# correlação t vs. algoritmos
cor.test(dados.t, dados.token, method="kendall")
cor.test(dados.t, dados.tokenw, method="kendall")
cor.test(dados.t, dados.text, method="kendall")
cor.test(dados.t, dados.tree, method="kendall")
cor.test(dados.t, dados.tfn, method="kendall")
cor.test(dados.t, dados.tft, method="kendall")

