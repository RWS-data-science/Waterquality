ui <- fluidPage(theme = shinytheme("cerulean"),
                h1("Waterkwaliteit analyses"),
                h1(" "),
                tabsetPanel(
                  tabPanel("Correlaties",
                           sidebarPanel(
                             checkboxGroupInput("par", "Kies parameters_HDH: ", pars, selected = pars),
                             checkboxGroupInput("months", "Kies maanden", c(1:12), selected = c(1:12) )
                             
                           
                  ),
                  mainPanel(
                    
                    h3("Correlatiematrix"),
                    p("Alleen de parameters met hoge beschikbaarheid worden weergegeven. Dat zijn er nog niet zo veel, maar kunnen we hopelijk nog aanvullen door slimmer te koppelen."),
                    em("NB: alle parameternamen zijn gecombineerd met de hoedanigheid (HDH). Iedere parameter is dus een combinatie van parameter met een bepaalde hoedanigheid."),
                    plotOutput("corr",height = 800),
                    
                    h3("Scatterplots"),
                    p("Selecteer twee parameters om tegen elkaar uit te zetten."),
                    uiOutput("pars_selected1"),
                    uiOutput("pars_selected2"),
                    plotOutput("scatter")
                  )
                ),
                  tabPanel("Trends",
                           sidebarPanel(
                             selectInput("par_trends", "Kies parameter: ", choices = pars),
                             selectInput("loc", "Kies locatie: ", choices = locs)
                           ),
                           mainPanel(
                             
                           )
                  )
                )
                
                
                
                # 
                # tabPanel("Aspect data"
                #          
                # )
                
                
                
                #a(icon("info-circle"),href="mailto:martijn.koole@rws.nl","Martijn Koole")
)
