library(prodest)
library(tidyverse)
df <- read.csv("test/01_TFP_SBC.gz") #%>% filter(complete.cases(.) & input_agg_o > 0)

df$id_1 <- df %>% group_indices(id) 

#df %>% filter(input_agg_o == 0)

OP.fit <- prodestOP(Y = log(df$output_agg_o),
                    fX = log(df$employment_agg_o),
                    sX= log(df$fa_net_agg_o),
                    pX = log(df$input_agg_o),
                    idvar = df$id_1,
                    timevar = df$year,
                    exit = TRUE)

summary(OP.fit)

df$tfp_OP <- log(df$output_agg_o) - (log(df$employment_agg_o) * OP.fit@Estimates$pars[1] +
                                      log(df$fa_net_agg_o) * OP.fit@Estimates$pars[2])

df %>% group_by(year, OWNERSHIP) %>% summarize( mean_tfpOP = mean(tfp_OP))

write.csv(df, "TFP_computed_ASIF_china.csv", row.names=FALSE)

#### Split by ownership

df_soe <- df %>% filter(OWNERSHIP == 'SOE')
OP.fit_SOE <- prodestOP(Y = log(df_soe$output_agg_o),
                    fX = log(df_soe$employment_agg_o),
                    sX= log(df_soe$fa_net_agg_o),
                    pX = log(df_soe$input_agg_o),
                    idvar = df_soe$id_1,
                    timevar = df_soe$year,
                    exit = TRUE)
summary(OP.fit_SOE)

df_soe$tfp_OP_soe <- log(df_soe$output_agg_o) - (log(df_soe$employment_agg_o) * OP.fit_SOE@Estimates$pars[1] +
                                       log(df_soe$fa_net_agg_o) * OP.fit_SOE@Estimates$pars[2])


write.csv(df_soe, "TFP_computed_ASIF_china_SOE.csv", row.names=FALSE)

df_pri <- df %>% filter(OWNERSHIP == 'PRIVATE')
OP.fit_PRI <- prodestOP(Y = log(df_pri$output_agg_o),
                        fX = log(df_pri$employment_agg_o),
                        sX= log(df_pri$fa_net_agg_o),
                        pX = log(df_pri$input_agg_o),
                        idvar = df_pri$id_1,
                        timevar = df_pri$year,
                        exit = TRUE)
summary(OP.fit_PRI)

df_pri$tfp_OP_pri <- log(df_pri$output_agg_o) - (log(df_pri$employment_agg_o) * OP.fit_PRI@Estimates$pars[1] +
                                                   log(df_pri$fa_net_agg_o) * OP.fit_PRI@Estimates$pars[2])

write.csv(df_pri, "TFP_computed_ASIF_china_PRI.csv", row.names=FALSE)

df_final <- df %>% 
  left_join(df_soe %>% select( id, OWNERSHIP, year, geocode4_corr, industry, tfp_OP_soe)) %>%
  left_join(df_pri %>% select( id, OWNERSHIP, year, geocode4_corr, industry, tfp_OP_pri)) %>%
  mutate(tfp_OWNERSHIP = ifelse( is.na(tfp_OP_soe), tfp_OP_pri, tfp_OP_soe))
  
write.csv(df_final, "TFP_computed_ASIF_china_final.csv", row.names=FALSE)

#### save models
saveRDS(OP.fit, "model_OP.rds")
saveRDS(OP.fit_PRI, "model_OP_PRI.rds")
saveRDS(OP.fit_SOE, "model_OP_SOE.rds")