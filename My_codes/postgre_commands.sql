-- # Insert data to a table from csv file
copy <schema>.signposts(country,dataset,signpost_id)
from 'D:\14_buildings_layer\XX_temp\PostgreSQL\signpost_test.csv' DELIMITER ',' CSV HEADER<optional>;


-- # Create new table from scratch
create table signposts (
    country varchar(3) NOT NULL,
    dataset varchar(3) NOT NULL,
    signpost_id varchar(15) primary key
);


-- # New table as a copy of another table
create table _si_2018_03_eur.signposts as
  select * from public.signposts;
  
  
create table manual_corrections (
    region varchar(3) NOT NULL,
    country varchar(3) NOT NULL,
    dataset varchar(3) NOT NULL,
    signpost_id varchar(15) primary key,
    description varchar(100) not null,
    release_id varchar(7) not null,
    
select cou.country_full as Country_name, count(cor.signpost_id) as Total_corrections
from <schema>.manual_corrections cor
join <schema>.countries cou
on cor.country = cou.country
group by Country_name
order by Total_corrections desc;

_____

create table <schema>.manual_corrections (
    region varchar(3) NOT NULL,
    country varchar(3) NOT NULL,
    dataset varchar(3) NOT NULL,
    signpost_id varchar(15) primary key,
    description varchar(200) not null,
    release_id varchar(7) not null,
    edit_time varchar(35)
);

create table <schema>.countries (
    country varchar(3) PRIMARY KEY,
    country_full varchar(30) not null
);

create table <schema>.signposts (
    country varchar(3) NOT NULL,
    dataset varchar(3) NOT NULL,
    signpost_id varchar(15) not null,
    primary key (dataset, signpost_id)
);

create table _si_2018_03_eur.cords (
    signpost_id varchar(15),
    xcor varchar(12) not null,
    ycor varchar(12) not null,
    yx varchar(26) not null,
    id serial not null primary key
);

--# Extract coordinates out of geometry
select feat_id, ST_AsText(geom), ST_Y(geom), ST_X(geom) from _2018_03_004_nam_usa_uar.mnr_maneuver;

--# Add column
alter table _manual_corrections.manual_corrections add column edit_time DATE DEFAULT CURRENT_DATE;

--# Remove a record
delete from _manual_corrections.manual_corrections where signpost_id = '111222333';

--# Insert a record
insert into _manual_corrections.manual_corrections(region,country,dataset,signpost_id,description,release_id)
values ('NAM','USA','ui2','111222333','this is a test','2018.03');