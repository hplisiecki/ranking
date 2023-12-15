library(jsonlite)
library(dplyr)

# Function to make short version of DOI
short_DOI <- function(DOI) {
  tryCatch({
    x <- unlist(strsplit(DOI, "org/"))[2]
    x <- gsub("\\.", "-", x)
    x <- gsub("/", "_", x)
    return(x)
  }, error = function(e) {
    message("__hjuston, mamy problem", DOI)
    return(paste("__hjuston, mamy problem", DOI))
  })
}

# Function to reverse short DOI to long DOI
long_DOI <- function(DOI) {
  x <- gsub("-", ".", DOI)
  x <- gsub("_", "/", x)
  return(paste0('https://doi.org/', x))
}

# Create Article ID
create_Article_ID <- function(row, DOI = "link", title = "title", journal = 'journal') {
  if (is.character(row)) {
    return(short_DOI(row))
  } else if (row[[DOI]] != "empty") {
    return(short_DOI(row[[DOI]]))
  } else {
    t <- paste(row[[title]], as.character(row[[journal]]))
    return(digest::digest(t))
  }
}

# Open JSON file
open_SONaa <- function(file) {
  List_of_articles <- fromJSON(file)
  return(List_of_articles)
}

# Filter by authors
filter_by_authors <- function(authors, SONaa_file) {
  if (is.character(authors)) {
    authors <- list(authors)
  }

  SONaa <- open_SONaa(SONaa_file)
  lid <- c()

  for (identificator in names(SONaa)) {
    article <- SONaa[[identificator]]

    aut = article[[1]]

    t1 = c(aut,authors[[1]])
    if (sum(duplicated(t1)) > 0) {lid = c(lid,identificator )}
    }

  return(lid)
}

# Filter by institutes
filter_by_institutes <- function(institute, authors_file, SONaa_file) {
  loa <- read.csv(authors_file, fileEncoding = 'UTF-8')
  authors <- loa %>% filter(main_job == institute)
  return(filter_by_authors(authors$id, SONaa_file))
}


SONaa_file <- "ranking/analyses/List_of_articles.SONaa"
sona = open_SONaa(SONaa_file)

institute <- 'SWPS_Uniwersytet_Humanistycznospołeczny_z_siedzibą_w_Warszawie'
authors_file <- 'ranking/analyses/List_of_authors.csv'


# Call the function and store the result
x <- filter_by_institutes(institute, authors_file, SONaa_file)
