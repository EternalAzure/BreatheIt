import sqlite3


with sqlite3.connect("AirQuality.db") as conn:
    cursor = conn.cursor()
    cursor.executescript("""
    INSERT INTO units (name) VALUES ('μg/m3');
    INSERT INTO units (name) VALUES ('mg/m3');
    INSERT INTO units (name) VALUES ('g/m3');
    INSERT INTO units (name) VALUES ('kg/m3');
    INSERT INTO units (name) VALUES ('grains/m3');
    INSERT INTO units (name) VALUES ('Wh m-2');

    INSERT INTO variables (short_name, long_name) VALUES ('PM2.5', 'Particulate matter d < 2.5 µm (PM2.5)');
    INSERT INTO variables (short_name, long_name) VALUES ('PM2.5 Nitrate', 'PM2.5 Nitrate');
    INSERT INTO variables (short_name, long_name) VALUES ('PM2.5 Sulphate', 'PM2.5 Sulphate');
    INSERT INTO variables (short_name, long_name) VALUES ('PM2.5 REC', 'PM2.5 residential elementary carbon');
    INSERT INTO variables (short_name, long_name) VALUES ('PM2.5 TEC', 'PM2.5 total elementary carbon');
    INSERT INTO variables (short_name, long_name) VALUES ('PM2.5 SIA', 'PM2.5 secondary inorganic aerosol');
    INSERT INTO variables (short_name, long_name) VALUES ('PM2.5 TOM', 'PM2.5 total organic matter');
    INSERT INTO variables (short_name, long_name) VALUES ('PM10', 'Particulate matter d < 10 µm (PM10)');
    INSERT INTO variables (short_name, long_name) VALUES ('PM10 Dust', 'PM10 Dust');
    INSERT INTO variables (short_name, long_name) VALUES ('PM10 Salt', 'PM10 Sea salt (dry)');
    INSERT INTO variables (short_name, long_name) VALUES ('NH3', 'Ammonia');
    INSERT INTO variables (short_name, long_name) VALUES ('CO', 'Carbon monoxide');
    INSERT INTO variables (short_name, long_name) VALUES ('HCHO', 'Formaldehyde');
    INSERT INTO variables (short_name, long_name) VALUES ('OCHCHO', 'Glyoxal');
    INSERT INTO variables (short_name, long_name) VALUES ('NO2', 'Nitrogen dioxide');
    INSERT INTO variables (short_name, long_name) VALUES ('VOCs', 'Non-methane volatile organic compounds');
    INSERT INTO variables (short_name, long_name) VALUES ('O3', 'Ozone');
    INSERT INTO variables (short_name, long_name) VALUES ('NO + NO2', 'Peroxyacyl nitrates');
    INSERT INTO variables (short_name, long_name) VALUES ('SO2', 'Sulfur dioxide');
    INSERT INTO variables (short_name, long_name) VALUES ('Alder pollen', 'Alder pollen');
    INSERT INTO variables (short_name, long_name) VALUES ('Birch pollen', 'Birch pollen');
    INSERT INTO variables (short_name, long_name) VALUES ('Grass pollen', 'Grass pollen');
    INSERT INTO variables (short_name, long_name) VALUES ('Mugwort pollen', 'Mugwort pollen');
    INSERT INTO variables (short_name, long_name) VALUES ('Olive pollen', 'Olive pollen');
    INSERT INTO variables (short_name, long_name) VALUES ('Ragweed pollen', 'Ragweed pollen');
    """)
    conn.commit()
