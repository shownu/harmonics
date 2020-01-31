nice_plot <- function(X, min=NULL, max=NULL, beams=NULL) {
  y <- X[,1] # first col with times
  times <- as.numeric(unlist(y))
  #  goodtimes <- seconds_to_period(times)
  freqs <- X[,-1] # count beams
  tot <- length(freqs)
  beam <- seq(0,tot-1,by=1)
  for (j in beam) {
    x <- X[,j+2]
    freqX <- as.numeric(unlist(x))
    if (!is.null(beams)) {
      if (is.element(j, beams)) {
        plot3d(times, freqX, j, xlab=NULL, type="l", add=TRUE, xlim=c(min,max))  
      } else {
        plot3d(times, freqX, j, xlab=NULL, type="l", col=5, add=TRUE, xlim=c(min,max))
      } 
    } else {
      plot3d(times, freqX, j, xlab=NULL, type="l", col=5, add=TRUE, xlim=c(min,max))
    }
  }
  aspect3d(5,1,1)
  decorate3d(xlab=NULL, ylab = "frequency (dB)", zlab="beam no", box=FALSE)
}
