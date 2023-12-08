library(zcurve)
library(dplyr)
library(jsonlite)


p_values = read.csv2('D:/data/ranking/statcheck_results/computed.csv', sep= ',')

institutes = read.csv2('data/institutes_ev.csv', sep= ',', fileEncoding = 'UTF-8')
institute_names = institutes$X

authors_file <- 'data/List_of_authors.csv'
loa <- read.csv(authors_file, fileEncoding = 'UTF-8')
open_SONaa <- function(file) {
  List_of_articles <- fromJSON(file)
  return(List_of_articles)
}
SONaa_file <- "data/List_of_articles.SONaa"
sona = open_SONaa(SONaa_file)

library(comprehenr)


uni_name = institute_names[1]

uni_name = "Wyzsza_Szkola_Bankowa_w_Toruniu"
uni_name = "Wyzsza_Szkola_Ekonomii_i_Innowacji_w_Lublinie"
for (uni_name in institute_names){
  temp_authors <- loa %>% filter(main_job == uni_name)

  sona_authors = to_list(for (id in sona) id$authors)

  temp_doi = to_vec(for(no in 1:length(sona)) if(any(sona_authors[no] %in% temp_authors$fullname)) names(sona)[no])

  x <- filter_by_institutes(uni_name, authors_file, SONaa_file)


  temp_p_values = p_values %>% filter(Source %in% temp_doi)

  error_occurred = FALSE

  tryCatch({
    fit <- zcurve(p = as.numeric(temp_p_values$Value))
  }, error = function(err) {
    print(paste0('Error occurred for:', uni_name))
    error_occurred <<- TRUE
  })
  print(error_occurred)
  if (error_occurred == TRUE){
    next
  }

  jpeg(file= paste0('plots/', 'computed/', uni_name, ".jpeg"))

  plot(fit, CI = TRUE, annotation = TRUE, main = uni_name)
  dev.off()
}


summary(fit)

summary(fit, all = TRUE)


library(zcurve)
p_values = read.csv2('D:/data/ranking/statcheck_results/computed.csv', sep= ',')

fit <- zcurve(p = as.numeric(p_values$Value))

jpeg(file= paste0('plots/', "all_unis.jpeg"))

plot(fit, CI = TRUE, annotation = TRUE, main = "All Universities")
dev.off()

# Open JSON file
open_SONaa <- function(file) {
  List_of_articles <- fromJSON(file)
  return(List_of_articles)
}
SONaa_file <- "data/List_of_articles.SONaa"
sona = open_SONaa(SONaa_file)

library(comprehenr)

years = c(2017, 2018, 2019, 2020, 2021)
for (year in years){
  dates = to_vec(for(id in sona) id$date)
  temp_doi = to_vec(for(no in 1:length(sona)) if(dates[no] == year) names(sona)[no])
  temp_p_values = p_values %>% filter(Source %in% temp_doi)
  fit <- zcurve(p = as.numeric(temp_p_values$Value))
  jpeg(file= paste0('plots/', 'computed/', year, ".jpeg"))

  plot(fit, CI = TRUE, annotation = TRUE, main = year)
  dev.off()
}


}


