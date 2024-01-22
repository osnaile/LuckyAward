import configparser

class config():
    file = 'data/config.ini'
    
    ListFont = "Kaiti SC"
    TitleFont = "PingFang SC"

    def ReadConfig():
        _configReader = configparser.ConfigParser()
        _configReader.read(config.file, encoding='utf-8')
        
        _sections = _configReader.sections()
        
        config.ListFont = _configReader.get('global', 'ListFont')
        config.TitleFont = _configReader.get('global', 'TitleFont')