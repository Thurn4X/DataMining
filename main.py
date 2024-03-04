import acquisition
import metadata
import addtags
import sorting
import create_training_dataset



if __name__ == '__main__':
    acquisition.acquire()
    metadata.create_metadata()
    addtags.window()
    sorting.tri()
    create_training_dataset.create()
