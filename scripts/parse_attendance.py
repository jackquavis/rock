import json
import re

raw_text = """First Name,Last Name,Total,Member Status,2026-09-11,2026-09-13,2026-09-18,2026-09-20,2026-09-25,2026-09-27,2026-10-02,2026-10-04,2026-10-09,2026-10-11,2026-10-16,2026-10-18,2026-10-23,2026-10-25,2026-10-30,2026-11-01,2026-11-06,2026-11-08,2026-11-13,2026-11-15,2026-11-20,2026-11-22,2026-11-27,2026-11-29
Joseph,Gambaccini,4,Comp,Present,Absent,Absent,Absent,Absent,Present,Present,Absent,Present,Present,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,,,
Tyler,Romano,0,Rec,Present,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,,,
Benny,Goldberg,0,Rec,Present,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,,,
Christopher,Shuba,12,Comp,Present,Absent,Absent,Absent,Absent,Present,Present,Present,Present,Present,Absent,Absent,Present,Present,Present,Absent,Present,Present,Present,Absent,Present,,,
Matthew,Diamond,0,Rec,Present,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,,,
Sabatino,Castellani,0,Rec,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,,,
Andrew,Sarraiocco,0,Rec,Present,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,,,
Joseph,Maldonado,0,Rec,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,,,
Justin,Geng,0,Rec,Absent,Present,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,,,
Angelo,Dimaggio,0,Rec,Absent,Present,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,,,
Benjamin,Matsko,0,Rec,Absent,Present,Absent,Present,Absent,Absent,Duplicate,Duplicate,Duplicate,Duplicate,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,,,
Leila,Gonzales,0,Rec,Absent,Present,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,,,
Maksym,Deyneka,0,Rec,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,,,
Ryan,Carlson,2,Rec,Absent,Absent,Present,Absent,Absent,Absent,Absent,Present,Absent,Absent,Absent,Present,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,,,
Jakub,Chojnowski,6,Comp,Present,Present,Present,Absent,Absent,Excused,Excused,Present,Absent,Present,Absent,Absent,Present,Absent,Absent,Absent,Present,Present,Present,Absent,Absent,,,
Evelyn,Oravez,0,Rec,Absent,Absent,Absent,Present,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,,,
Thomas,Harradine,2,Rec,Absent,Absent,Absent,Present,Absent,Absent,Absent,Present,Absent,Present,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,,,
Maximillian,Zubiria,2,Comp,Absent,Absent,Absent,Present,Absent,Absent,Present,Absent,Absent,Present,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,,,
Imran,Khawaja,0,Rec,Absent,Absent,Absent,Present,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,,,
Efieson,Zeamuru,4,Rec,Absent,Absent,Absent,Present,Absent,Absent,Present,Absent,Absent,Absent,Absent,Present,Present,Absent,Absent,Absent,Present,Absent,Absent,Absent,Absent,,,
Kathya,Aquino,1,Rec,Absent,Absent,Absent,Present,Absent,Absent,Absent,Present,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,,,
Francis,Gamil,5,Comp,Absent,Absent,Absent,Present,Absent,Present,Absent,Present,Present,Present,Absent,Absent,Absent,Absent,Present,Absent,Absent,Absent,Absent,Absent,Absent,,,
Joshua,Lim,8,Comp,Absent,Absent,Absent,Present,Absent,Present,Present,Present,Absent,Present,Absent,Absent,Absent,Present,Present,Absent,Present,Absent,Present,Absent,Absent,,,
Gina,Girgus,0,Rec,Absent,Absent,Absent,Present,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,,,
Hannah,Lee,0,Rec,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,,,
Gabby,Cruz,6,Comp,Absent,Absent,Absent,Absent,Absent,Absent,Present,Present,Present,Present,Absent,Absent,Present,Present,Absent,Absent,Absent,Absent,Absent,Absent,Absent,,,
Wyatt,Jaeger,6,Comp,Absent,Absent,Absent,Absent,Absent,Present,Absent,Present,Absent,Present,Absent,Absent,Present,Present,Absent,Absent,Absent,Present,Absent,Absent,Absent,,,
Gigi,Keil,8,Comp,Absent,Absent,Absent,Absent,Absent,Absent,Present,Present,Absent,Present,Absent,Absent,Present,Absent,Present,Absent,Absent,Present,Present,Absent,Present,,,
Niti,Mali,6,Rec,Absent,Absent,Absent,Absent,Absent,Present,Absent,Absent,Present,Absent,Present,Absent,Present,Absent,Absent,Absent,Absent,Absent,Present,Absent,Present,,,
Nich,Shelhoff,1,Rec,Absent,Absent,Absent,Absent,Absent,Present,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,,,
Hana,Zemlicka,1,Rec,Absent,Absent,Absent,Absent,Absent,Present,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,,,
Natalie,Detample,8,Comp,Absent,Absent,Absent,Absent,Absent,Present,Present,Present,Present,Present,Absent,Absent,Present,Absent,Present,Absent,Absent,Present,Absent,Absent,Absent,,,
Anthony,Eames-Egidi,9,Comp,Absent,Absent,Absent,Absent,Absent,Present,Present,Absent,Present,Present,Absent,Absent,Present,Present,Absent,Absent,Present,Present,Present,Absent,Absent,,,
Ben,Yavin,2,Comp,Absent,Absent,Absent,Absent,Absent,Present,Absent,Absent,Absent,Present,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,,,
Farhan,Amir,0,Rec,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,,,
Sulayman,Khan,9,Comp,Absent,Absent,Absent,Absent,Absent,Present,Present,Absent,Present,Present,Absent,Absent,Present,Present,Present,Absent,Present,Present,Absent,Absent,Absent,,,
Katie,Sullivan,8,Comp,Absent,Absent,Absent,Absent,Absent,Present,Absent,Present,Present,Present,Absent,Absent,Absent,Present,Absent,Absent,Present,Absent,Present,Absent,Present,,,
Jack,Karam,6,Comp,Absent,Absent,Absent,Absent,Absent,Present,Excused,Present,Excused,Present,Absent,Absent,Present,Absent,Absent,Absent,Present,Present,Absent,Absent,Absent,,,
Logan,Sharrott,9,Comp,Absent,Absent,Absent,Absent,Absent,Present,Present,Present,Present,Present,Absent,Absent,Absent,Present,Absent,Absent,Absent,Present,Present,Absent,Present,,,
Max,Zubiria,0,Rec,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,,,
Ryan,Chen,7,Comp,Absent,Absent,Absent,Absent,Absent,Present,Absent,Present,Present,Present,Absent,Absent,Absent,Present,Absent,Absent,Absent,Absent,Present,Absent,Present,,,
Alex,Kwok,7,Comp,Absent,Absent,Absent,Absent,Absent,Present,Absent,Present,Present,Present,Absent,Absent,Present,Absent,Present,Absent,Present,Absent,Absent,Absent,Absent,,,
Anna,Bryan-Jones,9,Comp,Absent,Absent,Absent,Absent,Absent,Present,Present,Present,Present,Present,Absent,Absent,Present,Present,Present,Absent,Present,Absent,Absent,Absent,Absent,,,
Phoenix,Blackford-Wadhams,2,Rec,Absent,Absent,Absent,Absent,Absent,Present,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Present,Absent,Absent,Absent,,,
Matthew,Enriquez,4,Comp,Absent,Absent,Absent,Absent,Absent,Present,Absent,Present,Absent,Present,Absent,Absent,Absent,Absent,Present,Absent,Absent,Absent,Absent,Absent,Absent,,,
Pierce,Jackson,2,Comp,Absent,Absent,Absent,Absent,Absent,Present,Absent,Absent,Absent,Present,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,,,
Nidhi,Karulkar,0,Rec,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,,,
Asmit,Chakraborty,0,Rec,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,,,
Ben,Matsko,4,Comp,Absent,Absent,Absent,Absent,Absent,Absent,Present,Present,Present,Present,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,,,
Rebekah,Han,1,Rec,Absent,Absent,Absent,Absent,Absent,Absent,Present,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,,,
Flora,Jeng,6,Comp,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Present,Present,Present,Absent,Absent,Present,Absent,Present,Absent,Absent,Present,Absent,Absent,Absent,,,
Angel,Pina,0,Rec,,,,,,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,,,
Akhil,Beere,5,Comp,,,,,,Absent,Absent,Present,Absent,Present,Absent,Absent,Present,Present,Present,Absent,Absent,Absent,Absent,Absent,Absent,,,
Samarth,Patade,1,Rec,,,,,,Absent,Present,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,,,
Ian,Soos,1,Rec,,,,,,Absent,Present,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,,,
Jonathan,Tillack,0,Rec,,,,,,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,,,
Marian,Pomasin,2,Rec,,,,,,Absent,Present,Absent,Present,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,,,
Gigi,Zhong,3,Rec,,,,,,Absent,Present,Absent,Absent,Present,Absent,Absent,Absent,Absent,Absent,Absent,Present,Absent,Absent,Absent,Absent,,,
Sophia,Pu,2,Rec,,,,,,Absent,Present,Absent,Absent,Present,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,,,
Maya,U,2,Comp,,,,,,Absent,Present,Absent,Absent,Present,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,,,
Jeremiah/Jeremy,Wachtel,2,Comp,,,,,,Excused,Absent,Present,Excused,Present,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,,,
Joseph,Park,3,Rec,,,,,,Absent,Absent,Present,Absent,Absent,Absent,Present,Absent,Absent,Absent,Absent,Absent,Present,Absent,Absent,Absent,,,
Yixuan,Li,1,Rec,,,,,,Absent,Absent,Present,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,,,
Ethan,Lam,0,Rec,,,,,,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,,,
Sia,Joshi,1,Rec,,,,,,Absent,Absent,Present,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,,,
Adriana,Nguyen,1,Rec,,,,,,Absent,Absent,Present,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,,,
Nick,Shelhoff,4,Comp,,,,,,Absent,Absent,Present,Present,Present,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Present,Absent,Absent,Absent,,,
Doje,Sim,3,Comp,,,,,,Absent,Absent,Excused,Present,Present,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Present,,,
Sean,Lee,1,Rec,,,,,,Absent,Absent,Absent,Present,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,,,
Randy,Veras,3,Rec,,,,,,Absent,Absent,Absent,Present,Absent,Absent,Absent,Present,Absent,Absent,Absent,Present,Absent,Absent,Absent,Absent,,,
Jei,Sweeney,1,Rec,,,,,,Absent,Absent,Absent,Present,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,,,
Gene,Lazarraga,1,Rec,,,,,,Absent,Absent,Absent,Present,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,,,
Enes,Atik,2,Rec,,,,,,Absent,Absent,Absent,Absent,Absent,Present,Absent,Absent,Absent,Absent,Absent,Present,Absent,Absent,Absent,Absent,,,
Vicki,Wong,3,Rec,,,,,,Absent,Absent,Absent,Present,Absent,Present,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Present,Absent,Absent,,,
Michael,Ho,2,Comp,,,,,,Absent,Absent,Excused,Absent,Present,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Present,,,
Eve,Kreger,12,Comp,,,,,,Present,Present,Present,Excused,Present,Present,Present,Present,Present,Present,Absent,Present,Present,Present,Absent,Absent,,,
Peter,Evanowski,2,Comp,,,,,,Excused,Excused,Excused,Excused,Present,Absent,Absent,Present,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,,,
Aadi,Kadam,1,Rec,,,,,,Absent,Absent,Absent,Absent,Present,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,,,
Jared,Yili,1,Rec,,,,,,Absent,Absent,Absent,Absent,Present,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,,,
Jeffrey,Han,1,Rec,,,,,,Absent,Absent,Absent,Absent,Present,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,,,
Helena,Chan,1,Rec,,,,,,Absent,Absent,Absent,Absent,Present,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,,,
Michael,Tam,1,Rec,,,,,,Absent,Absent,Absent,Absent,Present,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,,,
Alison,Yan,1,Rec,,,,,,Absent,Absent,Absent,Absent,Present,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,,,
Selina,Lin,1,Rec,,,,,,Absent,Absent,Absent,Absent,Present,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,,,
Samory,Greene,2,Rec,,,,,,Absent,Absent,Absent,Absent,Present,Absent,Absent,Present,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,,,
Kevin,Li,1,Rec,,,,,,Absent,Absent,Absent,Absent,Present,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,,,
Changha,Choi,0,,,,,,,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,,,
Strine,Compton,1,,,,,,,Absent,Absent,Absent,Absent,Absent,Present,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,,,
Liam,Kennedy,2,,,,,,,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Present,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Present,,,
Jiyun,Lee,1,,,,,,,Absent,Absent,Absent,Absent,Absent,Present,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,,,
Karol,Agila,1,,,,,,,Absent,Absent,Absent,Absent,Absent,Present,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,,,
Ian,Badilla,1,,,,,,,Absent,Absent,Absent,Absent,Absent,Present,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,,,
Ajani,Grady-Willis,1,,,,,,,Absent,Absent,Absent,Absent,Absent,Absent,Present,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,,,
Jack,Rodgers,5,,,,,,,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Present,Absent,Present,Absent,Present,Present,Absent,Absent,Present,,,
Elvis,Liu,0,,,,,,,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,,,
Alex,Guo,1,,,,,,,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Present,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,,,
Elliot,Malamud,0,,,,,,,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,,,
Alsx,Kwok,1,,,,,,,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Present,Absent,Absent,Absent,Absent,Absent,Absent,Absent,,,
Sumaya,Sahabuddin,0,,,,,,,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,,,
Jeremy,Wachtel,1,,,,,,,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Present,Absent,Absent,Absent,Absent,Absent,Absent,,,
Gabrielle,Cruz,2,,,,,,,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Present,Absent,Absent,Absent,Present,,,
Ethan,Bui,1,,,,,,,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Present,Absent,Absent,Absent,Absent,,,
Sarah Marlene,Goufo Lontchi,1,,,,,,,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Present,Absent,Absent,Absent,Absent,,,
Showrya,Bandi,1,,,,,,,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Present,Absent,Absent,,,
Olivia,Okparaeke,1,,,,,,,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Absent,Present,Absent,Absent,,,
"""

