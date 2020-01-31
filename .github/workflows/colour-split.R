library(readr)
dat <- read_csv("~/full dataset (open in notepad).csv", col_names = FALSE)
library(ggplot2)
library(plotly)

hms <- function(t){
  paste(formatC(t %/% (60*60) %% 24, width = 2, format = "d", flag = "0")
        ,formatC(t %/% 60 %% 60, width = 2, format = "d", flag = "0")
        ,formatC(t %% 60, width = 2, format = "d", flag = "0")
        ,sep = ":"
  )
}

## check is a function taking values from 1 to 3282 inclusive, from 8:06:28 to 15:49:00
check <- function(t) {
  newer <- split(dat,dat$X1)
  new <- newer[[t]]
  beam <- new$X2
  level <- new$X4
  freq <- factor(new$X3)
  time <- hms(new$X1[1])
  main <- paste("Variation in level by beam at", time, "- the darker a point, the higher its frequency...", sep=" ")
  p <- ggplot(new, aes(beam, level), group=freq) + ggtitle(main) + geom_point(aes(color = freq)) + 
    scale_color_viridis(discrete=TRUE, option = "D", direction=-1) + theme_minimal()
  p <- ggplotly(p)
  p
}

check(sample(1:3282,1)) ## a random time

## for lines (looks awful)
  main <- paste("Variation in level by beam at", time, "- the darker a line, the higher its frequency...", sep=" ")
  p <- ggplot(new, aes(beam, level), group=freq) + ggtitle(main) + geom_point(aes(color = freq)) + 
    scale_color_viridis(discrete=TRUE, option = "D", direction=-1) + theme_minimal()
  
## for points (much better)
  main <- paste("Variation in level by beam at", time, "- the darker a point, the higher its frequency...", sep=" ")
  p <- ggplot(new, aes(beam, level), group=freq) + ggtitle(main) + geom_point(aes(color = freq)) + 
    scale_color_viridis(discrete=TRUE, option = "D", direction=-1) + theme_minimal()
