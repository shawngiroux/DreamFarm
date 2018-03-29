import os
import MySQLdb
import warnings

# Initialize the database schema if not set up already and return a connection object
class DB:
    conn = None

    @staticmethod
    def initialize():
        host = os.environ.get('DB_HOST')
        port = int(os.environ.get('DB_PORT'))
        db = os.environ.get('DB_NAME')
        user = os.environ.get('DB_USER')
        passwd = os.environ.get('DB_PASSWD')

        conn = MySQLdb.connect(host=host, port=port, user=user, passwd=passwd, db=db)
        cursor = conn.cursor()

        warnings.filterwarnings('ignore', category=MySQLdb.Warning)

        try:
            cursor.execute("""CREATE TABLE IF NOT EXISTS `users` (
                `duid` bigint(11) unsigned NOT NULL,
                `name` varchar(11) NOT NULL DEFAULT '',
                `money` bigint(11) unsigned NOT NULL DEFAULT '0',
                `current_plot_num` int(11) unsigned NOT NULL DEFAULT '0',
                PRIMARY KEY (`duid`)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8;""")

            cursor.execute("""CREATE TABLE IF NOT EXISTS `farms` (
                `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
                `duid` bigint(11) unsigned NOT NULL,
                `plot_id` int(11) unsigned NOT NULL,
                `plot_num` int(11) unsigned NOT NULL,
                PRIMARY KEY (`id`),
                KEY `duid` (`duid`)
                ) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;""")

            cursor.execute("""CREATE TABLE IF NOT EXISTS `plots` (
                `plot_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
                `duid` bigint(11) unsigned NOT NULL,
                `tile_data` blob NOT NULL,
                `object_data` blob NOT NULL,
                PRIMARY KEY (`plot_id`),
                KEY `duid` (`duid`)
                ) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8;""")

            cursor.execute("""CREATE TABLE IF NOT EXISTS `crops` (
                `duid` bigint(11) unsigned NOT NULL,
                `plot_id` int(11) unsigned NOT NULL,
                `type` int(11) unsigned NOT NULL DEFAULT '0',
                `state` int(11) unsigned NOT NULL DEFAULT '0'
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8;""")

            conn.commit()
        except:
            conn.rollback()

        DB.conn = conn
