source("lib.R")

load("data/data_tot.RData")

#combineer parameters en HDH

data_tot$PAROMS_HDH <- paste(data_tot$PAROMS, data_tot$HDH, sep="_")



#Selecteer nutrienten, PAK's en wat andere mogelijk relevante parameters
pak <- data_tot[which(data_tot$is_PAK == 1),]
df <- data_tot[which(data_tot$PAROMS %in% c("chlorofyl-a","nitraat","nitriet", "stikstof","orthofosfaat",
                                                "ammonium","totaal fosfaat", "Zwevende stof", "zuurstof", "Doorzicht","Zuurgraad","Kjeldahl stikstof",
                                                "calcium", "kalium", "sulfaat") |
                           data_tot$is_PAK == 1),]

df$datum_week <- format(as.Date(df$DATUM), "%Y-%V")
df$month <- as.factor(month(df$DATUM))

df_wide <- dcast(df, 
                     datum_week + month + LOCOMS + knmi_STN +TN ~ PAROMS_HDH, value.var = "WAARDE", drop = T,fun.aggregate = mean) #dagen met meerdere metingen worden gemiddeld

#df_wide$month <- as.factor(month(as.Date(df_wide$datum_week, format = "%Y-%V")))

#verwijder outliers voor alle parameters

for (i in colnames(df_wide)[4:(ncol(df_wide)-1)]){
  q99 <- quantile(df_wide[,i],c(0.005, 0.995), na.rm=T) #0.5 en 99.5 percentiel

  df_wide[which(df_wide[,i] > q99[2]|
                    df_wide[,i] < q99[1]),] <- NA
}


#keep only columns with high availability
na_count <-sapply(df_wide, function(y) sum(length(which(is.na(y)))))/nrow(df_wide)

df_wide <- df_wide[,which(na_count<0.6)]

df_wide$temperatuur_KNMI <- df_wide$TN
df_wide$TN <- NULL

save(df_wide, file="visualizations/df_wide.RData")

