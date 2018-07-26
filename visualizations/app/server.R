server <- function(input, output, session) {

  df_cor <- reactive({
    df_wide[which(df_wide$month %in% input$months),input$par]
  })

  col <- colorRampPalette(c("#BB4444", "#EE9988", "#FFFFFF", "#77AADD", "#4477AA"))
  
  output$corr <- renderPlot({
    M <- cor(df_cor(), use = "pairwise.complete.obs")
    #p.mat <- cor.mtest(df_cors())$p

    corrplot(M, method = "color", col = col(200),
             type = "upper", order = "hclust", number.cex = .7,
             addCoef.col = "black", # Add coefficient of correlation
             tl.col = "black", tl.srt = 90, # Text label color and rotation
             # Combine with significance
             #p.mat = p.mat, sig.level = 0.01, insig = "blank",
             # hide correlation coefficient on the principal diagonal
             diag = FALSE)
    
  }, height = 800, width = 800)

  output$pars_selected1 <- renderUI({
    selectInput("par1", "Parameter 1: ", choices = input$par, selected = input$par[1])
  })
  output$pars_selected2 <- renderUI({
    selectInput("par2", "Parameter 2: ", choices = input$par, selected = input$par[2])
  })
  
  output$scatter <- renderPlot({
    ggplot(df_cor(), aes_string(x = paste0('`',input$par1,'`'), y = paste0('`',input$par2, '`'))) + geom_point(alpha = 0.5, col = "cyan4")
    }, height = 600, width = 800)
  
}
