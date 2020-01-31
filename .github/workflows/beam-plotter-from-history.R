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
