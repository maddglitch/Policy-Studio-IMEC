# IMEC Trade Facilitation - LPI data manipulation
# Author: Mohammad Eisa AlDarmaki
# Dataset: World Bank Logistics Performance Index (LPI), 15 corridor economies, 2007-2022.

# Load tidyverse
library(tidyverse)

# Import the dataset
lpi_raw <- read_csv("data/raw/lpi_corridor_raw.csv")

# select(): keep the columns I need
lpi <- select(lpi_raw, country, iso, year, indicator_code, value)

# filter(): keep only the customs efficiency score
lpi <- filter(lpi, indicator_code == "LP.LPI.CUST.XQ")

# mutate(): add a region column for each economy
lpi <- mutate(lpi,
  region = case_when(
    iso == "IND" ~ "India",
    iso %in% c("ARE", "SAU", "QAT", "KWT", "BHR", "OMN") ~ "Gulf",
    iso %in% c("JOR", "ISR") ~ "Levant",
    iso %in% c("GRC", "FRA", "DEU") ~ "Europe",
    iso %in% c("SGP", "MYS", "THA") ~ "ASEAN"
  )
)

# group_by() and summarize(): average customs score by region and year
summary_table <- lpi %>%
  group_by(region, year) %>%
  summarize(avg_customs = mean(value))

# Export the aggregation as a CSV
write_csv(summary_table, "output/lpi_corridor_summary.csv")

# Second aggregation: rank economies by their 2022 customs score
ranking <- lpi %>%
  filter(year == 2022) %>%
  group_by(region, country) %>%
  summarize(customs_2022 = mean(value)) %>%
  arrange(desc(customs_2022))

# Export the ranking as a CSV
write_csv(ranking, "output/lpi_latest_ranking_2022.csv")
