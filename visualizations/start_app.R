##
library(data.table)
library(corrplot)
library(ggplot2)
library(dplyr)
library(shiny)
library(shinythemes)


load("visualizations/df_wide.RData")

pars <- colnames(df_wide)[5:(ncol(df_wide)-1)] 

locs <- c("MAASSS","SASVGT","SCHAARVODLL","KEIZVR","NIEUWSS","BRAKL","ANDK","EIJSDPTN","LOBPTN","AMSDM","IJMDN1","KETMWT",
                  "BOCHTVWTM","HEEL","MARKMMDN","NIEUWGN","NOORDWK2","PUTTHK","SCHEELHK","VROUWZD","WIENE"
)





#voor PCF
port <- Sys.getenv('PORT') 
print(port)

shiny::runApp('dashboard',host = '0.0.0.0', port = as.numeric(port))
