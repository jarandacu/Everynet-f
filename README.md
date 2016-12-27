Necessary steps to run the application
==========================================

*** 0. Go to dashboard ***

https://my.everynet.com demo@everynet.com demodemo



**1. Install required python packets**
```bash
pip install -r requirements.txt
```

**2. Run Redis**

**3. Create mysql database ant table **
```sql
CREATE DATABASE lora;
CREATE TABLE packets (
    `packet_id` INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `dev_eui` VARCHAR(32) NOT NULL,
    `dev_addr` VARCHAR(16) NOT NULL,
    `rx_time` INT(11) NOT NULL,
    `counter_up` INT NOT NULL,
    `port` INT NOT NULL,
    `encrypted_payload` VARCHAR(1024) NULL,
    `payload` VARCHAR(1024) NULL
);
```
