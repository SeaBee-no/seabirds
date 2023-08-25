CREATE TABLE sigmasetup.activity (
    id bigint NOT NULL,
    description text NOT NULL
);

CREATE TABLE sigmasetup.age (
    id bigint NOT NULL,
    description text NOT NULL
);

CREATE TABLE sigmasetup.sex (
    id bigint NOT NULL,
    description text NOT NULL
);

CREATE TABLE species (
    id bigint NOT NULL,
    norwegian text NOT NULL,
    english text,
    latin text
);

CREATE TABLE detections (
    id integer NOT NULL,
    geom public.geometry(Polygon,4326) NOT NULL,
    fileid bigint NOT NULL,
    individualid bigint NOT NULL,
    species smallint NOT NULL,
    activity smallint NOT NULL,
    sex smallint NOT NULL,
    age smallint NOT NULL,
    datetimereg timestamp with time zone DEFAULT now() NOT NULL,
    visibleonimage boolean NOT NULL,
    comment text,
    modelversion bigint,
    score_species numeric,
    score_activity numeric,
    score_sex numeric,
    score_age numeric,
    manuallyverified boolean NOT NULL
);

CREATE TABLE files (
    id BIGINT NOT NULL,
    rootdirectory text NOT NULL,
    mission text,
    subdirectory text,
    filename text NOT NULL,
    filemodifydate timestamp without time zone NOT NULL,
    datetimeoriginal timestamp without time zone,
    filetype text NOT NULL,
    filesize BIGINT NOT NULL,
    geom public.geometry(Point,4326),
    ExposureTime text,
    FNumber numeric,
    ISO integer,
    width integer,
    height integer,
    Make text,
    Model text,
    BodySerialNumber text,
    GPSStatus text,
    AbsoluteAltitude numeric,
    RelativeAltitude numeric,
    GimbalRollDegree numeric,
    GimbalYawDegree numeric,
    GimbalPitchDegree numeric,
    FlightRollDegree numeric,
    FlightYawDegree numeric,
    FlightPitchDegree numeric,
    FlightXSpeed numeric,
    FlightYSpeed numeric,
    FlightZSpeed numeric
);

CREATE SEQUENCE detections_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

CREATE SEQUENCE detections_individualid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

CREATE SEQUENCE files_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE files_id_seq RESTART WITH 1;

ALTER TABLE ONLY detections ALTER COLUMN id SET DEFAULT nextval('detections_id_seq'::regclass);
ALTER TABLE ONLY detections ALTER COLUMN individualid SET DEFAULT nextval('detections_individualid_seq'::regclass);
ALTER TABLE ONLY files ALTER COLUMN id SET DEFAULT nextval('files_id_seq'::regclass);

ALTER TABLE ONLY detections ADD CONSTRAINT detections_pkey PRIMARY KEY (id);
ALTER TABLE ONLY files ADD CONSTRAINT files_pkey PRIMARY KEY (id);
ALTER TABLE ONLY activity ADD CONSTRAINT activity_pkey PRIMARY KEY (id);
ALTER TABLE ONLY age ADD CONSTRAINT age_pkey PRIMARY KEY (id);
ALTER TABLE ONLY sex ADD CONSTRAINT sex_pkey PRIMARY KEY (id);
ALTER TABLE ONLY species ADD CONSTRAINT species_pkey PRIMARY KEY (id);

insert into age (id, description) values (0, 'Unknown'), (1, 'Pullus'), (2, 'Immature'), (3, 'Adult'), (4, '1K'), (5, '2K'), (6, '3K'), (7, '4K'), (8, '5K');
insert into activity (id, description) values (0, 'Unknown'), (1, 'On nest'), (2, 'On land'), (3, 'On water'), (4, 'In flight'), (5, 'Dead on water'), (6, 'Dead on land'), (7, 'Nest without bird');
insert into sex (id, description) values (0, 'Unknown'), (1, 'Male'), (2, 'Female'), (3, 'Female colored');

