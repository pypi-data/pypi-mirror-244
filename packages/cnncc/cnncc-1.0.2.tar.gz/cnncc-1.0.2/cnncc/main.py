from .models.resnet import model as resnet
import argparse
from .utils import pretty_print
    
def predict(model: str, image_path: str): 
    
    if model == "ResNet":
        model = resnet.load_pretrained_model()
        image = resnet.prepare_img_for_inference(image_path)
        out, p, classe = resnet.inference(model, image)
        
    return out, p, classe

def test():
    print("coucou dalil")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, required=True)
    parser.add_argument("--image", type=str, required=True)
    args = parser.parse_args()
    out, p, classe = predict(args.model, args.image)
    pretty_print(out, p, classe)
    
# if __name__ == "__main__":
#     main()