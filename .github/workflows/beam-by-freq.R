library(readr)
first_time <- read_csv("~/until 8.58 part1.csv", col_names = FALSE)

freqsfrom <- function(time,x) {
  dat <- split(first_time,first_time$X1)
  new <- dat[[time]]
  newer <- split(new,new$X3)
  
  freq <- newer[[x]]
  bn <- freq[2]
  b <- as.numeric(unlist(bn))
  ln <- freq[4]
  l <- as.numeric(unlist(ln))   
  freq1 <- newer[[x+1]]
  bn <- freq1[2]
  b1 <- as.numeric(unlist(bn))
  ln <- freq1[4]
  l1 <- as.numeric(unlist(ln))   
  freq2 <- newer[[x+2]]
  bn <- freq2[2]
  b2 <- as.numeric(unlist(bn))
  ln <- freq2[4]
  l2 <- as.numeric(unlist(ln))  
  freq3 <- newer[[x+3]]
  bn <- freq3[2]
  b3 <- as.numeric(unlist(bn))
  ln <- freq3[4]
  l3 <- as.numeric(unlist(ln))
  
  xmin <- min(min(b),min(b1),min(b2),min(b3))
  xmax <- max(max(b),max(b1),max(b2),max(b3))
  ymin <- min(min(l),min(l1),min(l2),min(l3))
  ymax <- max(max(l),max(l1),max(l2),max(l3))
  title <- paste(29180 + (time*8),"seconds into the day - frequencies in legend", sep=" ")
  
  plot(b,l, col="deeppink4", pch=20, xlab="beam", ylab = "level (dB)", 
       xlim=c(xmin,xmax), ylim=c(ymin,ymax), main=title)
  points(b1, l1, col="mediumpurple1", pch=20)
  points(b2, l2, col="green", pch=20)
  points(b3, l3, col="deepskyblue", pch=20)
  
  legend("topright", legend=c(freq[3,3], freq1[3,3], freq2[3,3], freq3[3,3]),
         col=c("deeppink4", "mediumpurple1", "green", "deepskyblue"), pch=20)
}

freqsfrom(1,3)
