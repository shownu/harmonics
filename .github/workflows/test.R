test <- function(i,x,abline=NULL,min=NULL,max=NULL) {
  dat <- split(first_time,first_time$X1)
  new <- dat[[x]]
  tn <- new[2]
  t <- as.numeric(unlist(tn))
  if (identical(0, i)) { #do frequency
    fn <- new[3]
    f <- as.numeric(unlist(fn))
    plot(t,f, col=3,
         xlab="beam", ylab = "frequency (dB)", type="p", xlim=c(min,max),
         main=paste(29180 + (x*8),"seconds into the day - freq",sep=" "))
    if (!is.null(abline)) {
    newer <- split(new,new$X2)
    newest <- newer[[abline]]
    abline(h=c(max(newest$X3)))
    }
  }
  if (identical(1, i)) { #do level
    ln <- new[4]
    l <- as.numeric(unlist(ln))
    plot(t,l, col="deeppink4", pch=20,
         xlab="beam", ylab = "level (dB)", xlim=c(min,max),
         main=paste(29180 + (x*8),"seconds into the day - level",sep=" "))
    if (!is.null(abline)) {
    newer <- split(new,new$X2)
    newest <- newer[[abline]]
    abline(h=c(max(newest$X4)))
    }
  }
}
