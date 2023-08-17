library(exifr)
library(openxlsx)
library(stringr)
require(RPostgres)

##### scan folder ####
dir = "Mounts/P-Prosjekter2/22660210_droner_sjofugl/2022/"
files <- list.files(dir, recursive = T)
datraw <- read_exif(paste0(dir,files))
dat <- datraw
datnames <- names(dat)
datnamesneg <- datnames[grep("Tag*",datnames)]
datnamesneg <- c(datnamesneg,datnames[grep("Metadata*",datnames)])
datnamesneg <- c(datnamesneg,"ThumbnailImage","PreviewImage")
datnames <- datnames[!(datnames %in% datnamesneg)]
dat <- dat[,datnames]

#dat2 <- dat[!duplicated(dat$FileType),]
#openxlsx::write.xlsx(dat[1:5000,], "Mounts/P-Prosjekter2/22660210_droner_sjofugl/exif2.xlsx")

#x <- as.data.frame.matrix(table(dat$Directory, dat$SerialNumber, useNA = "always"))

##### connects to db ####
source("dblogin.R")
con <- dbConnect(Postgres(),
                 host = "droner_sjofugl-db.nina.no",
                 dbname = "droner_sjofugl",
                 user = user,
                 password = pwd)

##### add new missions ####

folderstofind <- c("images","unused")
for(foldertofind in folderstofind) {
  existingmissions <- dbReadTable(con, "missions")
  newmissions <- dat[substr(dat$Directory, nchar(dat$Directory)-(nchar(foldertofind)), nchar(dat$Directory)) == paste0("/",foldertofind),]
  newmissions <- substr(newmissions$Directory, 1, nchar(newmissions$Directory)-(nchar(foldertofind)+1))
  newmissions <- unique(newmissions)
  newmissions <- newmissions[!(newmissions %in% existingmissions$directory)]
  for(directory in newmissions) {
    mission <- str_split(directory,"/")
    mission <- mission[[1]][length(mission[[1]])]
    dbExecute(con, paste0("INSERT INTO missions (directory, mission, status) VALUES ('",directory,"', '",mission,"', 0)"))
  }
}


##### insert new files ####
existingmissions <- dbReadTable(con, "missions")
existingfiles <- dbReadTable(con, "files")
dat <- dat[!(paste0(dat$Directory,"/",dat$FileName) %in% paste0(existingfiles$directory,"/",existingfiles$filename)),]
if(nrow(dat) > 0) {
  for(i in 1:nrow(dat)) {
    directory <- dat$Directory[i]
    filename <- dat$FileName[i]
    filemodifydate <- dat$FileModifyDate[i]
    filemodifydate <- str_replace(filemodifydate,":","-")
    filemodifydate <- str_replace(filemodifydate,":","-")
    filetype <- dat$FileType[i]
    serialnumber <- dat$SerialNumber[i]
    gpslatitude <- dat$GPSLatitude[i]
    gpslongitude <- dat$GPSLongitude[i]
    mission <- dat$Directory[i]
    #this will get ugly... to find mission
    nomatches = TRUE
    curmiss = mission
    while (nomatches) {
      matching_key <- existingmissions$directory[grep(curmiss, existingmissions$directory)]
      if(curmiss == "/") {
        nomatches = FALSE
        mission = 0
        break
      }
      if(length(matching_key)>1) {
        nomatches = FALSE
        mission = 0
        break
      }
      if(length(matching_key)==1) {
        nomatches = FALSE
        mission = existingmissions$id[existingmissions$directory == matching_key]
      }
      curmiss = dirname(curmiss)
    }
    
    endvalues <- c()
    endfields <- ""
    geomvalues <- c()
    geomfields <- ""
    if(!is.na(serialnumber)) { endvalues <- c(endvalues,serialnumber); endfields <- paste0(endfields,", serialnumber") }
    if(!is.na(gpslatitude)) { geomvalues <- c(paste0("ST_SetSRID(ST_MakePoint(",gpslongitude,", ",gpslatitude,"), 4326)")); geomfields <- paste0(geomfields,", geom") }
    values <- paste(mission, directory, filename, filemodifydate, filetype, sep="','")
    if(!is.null(endvalues)) {
      values <- paste(values, paste(endvalues, collapse="','"), sep="','")
    }
    values <- paste0("('",values,"'")
    if(!is.null(geomvalues)) {
      values <- paste0(values, ", ",geomvalues)
    }
    #geom = ST_SetSRID(ST_MakePoint(gpslongitude, gpslatitude), 4326)
    query <- paste0("INSERT INTO files (mission, directory, filename, filemodifydate, filetype",endfields,geomfields,") VALUES ",values,")")
    query
    dbExecute(con, query)
  }
}

dbDisconnect(con)
