library(readr)
beams <- read_csv("~/ALL BEAMS.csv", col_names = FALSE)

beam_plotter <- function(x,i) {
  dat <- split(beams,beams$X2)
  new <- dat[[i+1]]
  tn <- new[1]
  t <- as.numeric(unlist(tn))
  if (identical(x, 0)) { #do frequency
    fn <- new[3]
    f <- as.numeric(unlist(fn))
    plot(t,f, col=3,
         xlab="time (s)", ylab = "frequency (dB)", type="p",
         main=paste("beam",i,"frequency from 8am to 3pm",sep=" "))
  }
  if (identical(x,1)) { #do level
    ln <- new[4]
    l <- as.numeric(unlist(ln))
    plot(t,l, col="deeppink4", pch=20, cex=0.7,
         xlab="time (s)", ylab = "level (?)",
         main=paste("beam",i,"level from 8am to 3pm",sep=" "))
  }
  abline(v=c(28800,32400,36000,39600,43200,46800,50400,54000))
}

beam_plotter(1,0)
beam_plotter(1,1)
beam_plotter(1,2)
beam_plotter(1,3)
beam_plotter(1,4)
beam_plotter(1,5)
beam_plotter(1,6)
beam_plotter(1,7)
beam_plotter(1,8)
beam_plotter(1,9)
beam_plotter(1,10)
beam_plotter(1,11)
beam_plotter(1,12)
beam_plotter(1,13)
beam_plotter(1,14)
beam_plotter(1,15)
beam_plotter(1,16)
beam_plotter(1,17)
beam_plotter(1,18)
beam_plotter(1,19)
beam_plotter(1,20)
beam_plotter(1,21)
beam_plotter(1,22)
beam_plotter(1,23)
beam_plotter(1,24)
beam_plotter(1,25)
beam_plotter(1,26)
beam_plotter(1,27)
beam_plotter(1,28)
beam_plotter(1,29)
beam_plotter(1,30)
beam_plotter(1,31)
beam_plotter(1,32)
