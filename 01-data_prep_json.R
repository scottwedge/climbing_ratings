# Convert theCrag API responses to ascent, page and route tables.

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

# Make sure to source("00-data_prep_functions.R") before sourcing this script.

period_length <- 604800 # seconds in 1 week

df_raw <- ReadAllJsonAscents(data_dir)
message(
  paste(
    prettyNum(nrow(df_raw), big.mark = ","), "expanded ascents by",
    prettyNum(nlevels(df_raw$climber), big.mark = ","), "climbers, over",
    prettyNum(nlevels(df_raw$route), big.mark = ","), "routes\n"
  )
)
df_clean <- CleanAscents(df_raw)
message(SummarizeAscents(df_clean))

dfs <- NormalizeTables(df_clean, period_length)
dfs$routes <- mutate(dfs$routes, gamma = TransformGrade(grade, 0.02, ref = 259))
WriteNormalizedTables(dfs, data_dir)
