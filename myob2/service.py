from models import FileDBModel
import json
import os


class FileDBService:
    def __init__(self):
        self.model = FileDBModel()

    def create(self, params):
        return self.model.create(params)

    def update(self, item_id, params):
        return self.model.update(item_id, params)

    def delete(self, item_id):
        return self.model.delete(item_id)

    def list(self,where_clause):
        response = self.model.list_items(where_clause)
        return response

class Tools:
    #def __init__(self):
    #    self.dbservice = FileDBService()

    def add_file_data(filename,filepath,description):
        try:
            add_result = FileDBService().create({'Filename': filename,'Filepath':filepath, 'Description': description})
        except:
            add_result = 'Failed'
        return add_result

    def get_file_id(filename):
        search_result = FileDBService().list(where_clause=" AND Filename='{F}'".format(F=filename))
        file_id = search_result[0]['id']
        return file_id

    def get_file_path(filename):
        search_result = FileDBService().list(where_clause=" AND Filename='{F}'".format(F=filename))
        file_path = search_result[0]['Filepath']
        return file_path

    def get_file_description(filename):
        search_result = FileDBService().list(where_clause=" AND Filename='{F}'".format(F=filename))
        file_description= search_result[0]['Description']
        return file_description

    def get_file_rank(file_id):
        search_result = FileDBService().list(where_clause="")
        file_rank = 0
        file_votes = 0

        for file in search_result:
            if file['id'] == file_id:
                file_votes = file['Votes']
        for file in search_result:
            if file['Votes'] > file_votes:
                file_rank += 1
        return file_rank
    
    def vote_for_file(file_id):
        params = {}
        search_result = FileDBService().list(where_clause=" AND ID={I}".format(I=file_id))
        counter = int(search_result[0]['Votes']) 
        params['Votes'] = counter + 1
        update_result = FileDBService().update(file_id, params)
        return update_result

    def delete_upload_file(item_nr):
        try:
            search_result = FileDBService().list(where_clause=" AND ID={I}".format(I=item_nr))
            filename = search_result[0]['Filename']
            filepath = search_result[0]['Filepath']
            os.remove(os.path.join(filepath,filename))
            FileDBService().delete(item_nr)
            return True
        except:
            False
    def healthcheck_db():
        try:
            FileDBService().list(where_clause="")
            return True, "sqlitedb OK"
        except:
            return False, "sqllite Failed"

    def healthcheck_uploads_dir():
        try:
            #os.chdir('upload_files')
            f = open('upload_files/test.file','w')
            f.close()
            os.remove('upload_files/test.file')
            return True, "UploadDir OK"
        except:
            return False, "UploadDir Failed"

    def read_app_metadata():
        with open('build_info.json','r') as j_file:
            metadata = json.load(j_file)
        return metadata