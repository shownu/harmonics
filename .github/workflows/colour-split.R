library(readr)
dat <- read_csv("~/XXXXXXXXXXXXXXXXX.csv", col_names = FALSE)
library(ggplot2)
library(plotly)
library(viridis)

hms <- function(t){
  paste(formatC(t %/% (60*60) %% 24, width = 2, format = "d", flag = "0")
        ,formatC(t %/% 60 %% 60, width = 2, format = "d", flag = "0")
        ,formatC(t %% 60, width = 2, format = "d", flag = "0")
        ,sep = ":"
  )
}

check <- function(dat, t) {
  newer <- split(dat,dat$time)
  new <- newer[[t]]
  beam <- new$beam
  level <- new$level
  freq <- factor(new$frequency)
  time <- hms(new$time[1])
  main <- paste("Variation in level by beam at", time, "- the darker a point, the higher its frequency...", sep=" ")
  p <- ggplot(new, aes(beam, level), group=freq) + ggtitle(main) + geom_point(aes(color = freq)) + 
    scale_color_viridis(discrete=TRUE, option = "D", direction=-1) + theme_minimal()
  p <- ggplotly(p)
  p
}

max <- length(unique(dat$time))

check(sample(1:max,1)) ## choose random time