method_31_names = [
    "Joseph Gambaccini", "Christopher Shuba", "Jakub Chojnowski", "Maximillian Zubiria",
    "Francis Gamil", "Joshua Lim", "Gabby Cruz", "Wyatt Jaeger", "Gigi Keil",
    "Natalie Detample", "Anthony Eames-Egidi", "Ben Yavin", "Sulayman Khan",
    "Katie Sullivan", "Jack Karam", "Logan Sharrott", "Ryan Chen", "Alex Kwok",
    "Anna Bryan-Jones", "Matthew Enriquez", "Pierce Jackson", "Ben Matsko",
    "Flora Jeng", "Akhil Beere", "Maya U", "Jeremiah/Jeremy Wachtel", "Nick Shelhoff",
    "Doje Sim", "Michael Ho", "Eve Kreger", "Peter Evanowski"
]

fight_knight_names = [
    "Tyler Tran", "Brennan Wyckoff", "Jose Marquez", "Nidhi Karulkar", "Charles Lin",
    "Guilherme Uchida", "Angela Zhou", "Joseph Gambaccini", "Charles Evans",
    "Matthew Yong", "Alex Kwok", "Anna Nunez Pena", "Albert Abzalimob", "Samuel Geller",
    "Lars Olsen", "Eve Kreger", "Cassie Krause", "Michael Ho", "Jeremiah Wachtel",
    "Maya Umylny", "Eli Hausman", "Akhil Beere", "Ryan Chen", "Anna Rozenbaum",
    "Francis Clyde Gamil", "Kenneth Cruz", "Peter Evanowski", "Christina Winter",
    "Lily Mcdonald", "Jared Yili", "Harish Krishnan", "Pravesh Jain", "Oliver Chan",
    "Bodhi Pirog", "Rain Lin", "Alyssa Keanini", "Jonathan Tillack", "Christopher Shuba",
    "James Yu", "Emmanuel Wertman", "Neel Pandruvada", "Matthew Enriquez", "Jordan Jimenez"
]

