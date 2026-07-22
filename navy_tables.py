# navy_tables.py
# Central location for all Book 5 Navy tables
# This breaks circular imports between b5_data.py and navy_res.py

navy_branch = ('Line', 'Flight', 'Gunnery', 'Engineering', 'Medical', 'Technical Services')

navy_life = ('Brawling', '+1 str', 'Carousing', 'Gambling', '+1 end', '+1 dex', '+1 end', '+1 edu', 'Carousing', 'Vacc Suit')

navy_cash_table = (1000, 5000, 5000, 10000, 20000, 50000, 50000)
navy_muster_table = ('Low Psg', '+1 int', '+2 edu', 'Blade', 'Travellers', 'High Psg', '+2 soc')

line_crew = ('Mechanical', 'Electronics', 'Gun Cbt', 'Nav', 'Computer', 'Liaison', 'Zero-G Cbt', 'Vacc Suit')
flight = ('Vacc Suit', 'Admin', 'Gun Cbt', 'Commo', 'Ships Boat', 'Nav', 'Pilot', 'Pilot')
gunnery = ('Fwd Obs', 'Gun Cbt', 'Commo', 'Computer', 'Gunnery', 'Gunnery', 'Gunnery', 'Gunnery')
engineering = ('Mechanical', 'Electronics', 'Engineering', 'Mechanical', 'Vacc Suit', 'Engineering', 'Engineering', 'Engineering')
medical = ('Admin', 'JoT', 'Electronics', 'Admin', 'Medical', 'Computer', 'Medical', 'Medical')
technical = ('Mechanical', 'Mechanical', 'Electronics', 'Electronics', 'Computer', 'Computer', 'Gravitics', 'JoT')

sd_enl = ['Cross Trng', 'Specialist School', 'Recruiting School', 'Gunnery School', 'Engineering School', 'OCS', 'OCS']
sd_officer = ['Cross Trng', 'Intelligence School', 'Recruiting Duty', 'Naval Attache/Aide', 'Command College', 'Staff College', 'Staff College']

specialist_school_table = ['Admin', 'Medical', 'Liaison', 'Mechanical', 'Electronics', 'Gravitics', 'Vehicle',
                           'Navigation', 'Computer', 'Ships Boat', 'Communications', 'Vacc Suit']

erank = ('Spacehand Recruit', 'Spacehand Apprentice', 'Able Spacehand', 'Petty Officer Third Class',
         'Petty Officer Second Class', 'Petty Officer First Class', 'Chief Petty Officer',
         'Senior Chief Petty Officer', 'Master Chief Petty Officer')
orank = ('Ensign', 'Sublieutenant', 'Lieutenant', 'Lieutenant Commander', 'Commander', 'Captain',
         'Commodore', 'Fleet Admiral', 'Sector Admiral', 'Grand Admiral')

# Additional Navy skill tables used by navy_ocs, get_command_skill, etc.

command_skills = ('Ship Tactics', 'Fleet Tactics', 'Leader', 'Admin', 'Tactics', 'Liaison', 'Computer')

staff_skills = ('Admin', 'Liaison', 'Computer', 'Leader', 'Fleet Tactics', 'Ship Tactics', 'Tactics')

po_skills = ('Leader', 'Admin', 'Computer', 'Tactics', 'Liaison', 'Recruiting', 'Instruction')

shipboard_skills = ('Ships Boat', 'Nav', 'Pilot', 'Gunnery', 'Engineering', 'Mechanical', 'Vacc Suit')

shoreduty_skills = ('Admin', 'Liaison', 'Recruiting', 'Computer', 'Leader', 'Streetwise', 'Vacc Suit')