em_depth <- c(0:100)

samples_at <- function(range) {
  par(mfrow=c(3,1))
  rx_depth <- c(25, 50, 75)
  loop.vector <- 1:3
  sample_rate <- 6000
  speed_of_sound <- 1500
  for (i in loop.vector) {
    direct_path <- sqrt(range^2 + (em_depth - rx_depth[i])^2)
    multi <- sqrt(range^2 + (em_depth + rx_depth[i])^2)
    path_length_diff <- multi - direct_path
    time_delay <- path_length_diff / speed_of_sound
    no_samples <- sample_rate * time_delay
    main <- paste("variation in samples with target depth when receiver is at depth", rx_depth[i], "m and target is", range, "m away")
    plot(no_samples, em_depth, main = main, xlim = c(0, 600))
    abline(h = rx_depth[i], col='red')
  }
}
