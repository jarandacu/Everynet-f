CREATE DATABASE IF NOT EXISTS lora;
USE lora;
CREATE TABLE IF NOT EXISTS packets (
    `packet_id`         INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `dev_eui`           VARCHAR(32) NOT NULL,
    `dev_addr`          VARCHAR(16) NOT NULL,
    `rx_time`           INT(11) NOT NULL,
    `counter_up`        INT NOT NULL,
    `port`              INT NOT NULL,
    `encrypted_payload` VARCHAR(1024) NULL,
    `payload`           VARCHAR(1024) NULL,

    `rssi`              INT   NULL,
    `lsnr`              FLOAT NULL,

    `group`             VARCHAR(32) NULL
);
