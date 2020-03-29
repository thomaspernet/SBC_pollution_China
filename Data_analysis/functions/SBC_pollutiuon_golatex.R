library(stargazer)

go_latex <- function(
results,
title,
dep_var,
addFE,
save, name, note = FALSE){
    ### name should includes .txt extension

  if (note != FALSE){

  latex <- capture.output(stargazer(results, title=title,
          dep.var.caption  = dep_var,
          dep.var.labels.include = FALSE,
          #column.labels = columns_label,
          #column.separate = column_sep,
          #omit = omit,
          #order = order,
          #covariate.labels=covariates,
          align=FALSE,
          no.space=TRUE,
          keep.stat = c('n', "rsq"),
          notes = c(note),
          notes.align = 'l',
          add.lines = addFE
    )
                          )


  }else{
    latex <- capture.output(stargazer(results, title=title,
          dep.var.caption  = dep_var,
          dep.var.labels.include = FALSE,
          #column.labels = columns_label,
          #column.separate = column_sep,
          #omit = omit,
          #order = order,
          #covariate.labels=covariates,
          align=FALSE,
          no.space=TRUE,
          keep.stat = c('n', "rsq"),
          omit.table.layout = "n",
          #notes.align = 'l',
          add.lines = addFE
    )
                          )

  }


  if (save == TRUE){

      lapply(latex, write, name, append=TRUE, ncolumns=1000)
  }
}
