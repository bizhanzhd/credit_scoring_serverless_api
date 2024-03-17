# Mapper version 1.0

import datetime

class Mapper:

    def __init__(self) -> None:
        self.date = datetime.datetime.now()

    def japan_date_to_days(self, date_int:int) -> int:
        date_int = str(date_int)
        year_ = int(date_int[0:4])
        month_ = int(date_int[4:6])
        day_ = int(date_int[6:8])

        year = (self.date.year - year_) * 365
        month = (self.date.month - month_) * 30
        day = (self.date.day - day_)
        total_days = year + month + day

        return total_days

    def date_to_days(self, date_str:str) -> int:
        lista = date_str.split("-")
        year_ = lista[0]
        month_ = lista[1]
        day_ = lista[2]

        year = (self.date.year - year_) * 365
        month = (self.date.month - month_) * 30
        day = (self.date.day - day_)
        total_days = year + month + day
        
        return total_days

    def residence_to_region_id(self, region:str) -> int:
        
        mapn = {
            'piemonte': 1,
            'valle daosta': 2,
            'lombardia': 3,
            'trentino alto adige': 4,
            'veneto': 5,
            'friuli venezia giulia': 6,
            'liguria': 7,
            'emilia romagna': 8,
            'toscana': 9,
            'umbria': 10,
            'marche': 11,
            'lazio': 12,           
            'abruzzo': 13,
            'molise': 14,
            'campania': 15,
            'puglia': 16,
            'basilicata': 17,
            'calabria': 18,
            'sicilia': 19,
            'sardegna': 20
            }

        istat_id = mapn[region]
        return istat_id

    def region_id_to_residence(self, region_id:int) -> str:
        
        mapn = {
            1 : 'piemonte',
            2 : 'valle daosta',
            3 : 'lombardia',
            4 : 'trentino alto adige',
            5 : 'veneto',
            6 : 'friuli venezia giulia',
            7 : 'liguria',
            8 : 'emilia romagna',
            9 : 'toscana',
            10 : 'umbria',
            11 : 'marche',
            12 : 'lazio',           
            13 : 'abruzzo',
            14 : 'molise',
            15 : 'campania',
            16 : 'puglia',
            17 : 'basilicata',
            18 : 'calabria',
            19 : 'sicilia',
            20 : 'sardegna'
            }

        region = mapn[region_id]
        return region

    def gender_to_gender_id(self, gender:str) -> int:

        mapn = {
            "m" : 1,
            "f" : 2,
            "o" : 3
        }
        
        gender_id = mapn[gender]
        return gender_id

    def gender_id_to_gender(self, gender_id:int) -> str:

        mapn = {
            1 : "m",
            2 : "f",
            3 : "o"
        }
        
        gender = mapn[gender_id]
        return gender

    def profession_to_profession_id(self, profession:str) -> int:
        mapn = {
            "dipendente a tempo determinato" : 1,
            "dipendente a tempo indeterminato" : 2,
            "imprenditore" : 3,
            "libero professionista" : 4,
            "consulente con partita IVA" : 5,
            "pensionato" : 6,
            "studente" : 7,
            "non occupato" : 7
        }
        profession_id = mapn[profession]
        return profession_id

    def profession_id_to_profession(self, profession_id:int) -> str:
        mapn = {
            1 : "dipendente a tempo determinato",
            2 : "dipendente a tempo indeterminato",
            3 : "imprenditore",
            4 : "libero professionista",
            5 : "consulente con partita IVA",
            6 : "pensionato",
            7 : "non occupato"
        }
        profession = mapn[profession_id]
        return profession

    def education_to_education_id(self, education:str) -> int:
        mapn = {
            "no education" : 1,
            "scuola primaria" : 2,
            "scuola secondaria di I grado" : 3,
            "scuola professionale" : 4,
            "scuola secondaria di II grado" : 5,
            "laurea" : 6,
            "master di II livello e PHD" : 7
        }
        education_id = mapn[education]
        return education_id

    def education_id_to_education(self, education_id:int) -> str:
        mapn = {
            1 : "none",
            2 : "scuola primaria",
            3 : "scuola secondaria di I grado",
            4 : "scuola professionale",
            5 : "scuola secondaria di II grado",
            6 : "laurea",
            7 : "master di II livello e PHD"
        }
        education = mapn[education_id]
        return education

    def sector_to_sector_id(self, sector:str) -> int:
        mapn = {
            "istruzione e formazione" : 1,
            "industria manufatturiera" : 2,
            "banca assicurazione e servizi finanziari" : 3,
            "tecnologia" : 4,
            "servizi immobiliari" : 5,
            "costruzioni" : 6,
            "trasporti e logistica" : 7,
            "turismo moda sport e tempo libero" : 8,
            "consulenza e servizi manageriali" : 9,
            "servizi medico sanitari" : 10,
            "design architettura e arti creative" : 11,
            "forze armate e forze dellordine" : 12,
            "commercio al dettaglio" : 13,
            "telecomunicazioni energia servizi di pubblica utilità" : 14,
            "settore legale" : 15,
            "servizi di assistenza sociale" : 16,
            "agricoltura, silvicoltura, pesca" : 17,
            "altro" : 18
        }
        sector_id = mapn[sector]
        return sector_id

    def sector_id_to_sector(self, sector_id:int) -> str:
        mapn = {
            1 : "istruzione e formazione",
            2 : "industria manufatturiera",
            3 : "banca assicurazione e servizi finanziari",
            4 : "tecnologia",
            5 : "servizi immobiliari",
            6 : "costruzioni",
            7 : "trasporti e logistica",
            8 : "turismo moda sport e tempo libero",
            9 : "consulenza e servizi manageriali",
            10 : "servizi medico sanitari",
            11 : "design architettura e arti creative",
            12 : "forze armate e forze dellordine",
            13 : "commercio al dettaglio",
            14 : "telecomunicazioni energia servizi di pubblica utilità",
            15 : "settore legale",
            16 : "servizi di assistenza sociale",
            17 : "agricoltura, silvicoltura, pesca",
            18 : "commercialisti e fiscalisti",
            19 : "altro"
        }
        sector = mapn[sector_id]
        return sector

    def merchant_to_merchant_id(self, merchant:str) -> int:
        mapn = {
            "avvocato" : 1,
            "oculista" : 2,
            "dentista" : 3,
            "commercialista" : 4,
            "notaio" : 5
        }
        merchant_id = mapn[merchant]
        return merchant_id
    
    def merchant_id_to_merchant(self, merchant_id:int) -> str:
        mapn = {
            1 : "avvocato",
            2 : "oculista",
            3 : "dentista",
            4 : "commercialista",
            5 : "notaio"
        }
        merchant = mapn[merchant_id]
        return merchant

    def device_to_device_id(self, device:str) -> int:
        mapn = {
            "samsung" : 1,
            "apple" : 2,
			"huawei" : 3,
            "xiaomi" : 4,
			"oppo" : 5,
            "motorola" : 6,
			"realme" : 7,
			"onepluse" : 8,
			"blackview" : 9,
			"htc" : 10,
			"nothing" : 11,
			"razer" : 12,
			"asus" : 13,
			"acer" : 14,
			"altro" : 15
        }
        device_id = mapn[device]
        return device_id

    def device_id_to_device(self, device_id:int) -> str:
        mapn = {
            1 : "samsung",
            2 : "apple",
			3 : "huawei",
            4 : "xiaomi",
			5 : "oppo",
            6 : "motorola",
			7 : "realme",
			8 : "onepluse",
			9 : "blackview",
			10 : "htc",
			11 : "nothing",
			12 : "razer",
			13 : "asus",
			14 : "acer",
			15 : "altro"
        }
        device = mapn[device_id]
        return device
