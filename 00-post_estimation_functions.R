# Functions for post-processing ratings estimates.

# Copyright 2019, 2020 Dean Scarff
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

library(ggplot2)


# Returns the probability an ascent is clean according to the Bradley-Terry
# model.
PredictBradleyTerry <- function(dfs) {
  page_gamma <- dfs$pages$gamma[dfs$ascents$page]
  route_gamma <- dfs$routes$gamma[dfs$ascents$route]
  page_gamma / (page_gamma + route_gamma)
}

# Read ratings results from "dir".
#
# Expects dir to contain two files:
# - "page_ratings.csv" containing climber, gamma and var columns
# - "route_ratings.csv" containing route, gamma and var columns
ReadRatings <- function(dir) {
  df_page_ratings <- read.csv(file.path(dir, "page_ratings.csv"),
    colClasses = c("integer", "numeric", "numeric")
  )

  df_route_ratings <- read.csv(file.path(dir, "route_ratings.csv"),
    colClasses = c("factor", "numeric", "numeric")
  )

  list(routes = df_route_ratings, pages = df_page_ratings)
}

# Updates the data frames in "dfs" with ratings results.
MergeWithRatings <- function(dfs, ratings) {
  dfs$pages$gamma <- ratings$pages$gamma
  dfs$pages$var <- ratings$pages$var
  dfs$routes$gamma <- ratings$routes$gamma
  dfs$routes$var <- ratings$routes$var

  dfs$ascents$predicted <- PredictBradleyTerry(dfs)
  dfs$routes$r <- log(dfs$routes$gamma)
  dfs$pages$r <- log(dfs$pages$gamma)
  dfs
}

# Plots the timeseries of rating estimates for a set of climbers.  The "friends"
# parameter should be a named vector where the names are the climber levels and
# the values are corresponding labels to apply in the plot.
PlotProgression <- function(df_pages, friends) {
  df_friends <- df_pages %>%
    filter(climber %in% names(friends)) %>%
    transmute(
      date = as.POSIXct(timestamp, origin = "1970-01-01"),
      climber = recode(climber, !!!friends),
      r = log(gamma),
      r_upper = r + qnorm(0.25) * sqrt(var),
      r_lower = r - qnorm(0.25) * sqrt(var)
    )
  ggplot(
    df_friends,
    aes(date, r, color = climber)
  ) +
    geom_smooth(
      aes(ymin = r_lower, ymax = r_upper, fill = climber),
      stat = "identity"
    )
}

# Plots (1 - alpha) confidence intervals for a set of routes.  The "selected"
# parameter should be a named vector where the names are the route levels and
# the values are corresponding labels to apply in the plot.
PlotSelectedRoutes <- function(df_routes, selected, alpha = 0.05) {
  df <- df_routes %>%
    filter(route %in% names(selected)) %>%
    transform(
      error = qnorm(alpha / 2, sd = sqrt(var)),
      route = recode(route, !!!selected)
    )
  ggplot(df, aes(r, route)) +
    geom_point() +
    geom_errorbarh(aes(xmin = r - error, xmax = r + error))
}

# Generates outlier labels for the route plot.
GetOutliers <- function(df_routes, alpha = 0.05) {
  m <- loess(r ~ grade, df_routes, weights = 1 / df_routes$var)
  e <- residuals(m)
  e <- e / sd(e)
  q <- qnorm(1 - alpha / 2)
  ifelse(
    abs(e) > q & sqrt(df_routes$var) < q,
    as.character(df_routes$route),
    NA
  )
}

# Plots conventional grades vs the estimated "natural rating" of routes.
# Outliers are labeled.
PlotRouteRating <- function(df_routes) {
  ggplot(
    df_routes %>% mutate(outlier = GetOutliers(df_routes)),
    aes(grade, r)
  ) +
    geom_point(alpha = 0.1, size = 0.5, color = "red") +
    geom_smooth() +
    geom_text(aes(label = outlier),
      na.rm = TRUE, size = 2, check_overlap = TRUE,
      hjust = 0, nudge_x = 0.1, vjust = "outward"
    )
}

# Plots the ratings distribution for pages and routes.
PlotRatingsDensity <- function(df_pages, df_routes) {
  page_ratings <- df_pages %>%
    mutate(type = "climber") %>%
    select(r, type)
  route_ratings <- df_routes %>%
    mutate(type = "route") %>%
    select(r, type)
  ratings <- bind_rows(page_ratings, route_ratings) %>%
    mutate(type = as.factor(type))
  ggplot(ratings, aes(r)) + facet_grid(rows = vars(type)) + geom_density()
}

# Plots precision vs recall given predicted probabilities of clean ascents.
PlotPrecisionRecall <- function(df_ascents) {
  sscurves <- precrec::evalmod(
    scores = dfs$ascents$predicted,
    labels = dfs$ascents$clean
  )
  autoplot(sscurves, "PRC", show_legend = FALSE)
}