# Canonical alias mapping
alias_map = {
    "jeremy wachtel": "Jeremiah Wachtel",
    "jeremiah/jeremy wachtel": "Jeremiah Wachtel",
    "jeremiah wachtel": "Jeremiah Wachtel",
    "gabrielle cruz": "Gabby Cruz",
    "gabby cruz": "Gabby Cruz",
    "max zubiria": "Maximillian Zubiria",
    "maximillian zubiria": "Maximillian Zubiria",
    "alsx kwok": "Alex Kwok",
    "alex kwok": "Alex Kwok",
    "maya u": "Maya Umylny",
    "maya umylny": "Maya Umylny",
    "ben matsko": "Benjamin Matsko",
    "benjamin matsko": "Benjamin Matsko",
    "nich shelhoff": "Nick Shelhoff",
    "nick shelhoff": "Nick Shelhoff",
    "francis clyde gamil": "Francis Gamil",
    "francis gamil": "Francis Gamil",
    "joshua lim": "Josh Lim",
    "josh lim": "Josh Lim",
    "jordan  jimenez": "Jordan Jimenez",
    "jordan jimenez": "Jordan Jimenez",
    "christopher shuba": "Chris Shuba",
    "chris shuba": "Chris Shuba"
}

def canonical_name(name):
    norm = " ".join(name.strip().lower().split())
    if norm in alias_map:
        return alias_map[norm]
    return " ".join([part.capitalize() for part in name.strip().split()])

