evaluate_model <- function(df, cluster, control, loop, i_min, i_max, j_min, j_max){

    if (control == FALSE){
        fo <- as.formula(paste(
        'log(tfp_def_fcit) ~ TCZ_c * polluted_thre * Period * SOE|FE_c_i_o + FE_t_c + FE_t_i+FE_t_o | 0 |',
            cluster
                          )
                    )

        p1 <- 11
        p2 <- 15
    }else{

        fo <- as.formula(paste(
        'log(tfp_def_fcit) ~ TCZ_c * polluted_thre * Period * SOE + output_fcit+ capital_fcit + labour_fcit| FE_c_i_o + FE_t_c + FE_t_i+FE_t_o |0 |',
        cluster
                          )
                    )

        p1 <- 14
        p2 <- 18

    }

    ### Make loop

    extra_args <- list(exactDOF = TRUE)

    #ticker_min = round(abs((i_min - i_max)), 1)/0.1
    #ticker_max = round(abs((j_max - j_min)), 1)/0.1

    #total_ticker = (ticker_min  + ticker_max) *2
    i_ <- 0
    if (loop == TRUE){

        pb <- progress_bar$new(total = length(seq(-6.5, 0, by=.1)))
        my_pval_0 <- list()
        my_pval_1 <- list()
        my_pol_0 <- list()
        my_pol_1 <- list()

        for (i in seq(i_min, i_max, by=.1)){
          pb$tick()
            for (j in seq(j_min, j_max , by=.5)){
                 i_ <- i_ +1



            t1 <- f_eval(~ felm(uqf(fo), uqs(extra_args), data =
                                df %>% filter( tfp_def_fcit > i&tfp_def_fcit <j)
                               )
                        )

            my_pval_0 <- append(my_pval_0, list(pval = as.numeric(t1$cpval[p1])))
            my_pval_1 <- append(my_pval_1, list(pval = as.numeric(t1$cpval[p2])))
            my_pol_0 <- append(my_pol_0, list(pol = i))
            my_pol_1 <- append(my_pol_1, list(pol = j))

            }
        }
    # Basic density
        print(ggplot(
           tibble(
            pval_0 = as.numeric(my_pval_0),
            pval_1 = as.numeric(my_pval_1)
           ) %>% gather(),
            aes(x=value, color=key))+geom_density()
             )

        print(ggplot(
            tibble(
                i = as.numeric(my_pol_0),
                j = as.numeric(my_pol_1),
                pval_0 = as.numeric(my_pval_0),
                pval_1 = as.numeric(my_pval_1)),
               aes(x=i, y=pval_1)

        ) +
          geom_point(aes(size=j))
             )

    ### Return values that works

        return(tibble(
            i = as.numeric(my_pol_0),
            j = as.numeric(my_pol_1),
            pval_0 = as.numeric(my_pval_0),
            pval_1 = as.numeric(my_pval_1)) %>% filter(pval_0 <= 0.1 &
                                                   pval_1 <= 0.1)
          )
         }else{

        return(summary(f_eval(~ felm(uqf(fo), uqs(extra_args), data = df))))
    }
    print(i_)
}
