library(stargazer)

go_latex <- function(results, title,addFE, save, name){
    ### name should includes .txt extension

  latex <- capture.output(stargazer(results, title=title,
          dep.var.caption  = "The Dependent variable:",
          dep.var.labels.include = FALSE,
          #column.labels = columns_label,
          #column.separate = column_sep,
          #omit = omit,
          #order = order,
          #covariate.labels=covariates,
          align=FALSE,
          no.space=TRUE,
          keep.stat = c('n', "rsq"),
          notes = c('Heteroskedasticity-robust standard errors in parentheses',
                    'are clustered by city'),
          notes.align = 'l',
          add.lines = addFE
    )
                          )

  if (save == TRUE){

      lapply(latex, write, name, append=TRUE, ncolumns=1000)
  }
}
