def main():
    import pandas as pd
    data = pd.read_csv('data.csv')
    
    filtered = data[~(data['SongName'].str.contains('\[')) ]
    
    filtered = filtered[~filtered.SongName.str.contains('Live')]
    filtered = filtered[~filtered.SongName.str.contains('remix')]
    filtered = filtered[~filtered.SongName.str.contains('Remix')]
    filtered = filtered.drop_duplicates('SongName')
    filtered = filtered[filtered.SongName.notnull()]
    filtered = filtered[filtered.Lyrics.notnull()]
    filtered['Lyrics'] = filtered.Lyrics.map(lambda x: x.replace('\r\r\n','.\n'))
    filtered.to_csv('cleaned_data.csv')
main()
