USE MarketWatch;
CREATE TABLE IF NOT EXISTS financial_data (
       id INT(11) NOT NULL AUTO_INCREMENT,
       company_name VARCHAR(100),
       company_tick VARCHAR(10),
       report_date DATE,
       metrics VARCHAR(100),
       metrics_value INT,
       metrics_unit VARCHAR(5),
       PRIMARY KEY (id)
) ENGINE=InnoDB;
