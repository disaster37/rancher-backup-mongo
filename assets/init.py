#!/usr/bin/python
import os
import re
import sys
import time
from rancher_metadata import MetadataAPI

__author__ = 'Sebastien LANGOUREAUX'

BACKUP_DIR = '/backup/mongo'


class ServiceRun():


  def backup_duplicity_ftp(self, ftp_server, ftp_port, ftp_user, ftp_password, target_path, is_init=False):
      global BACKUP_DIR
      if ftp_server is None or ftp_server == "":
          raise KeyError("You must set the ftp server")
      if ftp_port is None:
          raise KeyError("You must set the ftp port")
      if ftp_user is None or ftp_user == "":
          raise KeyError("You must set the ftp user")
      if ftp_password is None or ftp_password == "":
          raise KeyError("You must set the ftp password")
      if target_path is None or target_path == "":
          raise KeyError("You must set the target path")

      ftp = "ftp://%s@%s:%d%s" % (ftp_user, ftp_server, ftp_port, target_path)
      cmd = "FTP_PASSWORD=%s duplicity " % (ftp_password)

      # First, we restore the last backup
      if is_init is True:
          print("Starting init the backup folder")
          os.system(cmd + '--no-encryption ' + ftp + ' ' + BACKUP_DIR + '/')


      else:
          # We backup on FTP
          print("Starting backup")
          os.system(cmd + '--no-encryption --allow-source-mismatch --full-if-older-than 7D ' + BACKUP_DIR + ' ' + ftp)

          # We clean old backup
          print("Starting cleanup")
          os.system(cmd + 'remove-all-but-n-full 3 --force --allow-source-mismatch --no-encryption ' + ftp)
          os.system(cmd + 'cleanup --force --no-encryption ' + ftp)





  def backup_mongo(self):
      global BACKUP_DIR

      # Identity database to backup
      metadata_manager = MetadataAPI()
      list_services = metadata_manager.get_service_links()
      list_mongo = []
      for service in list_services:
          service_name = list_services[service]
          service_name_env = service_name.upper().replace('-', '_')
          database = {}
          database['host'] = service_name
          database['name'] = service

          list_mongo.append(database)
          print("Found Mongo host to backup : " + service + " (" + service_name + ")")

      # Backup database
      for database in list_mongo:

          cmd = 'mongodump --host ' + database['host']

          path = BACKUP_DIR + '/' + database['name']
          os.system('mkdir -p ' + path)
          os.system('rm ' + path + '/*')
          cmd += " --out %s" % (path)
          os.system(cmd)
          print("We dump all databases and all collections for (" + database['name'] + ") in " + path)

if __name__ == '__main__':
    service = ServiceRun()

    service.backup_duplicity_ftp(os.getenv('FTP_SERVER'), os.getenv('FTP_PORT', 21), os.getenv('FTP_LOGIN'), os.getenv('FTP_PASSWORD'), os.getenv('FTP_TARGET_PATH', BACKUP_DIR), True)
    service.backup_mongo()
    service.backup_duplicity_ftp(os.getenv('FTP_SERVER'), os.getenv('FTP_PORT', 21), os.getenv('FTP_LOGIN'), os.getenv('FTP_PASSWORD'), os.getenv('FTP_TARGET_PATH', BACKUP_DIR))
