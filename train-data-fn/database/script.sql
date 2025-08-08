CREATE TABLE TrainDepartures (
    id INT IDENTITY(1,1) PRIMARY KEY,
    -- Infos station
    stationId NVARCHAR(100),
    stationName NVARCHAR(100),
    standardStationName NVARCHAR(100),
    longitude FLOAT,
    latitude FLOAT,
    iriUrl NVARCHAR(200),

    -- Infos train
    vehicle NVARCHAR(50),
    trainType NVARCHAR(20),
    trainNumber NVARCHAR(20),
    platform NVARCHAR(10),
    time DATETIME,
    delaySeconds INT,
    canceled BIT
);

CREATE TABLE TrainConnections (
    id INT IDENTITY(1,1) PRIMARY KEY,
    departureStation NVARCHAR(100),
    arrivalStation NVARCHAR(100),
    departureTime DATETIME,
    arrivalTime DATETIME,
    duration NVARCHAR(20),
    trainVehicle NVARCHAR(50),
    numberOfVias INT
);

CREATE TABLE Disturbances (
    id INT PRIMARY KEY,
    title NVARCHAR(MAX),
    description NVARCHAR(MAX),
    type NVARCHAR(50),
    timestamp DATETIME,
    link NVARCHAR(MAX),
    attachment NVARCHAR(MAX)
);
