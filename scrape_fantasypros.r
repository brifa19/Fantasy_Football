library(ffpros)
library(jsonlite)

cat("DEBUG: Starting FantasyPros scrape...\n", file=stderr())

tryCatch({
  rankings <- fp_rankings(page = "consensus-cheatsheets", sport = "nfl", season = 2025, "scoring" = "half-ppr")
  
  if (is.null(rankings)) {
    cat("DEBUG: fp_rankings returned NULL\n", file=stderr())
    quit(status = 1)
  }

  cat("DEBUG: Rows downloaded: ", nrow(rankings), "\n", sep="", file=stderr())

  if (nrow(rankings) == 0) {
    cat("DEBUG: Rankings is empty\n", file=stderr())
    quit(status = 1)
  }

  # Only JSON goes to stdout
  cat(toJSON(rankings, dataframe = "rows", pretty = FALSE, auto_unbox = TRUE))
}, error = function(e) {
  cat("DEBUG: Error - ", e$message, "\n", sep="", file=stderr())
  quit(status = 1)
})
