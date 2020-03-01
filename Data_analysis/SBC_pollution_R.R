### R function
library(lazyeval)

################################################################################
################################################################################
################################################################################
############## benchmark table


final_model <- function(df, target,pol, SOE, control, cluster, print){

    if (control == FALSE){
        fo <- as.formula(paste(
        'log(tso2_cit) ~ ',
        target,'*',
        pol,'*',
        SOE,' * Period| FE_t_c + FE_t_i + FE_c_i |0 |', cluster
                          )
                    )

        p1 <- 12
        p2 <- 15
    }else{

        fo <- as.formula(paste(
        'log(tso2_cit) ~ ',
        target,'*',
        pol,'*',
        SOE,' * Period + output_fcit+ capital_fcit + labour_fcit| FE_t_c + FE_t_i + FE_c_i |0 |',cluster
                          )
                    )

        p1 <- 15
        p2 <- 18

    }

    extra_args <- list(exactDOF = TRUE)

    t1 <- f_eval(~ felm(uqf(fo), uqs(extra_args), data =
                                df
                               )
                        )
    if (print == TRUE){

    print(summary(t1))
    }

    return(t1)

}

################################################################################
################################################################################
################################################################################
############## robustness: parallel_trend

parallel_trend <- function(df, option, print_){

    if (option == "All"){

        t1 = felm(formula=log(tso2_cit) ~ TCZ_c * polluted_thre * as.factor(year)
                  + output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c +  FE_t_i + FE_c_i | 0 |
             cityen, data= df,
             exactDOF=TRUE)

    }else{

        t1 = felm(formula=log(tso2_cit) ~ polluted_thre * as.factor(year)
             #+ output_fcit + capital_fcit + labour_fcit
                  |
             FE_t_c + FE_c_i | 0 |
             cityen, data= df %>% filter(TCZ_c == option),
             exactDOF=TRUE)

    }

    if (print_ == TRUE){

    print(summary(t1))
    }

    return(t1)
}

################################################################################
################################################################################
################################################################################
############## Additional controls

add_control_city_1 <- function(df, SOE, cluster, print_){

    fo <- as.formula(paste(
        'log(tso2_cit) ~ TCZ_c * Period * polluted_thre * ', SOE,
        '+ SPZ * Period * polluted_thre * ', SOE,
        '+ Coastal * Period * polluted_thre * ', SOE,
        '+ output_fcit + capital_fcit + labour_fcit | FE_t_c + FE_t_i + FE_c_i| 0 |',
        cluster
                          )
                    )

    extra_args <- list(exactDOF = TRUE)

    t1 <- f_eval(~ felm(uqf(fo), uqs(extra_args), data =
                                df
                               )
                        )

    if (print_ == TRUE){

                        print(summary(t1))
                        }

    return(t1)
}

add_control_city_2 <- function(df, SOE, cluster, print_){

    fo <- as.formula(paste(
        'log(tso2_cit) ~ TCZ_c * Period * polluted_thre * ', SOE,
        '+ polluted_thre * log(gdp_cap) + polluted_thre * log(population) + output_fcit + capital_fcit + labour_fcit | FE_t_c + FE_t_i + FE_c_i| 0 |',
        cluster
                          )
                    )

    extra_args <- list(exactDOF = TRUE)

    t1 <- f_eval(~ felm(uqf(fo), uqs(extra_args), data =
                                df
                               )
                        )

    if (print_ == TRUE){

                                            print(summary(t1))
                                            }

    return(t1)
}

################################################################################
################################################################################
################################################################################
############## Additiona controls

SOE_dominate <- function(df, option, dominated, cluster, print_){

#### Function for additional robustness test
#### Option is the variable to split the industries


    myenc <- enquo(option)
    SOE_option_distinct <- df_final %>%
            select(industry, !!myenc) %>%
            distinct() %>%
            summarize_at(vars(option), funs(mean_ = mean, median_ = median))
    fo <- as.formula(paste(
                'log(tso2_cit) ~  TCZ_c * polluted_thre * Period + output_fcit + capital_fcit + labour_fcit | FE_t_c + FE_t_i + FE_c_i| 0 |',
                cluster
                                  )
                            )
    extra_args <- list(exactDOF = TRUE)
    if (dominated == TRUE){

    #### Add manual filter because filter_ is deprecated

        if (option == 'count_SOE'){

            df_filtered = df %>% filter(count_SOE >=
                                as.numeric(SOE_option_distinct[1])
                               )

        }else if (option == 'out_share_SOE'){

            df_filtered = df %>% filter(out_share_SOE >=
                                as.numeric(SOE_option_distinct[1])
                               )

        }else if (option == 'cap_share_SOE'){

        df_filtered = df %>% filter(cap_share_SOE >=
                                as.numeric(SOE_option_distinct[1])
                               )
        }else{

        df_filtered = df %>% filter(lab_share_SOE >=
                                as.numeric(SOE_option_distinct[1])
                               )

    }

    t1 <- f_eval(~ felm(uqf(fo), uqs(extra_args), data =df_filtered
                               )
                        )

    }else{

        if (option == 'count_SOE'){

            df_filtered = df %>% filter(count_SOE <
                                as.numeric(SOE_option_distinct[1])
                               )

        }else if (option == 'out_share_SOE'){

            df_filtered = df %>% filter(out_share_SOE <
                                as.numeric(SOE_option_distinct[1])
                               )

        }else if (option == 'cap_share_SOE'){

        df_filtered = df %>% filter(cap_share_SOE <
                                as.numeric(SOE_option_distinct[1])
                               )
        }else{

        df_filtered = df %>% filter(lab_share_SOE <
                                as.numeric(SOE_option_distinct[1])
                               )

    }

    t1 <- f_eval(~ felm(uqf(fo), uqs(extra_args), data =
                                df_filtered
                               )
                        )

    }

    if (print_ == TRUE){

    print(summary(t1))
                                            }

    return(t1)

}