insert into species (id, norwegian, english, latin) values (10, 'Smålom', 'Red-throated Diver', 'Gavia stellata');
insert into species (id, norwegian, english, latin) values (20, 'Storlom', 'Black-throated Diver', 'Gavia arctica');
insert into species (id, norwegian, english, latin) values (30, 'Islom', 'Great Northern Diver', 'Gavia immer');
insert into species (id, norwegian, english, latin) values (40, 'Gulnebblom', 'White-billed Diver', 'Gavia adamsii');
insert into species (id, norwegian, english, latin) values (50, 'Dvergdykker', 'Little Grebe', 'Tachybaptus ruficollis');
insert into species (id, norwegian, english, latin) values (60, 'Horndykker', 'Slavonian Grebe', 'Podiceps auritus');
insert into species (id, norwegian, english, latin) values (70, 'Svarthalsdykker', 'Black-necked Grebe', 'Podiceps nigricollis');
insert into species (id, norwegian, english, latin) values (80, 'Toppdykker', 'Great Crested Grebe', 'Podiceps cristatus');
insert into species (id, norwegian, english, latin) values (90, 'Gråstrupedykker', 'Red-Necked Grebe', 'Podiceps grisegena');
insert into species (id, norwegian, english, latin) values (100, 'Vandrealbatross', 'Wandering Albatross', 'Diomedea exulans');
insert into species (id, norwegian, english, latin) values (110, 'Svartbrynalbatross', 'Black-browed Albatross', 'Diomedea melanophris');
insert into species (id, norwegian, english, latin) values (130, 'Gråhodealbatross', 'Grey-headed Albatross', 'Diomedea chrysostoma');
insert into species (id, norwegian, english, latin) values (150, 'Kappdue', 'Cape Pigeon', 'Daption capense');
insert into species (id, norwegian, english, latin) values (160, 'Havhest', 'Fulmar', 'Fulmarus glacialis');
insert into species (id, norwegian, english, latin) values (170, 'Gulnebblire', 'Cory''s Shearwater', 'Calonectris diomedea');
insert into species (id, norwegian, english, latin) values (180, 'Storlire', 'Great Shearwater', 'Puffinus gravis');
insert into species (id, norwegian, english, latin) values (190, 'Grålire', 'Sooty Shearwater', 'Puffinus griseus');
insert into species (id, norwegian, english, latin) values (200, 'Havlire', 'Manx Shearwater', 'Puffinus puffinus');
insert into species (id, norwegian, english, latin) values (270, 'Wilsonstormsvale', 'Wilson''s Petrel', 'Oceanites oceanicus');
insert into species (id, norwegian, english, latin) values (290, 'Havsvale', 'Storm Petrel', 'Hydrobates pelagicus');
insert into species (id, norwegian, english, latin) values (310, 'Stormsvale', 'Leach''s Storm Petrel', 'Oceanodroma leucorhoa');
insert into species (id, norwegian, english, latin) values (320, 'Hvitpelikan', 'White Pelican', 'Pelecanus onocrotalus');
insert into species (id, norwegian, english, latin) values (330, 'Krøllpelikan', 'Dalmatian Pelican', 'Pelecanus crispus');
insert into species (id, norwegian, english, latin) values (340, 'Havsule', 'Gannet', 'Morus bassanus');
insert into species (id, norwegian, english, latin) values (350, 'Storskarv', 'Great Cormorant', 'Phalacrocorax carbo');
insert into species (id, norwegian, english, latin) values (351, 'STORSKARV P.c.carbo', 'CORMORANT P.c.carbo', 'PHALACROCORAX CARBO CARBO');
insert into species (id, norwegian, english, latin) values (352, 'STORSKARV P.c.sinensis', 'CORMORANT P.c.sinensis', 'PHALACROCORAX CARBO SINENSIS');
insert into species (id, norwegian, english, latin) values (360, 'Toppskarv', 'Shag', 'Phalacrocorax aristotelis');
insert into species (id, norwegian, english, latin) values (370, 'Dvergskarv', 'Pygmy Cormorant', 'Phalacrocorax pygmeus');
insert into species (id, norwegian, english, latin) values (390, 'Gråhegre', 'Grey Heron', 'Ardea cinerea');
insert into species (id, norwegian, english, latin) values (400, 'Purpurhegre', 'Purple Heron', 'Ardea purpurea');
insert into species (id, norwegian, english, latin) values (430, 'Kuhegre', 'Cattle Egret', 'Bubulcus ibis');
insert into species (id, norwegian, english, latin) values (440, 'Egretthegre', 'Great White Egret', 'Egretta alba');
insert into species (id, norwegian, english, latin) values (450, 'Silkehegre', 'Little Egret', 'Egretta garzetta');
insert into species (id, norwegian, english, latin) values (460, 'Natthegre', 'Night Heron', 'Nycticorax nycticorax');
insert into species (id, norwegian, english, latin) values (470, 'Dvergrørdrum', 'Little Bittern', 'Ixobrychus minutus');
insert into species (id, norwegian, english, latin) values (480, 'Rørdrum', 'Bittern', 'Botaurus stellaris');
insert into species (id, norwegian, english, latin) values (490, 'Amerikarørdrum', 'American Bittern', 'Botaurus lentiginosus');
insert into species (id, norwegian, english, latin) values (500, 'Stork', 'White Stork', 'Ciconia ciconia');
insert into species (id, norwegian, english, latin) values (510, 'Svartstork', 'Black Stork', 'Ciconia nigra');
insert into species (id, norwegian, english, latin) values (520, 'Skjestork', 'Spoonbill', 'Platalea leucorodia');
insert into species (id, norwegian, english, latin) values (530, 'Bronseibis', 'Glossy Ibis', 'Plegadis falcinellus');
insert into species (id, norwegian, english, latin) values (540, 'Flamingo', 'Greater Flamingo', 'Phoenicopterus ruber');
insert into species (id, norwegian, english, latin) values (550, 'Sangsvane', 'Whooper Swan', 'Cygnus cygnus');
insert into species (id, norwegian, english, latin) values (560, 'Dvergsvane', 'Bewick''s Swan', 'Cygnus columbianus');
insert into species (id, norwegian, english, latin) values (570, 'Knoppsvane', 'Mute Swan', 'Cygnus olor');
insert into species (id, norwegian, english, latin) values (580, 'Snøgås', 'Snow Goose', 'Anser caerulescens');
insert into species (id, norwegian, english, latin) values (590, 'Grågås', 'Greylag Goose', 'Anser anser');
insert into species (id, norwegian, english, latin) values (600, 'Tundragås', 'White-fronted Goose', 'Anser albifrons');
insert into species (id, norwegian, english, latin) values (610, 'Dverggås', 'Lesser White-fronted Goos', 'Anser erythropus');
insert into species (id, norwegian, english, latin) values (620, 'Sædgås', 'Bean Goose', 'Anser fabalis');
insert into species (id, norwegian, english, latin) values (622, 'Kortnebbgås', 'Pink-footed Goose', 'Anser brachyrhynchus');
insert into species (id, norwegian, english, latin) values (640, 'Stripegås', 'Bar-headed Goose', 'Anser indicus');
insert into species (id, norwegian, english, latin) values (660, 'Ringgås', 'Brent Goose', 'Branta bernicla');
insert into species (id, norwegian, english, latin) values (670, 'Hvitkinngås', 'Barnacle Goose', 'Branta leucopsis');
insert into species (id, norwegian, english, latin) values (680, 'Kanadagås', 'Canada Goose', 'Branta canadensis');
insert into species (id, norwegian, english, latin) values (690, 'Rødhalsgås', 'Red-breasted Goose', 'Branta ruficollis');
insert into species (id, norwegian, english, latin) values (700, 'Rustand', 'Ruddy Shelduck', 'Tadorna ferruginea');
insert into species (id, norwegian, english, latin) values (710, 'Gravand', 'Shelduck', 'Tadorna tadorna');
insert into species (id, norwegian, english, latin) values (720, 'Stokkand', 'Mallard', 'Anas platyrhynchos');
insert into species (id, norwegian, english, latin) values (740, 'Knekkand', 'Garganey', 'Anas querquedula');
insert into species (id, norwegian, english, latin) values (750, 'Krikkand', 'Teal', 'Anas crecca');
insert into species (id, norwegian, english, latin) values (760, 'Gulkinnand', 'Baikal Teal', 'Anas formosa');
insert into species (id, norwegian, english, latin) values (780, 'Stjertand', 'Pintail', 'Anas acuta');
insert into species (id, norwegian, english, latin) values (800, 'Brunnakke', 'Wigeon', 'Anas penelope');
insert into species (id, norwegian, english, latin) values (810, 'Amerikablesand', 'American Wigeon', 'Anas americana');
insert into species (id, norwegian, english, latin) values (820, 'Snadderand', 'Gadwall', 'Anas strepera');
insert into species (id, norwegian, english, latin) values (830, 'Skjeand', 'Shoveler', 'Anas clypeata');
insert into species (id, norwegian, english, latin) values (840, 'Mandarinand', 'Mandarin Duck', 'Aix galericulata');
insert into species (id, norwegian, english, latin) values (850, 'Rødhodeand', 'Red-crested Pochard', 'Netta rufina');
insert into species (id, norwegian, english, latin) values (860, 'Taffeland', 'Pochard', 'Aythya ferina');
insert into species (id, norwegian, english, latin) values (870, 'Toppand', 'Tufted Duck', 'Aythya fuligula');
insert into species (id, norwegian, english, latin) values (880, 'Hvitøyeand', 'Ferruginous Duck', 'Aythya nyroca');
insert into species (id, norwegian, english, latin) values (890, 'Bergand', 'Scaup', 'Aythya marila');
insert into species (id, norwegian, english, latin) values (900, 'Kvinand', 'Goldeneye', 'Bucephala clangula');
insert into species (id, norwegian, english, latin) values (910, 'Islandsand', 'Barrow''s Goldeneye', 'Bucephala islandica');
insert into species (id, norwegian, english, latin) values (930, 'Havelle', 'Long-tailed Duck', 'Clangula hyemalis');
insert into species (id, norwegian, english, latin) values (940, 'Harlekinand', 'Harlequin Duck', 'Histrionicus histrionicus');
insert into species (id, norwegian, english, latin) values (950, 'Ærfugl', 'Eider', 'Somateria mollissima');
insert into species (id, norwegian, english, latin) values (960, 'Praktærfugl', 'King Eider', 'Somateria spectabilis');
insert into species (id, norwegian, english, latin) values (970, 'Brilleærfugl', 'Spectacled Eider', 'Somateria fischeri');
insert into species (id, norwegian, english, latin) values (980, 'Svartand', 'Common Scoter', 'Melanitta nigra');
insert into species (id, norwegian, english, latin) values (990, 'Sjøorre', 'Velvet Scoter', 'Melanitta fusca');
insert into species (id, norwegian, english, latin) values (1000, 'Brilleand', 'Surf Scoter', 'Melanitta perspicillata');
insert into species (id, norwegian, english, latin) values (1010, 'Stellerand', 'Steller''s Eider', 'Polysticta stellerii');
insert into species (id, norwegian, english, latin) values (1040, 'Lappfiskand', 'Smew', 'Mergellus albellus');
insert into species (id, norwegian, english, latin) values (1050, 'Laksand', 'Goosander', 'Mergus merganser');
insert into species (id, norwegian, english, latin) values (1060, 'Siland', 'Red-breasted Merganser', 'Mergus serrator');
insert into species (id, norwegian, english, latin) values (1110, 'Hønsehauk', 'Goshawk', 'Accipiter gentilis');
insert into species (id, norwegian, english, latin) values (1200, 'Kongeørn', 'Golden Eagle', 'Aquila chrysaetos');
insert into species (id, norwegian, english, latin) values (1270, 'Havørn', 'White-tailed Eagle', 'Haliaeetus albicilla');
insert into species (id, norwegian, english, latin) values (1410, 'Jaktfalk', 'Gyrfalcon', 'Falco rusticolus');
insert into species (id, norwegian, english, latin) values (1420, 'Vandrefalk', 'Peregrine', 'Falco peregrinus');
insert into species (id, norwegian, english, latin) values (1670, 'Vannrikse', 'Water Rail', 'Rallus aquaticus');
insert into species (id, norwegian, english, latin) values (1680, '?\u0085kerrikse', 'Corncrake', 'Crex crex');
insert into species (id, norwegian, english, latin) values (1690, 'Sumprikse', 'Little Crake', 'Porzana parva');
insert into species (id, norwegian, english, latin) values (1710, 'Myrrikse', 'Spotted Crake', 'Porzana porzana');
insert into species (id, norwegian, english, latin) values (1730, 'Sivhøne', 'Moorhen', 'Gallinula chloropus');
insert into species (id, norwegian, english, latin) values (1750, 'Sultanhøne', 'Purple Gallinule', 'Porphyrio porphyrio');
insert into species (id, norwegian, english, latin) values (1770, 'Sothøne', 'Coot', 'Fulica atra');
insert into species (id, norwegian, english, latin) values (1820, 'Tjeld', 'Oystercatcher', 'Haematopus ostralegus');
insert into species (id, norwegian, english, latin) values (1850, 'Vipe', 'Lapwing', 'Vanellus vanellus');
insert into species (id, norwegian, english, latin) values (1870, 'Tundralo', 'Grey Plover', 'Pluvialis squatarola');
insert into species (id, norwegian, english, latin) values (1880, 'Heilo', 'Golden Plover', 'Pluvialis apricaria');
insert into species (id, norwegian, english, latin) values (1890, 'Beringlo', 'American Golden Plover', 'Pluvialis dominica');
insert into species (id, norwegian, english, latin) values (1910, 'Sandlo', 'Ringed Plover', 'Charadrius hiaticula');
insert into species (id, norwegian, english, latin) values (1920, 'Dverglo', 'Little Ringed Plover', 'Charadrius dubius');
insert into species (id, norwegian, english, latin) values (1930, 'Hvitbrystlo', 'Kentish Plover', 'Charadrius alexandrinus');
insert into species (id, norwegian, english, latin) values (1940, 'Tobeltelo', 'Killdeer', 'Charadrius vociferus');
insert into species (id, norwegian, english, latin) values (1960, 'Rødbrystlo', 'Caspian Plover', 'Charadrius asiaticus');
insert into species (id, norwegian, english, latin) values (1970, 'Boltit', 'Eurasian Dotterel', 'Eudromias morinellus');
insert into species (id, norwegian, english, latin) values (2000, 'Småspove', 'Whimbrel', 'Numenius phaeopus');
insert into species (id, norwegian, english, latin) values (2020, 'Storspove', 'Curlew', 'Numenius arquata');
insert into species (id, norwegian, english, latin) values (2030, 'Svarthalespove', 'Black-tailed Godwit', 'Limosa limosa');
insert into species (id, norwegian, english, latin) values (2040, 'Lappspove', 'Bar-tailed Godwit', 'Limosa lapponica');
insert into species (id, norwegian, english, latin) values (2050, 'Sotsnipe', 'Spotted Redshank', 'Tringa erythropus');
insert into species (id, norwegian, english, latin) values (2060, 'Rødstilk', 'Redshank', 'Tringa totanus');
insert into species (id, norwegian, english, latin) values (2070, 'Gulbeinsnipe', 'Lesser Yellowlegs', 'Tringa flavipes');
insert into species (id, norwegian, english, latin) values (2080, 'Damsnipe', 'Marsh Sandpiper', 'Tringa stagnatilis');
insert into species (id, norwegian, english, latin) values (2090, 'Gluttsnipe', 'Greenshank', 'Tringa nebularia');
insert into species (id, norwegian, english, latin) values (2110, 'Skogsnipe', 'Green Sandpiper', 'Tringa ochropus');
insert into species (id, norwegian, english, latin) values (2130, 'Grønnstilk', 'Wood Sandpiper', 'Tringa glareola');
insert into species (id, norwegian, english, latin) values (2140, 'Strandsnipe', 'Common Sandpiper', 'Actitis hypoleucos');
insert into species (id, norwegian, english, latin) values (2150, 'Flekksnipe', 'Spotted Sandpiper', 'Actitis macularia');
insert into species (id, norwegian, english, latin) values (2160, 'Tereksnipe', 'Terek Sandpiper', 'Xenus cinereus');
insert into species (id, norwegian, english, latin) values (2180, 'Steinvender', 'Turnstone', 'Arenaria interpres');
insert into species (id, norwegian, english, latin) values (2190, 'Kortnebbekkasinsnipe', 'Short-billed Dowitcher', 'Limnodromus griseus');
insert into species (id, norwegian, english, latin) values (2200, 'Dobbeltbekkasin', 'Great Snipe', 'Gallinago media');
insert into species (id, norwegian, english, latin) values (2210, 'Enkeltbekkasin', 'Snipe', 'Gallinago gallinago');
insert into species (id, norwegian, english, latin) values (2220, 'Kvartbekkasin', 'Jack Snipe', 'Lymnocryptes minimus');
insert into species (id, norwegian, english, latin) values (2230, 'Rugde', 'Woodcock', 'Scolopax rusticola');
insert into species (id, norwegian, english, latin) values (2240, 'Sandløper', 'Sanderling', 'Calidris alba');
insert into species (id, norwegian, english, latin) values (2250, 'Polarsnipe', 'Knot', 'Calidris canutus');
insert into species (id, norwegian, english, latin) values (2260, 'Sandsnipe', 'Semi-palmated Sandpiper', 'Calidris pusilla');
insert into species (id, norwegian, english, latin) values (2270, 'Dvergsnipe', 'Little Stint', 'Calidris minuta');
insert into species (id, norwegian, english, latin) values (2280, 'Temmincksnipe', 'Temminck''s Stint', 'Calidris temminckii');
insert into species (id, norwegian, english, latin) values (2290, 'Pygmesnipe', 'Least Sandpiper', 'Calidris minutilla');
insert into species (id, norwegian, english, latin) values (2300, 'Bonapartesnipe', 'White-rumped Sandpiper', 'Calidris fuscicollis');
insert into species (id, norwegian, english, latin) values (2310, 'Gulbrystsnipe', 'Baird''s Sandpiper', 'Calidris bairdii');
insert into species (id, norwegian, english, latin) values (2320, 'Alaskasnipe', 'Pectoral Sandpiper', 'Calidris melanotos');
insert into species (id, norwegian, english, latin) values (2330, 'Spisshalesnipe', 'Sharp-tailed Sandpiper', 'Calidris acuminata');
insert into species (id, norwegian, english, latin) values (2340, 'Fjæreplytt', 'Purple Sandpiper', 'Calidris maritima');
insert into species (id, norwegian, english, latin) values (2350, 'Myrsnipe', 'Dunlin', 'Calidris alpina');
insert into species (id, norwegian, english, latin) values (2360, 'Tundrasnipe', 'Curlew Sandpiper', 'Calidris ferruginea');
insert into species (id, norwegian, english, latin) values (2370, 'Fjellmyrløper', 'Broad-billed Sandpiper', 'Limicola falcinellus');
insert into species (id, norwegian, english, latin) values (2380, 'Rustsnipe', 'Buff-breasted Sandpiper', 'Tryngites subruficollis');
insert into species (id, norwegian, english, latin) values (2390, 'Brushane', 'Ruff', 'Philomachus pugnax');
insert into species (id, norwegian, english, latin) values (2400, 'Stylteløper', 'Black-winged Stilt', 'Himantopus himantopus');
insert into species (id, norwegian, english, latin) values (2410, 'Avosett', 'Avocet', 'Recurvirostra avosetta');
insert into species (id, norwegian, english, latin) values (2420, 'Polarsvømmesnipe', 'Grey Phalarope', 'Phalaropus fulicarius');
insert into species (id, norwegian, english, latin) values (2430, 'Svømmesnipe', 'Red-necked Phalarope', 'Phalaropus lobatus');
insert into species (id, norwegian, english, latin) values (2440, 'Triel', 'Stone-curlew', 'Burhinus oedicnemus');
insert into species (id, norwegian, english, latin) values (2460, 'Ørkenloper', 'Cream-coloured Courser', 'Cursorius cursor');
insert into species (id, norwegian, english, latin) values (2470, 'Brakksvale', 'Collared Pratincole', 'Glareola pratincola');
insert into species (id, norwegian, english, latin) values (2480, 'Steppebrakksvale', 'Black-winged Pratincole', 'Glareola nordmanni');
insert into species (id, norwegian, english, latin) values (2490, 'Storjo', 'Great Skua', 'Catharacta skua');
insert into species (id, norwegian, english, latin) values (2500, 'Polarjo', 'Pomarine Skua', 'Stercorarius pomarinus');
insert into species (id, norwegian, english, latin) values (2510, 'Tyvjo', 'Arctic Skua', 'Stercorarius parasiticus');
insert into species (id, norwegian, english, latin) values (2520, 'Fjelljo', 'Long-tailed Skua', 'Stercorarius longicaudus');
insert into species (id, norwegian, english, latin) values (2530, 'Ismåke', 'Ivory Gull', 'Pagophila eburnea');
insert into species (id, norwegian, english, latin) values (2550, 'Fiskemåke', 'Common Gull', 'Larus canus');
insert into species (id, norwegian, english, latin) values (2560, 'Gråmåke', 'Herring Gull', 'Larus argentatus');
insert into species (id, norwegian, english, latin) values (2570, 'Sildemåke', 'Lesser Black-backed Gull', 'Larus fuscus');
insert into species (id, norwegian, english, latin) values (2580, 'Svartbak', 'Great Black-backed Gull', 'Larus marinus');
insert into species (id, norwegian, english, latin) values (2590, 'Polarmåke', 'Glaucous Gull', 'Larus hyperboreus');
insert into species (id, norwegian, english, latin) values (2600, 'Grønlandsmåke', 'Iceland Gull', 'Larus glaucoides');
insert into species (id, norwegian, english, latin) values (2610, 'Steppemåke', 'Great Black-headed Gull', 'Larus ichthyaetus');
insert into species (id, norwegian, english, latin) values (2620, 'Svartehavsmåke', 'Mediterranean Gull', 'Larus melanocephalus');
insert into species (id, norwegian, english, latin) values (2630, 'Hettemåke', 'Black-headed Gull', 'Chroicocephalus ridibundus');
insert into species (id, norwegian, english, latin) values (2640, 'Smalnebbmåke', 'Slender-billed Gull', 'Chroicocephalus genei');
insert into species (id, norwegian, english, latin) values (2650, 'Kanadahettemåke', 'Bonaparte''s Gull', 'Chroicoceohalus ohiladelphia');
insert into species (id, norwegian, english, latin) values (2660, 'Dvergmåke', 'Little Gull', 'Hydrocoloeus minutus');
insert into species (id, norwegian, english, latin) values (2670, 'Rosenmåke', 'Ross''s Gull', 'Rhodostethia rosea');
insert into species (id, norwegian, english, latin) values (2680, 'Krykkje', 'Kittiwake', 'Rissa tridactyla');
insert into species (id, norwegian, english, latin) values (2690, 'Sabinemåke', 'Sabine''s Gull', 'Xema sabini');
insert into species (id, norwegian, english, latin) values (2700, 'Hvitkinnsvartterne', 'Whiskered Tern', 'Chlidonias hybrida');
insert into species (id, norwegian, english, latin) values (2710, 'Hvitvingesvartterne', 'White-Winged Black Tern', 'Chlidonias leucopterus');
insert into species (id, norwegian, english, latin) values (2720, 'Svartterne', 'Black Tern', 'Chlidonias niger');
insert into species (id, norwegian, english, latin) values (2730, 'Sandterne', 'Gull-Billed Tern', 'Gelochelidon nilotica');
insert into species (id, norwegian, english, latin) values (2740, 'Rovterne', 'Caspian Tern', 'Hydroprogne caspia');
insert into species (id, norwegian, english, latin) values (2750, 'Makrellterne', 'Common Tern', 'Sterna hirundo');
insert into species (id, norwegian, english, latin) values (2760, 'Rødnebbterne', 'Arctic Tern', 'Sterna paradisaea');
insert into species (id, norwegian, english, latin) values (2770, 'Rosenterne', 'Roseate Tern', 'Sterna dougallii');
insert into species (id, norwegian, english, latin) values (2790, 'Sotterne', 'Sooty Tern', 'Onychoprion fuscatus');
insert into species (id, norwegian, english, latin) values (2800, 'Dvergterne', 'Little Tern', 'Sternula albifrons');
insert into species (id, norwegian, english, latin) values (2820, 'Splitterne', 'Sandwich Tern', 'Sterna sandvicensis');
insert into species (id, norwegian, english, latin) values (2830, 'Brunnoddy', 'Noddy', 'Anous stolidus');
insert into species (id, norwegian, english, latin) values (2840, 'Alkekonge', 'Little Auk', 'Alle alle');
insert into species (id, norwegian, english, latin) values (2860, 'Alke', 'Razorbill', 'Alca torda');
insert into species (id, norwegian, english, latin) values (2870, 'Polarlomvi', 'Brünnich''s Guillemot', 'Uria lomvia');
insert into species (id, norwegian, english, latin) values (2880, 'Lomvi', 'Guillemot', 'Uria aalge');
insert into species (id, norwegian, english, latin) values (2890, 'Teist', 'Black Guillemot', 'Cepphus grylle');
insert into species (id, norwegian, english, latin) values (2920, 'Lunde', 'Atlantic Puffin', 'Fratercula arctica');
insert into species (id, norwegian, english, latin) values (3090, 'Hubro', 'Eagle Owl', 'Bubo bubo');
insert into species (id, norwegian, english, latin) values (3670, 'Ravn', 'Raven', 'Corvus corax');
insert into species (id, norwegian, english, latin) values (3680, 'Kråke', 'Crow', 'Corvus corone');
insert into species (id, norwegian, english, latin) values (3700, 'Kornkråke', 'Rook', 'Corvus frugilegus');
insert into species (id, norwegian, english, latin) values (3710, 'Kaie', 'Jackdaw', 'Corvus monedula');
insert into species (id, norwegian, english, latin) values (3720, 'Skjære', 'Magpie', 'Pica pica');
insert into species (id, norwegian, english, latin) values (8010, 'Kongepingvin', 'King Penguin', 'Aptenodytes patagonocius');
insert into species (id, norwegian, english, latin) values (8020, 'Keiserpingvin', 'Emperor Penguin', 'Aptenodytes forsteri');
insert into species (id, norwegian, english, latin) values (8030, 'Adeliepingvin', 'Adelie Penguin', 'Pygoscelis adeliae');
insert into species (id, norwegian, english, latin) values (8040, 'Brednebbhvalfugl', 'Broad-billed Prion', 'Pachyptila vittata');
insert into species (id, norwegian, english, latin) values (8500, 'Steinkobbe', 'Harbour seal', 'Phoca vitulina');
insert into species (id, norwegian, english, latin) values (8501, 'Sel ubest.', 'Seal indet.', 'Phocidae Sp.');
insert into species (id, norwegian, english, latin) values (8510, 'Havert', 'Grey Seal', 'Halichoerus grypus');
insert into species (id, norwegian, english, latin) values (8520, 'Grønlandssel', 'Harp Seal', 'Phoca groenlandica');
insert into species (id, norwegian, english, latin) values (8530, 'Ringsel', 'Ringed Seal', 'Phoca hispida');
insert into species (id, norwegian, english, latin) values (8600, 'Nise', 'Harbour porpoise', 'Phocoena phocoena');
insert into species (id, norwegian, english, latin) values (8601, 'Hval ubest.', 'Whale indet.', 'Cetacea Sp.');
insert into species (id, norwegian, english, latin) values (8610, 'Kvitnos', 'White-beaked dolphin', 'Lagenorhynchos albirostris');
insert into species (id, norwegian, english, latin) values (8620, 'Kvitskjeving', 'Atlantic white-sided dolphin', 'Lagenorhynchos acutus');
insert into species (id, norwegian, english, latin) values (8630, 'Spekkhogger', 'Killer Whale', 'Orcinus orca');
insert into species (id, norwegian, english, latin) values (8640, 'Vågehval', 'Minke Whale', 'Balaenoptera acutorostrata');
insert into species (id, norwegian, english, latin) values (8650, 'Seihval', 'Sei Whale', 'Balaenoptera borealis');
insert into species (id, norwegian, english, latin) values (8660, 'Finnhval', 'Fin Whale', 'Balaenoptera physalus');
insert into species (id, norwegian, english, latin) values (8700, 'Mink', 'American Mink', 'Mustella vision');
insert into species (id, norwegian, english, latin) values (8710, 'Oter', 'European Otter', 'Lutra lutra');
insert into species (id, norwegian, english, latin) values (9012, 'Snipe, ubest.', 'Vader indet.', 'Scolopacidae, Indet.');
insert into species (id, norwegian, english, latin) values (9015, 'Ørn, ubest.', 'Eagle indet.', 'Haliaeetus / Aquila Sp.');
insert into species (id, norwegian, english, latin) values (9030, 'Lom, ubest.', 'Diver indet.', 'Gavia Sp.');
insert into species (id, norwegian, english, latin) values (9031, 'Gulnebblom/Islom', 'Great Norther/White-billed Diver', 'Gavia immer/adamsi');
insert into species (id, norwegian, english, latin) values (9040, 'Dykker, ubest.', 'Grebe indet.', 'Podicipediformes, Indet.');
insert into species (id, norwegian, english, latin) values (9045, 'Havsvale/Stormsvale', 'Leach''s Storm Petrel/Storm Petrel', 'Hydrobates pelagicus/Oceanodroma leucorhoa');
insert into species (id, norwegian, english, latin) values (9050, 'Skarv, ubest.', 'Cormorant/Shag', 'Phalacrocorax Sp.');
insert into species (id, norwegian, english, latin) values (9060, 'Gressand, ubest.', 'Dabbling duck indet.', 'Anas Sp.');
insert into species (id, norwegian, english, latin) values (9070, 'Dykkand, ubest.', 'Diving duck indet.', 'Aythya / Somateria / Clangula / Bucepha');
insert into species (id, norwegian, english, latin) values (9071, 'Ærfugl/Praktærfugl', 'Common/King Eider', 'Somateria mollissima/spectabilis');
insert into species (id, norwegian, english, latin) values (9072, 'Ærfugl/Sjøorre', 'Common Eider/Velvet Scooter', 'Somateria mollissima/Melanitta fusca');
insert into species (id, norwegian, english, latin) values (9073, 'Sjøorre / Svartand', 'Velvet Scooter/Common Scooter', 'Melanitta fuscus/ Melanitta nigra');
insert into species (id, norwegian, english, latin) values (9080, 'Fiskand, ubest.', 'Mergus', 'Mergus Sp.');
insert into species (id, norwegian, english, latin) values (9089, 'And ubest.', 'Duck Indet.', 'Anatidae Sp.');
insert into species (id, norwegian, english, latin) values (9090, 'Grå gås, ubest.', 'Grey Goose indet.', 'Anser Sp.');
insert into species (id, norwegian, english, latin) values (9100, 'Gås, ubest.', 'Goose indet.', 'Anser / Branta Sp.');
insert into species (id, norwegian, english, latin) values (9110, 'Svane, ubest.', 'Swan indet.', 'Cygnus Sp.');
insert into species (id, norwegian, english, latin) values (9135, 'Storfalk ubest.', 'Peregrine/Gyrfalcon', 'Falco peregrinus/F. rusticolus');
insert into species (id, norwegian, english, latin) values (9150, 'Lo, ubest.', 'Plover indet.', 'Charadrius / Pluvialis Sp.');
insert into species (id, norwegian, english, latin) values (9160, 'Bekkasin, ubest.', 'Snipe indet.', 'Lymnocryptes / Gallinago Sp.');
insert into species (id, norwegian, english, latin) values (9170, 'Småspove / storspove, ubest.', 'Curlew/Wimbrel', 'Numenius Sp.');
insert into species (id, norwegian, english, latin) values (9180, 'Svarthalespove / lappspove, ubest.', 'Godwit indet.', 'Limosa Sp.');
insert into species (id, norwegian, english, latin) values (9190, 'Storsnipe, ubest.', 'Large Vader indet.', 'Tringa Sp.');
insert into species (id, norwegian, english, latin) values (9195, 'Mellomstor vader ubest.', 'Medium Vader indet.', 'Calidris/Tringa Sp.');
insert into species (id, norwegian, english, latin) values (9200, 'Småsnipe, ubest.', 'Small Vader indet.', 'Calidris Sp.');
insert into species (id, norwegian, english, latin) values (9210, 'Måke, ubest.', 'Gull indet.', 'Larus Sp.');
insert into species (id, norwegian, english, latin) values (9215, 'Jo ubest.', 'Skua indet.', 'Stercorarius Sp.');
insert into species (id, norwegian, english, latin) values (9220, 'Terne, ubest.', 'Tern indet.', 'Sterna / Chlidonias Sp.');
insert into species (id, norwegian, english, latin) values (9225, 'Makrellterne/Rødnebbterne', 'Common/Arctic Tern', 'Sterna hirundo/S. paradisaea');
insert into species (id, norwegian, english, latin) values (9320, 'Rikse, ubest.', 'Rallidae', 'Rallus / Porzana Sp.');
insert into species (id, norwegian, english, latin) values (9340, 'Alke / lomvi, ubest.', 'Razorbill/Common Guillemot', 'Uria / Alca Sp.');
insert into species (id, norwegian, english, latin) values (9341, 'Alkefugl ubest.', 'Auk indet.', 'Alcidae');
insert into species (id, norwegian, english, latin) values (9390, 'Amerikapurpurhøne', 'American Purple Gallinule', 'Porphyrula martinica');
insert into species (id, norwegian, english, latin) values (9400, 'Brudeand', 'Wood Duck', 'Aix sponsa');
insert into species (id, norwegian, english, latin) values (9410, 'Vinhegre', 'Chinese Pond Heron', 'Ardela bacchus');
insert into species (id, norwegian, english, latin) values (9420, 'Ringand', 'Ring-necked Duck', 'Aythya collaris');
insert into species (id, norwegian, english, latin) values (9430, 'Mongollo', 'Lesser Sand Plover', 'Charadrius mongolus');
insert into species (id, norwegian, english, latin) values (9440, 'Langnebbekkasinsnipe', 'Long-billed Dowitcher', 'Limnodromus scolopaceus');
insert into species (id, norwegian, english, latin) values (9450, 'Dvergspove', 'Little Whimbrel', 'Numenius minutus');
insert into species (id, norwegian, english, latin) values (9460, 'Hvithalesvømmesnipe', 'Wilson''s Phalarope', 'Phalaropus tricolor');
insert into species (id, norwegian, english, latin) values (9470, 'Franklinmåke', 'Franklin''s Gull', 'Larus pipixcan');
insert into species (id, norwegian, english, latin) values (9480, 'Ringnebbmåke', 'Ring-billed Gull', 'Larus delawarensis');
insert into species (id, norwegian, english, latin) values (9490, 'Kongeterne', 'Royal Tern', 'Sterna maxima');
insert into species (id, norwegian, english, latin) values (9550, 'Asiasnipe', 'Long-toed Stint', 'Calidris subminuta');
insert into species (id, norwegian, english, latin) values (9640, 'Gråhodemåke', 'Grey-headed Gull', 'Larus cirrocephalus');
insert into species (id, norwegian, english, latin) values (9700, 'Ørkenlo', 'Greater Sandplover', 'Charadrius leschenaultii');
insert into species (id, norwegian, english, latin) values (9720, 'Hjelmfiskand', 'Hooded Merganser', 'Lophodytes cullatus');
insert into species (id, norwegian, english, latin) values (9740, 'Sørjo', 'Mccormick''s Skua', 'Stercorarius maccormicki');
insert into species (id, norwegian, english, latin) values (9750, 'Antarktispetrell', 'Antarctic Petrel', 'Thalassoica antarctica');
insert into species (id, norwegian, english, latin) values (9760, 'Snøpetrell', 'Snow Petrel', 'Pagodroma nivea');
insert into species (id, norwegian, english, latin) values (9770, 'Ringpingvin', 'Bearded Penguin', 'Pygoscelis antarctica');
insert into species (id, norwegian, english, latin) values (9780, 'Gulltoppingvin', 'Macaroni Penguin', 'Eudyptes chrysolophus');
insert into species (id, norwegian, english, latin) values (9820, 'Kittlitzlo', 'Kittlitz''s Plover', 'Charadriu pecuarius');
insert into species (id, norwegian, english, latin) values (9850, 'Stivhaleand', 'Ruddy Duck', 'Oxyura jamaicensis');
insert into species (id, norwegian, english, latin) values (9860, 'Rødfotsule', 'Red-Footed Booby', 'Sula sula');
insert into species (id, norwegian, english, latin) values (9870, 'Rødfotand', 'Amerikan Black Duck', 'Anas rubripes');
insert into species (id, norwegian, english, latin) values (9910, 'Sibirsnipe', 'Great Knot', 'Calidris tenuirostris');
insert into species (id, norwegian, english, latin) values (9920, 'Styltesnipe', 'Stilt Sandpiper', 'Calidris himantopus');
insert into species (id, norwegian, english, latin) values (9940, 'Kjempestormfugl', 'Southern Giant Petrel', 'Macronectes giganteus');
insert into species (id, norwegian, english, latin) values (9950, 'Sørhavhest', 'Southern Fulmar', 'Fulmarus glacialoides');
insert into species (id, norwegian, english, latin) values (9960, 'Svartbukstormsvale', 'Black-bellied Storm Petrel', 'Fregetta tropica');
insert into species (id, norwegian, english, latin) values (9970, 'Dominikanermåke', 'Southern Black-backed Gull', 'Larus dominicanus');
insert into species (id, norwegian, english, latin) values (9980, 'Antarktisterne', 'Swallow-tailed Tern', 'Sterna vittata');
insert into species (id, norwegian, english, latin) values (9981, 'Gyldenpipp', 'Goldpoop', 'Pippus goldensus');
insert into species (id, norwegian, english, latin) values (0, 'Masker IKKE ANALYSER', 'Mask DONT ANALYZE', 'mask');
insert into species (id, norwegian, english, latin) values (10001, 'Sau', 'Sheep', 'Ovis aries');