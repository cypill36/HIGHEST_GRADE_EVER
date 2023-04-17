import pymysql
import csi3335 as cfg

con = pymysql.connect(host=cfg.mysql['location'], user=cfg.mysql['user'], password=cfg.mysql['password'], dv=cfg.mysql['database'])