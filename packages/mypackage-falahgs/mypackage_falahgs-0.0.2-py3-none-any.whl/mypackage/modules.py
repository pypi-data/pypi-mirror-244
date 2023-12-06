from autodistill.detection import CaptionOntology
from autodistill_grounded_sam import GroundedSAM
from google_images_downloader import GoogleImagesDownloader

def download_images(class_name,count):
    downloader = GoogleImagesDownloader(browser="chrome", show=False, debug=False,
                                        quiet=False, disable_safeui=False)  # Constructor with default values

    downloader.download(class_name, limit=count)  # Download 50 images in ./downloads folder
    downloader.close()
def create_ontology_dict():
    ontology_input = input("Enter the ontology as a comma-separated list (e.g.,car:car or more classes  car:vehicle,person:human): ")

    if ":" in ontology_input:
        ontology_dict = dict(item.split(":") for item in ontology_input.split(","))
    else:
        ontology_dict = {ontology_input: ontology_input}

    return ontology_dict

def create_captions(ontology_dict, image_folder, dataset_folder):
    ontology = CaptionOntology(ontology_dict)
    base_model = GroundedSAM(ontology=ontology)
    dataset = base_model.label(
        input_folder=image_folder,
        extension=".png",
        output_folder=dataset_folder
    )
    return dataset

# Example usage:
#ontology_dict = create_ontology_dict()
#print("Ontology Dictionary:", ontology_dict)

# Example usage:
#ontology_dict = create_ontology_dict() #function 1
#create_ontology_dict()
#print("Ontology Dictionary:", ontology_dict)
#upload_images("images", "dataset") #function 2
#create_captions(ontology_dict, "images", "dataset") #function 3

