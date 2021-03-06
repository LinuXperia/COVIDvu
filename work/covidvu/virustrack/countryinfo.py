#!/usr/bin/env python3
# See: https://github.com/pr3d4t0r/COVIDvu/blob/master/LICENSE 
# vim: set fileencoding=utf-8:


# covidvu.virustrack
# AWS Lambda Edge functions


import json


# --- constants ---

CF_VIEWER_COUNTRY = 'cloudfront-viewer-country'
COUNTRIES_INFO    = {'Afghanistan': {'capital': 'Kabul',
  'codeISO': 'AF',
  'languages': 'fa-AF,ps,uz-AF,tk',
  'region': 'Asia'},
 'Albania': {'capital': 'Tirana',
  'codeISO': 'AL',
  'languages': 'sq,el',
  'region': 'Europe'},
 'Algeria': {'capital': 'Algiers',
  'codeISO': 'DZ',
  'languages': 'ar-DZ',
  'region': 'Africa'},
 'Andorra': {'capital': 'Andorra la Vella',
  'codeISO': 'AD',
  'languages': 'ca',
  'region': 'Europe'},
 'Angola': {'capital': 'Luanda',
  'codeISO': 'AO',
  'languages': 'pt-AO',
  'region': 'Africa'},
 'Argentina': {'capital': 'Buenos Aires',
  'codeISO': 'AR',
  'languages': 'es-AR,en,it,de,fr,gn',
  'region': 'South America'},
 'Armenia': {'capital': 'Yerevan',
  'codeISO': 'AM',
  'languages': 'hy',
  'region': 'Asia'},
 'Australia': {'capital': 'Canberra',
  'codeISO': 'AU',
  'languages': 'en-AU',
  'region': 'Oceania'},
 'Austria': {'capital': 'Vienna',
  'codeISO': 'AT',
  'languages': 'de-AT,hr,hu,sl',
  'region': 'Europe'},
 'Azerbaijan': {'capital': 'Baku',
  'codeISO': 'AZ',
  'languages': 'az,ru,hy',
  'region': 'Asia'},
 'Bahamas': {'capital': 'Nassau',
  'codeISO': 'BS',
  'languages': 'en-BS',
  'region': 'Central America'},
 'Bahrain': {'capital': 'Manama',
  'codeISO': 'BH',
  'languages': 'ar-BH,en,fa,ur',
  'region': 'Asia'},
 'Bangladesh': {'capital': 'Dhaka',
  'codeISO': 'BD',
  'languages': 'bn-BD,en',
  'region': 'Asia'},
 'Barbados': {'capital': 'Bridgetown',
  'codeISO': 'BB',
  'languages': 'en-BB',
  'region': 'Central America'},
 'Belarus': {'capital': 'Minsk',
  'codeISO': 'BY',
  'languages': 'be,ru',
  'region': 'Europe'},
 'Belgium': {'capital': 'Brussels',
  'codeISO': 'BE',
  'languages': 'nl-BE,fr-BE,de-BE',
  'region': 'Europe'},
 'Belize': {'capital': 'Belmopan',
  'codeISO': 'BZ',
  'languages': 'en-BZ,es',
  'region': 'Central America'},
 'Benin': {'capital': 'Porto-Novo',
  'codeISO': 'BJ',
  'languages': 'fr-BJ',
  'region': 'Africa'},
 'Bhutan': {'capital': 'Thimphu',
  'codeISO': 'BT',
  'languages': 'dz',
  'region': 'Asia'},
 'Bolivia': {'capital': 'Sucre',
  'codeISO': 'BO',
  'languages': 'es-BO,qu,ay',
  'region': 'South America'},
 'Botswana': {'capital': 'Gaborone',
  'codeISO': 'BW',
  'languages': 'en-BW,tn-BW',
  'region': 'Africa'},
 'Brazil': {'capital': 'Brasilia',
  'codeISO': 'BR',
  'languages': 'pt-BR,es,en,fr',
  'region': 'South America'},
 'Brunei': {'capital': 'Bandar Seri Begawan',
  'codeISO': 'BN',
  'languages': 'ms-BN,en-BN',
  'region': 'Asia'},
 'Bulgaria': {'capital': 'Sofia',
  'codeISO': 'BG',
  'languages': 'bg,tr-BG,rom',
  'region': 'Europe'},
 'Burkina Faso': {'capital': 'Ouagadougou',
  'codeISO': 'BF',
  'languages': 'fr-BF',
  'region': 'Africa'},
 'Burundi': {'capital': 'Bujumbura',
  'codeISO': 'BI',
  'languages': 'fr-BI,rn',
  'region': 'Africa'},
 'Cambodia': {'capital': 'Phnom Penh',
  'codeISO': 'KH',
  'languages': 'km,fr,en',
  'region': 'Asia'},
 'Cameroon': {'capital': 'Yaounde',
  'codeISO': 'CM',
  'languages': 'en-CM,fr-CM',
  'region': 'Africa'},
 'Canada': {'capital': 'Ottawa',
  'codeISO': 'CA',
  'languages': 'en-CA,fr-CA,iu',
  'region': 'North America'},
 'Central African Republic': {'capital': 'Bangui',
  'codeISO': 'CF',
  'languages': 'fr-CF,sg,ln,kg',
  'region': 'Africa'},
 'Chad': {'capital': "N'Djamena",
  'codeISO': 'TD',
  'languages': 'fr-TD,ar-TD,sre',
  'region': 'Africa'},
 'Chile': {'capital': 'Santiago',
  'codeISO': 'CL',
  'languages': 'es-CL',
  'region': 'South America'},
 'China': {'capital': 'Beijing',
  'codeISO': 'CN',
  'languages': 'zh-CN,yue,wuu,dta,ug,za',
  'region': 'Mainland China'},
 'Colombia': {'capital': 'Bogota',
  'codeISO': 'CO',
  'languages': 'es-CO',
  'region': 'South America'},
 'Comoros': {'capital': 'Moroni',
  'codeISO': 'KM',
  'languages': 'ar,fr-KM',
  'region': 'Africa'},
 'Costa Rica': {'capital': 'San Jose',
  'codeISO': 'CR',
  'languages': 'es-CR,en',
  'region': 'Central America'},
 'Croatia': {'capital': 'Zagreb',
  'codeISO': 'HR',
  'languages': 'hr-HR,sr',
  'region': 'Europe'},
 'Cuba': {'capital': 'Havana',
  'codeISO': 'CU',
  'languages': 'es-CU',
  'region': 'Central America'},
 'Cyprus': {'capital': 'Nicosia',
  'codeISO': 'CY',
  'languages': 'el-CY,tr-CY,en',
  'region': 'Europe'},
 'Czechia': {'capital': 'Prague',
  'codeISO': 'CZ',
  'languages': 'cs,sk',
  'region': 'Europe'},
 'Denmark': {'capital': 'Copenhagen',
  'codeISO': 'DK',
  'languages': 'da-DK,en,fo,de-DK',
  'region': 'Europe'},
 'Djibouti': {'capital': 'Djibouti',
  'codeISO': 'DJ',
  'languages': 'fr-DJ,ar,so-DJ,aa',
  'region': 'Africa'},
 'Dominica': {'capital': 'Roseau',
  'codeISO': 'DM',
  'languages': 'en-DM',
  'region': 'Central America'},
 'Dominican Republic': {'capital': 'Santo Domingo',
  'codeISO': 'DO',
  'languages': 'es-DO',
  'region': 'Central America'},
 'Ecuador': {'capital': 'Quito',
  'codeISO': 'EC',
  'languages': 'es-EC',
  'region': 'South America'},
 'Egypt': {'capital': 'Cairo',
  'codeISO': 'EG',
  'languages': 'ar-EG,en,fr',
  'region': 'Africa'},
 'El Salvador': {'capital': 'San Salvador',
  'codeISO': 'SV',
  'languages': 'es-SV',
  'region': 'Central America'},
 'Equatorial Guinea': {'capital': 'Malabo',
  'codeISO': 'GQ',
  'languages': 'es-GQ,fr',
  'region': 'Africa'},
 'Eritrea': {'capital': 'Asmara',
  'codeISO': 'ER',
  'languages': 'aa-ER,ar,tig,kun,ti-ER',
  'region': 'Africa'},
 'Estonia': {'capital': 'Tallinn',
  'codeISO': 'EE',
  'languages': 'et,ru',
  'region': 'Europe'},
 'Ethiopia': {'capital': 'Addis Ababa',
  'codeISO': 'ET',
  'languages': 'am,en-ET,om-ET,ti-ET,so-ET,sid',
  'region': 'Africa'},
 'Fiji': {'capital': 'Suva',
  'codeISO': 'FJ',
  'languages': 'en-FJ,fj',
  'region': 'Oceania'},
 'Finland': {'capital': 'Helsinki',
  'codeISO': 'FI',
  'languages': 'fi-FI,sv-FI,smn',
  'region': 'Europe'},
 'France': {'capital': 'Paris',
  'codeISO': 'FR',
  'languages': 'fr-FR,frp,br,co,ca,eu,oc',
  'region': 'Europe'},
 'Gabon': {'capital': 'Libreville',
  'codeISO': 'GA',
  'languages': 'fr-GA',
  'region': 'Africa'},
 'Gambia': {'capital': 'Banjul',
  'codeISO': 'GM',
  'languages': 'en-GM,mnk,wof,wo,ff',
  'region': 'Africa'},
 'Georgia': {'capital': 'Tbilisi',
  'codeISO': 'GE',
  'languages': 'ka,ru,hy,az',
  'region': 'Europe'},
 'Germany': {'capital': 'Berlin',
  'codeISO': 'DE',
  'languages': 'de',
  'region': 'Europe'},
 'Ghana': {'capital': 'Accra',
  'codeISO': 'GH',
  'languages': 'en-GH,ak,ee,tw',
  'region': 'Africa'},
 'Greece': {'capital': 'Athens',
  'codeISO': 'GR',
  'languages': 'el-GR,en,fr',
  'region': 'Europe'},
 'Grenada': {'capital': "St. George's",
  'codeISO': 'GD',
  'languages': 'en-GD',
  'region': 'Central America'},
 'Guatemala': {'capital': 'Guatemala City',
  'codeISO': 'GT',
  'languages': 'es-GT',
  'region': 'Central America'},
 'Guinea': {'capital': 'Conakry',
  'codeISO': 'GN',
  'languages': 'fr-GN',
  'region': 'Africa'},
 'Guinea-Bissau': {'capital': 'Bissau',
  'codeISO': 'GW',
  'languages': 'pt-GW,pov',
  'region': 'Africa'},
 'Guyana': {'capital': 'Georgetown',
  'codeISO': 'GY',
  'languages': 'en-GY',
  'region': 'South America'},
 'Haiti': {'capital': 'Port-au-Prince',
  'codeISO': 'HT',
  'languages': 'ht,fr-HT',
  'region': 'Central America'},
 'Vatican City': {'capital': 'Vatican City',
  'codeISO': 'VA',
  'languages': 'la,it,fr',
  'region': 'Europe'},
 'Honduras': {'capital': 'Tegucigalpa',
  'codeISO': 'HN',
  'languages': 'es-HN',
  'region': 'Central America'},
 'Hungary': {'capital': 'Budapest',
  'codeISO': 'HU',
  'languages': 'hu-HU',
  'region': 'Europe'},
 'Iceland': {'capital': 'Reykjavik',
  'codeISO': 'IS',
  'languages': 'is,en,de,da,sv,no',
  'region': 'Europe'},
 'India': {'capital': 'New Delhi',
  'codeISO': 'IN',
  'languages': 'en-IN,hi,bn,te,mr,ta,ur,gu,kn,ml,or,pa,as,bh,sat,ks,ne,sd,kok,doi,mni,sit,sa,fr,lus,inc',
  'region': 'Asia'},
 'Indonesia': {'capital': 'Jakarta',
  'codeISO': 'ID',
  'languages': 'id,en,nl,jv',
  'region': 'Asia'},
 'Iran': {'capital': 'Tehran',
  'codeISO': 'IR',
  'languages': 'fa-IR,ku',
  'region': 'Asia'},
 'Iraq': {'capital': 'Baghdad',
  'codeISO': 'IQ',
  'languages': 'ar-IQ,ku,hy',
  'region': 'Asia'},
 'Ireland': {'capital': 'Dublin',
  'codeISO': 'IE',
  'languages': 'en-IE,ga-IE',
  'region': 'Europe'},
 'Israel': {'capital': 'Jerusalem',
  'codeISO': 'IL',
  'languages': 'he,ar-IL,en-IL,',
  'region': 'Asia'},
 'Italy': {'capital': 'Rome',
  'codeISO': 'IT',
  'languages': 'it-IT,de-IT,fr-IT,sc,ca,co,sl',
  'region': 'Europe'},
 'Jamaica': {'capital': 'Kingston',
  'codeISO': 'JM',
  'languages': 'en-JM',
  'region': 'Central America'},
 'Japan': {'capital': 'Tokyo',
  'codeISO': 'JP',
  'languages': 'ja',
  'region': 'Asia'},
 'Jordan': {'capital': 'Amman',
  'codeISO': 'JO',
  'languages': 'ar-JO,en',
  'region': 'Asia'},
 'Kazakhstan': {'capital': 'Astana',
  'codeISO': 'KZ',
  'languages': 'kk,ru',
  'region': 'Asia'},
 'Kenya': {'capital': 'Nairobi',
  'codeISO': 'KE',
  'languages': 'en-KE,sw-KE',
  'region': 'Africa'},
 'Kiribati': {'capital': 'Tarawa',
  'codeISO': 'KI',
  'languages': 'en-KI,gil',
  'region': 'Oceania'},
 'Kuwait': {'capital': 'Kuwait City',
  'codeISO': 'KW',
  'languages': 'ar-KW,en',
  'region': 'Asia'},
 'Kyrgyzstan': {'capital': 'Bishkek',
  'codeISO': 'KG',
  'languages': 'ky,uz,ru',
  'region': 'Asia'},
 'Laos': {'capital': 'Vientiane',
  'codeISO': 'LA',
  'languages': 'lo,fr,en',
  'region': 'Asia'},
 'Latvia': {'capital': 'Riga',
  'codeISO': 'LV',
  'languages': 'lv,ru,lt',
  'region': 'Europe'},
 'Lebanon': {'capital': 'Beirut',
  'codeISO': 'LB',
  'languages': 'ar-LB,fr-LB,en,hy',
  'region': 'Asia'},
 'Lesotho': {'capital': 'Maseru',
  'codeISO': 'LS',
  'languages': 'en-LS,st,zu,xh',
  'region': 'Africa'},
 'Liberia': {'capital': 'Monrovia',
  'codeISO': 'LR',
  'languages': 'en-LR',
  'region': 'Africa'},
 'Libya': {'capital': 'Tripoli',
  'codeISO': 'LY',
  'languages': 'ar-LY,it,en',
  'region': 'Africa'},
 'Liechtenstein': {'capital': 'Vaduz',
  'codeISO': 'LI',
  'languages': 'de-LI',
  'region': 'Europe'},
 'Lithuania': {'capital': 'Vilnius',
  'codeISO': 'LT',
  'languages': 'lt,ru,pl',
  'region': 'Europe'},
 'Luxembourg': {'capital': 'Luxembourg',
  'codeISO': 'LU',
  'languages': 'lb,de-LU,fr-LU',
  'region': 'Europe'},
 'Madagascar': {'capital': 'Antananarivo',
  'codeISO': 'MG',
  'languages': 'fr-MG,mg',
  'region': 'Africa'},
 'Malawi': {'capital': 'Lilongwe',
  'codeISO': 'MW',
  'languages': 'ny,yao,tum,swk',
  'region': 'Africa'},
 'Malaysia': {'capital': 'Kuala Lumpur',
  'codeISO': 'MY',
  'languages': 'ms-MY,en,zh,ta,te,ml,pa,th',
  'region': 'Asia'},
 'Maldives': {'capital': 'Male',
  'codeISO': 'MV',
  'languages': 'dv,en',
  'region': 'Asia'},
 'Mali': {'capital': 'Bamako',
  'codeISO': 'ML',
  'languages': 'fr-ML,bm',
  'region': 'Africa'},
 'Malta': {'capital': 'Valletta',
  'codeISO': 'MT',
  'languages': 'mt,en-MT',
  'region': 'Europe'},
 'Mauritania': {'capital': 'Nouakchott',
  'codeISO': 'MR',
  'languages': 'ar-MR,fuc,snk,fr,mey,wo',
  'region': 'Africa'},
 'Mauritius': {'capital': 'Port Louis',
  'codeISO': 'MU',
  'languages': 'en-MU,bho,fr',
  'region': 'Africa'},
 'Mexico': {'capital': 'Mexico City',
  'codeISO': 'MX',
  'languages': 'es-MX',
  'region': 'North America'},
 'Monaco': {'capital': 'Monaco',
  'codeISO': 'MC',
  'languages': 'fr-MC,en,it',
  'region': 'Europe'},
 'Mongolia': {'capital': 'Ulan Bator',
  'codeISO': 'MN',
  'languages': 'mn,ru',
  'region': 'Asia'},
 'Montenegro': {'capital': 'Podgorica',
  'codeISO': 'ME',
  'languages': 'sr,hu,bs,sq,hr,rom',
  'region': 'Europe'},
 'Morocco': {'capital': 'Rabat',
  'codeISO': 'MA',
  'languages': 'ar-MA,ber,fr',
  'region': 'Africa'},
 'Mozambique': {'capital': 'Maputo',
  'codeISO': 'MZ',
  'languages': 'pt-MZ,vmw',
  'region': 'Africa'},
 'Myanmar': {'capital': 'Nay Pyi Taw',
  'codeISO': 'MM',
  'languages': 'my',
  'region': 'Asia'},
 'Namibia': {'capital': 'Windhoek',
  'codeISO': 'NA',
  'languages': 'en-NA,af,de,hz,naq',
  'region': 'Africa'},
 'Nauru': {'capital': 'Yaren',
  'codeISO': 'NR',
  'languages': 'na,en-NR',
  'region': 'Oceania'},
 'Nepal': {'capital': 'Kathmandu',
  'codeISO': 'NP',
  'languages': 'ne,en',
  'region': 'Asia'},
 'Netherlands': {'capital': 'Amsterdam',
  'codeISO': 'NL',
  'languages': 'nl-NL,fy-NL',
  'region': 'Europe'},
 'New Zealand': {'capital': 'Wellington',
  'codeISO': 'NZ',
  'languages': 'en-NZ,mi',
  'region': 'Oceania'},
 'Nicaragua': {'capital': 'Managua',
  'codeISO': 'NI',
  'languages': 'es-NI,en',
  'region': 'Central America'},
 'Niger': {'capital': 'Niamey',
  'codeISO': 'NE',
  'languages': 'fr-NE,ha,kr,dje',
  'region': 'Africa'},
 'Nigeria': {'capital': 'Abuja',
  'codeISO': 'NG',
  'languages': 'en-NG,ha,yo,ig,ff',
  'region': 'Africa'},
 'Norway': {'capital': 'Oslo',
  'codeISO': 'NO',
  'languages': 'no,nb,nn,se,fi',
  'region': 'Europe'},
 'Oman': {'capital': 'Muscat',
  'codeISO': 'OM',
  'languages': 'ar-OM,en,bal,ur',
  'region': 'Asia'},
 'Pakistan': {'capital': 'Islamabad',
  'codeISO': 'PK',
  'languages': 'ur-PK,en-PK,pa,sd,ps,brh',
  'region': 'Asia'},
 'Panama': {'capital': 'Panama City',
  'codeISO': 'PA',
  'languages': 'es-PA,en',
  'region': 'Central America'},
 'Paraguay': {'capital': 'Asuncion',
  'codeISO': 'PY',
  'languages': 'es-PY,gn',
  'region': 'South America'},
 'Peru': {'capital': 'Lima',
  'codeISO': 'PE',
  'languages': 'es-PE,qu,ay',
  'region': 'South America'},
 'Philippines': {'capital': 'Manila',
  'codeISO': 'PH',
  'languages': 'tl,en-PH,fil',
  'region': 'Asia'},
 'Poland': {'capital': 'Warsaw',
  'codeISO': 'PL',
  'languages': 'pl',
  'region': 'Europe'},
 'Portugal': {'capital': 'Lisbon',
  'codeISO': 'PT',
  'languages': 'pt-PT,mwl',
  'region': 'Europe'},
 'Qatar': {'capital': 'Doha',
  'codeISO': 'QA',
  'languages': 'ar-QA,es',
  'region': 'Asia'},
 'Moldova': {'capital': 'Chisinau',
  'codeISO': 'MD',
  'languages': 'ro,ru,gag,tr',
  'region': 'Europe'},
 'Romania': {'capital': 'Bucharest',
  'codeISO': 'RO',
  'languages': 'ro,hu,rom',
  'region': 'Europe'},
 'Russia': {'capital': 'Moscow',
  'codeISO': 'RU',
  'languages': 'ru,tt,xal,cau,ady,kv,ce,tyv,cv,udm,tut,mns,bua,myv,mdf,chm,ba,inh,tut,kbd,krc,av,sah,nog',
  'region': 'Europe'},
 'Rwanda': {'capital': 'Kigali',
  'codeISO': 'RW',
  'languages': 'rw,en-RW,fr-RW,sw',
  'region': 'Africa'},
 'San Marino': {'capital': 'San Marino',
  'codeISO': 'SM',
  'languages': 'it-SM',
  'region': 'Europe'},
 'Saudi Arabia': {'capital': 'Riyadh',
  'codeISO': 'SA',
  'languages': 'ar-SA',
  'region': 'Asia'},
 'Senegal': {'capital': 'Dakar',
  'codeISO': 'SN',
  'languages': 'fr-SN,wo,fuc,mnk',
  'region': 'Africa'},
 'Serbia': {'capital': 'Belgrade',
  'codeISO': 'RS',
  'languages': 'sr,hu,bs,rom',
  'region': 'Europe'},
 'Seychelles': {'capital': 'Victoria',
  'codeISO': 'SC',
  'languages': 'en-SC,fr-SC',
  'region': 'Africa'},
 'Sierra Leone': {'capital': 'Freetown',
  'codeISO': 'SL',
  'languages': 'en-SL,men,tem',
  'region': 'Africa'},
 'Singapore': {'capital': 'Singapore',
  'codeISO': 'SG',
  'languages': 'cmn,en-SG,ms-SG,ta-SG,zh-SG',
  'region': 'Asia'},
 'Slovakia': {'capital': 'Bratislava',
  'codeISO': 'SK',
  'languages': 'sk,hu',
  'region': 'Europe'},
 'Slovenia': {'capital': 'Ljubljana',
  'codeISO': 'SI',
  'languages': 'sl,sh',
  'region': 'Europe'},
 'Somalia': {'capital': 'Mogadishu',
  'codeISO': 'SO',
  'languages': 'so-SO,ar-SO,it,en-SO',
  'region': 'Africa'},
 'South Africa': {'capital': 'Pretoria',
  'codeISO': 'ZA',
  'languages': 'zu,xh,af,nso,en-ZA,tn,st,ts,ss,ve,nr',
  'region': 'Africa'},
 'South Sudan': {'capital': 'Juba',
  'codeISO': 'SS',
  'languages': 'en',
  'region': 'Africa'},
 'Spain': {'capital': 'Madrid',
  'codeISO': 'ES',
  'languages': 'es-ES,ca,gl,eu,oc',
  'region': 'Europe'},
 'Sri Lanka': {'capital': 'Colombo',
  'codeISO': 'LK',
  'languages': 'si,ta,en',
  'region': 'Asia'},
 'Palestine': {'capital': 'East Jerusalem',
  'codeISO': 'PS',
  'languages': 'ar-PS',
  'region': 'Asia'},
 'Sudan': {'capital': 'Khartoum',
  'codeISO': 'SD',
  'languages': 'ar-SD,en,fia',
  'region': 'Africa'},
 'Suriname': {'capital': 'Paramaribo',
  'codeISO': 'SR',
  'languages': 'nl-SR,en,srn,hns,jv',
  'region': 'South America'},
 'Sweden': {'capital': 'Stockholm',
  'codeISO': 'SE',
  'languages': 'sv-SE,se,sma,fi-SE',
  'region': 'Europe'},
 'Switzerland': {'capital': 'Bern',
  'codeISO': 'CH',
  'languages': 'de-CH,fr-CH,it-CH,rm',
  'region': 'Europe'},
 'Syria': {'capital': 'Damascus',
  'codeISO': 'SY',
  'languages': 'ar-SY,ku,hy,arc,fr,en',
  'region': 'Asia'},
 'Tajikistan': {'capital': 'Dushanbe',
  'codeISO': 'TJ',
  'languages': 'tg,ru',
  'region': 'Asia'},
 'Thailand': {'capital': 'Bangkok',
  'codeISO': 'TH',
  'languages': 'th,en',
  'region': 'Asia'},
 'Timor-Leste': {'capital': 'Dili',
  'codeISO': 'TL',
  'languages': 'tet,pt-TL,id,en',
  'region': 'Asia'},
 'Togo': {'capital': 'Lome',
  'codeISO': 'TG',
  'languages': 'fr-TG,ee,hna,kbp,dag,ha',
  'region': 'Africa'},
 'Tonga': {'capital': "Nuku'alofa",
  'codeISO': 'TO',
  'languages': 'to,en-TO',
  'region': 'Oceania'},
 'Tunisia': {'capital': 'Tunis',
  'codeISO': 'TN',
  'languages': 'ar-TN,fr',
  'region': 'Africa'},
 'Turkey': {'capital': 'Ankara',
  'codeISO': 'TR',
  'languages': 'tr-TR,ku,diq,az,av',
  'region': 'Europe'},
 'Turkmenistan': {'capital': 'Ashgabat',
  'codeISO': 'TM',
  'languages': 'tk,ru,uz',
  'region': 'Asia'},
 'Tuvalu': {'capital': 'Funafuti',
  'codeISO': 'TV',
  'languages': 'tvl,en,sm,gil',
  'region': 'Oceania'},
 'Uganda': {'capital': 'Kampala',
  'codeISO': 'UG',
  'languages': 'en-UG,lg,sw,ar',
  'region': 'Africa'},
 'Ukraine': {'capital': 'Kiev',
  'codeISO': 'UA',
  'languages': 'uk,ru-UA,rom,pl,hu',
  'region': 'Europe'},
 'United Arab Emirates': {'capital': 'Abu Dhabi',
  'codeISO': 'AE',
  'languages': 'ar-AE,fa,en,hi,ur',
  'region': 'Asia'},
 'Tanzania': {'capital': 'Dodoma',
  'codeISO': 'TZ',
  'languages': 'sw-TZ,en,ar',
  'region': 'Africa'},
 'US': {'capital': 'Washington',
  'codeISO': 'US',
  'languages': 'en-US,es-US,haw,fr',
  'region': 'North America'},
 'Uruguay': {'capital': 'Montevideo',
  'codeISO': 'UY',
  'languages': 'es-UY',
  'region': 'South America'},
 'Uzbekistan': {'capital': 'Tashkent',
  'codeISO': 'UZ',
  'languages': 'uz,ru,tg',
  'region': 'Asia'},
 'Vanuatu': {'capital': 'Port Vila',
  'codeISO': 'VU',
  'languages': 'bi,en-VU,fr-VU',
  'region': 'Oceania'},
 'Venezuela': {'capital': 'Caracas',
  'codeISO': 'VE',
  'languages': 'es-VE',
  'region': 'South America'},
 'Vietnam': {'capital': 'Hanoi',
  'codeISO': 'VN',
  'languages': 'vi,en,fr,zh,km',
  'region': 'Asia'},
 'Yemen': {'capital': 'Sanaa',
  'codeISO': 'YE',
  'languages': 'ar-YE',
  'region': 'Asia'},
 'Zambia': {'capital': 'Lusaka',
  'codeISO': 'ZM',
  'languages': 'en-ZM,bem,loz,lun,lue,ny,toi',
  'region': 'Africa'},
 'Zimbabwe': {'capital': 'Harare',
  'codeISO': 'ZW',
  'languages': 'en-ZW,sn,nr,nd',
  'region': 'Africa'},
 'Congo (Kinshasa)': {'capital': 'Kinshasa',
  'codeISO': 'CD',
  'languages': 'fr-CD,ln,kg',
  'region': 'Africa'},
 'Congo (Brazzaville)': {'capital': 'Brazzaville',
  'codeISO': 'CG',
  'languages': 'fr-CG,kg,ln-CG',
  'region': 'Africa'},
 "Cote d'Ivoire": {'capital': 'Yamoussoukro',
  'codeISO': 'CI',
  'languages': 'fr-CI',
  'region': 'Africa'},
 'Taiwan*': {'capital': 'Taipei',
  'codeISO': 'TW',
  'languages': 'zh-TW,zh,nan,hak',
  'region': 'Asia'},
 'Bosnia and Herzegovina': {'capital': 'Sarajevo',
  'codeISO': 'BA',
  'languages': 'bs,hr-BA,sr-BA',
  'region': 'Europe'},
 'Korea, North': {'capital': 'Pyongyang',
  'codeISO': 'KP',
  'languages': 'ko-KP',
  'region': 'Asia'},
 'Korea, South': {'capital': 'Seoul',
  'codeISO': 'KR',
  'languages': 'ko-KR,en',
  'region': 'Asia'},
 'North Macedonia': {'capital': 'Skopje',
  'codeISO': 'MK',
  'languages': 'mk,sq,tr,rmm,sr',
  'region': 'Europe'},
 'United Kingdom': {'capital': 'London',
  'codeISO': 'GB',
  'languages': 'en-GB,cy-GB,gd',
  'region': 'Europe'}
}
CODES_COUNTRIES = dict([(item[1]['codeISO'], item[0]) for item in COUNTRIES_INFO.items()])
ISO_CODE_REF    = 'codeISO'
TOTAL_US_NAME   = '!Total US'
US_REGIONS      = {
    TOTAL_US_NAME: TOTAL_US_NAME,
    'Alabama': 'South',
    'Alaska': 'West',
    'American Samoa': 'Other',
    'Arizona': 'West',
    'Arkansas': 'South',
    'California': 'West',
    'Colorado': 'West',
    'Connecticut': 'Northeast',
    'Delaware': 'South',
    'District of Columbia': 'South',
    'Florida': 'South',
    'Georgia': 'South',
    'Hawaii': 'West',
    'Idaho': 'West',
    'Illinois': 'Midwest',
    'Indiana': 'Midwest',
    'Iowa': 'Midwest',
    'Kansas': 'Midwest',
    'Kentucky': 'South',
    'Louisiana': 'South',
    'Maine': 'Northeast',
    'Maryland': 'Northeast',
    'Massachusetts': 'Northeast',
    'Michigan': 'Midwest',
    'Minnesota': 'Midwest',
    'Mississippi': 'Midwest',
    'Missouri': 'South',
    'Montana': 'Midwest',
    'Nebraska': 'Midwest',
    'Nevada': 'West',
    'New Hampshire': 'Northeast',
    'New Jersey': 'Northeast',
    'New Mexico': 'West',
    'New York': 'Northeast',
    'North Carolina': 'South',
    'North Dakota': 'Midwest',
    'Ohio': 'Midwest',
    'Oklahoma': 'Midwest',
    'Oregon': 'West',
    'Pennsylvania': 'Northeast',
    'Rhode Island': 'Northeast',
    'South Carolina': 'South',
    'South Dakota': 'Midwest',
    'Tennessee': 'South',
    'Texas': 'South',
    'Utah': 'West',
    'Vermont': 'Northeast',
    'Virginia': 'South',
    'Washington': 'West',
    'West Virginia': 'South',
    'Wisconsin': 'Midwest',
    'Wyoming': 'West',
    'Guam': 'Other',
    'Marshall Islands': 'Other',
    'Micronesia': 'Other',
    'Palau': 'Other',
    'Puerto Rico': 'Other',
    'Virgin Islands': 'Other',
    'Marianas': 'Other',
}




def lambdaHandler(event, context):
    request     = event['Records'][0]['cf']['request']
    headers     = request['headers']
    countryCode = headers.get(CF_VIEWER_COUNTRY)[0]['value']

    responseBody = {
        ISO_CODE_REF: countryCode,
        'name': CODES_COUNTRIES[countryCode],
    }
    
    return {
         'status': '200',
         'statusDescription': 'OK',
         'headers': {
             'cache-control': [
                 {
                     'key': 'Cache-Control',
                     'value': 'max-age=3600'
                 }
             ],
             'content-encoding': [
                 {
                     'key': 'Content-Encoding',
                     'value': 'UTF-8'
                 }
             ],
             "content-type": [
                 {
                     'key': 'Content-Type',
                     'value': 'application/json'
                 }
             ],
         },
         'body': json.dumps(responseBody)
     }


def generateCodesAndCountriesTable():
    return json.dumps(CODES_COUNTRIES)

