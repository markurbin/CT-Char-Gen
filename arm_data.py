branches = ('Imperial Army', 'Imperial Marines', 'Imperial Navy')
arms = ('Infantry', 'Cavalry', 'Artillery', 'Support', 'Commando')
arm_Table = {}
arm_Table['Infantry'] = {
  "mos": ['Gun Cmbt', 'Gun Cmbt', 'Hvy Wpns', 'Hvy Wpns', 'Vehicle', 'Recon', 'Vac Suit'],
  # general assignment
  "ga":  ['Command', 'Command', 'Command', 'Command', 'Staff', 'Staff', 'Special', 'Special'],
  # unit assignment
  "ua":  ['Raid', 'Trng', 'Ctr Ins', 'Ctr Ins', 'Garr', 'Garr', 'Garr', 'Trng', 'Pol Act', 'Intl Sec', 'Intl Sec']
}
arm_Table['Cavalry'] = {
  "mos": ['Vehicle', 'Vehicle', 'Vehicle', 'Hvy Wpns', 'Hvy Wpns', 'Mechanical', 'Computer'],
  "ga":  ['Command', 'Command', 'Command', 'Command', 'Staff', 'Staff', 'Special', 'Special'],
  "ua":  ['Raid', 'Trng', 'Ctr Ins', 'Pol Act', 'Garr', 'Garr', 'Garr', 'Trng', 'Pol Act', 'Intl Sec', 'Trng']
}
arm_Table['Artillery'] = {
  "mos": ['FA Gunner', 'FA Gunner', 'Vehicle', 'Mechanical', 'Fwd Obs', 'Computer', 'Electronics'],
  "ga":  ['Command', 'Command', 'Command', 'Staff', 'Staff', 'Staff', 'Special', 'Special'],
  "ua":  ['Raid', 'Trng', 'Ctr Ins', 'Pol Act', 'Garr', 'Garr', 'Garr', 'Trng', 'Pol Act', 'Ctr Ins', 'Trng']
}
arm_Table['Support'] = {
  "mos": ['Vehicle', 'Cmbt Eng', 'Vehicle', 'Mechanical', 'Electronics', 'Medic', 'Computer'],
  "ga":  ['Command', 'Command', 'Staff', 'Staff', 'Staff', 'Staff', 'Special', 'Special'],
  "ua":  ['Raid', 'Intl Sec', 'Ctr Ins', 'Garr', 'Garr', 'Garr', 'Garr', 'Trng', 'Pol Act', 'Intl Sec', 'Pol Act', ]
}
arm_Table['Commando'] = {
  "mos": ['Gun Cmbt', 'Gun Cmbt', 'Hvy Wpns', 'Demolition', 'Survival', 'Recon', 'Battle dress'],
  "ga":  ['Command', 'Command', 'Command', 'Command', 'Staff', 'Special', 'Special'],
  "ua":  ['Raid', 'Raid', 'Ctr Ins', 'Pol Act', 'Intl Sec', 'Garr', 'Trng', 'Trng', 'Ctr Ins', 'Raid', 'Raid']
}

marine_Table = {
  "mos": ['Gun Cmbt', 'Gun Cmbt', 'Zero-G', 'Zero-G', 'Hvy Wpns', 'Fwd Obs', 'Battle dress'],
  "ga":  ['Command', 'Command', 'Command', 'Command', 'Staff', 'Staff', 'Special', 'Special'],
  "ua":  ['Raid', 'Raid', 'Ctr Ins', 'Intl Sec', 'Shp Trp', 'Garr', 'Shp Trp', 'Trng', 'Ctr Ins', 'Pol Act', 'Pol Act']
}
