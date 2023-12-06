
rootdir <- "shared-seabee-ns9879k/seabirds/2023/"


folders <- dir(rootdir)
data <- data.frame(mission = "", total_time = 1.2, gps_error = 0.1, threed_error = 0.1, gcp_error = 0.1, average_gsd = 0.4)
data <- data[0,]
for( folder in folders ) {
  filename <- paste0(rootdir,folder,"/report/stats.json")
  if(file.exists(filename)) {
    tempdata <- fromJSON(filename)
    
    gps_error <- tempdata$gps_errors$average_error
    threed_error <- ifelse(is.null(tempdata$'3d_errors'$average_error), NA, tempdata$'3d_errors'$average_error)
    gcp_error <- ifelse(is.null(tempdata$gcp_errors$average_error), NA, tempdata$gcp_errors$average_error)
    total_time <- tempdata$odm_processing_statistics$total_time
    average_gsd <- tempdata$odm_processing_statistics$average_gsd
    temp <- data.frame(mission = folder, total_time, gps_error, threed_error, gcp_error, average_gsd)
    data <- rbind(data, temp)
  }
}


hist(data$threed_error, breaks = 100)
library(ggplot2)
ggplot(data = data, aes(x=average_gsd)) + geom_histogram(bins = 100) + geom_vline(xintercept = 1.1, color = "darkgreen") +
  theme_linedraw() + xlim(0,2)

sjekk <- data[data$average_gsd > 1.1 & data$average_gsd < 1.2,]