# Let's parse the spreadsheet lines
lines = raw_text.strip().split("\n")
header = [h.strip() for h in lines[0].split(",")]
date_cols = header[4:]
print(f"Dates in sheet ({len(date_cols)}):", date_cols)

people_records = {} # canon_name -> { team, dates: { date: status }, total_in_sheet: int }

for line in lines[1:]:
    if not line.strip(): continue
    parts = [p.strip() for p in line.split(",")]
    if len(parts) < 4: continue
    first = parts[0]
    last = parts[1]
    if not first and not last: continue
    raw_name = f"{first} {last}".strip()
    c_name = canonical_name(raw_name)
    total_str = parts[2] if len(parts) > 2 else "0"
    try:
        total_val = int(total_str)
    except:
        total_val = 0
    status_team = parts[3] if len(parts) > 3 else "Rec"
    if not status_team: status_team = "Rec"
    team = "Comp Team" if "comp" in status_team.lower() else "Rec Team"

    if c_name not in people_records:
        people_records[c_name] = {
            "canonical_name": c_name,
            "raw_names": set([raw_name]),
            "team": team,
            "attendance": {},
            "sheet_total": total_val
        }
    else:
        people_records[c_name]["raw_names"].add(raw_name)
        if team == "Comp Team":
            people_records[c_name]["team"] = "Comp Team"
        people_records[c_name]["sheet_total"] += total_val

    # Parse date values
    for idx, d in enumerate(date_cols):
        col_idx = 4 + idx
        val = parts[col_idx] if col_idx < len(parts) else ""
        val = val.strip()
        if not val or val.lower() == "duplicate":
            continue
        existing_val = people_records[c_name]["attendance"].get(d)
        if val in ["Present", "Excused"]:
            people_records[c_name]["attendance"][d] = val
        elif val == "Absent":
            if not existing_val:
                people_records[c_name]["attendance"][d] = "Absent"

print(f"Total canonical athletes in sheet: {len(people_records)}")

# Print merged duplicates
merged = [p for p in people_records.values() if len(p['raw_names']) > 1]
print("Merged duplicates count:", len(merged))
for m in merged:
    print(f"  {m['canonical_name']} merged from {m['raw_names']}")
