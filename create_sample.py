import pandas as pd

data = {
    'Location': [
        # Hyderabad, Telangana
        'Gachibowli - Hyderabad', 'Kondapur - Hyderabad', 'Banjara Hills - Hyderabad',
        'Madhapur - Hyderabad', 'Hitech City - Hyderabad',

        # Bangalore, Karnataka
        'Whitefield - Bangalore', 'Koramangala - Bangalore', 'Indiranagar - Bangalore',
        'Electronic City - Bangalore', 'HSR Layout - Bangalore',

        # Mumbai, Maharashtra
        'Andheri - Mumbai', 'Bandra - Mumbai', 'Powai - Mumbai',
        'Thane - Mumbai', 'Navi Mumbai - Mumbai',

        # Chennai, Tamil Nadu
        'OMR - Chennai', 'Anna Nagar - Chennai', 'Velachery - Chennai',
        'Porur - Chennai', 'Tambaram - Chennai',

        # Delhi NCR
        'Dwarka - Delhi', 'Noida Sector 62 - Delhi', 'Gurgaon - Delhi',
        'Rohini - Delhi', 'Vasant Kunj - Delhi',

        # Pune, Maharashtra
        'Hinjewadi - Pune', 'Kothrud - Pune', 'Wakad - Pune',
        'Baner - Pune', 'Hadapsar - Pune',
    ],
    'BHK': [
        2,3,4,2,3,
        2,3,3,2,3,
        2,4,3,2,2,
        2,3,2,2,2,
        3,2,4,2,3,
        2,3,2,3,2,
    ],
    'Area_sqft': [
        1200,1800,3200,1100,2100,
        1300,1900,2000,1100,1800,
        950,2800,1700,1050,1000,
        1200,2100,1100,1000,950,
        1500,1100,3000,1200,2200,
        1100,1700,1050,1600,1000,
    ],
    'Price_Lakhs': [
        85,145,380,72,210,
        95,220,280,68,190,
        180,650,320,120,110,
        82,195,78,65,55,
        150,95,480,110,320,
        88,160,92,175,70,
    ],
    'Age_Years': [
        3,7,15,2,5,
        4,8,10,3,6,
        12,20,8,5,4,
        3,15,6,4,8,
        10,3,18,7,12,
        2,9,3,7,5,
    ],
    'Parking': [
        'Yes','Yes','Yes','No','Yes',
        'Yes','Yes','Yes','No','Yes',
        'No','Yes','Yes','No','No',
        'Yes','Yes','No','No','No',
        'Yes','No','Yes','Yes','Yes',
        'Yes','Yes','Yes','Yes','No',
    ],
    'Status': [
        'Sold','Available','Sold','Available','Sold',
        'Sold','Available','Sold','Sold','Available',
        'Sold','Available','Sold','Available','Sold',
        'Sold','Sold','Available','Sold','Available',
        'Available','Sold','Sold','Available','Sold',
        'Sold','Available','Sold','Sold','Available',
    ]
}

df = pd.DataFrame(data)
df.to_csv('sample_properties.csv', index=False)
print(f'CSV created with {len(df)} properties across 6 cities!')
print(f'Cities: Hyderabad, Bangalore, Mumbai, Chennai, Delhi, Pune')