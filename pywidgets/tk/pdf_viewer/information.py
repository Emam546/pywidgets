from pathlib import Path
import pickle
def import_data(path):
    if  Path(path).exists():
        try:
            scripts_id_file=open(path,"rb")
            scripts=pickle.load(scripts_id_file)
            scripts_id_file.close()
            return scripts
        except:pass
    else:
        diction={
            "path":{
                "question_json":None,
            }
        }
the_data=import_data("pdf_viewer_autontication.data")
def save_data(path,object):
    if  Path(path).exists():
        picle_out=open(path,"wb")
        pickle.dump(object,picle_out)
        picle_out.close()

 