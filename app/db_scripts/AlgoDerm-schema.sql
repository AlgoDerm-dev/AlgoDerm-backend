CREATE TABLE patient
    (patient_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_fname VARCHAR(100),
    patient_lname VARCHAR(100),
    patient_gender VARCHAR(10),
    patient_complexion VARCHAR(100),
    patient_race VARCHAR (100),
    patient_location VARCHAR(100));
CREATE TABLE new_image
            (img_id INT AUTO_INCREMENT PRIMARY KEY,
            patient_id INT,
            img_name VARCHAR(100),
            img_location VARCHAR(100),
            img_date DATE,
            img_dbmatchid INT,
            FOREIGN KEY (patient_id) REFERENCES patient(patient_id));
CREATE TABLE description
            (img_id INT,
            des_size VARCHAR(100),
            des_description VARCHAR(100),
            des_color VARCHAR(100),
            des_3D VARCHAR(2),
            des_locationOnBody INT,
            FOREIGN KEY (img_id) REFERENCES new_image(img_id));
 CREATE TABLE db_image
            (dbimg_diseasedID INT AUTO_INCREMENT PRIMARY KEY,
            img_dbmatchid INT,
            FOREIGN KEY (img_dbmatchid) REFERENCES new_image(img_dbmatchid));