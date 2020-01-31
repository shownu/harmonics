library(readr)
harmonics_OCT_31 <- read_csv("~/R datasets/harmonics OCT 31 3+.csv")
library(ggplot2)
library(viridis)
library(plotly)
library(plyr)


show_harmonics <- function(dat, count) {
  hz <- 3
  freq <- dat$fundamental
  time <- dat$time
  dat2 <- count(dat, 'fundamental')
  new <- subset(dat2, fundamental>hz & freq>count)
  main <- paste("fundamental harmonic over time - lines show harmonics above", hz, "Hz with more than", count, "occurrences", sep=" ")
  p <- ggplot(dat, aes(freq, time)) + ggtitle(main) + geom_point(color = 'deeppink3') + geom_vline(xintercept = new$fundamental, size = 0.2) +
    theme_minimal() + labs(y = "time (sec)", x = "harmonic (Hz)")
  p <- ggplotly(p)
  p
}
