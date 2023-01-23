import logging
import os
import helper

#Directory paths ermitteln
src_path = str(os.path.dirname(__file__))
log_path = str(os.path.join(src_path, '../logs'))

#config einlesen
config = helper.get_config()

def setup_login():
    """
    In dieser Funktion werden die logging einstellungen festgelegt
    """
    # Logging
    log_level = config['log_level']
    logging.basicConfig(
        filename=os.path.join(log_path, 'data-simulation.log'),
        filemode='w',
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%d.%m.%y %H:%M:%S',
        encoding='utf-8',
        level=log_level,
        force=True
    )
    logging.info("Login wurde aufgesetzt")



