by_date <- function(dat, beam_no) {
  new <- split(dat, dat$beam)
  newer <- new[[beam_no]]
  freq <- newer$frequency
  time <- newer$time
  main <- paste("all frequencies in beam", beam_no, "over time", sep=" ")
  p <- ggplot(newer, aes(time, freq)) + ggtitle(main) + geom_point(size = 0.7) +
    theme_minimal() + labs(y = "frequency (Hz)", x = "time (sec)")
  p <- ggplotly(p)
  p
}
